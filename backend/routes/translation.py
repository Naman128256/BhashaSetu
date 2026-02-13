"""
Translation and text processing routes
"""

from flask import Blueprint, request, jsonify
from services.translation_service import TranslationService
from services.summarizer_service import SummarizerService
from utils.logger import get_logger

translation_bp = Blueprint('translation', __name__)
logger = get_logger(__name__)

@translation_bp.route('/translate', methods=['POST'])
def translate_text():
    """Translate text directly (without file upload)"""
    logger.info("Direct text translation requested")
    
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        source_lang = data.get('source_lang', 'auto')
        target_lang = data.get('target_lang', 'en')
        
        translation_service = TranslationService()
        result = translation_service.translate(text, source_lang, target_lang)
        
        logger.info(f"Text translation completed for {len(text)} characters")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in text translation: {e}")
        return jsonify({'error': str(e)}), 500

@translation_bp.route('/detect-language', methods=['POST'])
def detect_language():
    """Detect language of provided text"""
    logger.info("Language detection requested")
    
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        translation_service = TranslationService()
        result = translation_service.detect_language(text)
        
        logger.info(f"Language detection completed")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in language detection: {e}")
        return jsonify({'error': str(e)}), 500

@translation_bp.route('/summarize', methods=['POST'])
def summarize_text():
    """Summarize provided text"""
    logger.info("Text summarization requested")
    
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        max_length = data.get('max_length', 150)
        
        summarizer_service = SummarizerService()
        result = summarizer_service.summarize(text, max_length)
        
        logger.info(f"Text summarization completed")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in text summarization: {e}")
        return jsonify({'error': str(e)}), 500