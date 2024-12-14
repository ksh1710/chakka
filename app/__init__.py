import os
import sys
from flask import Flask
from flask_socketio import SocketIO

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

socketio = SocketIO()

def create_app(config_class=None):
    app = Flask(__name__)
    
    # If no config is specified, try to import from config.py
    if config_class is None:
        try:
            from config import Config
            config_class = Config
        except ImportError:
            # Fallback to a default configuration
            class Config:
                SECRET_KEY = 'default_secret_key'
                DEBUG = True
    
    # Apply configuration
    app.config.from_object(config_class)

    # Initialize SocketIO
    socketio.init_app(app)

    # Import routes and initialize them
    from . import routes
    routes.init_routes(app)

    return app