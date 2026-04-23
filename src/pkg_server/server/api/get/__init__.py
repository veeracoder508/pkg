import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from sqlalchemy import select
from pkg_server.database.config import db
from pkg_server.database.database import PkgDatabase


serv_getter = Blueprint("getter", __name__)

@serv_getter.route("/api/get/search")
def search():
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

@serv_getter.route('/api/get/download', methods=['GET'])
def download_package():
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