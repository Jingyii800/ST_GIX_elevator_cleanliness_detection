from flask import Flask
from flask_cors import CORS
from .routes import bp
from .config import Config
from .database import get_db_connection

def create_app():
    app = Flask(__name__)

    # Load config from config.py
    app.config.from_object(Config)

    app.register_blueprint(bp)

    # Enable CORS for all routes
    CORS(app)

    # Test database connection on startup
    try:
        conn = get_db_connection()
        if conn:
            print("Database connection successful.")
            conn.close()
        else:
            print("Failed to connect to database.")
    except Exception as e:
        print(f"Database connection error: {e}")

    return app