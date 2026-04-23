import os
from flask import Flask
from pkg_server.database.config import db, Config
from pkg_server.server.api import *


def create_app() -> Flask:
    """Create and configure the Flask application."""
    # Calculate the project root directory (3 levels up from this file)
    # to ensure the instance folder and database are created in the project root.
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    instance_path = os.path.join(root_path, "instance")
    
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
