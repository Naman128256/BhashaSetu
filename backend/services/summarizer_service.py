"""
Summarizer Service - Handles text summarization requests
"""

from utils.logger import get_logger
from summarizer.summarizer import Summarizer

logger = get_logger(__name__)

class SummarizerService:
    """Service for handling summarization requests"""
    
    def __init__(self):
        self.summarizer = Summarizer()
    
    def summarize(self, text, max_length=150):
        """Summarize the provided text"""
        logger.info(f"Summarizing text: {len(text)} characters")
        
        try:
            result = self.summarizer.summarize(text, max_length)
            
            return {
                'original_text': text,
                'summary': result['summary'],
                'original_length': len(text),
                'summary_length': len(result['summary']),
                'compression_ratio': len(result['summary']) / len(text)
            }
            
        except Exception as e:
            logger.error(f"Summarization error: {e}")
            raise