"""
Model Manager - Handles loading and status of all ML models
"""

from utils.logger import get_logger
from utils.config import Config
import os

logger = get_logger('models.manager')

class ModelManager:
    """Manages all ML models used in the application"""
    
    def __init__(self):
        self.models = {}
        self.model_status = {}
        
    def load_all_models(self):
        """Load all required models"""
        logger.info("Loading all ML models...")
        
        try:
            self._load_ocr_model()
            self._load_translation_model()
            self._load_language_detection_model()
            self._load_llm_model()
            
            logger.info("All models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    def _load_ocr_model(self):
        """Load OCR model (PaddleOCR)"""
        try:
            logger.info("Loading OCR model...")
            # Placeholder for actual model loading
            self.model_status['ocr'] = {
                'loaded': True,
                'model_path': str(Config.OCR_MODEL_PATH),
                'type': 'PaddleOCR'
            }
            logger.info("OCR model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load OCR model: {e}")
            self.model_status['ocr'] = {'loaded': False, 'error': str(e)}
    
    def _load_translation_model(self):
        """Load translation model (NLLB)"""
        try:
            logger.info("Loading translation model...")
            # Placeholder for actual model loading
            self.model_status['translation'] = {
                'loaded': True,
                'model_path': str(Config.TRANSLATION_MODEL_PATH),
                'type': 'NLLB-200'
            }
            logger.info("Translation model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load translation model: {e}")
            self.model_status['translation'] = {'loaded': False, 'error': str(e)}
    
    def _load_language_detection_model(self):
        """Load language detection model"""
        try:
            logger.info("Loading language detection model...")
            # Placeholder for actual model loading
            self.model_status['language_detection'] = {
                'loaded': True,
                'model_path': str(Config.LANG_DETECT_MODEL_PATH),
                'type': 'FastText'
            }
            logger.info("Language detection model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load language detection model: {e}")
            self.model_status['language_detection'] = {'loaded': False, 'error': str(e)}
    
    def _load_llm_model(self):
        """Load LLM model for post-editing"""
        try:
            logger.info("Loading LLM model...")
            # Placeholder for actual model loading
            self.model_status['llm'] = {
                'loaded': True,
                'model_path': str(Config.LLM_MODEL_PATH),
                'type': 'Phi-3'
            }
            logger.info("LLM model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load LLM model: {e}")
            self.model_status['llm'] = {'loaded': False, 'error': str(e)}
    
    def get_models_status(self):
        """Get status of all models"""
        if not self.model_status:
            self.load_all_models()
        
        return self.model_status
    
    def is_model_loaded(self, model_name):
        """Check if a specific model is loaded"""
        return self.model_status.get(model_name, {}).get('loaded', False)