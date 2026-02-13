#!/usr/bin/env python3
"""
Main Flask Application Entry Point
Offline Nepali & Sinhala Literature Translator Backend
"""

import os
import sys
from flask import Flask
from flask_cors import CORS
from utils.logger import setup_logging
from utils.config import Config
from routes import register_routes

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for Electron frontend
    CORS(app, origins=["http://localhost:3000", "file://"])
    
    # Setup logging
    setup_logging()
    
    # Register all routes
    register_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Log startup
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Starting Flask backend server...")
    logger.info(f"Server will run on {Config.HOST}:{Config.PORT}")
    
    try:
        app.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=Config.DEBUG,
            threaded=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)