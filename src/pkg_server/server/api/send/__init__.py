"""
This package defines the API endpoints for publishing and managing package uploads
to the registry.
"""

import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from sqlalchemy import select
from pkg_server.database.config import db
from pkg_server.database.database import PkgDatabase, PkgMetaData


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
        file.save(save_path)

        # Database operations: Update existing package or create a new entry
        stmt = select(PkgDatabase).where(PkgDatabase.name == name)
        pkg = db.session.execute(stmt).scalar_one_or_none()

        if not pkg:
            pkg = PkgDatabase(name=name, latest_version=version)
            db.session.add(pkg)
        else:
            pkg.latest_version = version
        
        db.session.flush() # Flush to ensure the pkg.id is available for metadata
        
        # Log metadata for the specific version being uploaded
        meta = PkgMetaData(pkg_id=pkg.id, version=version)
        db.session.add(meta)
        db.session.commit()

        return jsonify({"message": f"Package {name} version {version} published successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500