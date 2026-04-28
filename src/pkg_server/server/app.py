import os
from pathlib import Path
from flask import Flask
from pkg_server.database.config import db, Config
from pkg_server.server.api import *


def create_app() -> Flask:
    """Create and configure the Flask application instance.

    Initializes the app, configures settings, sets up SQLAlchemy, registers 
    blueprints, and creates database tables.

    The instance folder is placed at the project root level to avoid conflicts 
    with package structure.

    Returns:
        Flask: A configured Flask application instance.
    """
    # Calculate project root relative to this file (src/pkg_server/server/app.py)
    project_root = Path(__file__).resolve().parents[3]
    instance_path = str(project_root / "instance")
    
    app = Flask(__name__, instance_path=instance_path)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize database with app
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(serv_getter)
    app.register_blueprint(serv_sender)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
