"""
This package defines the API endpoints for publishing and managing package uploads
to the registry.
"""

import os
import tarfile
from pathlib import Path
try:
    import tomllib
except Exception:
    import tomli as tomllib  # type: ignore
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from sqlalchemy import select
from pkg_server.database.config import db
from pkg_server.database.database import PkgDatabase, PkgMetaData
from pkg_server.utils.fs import ensure_parent_dir_and_touch


serv_sender = Blueprint("sender", __name__) # Blueprint for handling package sending/publishing operations.

@serv_sender.route('/api/send/publish', methods=['POST'])
def publish_package():
    """Handle package publication by saving the file and updating the database.

    This endpoint expects a `multipart/form-data` request containing:
        package: The package file itself (e.g., a .tar.gz archive).
        name: The name of the package (form field).
        version: The version of the package (form field).

    Returns:
        Response: A JSON response indicating success (201) or error (400/500).

    Raises:
        Exception: If file I/O or database operations fail.
    """
    if 'package' not in request.files:
        return jsonify({"error": "No package file provided"}), 400
    
    file = request.files['package']
    name = request.form.get('name')
    version = request.form.get('version')
    
    if not name or not version:
        return jsonify({"error": "Package name and version are required"}), 400

    if file.filename == '':
        return jsonify({"error": "Filename is empty"}), 400

    try:
        # Ensure storage directory exists within the application instance folder
        storage_path = os.path.join(current_app.instance_path, "package_storage")
        os.makedirs(storage_path, exist_ok=True)
        
        filename = secure_filename(f"{name}-{version}.tar.gz")
        save_path = os.path.join(storage_path, filename)
        # Ensure parent dir and file exist before saving
        ensure_parent_dir_and_touch(save_path)
        file.save(save_path)

        # Attempt to read package metadata from pyproject.toml inside archive
        author_val = None
        user_name_val = None
        license_val = None

        try:
            with tarfile.open(save_path, "r:gz") as tar:
                # Look for a pyproject.toml at the top level or within members
                toml_member = None
                for m in tar.getmembers():
                    if Path(m.name).name == "pyproject.toml":
                        toml_member = m
                        break

                if toml_member is not None:
                    f = tar.extractfile(toml_member)
                    if f is not None:
                        toml_bytes = f.read()
                        try:
                            toml_data = tomllib.loads(toml_bytes.decode("utf-8"))
                        except AttributeError:
                            # tomllib in py3.11 accepts bytes for loads in some backports
                            toml_data = tomllib.loads(toml_bytes)

                        project = toml_data.get("project") or toml_data.get("tool", {}).get("poetry") or {}

                        # author: try authors list, fall back to maintainer or name
                        authors = project.get("authors") or project.get("author")
                        if isinstance(authors, list) and authors:
                            first = authors[0]
                            if isinstance(first, dict):
                                author_val = first.get("name") or first.get("email")
                            else:
                                author_val = str(first)
                        elif isinstance(authors, str):
                            author_val = authors

                        # license
                        lic = project.get("license")
                        if isinstance(lic, dict):
                            license_val = lic.get("text") or lic.get("file") or lic.get("expression")
                        elif isinstance(lic, str):
                            license_val = lic

                        # user_name: prefer email local-part if available
                        if isinstance(authors, list) and authors:
                            first = authors[0]
                            email = None
                            if isinstance(first, dict):
                                email = first.get("email")
                            elif isinstance(first, str) and "@" in first:
                                email = first
                            if email:
                                user_name_val = email.split("@")[0]

        except Exception:
            # Non-fatal: if parsing fails, continue without metadata
            author_val = author_val

        # Database operations: Update existing package or create a new entry
        stmt = select(PkgDatabase).where(PkgDatabase.name == name)
        pkg = db.session.execute(stmt).scalar_one_or_none()

        if not pkg:
            pkg = PkgDatabase(name=name, latest_version=version)
            db.session.add(pkg)
        else:
            pkg.latest_version = version
        
        db.session.flush() # Flush to ensure the pkg.id is available for metadata

        # If this exact version already exists for the package, don't store duplicate
        stmt_existing = select(PkgMetaData).where(
            PkgMetaData.pkg_id == pkg.id,
            PkgMetaData.version == version
        )
        existing_meta = db.session.execute(stmt_existing).scalar_one_or_none()
        if existing_meta is not None:
            # remove saved file to avoid duplicate storage
            try:
                if os.path.exists(save_path):
                    os.remove(save_path)
            except Exception:
                pass
            db.session.rollback()
            return jsonify({"error": f"Package {name} version {version} already exists"}), 409

        # Log metadata for the specific version being uploaded
        meta_kwargs = {"pkg_id": pkg.id, "version": version}
        if author_val:
            meta_kwargs["author"] = author_val
        if user_name_val:
            meta_kwargs["user_name"] = user_name_val
        if license_val:
            meta_kwargs["license"] = license_val

        meta = PkgMetaData(**meta_kwargs)
        db.session.add(meta)
        db.session.commit()

        return jsonify({"message": f"Package {name} version {version} published successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500