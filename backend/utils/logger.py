"""
Logging configuration for the Flask backend
Implements rotating file logs with separate handlers for different log types
"""

import logging
import logging.handlers
import os
from pathlib import Path
from utils.config import Config

def setup_logging():
    """Setup comprehensive logging system with rotating file handlers"""
    
    # Ensure logs directory exists
    Config.init_directories()
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File formatter
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    # App log handler (general application logs)
    app_handler = logging.handlers.RotatingFileHandler(
        Config.LOGS_DIR / 'app.log',
        maxBytes=Config.LOG_MAX_BYTES,
        backupCount=Config.LOG_BACKUP_COUNT
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(file_formatter)
    root_logger.addHandler(app_handler)
    
    # Error log handler (errors and warnings only)
    error_handler = logging.handlers.RotatingFileHandler(
        Config.LOGS_DIR / 'error.log',
        maxBytes=Config.LOG_MAX_BYTES,
        backupCount=Config.LOG_BACKUP_COUNT
    )
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(file_formatter)
    root_logger.addHandler(error_handler)
    
    # Model log handler (ML model specific logs)
    model_logger = logging.getLogger('models')
    model_handler = logging.handlers.RotatingFileHandler(
        Config.LOGS_DIR / 'model.log',
        maxBytes=Config.LOG_MAX_BYTES,
        backupCount=Config.LOG_BACKUP_COUNT
    )
    model_handler.setLevel(logging.DEBUG)
    model_handler.setFormatter(file_formatter)
    model_logger.addHandler(model_handler)
    model_logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate logs
    model_logger.propagate = False
    
    logging.info("Logging system initialized successfully")

def get_logger(name):
    """Get a logger instance for a specific module"""
    return logging.getLogger(name)