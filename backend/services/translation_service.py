"""
Translation Service - Handles direct text translation requests
"""

from utils.logger import get_logger
from translation.translator import Translator
from language_detection.detector import LanguageDetector

logger = get_logger(__name__)

class TranslationService:
    """Service for handling translation requests"""
    
    def __init__(self):
        self.translator = Translator()
        self.language_detector = LanguageDetector()
    
    def translate(self, text, source_lang='auto', target_lang='en'):
        """Translate text from source to target language"""
        logger.info(f"Translating text: {len(text)} characters")
        
        try:
            # Auto-detect source language if needed
            if source_lang == 'auto':
                detection_result = self.language_detector.detect(text)
                source_lang = detection_result['language']
                logger.info(f"Auto-detected language: {source_lang}")
            
            # Perform translation
            result = self.translator.translate(text, source_lang, target_lang)
            
            return {
                'original_text': text,
                'translated_text': result['translated_text'],
                'source_language': source_lang,
                'target_language': target_lang,
                'confidence': result.get('confidence', 0.0)
            }
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            raise
    
    def detect_language(self, text):
        """Detect language of the provided text"""
        logger.info(f"Detecting language for text: {len(text)} characters")
        
        try:
            result = self.language_detector.detect(text)
            return result
            
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            raise