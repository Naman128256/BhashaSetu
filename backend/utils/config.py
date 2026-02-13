"""
Configuration settings for the Flask backend
"""

import os
from pathlib import Path

class Config:
    """Base configuration class"""
    
    # Server settings
    HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    PORT = int(os.getenv('FLASK_PORT', 5005))
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Application settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    MODELS_DIR = BASE_DIR / 'models' / 'models'
    LOGS_DIR = BASE_DIR / 'logs'
    TEMP_DIR = BASE_DIR / 'temp'
    
    # Model settings
    OCR_MODEL_PATH = MODELS_DIR / 'paddleocr'
    TRANSLATION_MODEL_PATH = MODELS_DIR / 'nllb_model'
    LLM_MODEL_PATH = MODELS_DIR / 'phi3'
    LANG_DETECT_MODEL_PATH = MODELS_DIR / 'fasttext' / 'lid.176.bin'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    @classmethod
    def init_directories(cls):
        """Create necessary directories"""
        for directory in [cls.MODELS_DIR, cls.LOGS_DIR, cls.TEMP_DIR]:
            directory.mkdir(parents=True, exist_ok=True)