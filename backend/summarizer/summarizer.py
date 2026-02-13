"""
Text Summarization Engine - Generates summaries of translated text
"""

from utils.logger import get_logger
from utils.config import Config
import re

logger = get_logger('models.summarizer')

class Summarizer:
    """Text summarization using extractive and abstractive methods"""
    
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load summarization model"""
        try:
            logger.info("Loading summarization model...")
            # Placeholder for actual model loading
            # from transformers import pipeline
            # self.model = pipeline("summarization", model="facebook/bart-large-cnn")
            
            self.model = "summarization_placeholder"
            logger.info("Summarization model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load summarization model: {e}")
            raise
    
    def summarize(self, text, max_length=150, min_length=30):
        """Generate summary of the input text"""
        logger.info(f"Summarizing text: {len(text)} characters")
        
        try:
            # Check if text is long enough to summarize
            if len(text.split()) < 50:
                return {
                    'summary': text,
                    'method': 'original',
                    'compression_ratio': 1.0
                }
            
            # Use extractive summarization for now (placeholder)
            summary = self._extractive_summarization(text, max_length)
            
            # Placeholder for abstractive summarization
            # summary = self.model(text, max_length=max_length, min_length=min_length, do_sample=False)
            # summary_text = summary[0]['summary_text']
            
            return {
                'summary': summary,
                'method': 'extractive',
                'original_length': len(text),
                'summary_length': len(summary),
                'compression_ratio': len(summary) / len(text)
            }
            
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            raise
    
    def _extractive_summarization(self, text, max_length):
        """Simple extractive summarization"""
        try:
            # Split into sentences
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if not sentences:
                return text
            
            # Score sentences by length and position
            scored_sentences = []
            for i, sentence in enumerate(sentences):
                # Simple scoring: prefer longer sentences and earlier positions
                score = len(sentence.split()) * (1 - i / len(sentences) * 0.5)
                scored_sentences.append((score, sentence))
            
            # Sort by score and select top sentences
            scored_sentences.sort(reverse=True)
            
            # Select sentences until max_length is reached
            selected_sentences = []
            current_length = 0
            
            for score, sentence in scored_sentences:
                if current_length + len(sentence) <= max_length:
                    selected_sentences.append(sentence)
                    current_length += len(sentence)
                else:
                    break
            
            # If no sentences fit, take the first one (truncated if necessary)
            if not selected_sentences and sentences:
                first_sentence = sentences[0]
                if len(first_sentence) > max_length:
                    first_sentence = first_sentence[:max_length-3] + "..."
                selected_sentences = [first_sentence]
            
            return '. '.join(selected_sentences) + '.'
            
        except Exception as e:
            logger.error(f"Extractive summarization failed: {e}")
            return text[:max_length] + "..." if len(text) > max_length else text