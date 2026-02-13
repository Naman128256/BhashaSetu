"""
Routes package initialization
Registers all Flask routes
"""

from .health import health_bp
from .translation import translation_bp
from .upload import upload_bp

def register_routes(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(health_bp)
    app.register_blueprint(translation_bp)
    app.register_blueprint(upload_bp)