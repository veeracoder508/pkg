from flask import Flask
from pkg_server.database.config import db, Config
from pkg_server.server.api import getter


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize database with app
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(getter)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
