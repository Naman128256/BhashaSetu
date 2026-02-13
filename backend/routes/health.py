"""
Health check and system status routes
"""

from flask import Blueprint, jsonify
from services.model_manager import ModelManager
from utils.logger import get_logger
import time

health_bp = Blueprint('health', __name__)
logger = get_logger(__name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Basic health check endpoint"""
    logger.info("Health check requested")
    return jsonify({
        'status': 'ok',
        'timestamp': time.time(),
        'service': 'nepali-sinhala-translator-backend'
    })

@health_bp.route('/version', methods=['GET'])
def version():
    """Return application version"""
    logger.info("Version check requested")
    return jsonify({
        'version': '1.0.0',
        'python_version': '3.13',
        'framework': 'Flask'
    })

@health_bp.route('/models/status', methods=['GET'])
def models_status():
    """Check status of all ML models"""
    logger.info("Models status check requested")
    
    try:
        model_manager = ModelManager()
        status = model_manager.get_models_status()
        
        return jsonify({
            'status': 'ok',
            'models': status
        })
    except Exception as e:
        logger.error(f"Error checking models status: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500