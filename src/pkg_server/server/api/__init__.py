from flask import Blueprint, request, jsonify
from sqlalchemy import select
from pkg_server.database.config import db
from pkg_server.database.database import PkgDatabase


getter = Blueprint("getter", __name__)

@getter.route("/search")
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
