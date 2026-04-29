"""
This package defines the API endpoints for retrieving package information
and downloading package files from the registry.
"""

import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from sqlalchemy import select
from pkg_server.database.config import db
from pkg_server.database.database import PkgDatabase, PkgMetaData


serv_getter = Blueprint("getter", __name__)

@serv_getter.route("/api/get/search")
def search():
    """Search for packages in the registry.

    This endpoint allows clients to search for packages by name using a partial,
    case-insensitive match.

    Args:
        name (str, optional): The partial name of the package to search for.
                              Provided as a query parameter.

    Returns:
        Response: A JSON response containing matching packages and their latest versions (200),
                  or an error message (400/500).
    """
    search_query = request.args.get("name")
    
    if not search_query:
        return jsonify({"error": "name parameter is required"}), 400
    
    try:
        # Query the database for packages matching the search query
        stmt = select(PkgDatabase).where(PkgDatabase.name.ilike(f"%{search_query}%"))
        results = db.session.execute(stmt).scalars().all()
        
        # Format results
        packages = [
            {
                "id": pkg.id,
                "name": pkg.name,
                "latest_version": pkg.latest_version
            }
            for pkg in results
        ]
        
        return jsonify({"results": packages, "count": len(packages)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@serv_getter.route("/api/get/versions")
def get_versions():
    """Retrieve a list of available package versions.

    This endpoint expects a GET request with a query parameter:
        name (str): The name of the package to retrieve versions for.

    Returns:
        Response: A JSON response containing a list of package versions (200),
                  or an error message (400/500).
    """
    pkg_name = request.args.get('name')

    if not pkg_name:
        return jsonify({"error": "name parameter is required"}), 400

    try:
        # Find the package by name
        stmt = select(PkgDatabase).where(PkgDatabase.name == pkg_name)
        pkg = db.session.execute(stmt).scalar_one_or_none()

        if not pkg:
            return jsonify({"error": f"Package {pkg_name} not found"}), 404

        # Retrieve all metadata entries (versions) for this package, newest first
        stmt_meta = select(PkgMetaData).where(PkgMetaData.pkg_id == pkg.id).order_by(PkgMetaData.id.desc())
        meta_results = db.session.execute(stmt_meta).scalars().all()

        versions = [m.version for m in meta_results]

        return jsonify({
            "name": pkg.name,
            "latest_version": pkg.latest_version,
            "versions": versions
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@serv_getter.route('/api/get/download', methods=['GET'])
def download_package():
    """Download a specific version of a package from the server.

    This endpoint expects a GET request with query parameters:
        name (str): The name of the package to download.
        version (str): The specific version string of the package.

    The function constructs the expected filename (e.g., `pkg_name-version.tar.gz`),
    locates it within the application's secure `instance/package_storage` directory,
    and serves it as an attachment.

    Returns:
        Response: The package file as a downloadable attachment if found (200),
                  or a JSON error response (400 if parameters are missing,
                  404 if the package/version is not found, 500 for other errors).

    Raises:
        Exception: Catches generic exceptions during file path construction or
                   access, returning a 500 error. Note that `send_from_directory`
                   handles file not found scenarios internally before this
                   exception catch.
    """
    package_name = request.args.get('name')
    version = request.args.get('version')

    if not package_name or not version:
        return jsonify({"error": "Package name and version are required"}), 400
    
    try:
        # Ensure we look in the same storage directory defined in the sender
        storage_path = os.path.join(current_app.instance_path, "package_storage")
        filename = secure_filename(f"{package_name}-{version}.tar.gz")
        file_path = os.path.join(storage_path, filename)

        if not os.path.exists(file_path):
            return jsonify({"error": f"Package {package_name} version {version} not found"}), 404

        return send_from_directory(
            directory=storage_path,
            path=filename,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
