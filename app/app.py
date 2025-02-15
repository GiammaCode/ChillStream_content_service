"""
Flask Application Factory

This module defines the main application factory for creating and configuring the Flask app.
It initializes the database and registers the API routes.

Functions:
    - `create_app()`: Creates and configures the Flask app instance.

Execution:
    If this script is run as the main module, it starts the Flask development server.

Components:
    - MongoDB: Configured as the application's database with URI `mongodb://mongodb:27017/contentdb`.
    - Routes: Registers all routes defined in the `routes` module.
"""

from flask import Flask
from services.db import init_db
from routes import init_routes  # Import routes to avoid circular dependencies
from flask_cors import CORS

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)

    # Application configuration
    app.config["MONGO_URI"] = "mongodb://content_mongodb:27017/contentdb"

    CORS(app)

    # Initialize database and routes
    init_db(app)
    init_routes(app)

    # Optional: Print all registered routes for debugging
    #print("Registered Routes:")
    #for rule in app.url_map.iter_rules():
    #    print(rule)

    return app

if __name__ == "__main__":
    # Create the application instance and run the development server
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
