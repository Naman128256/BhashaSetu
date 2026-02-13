"""
Language Detection Engine - Detects language of input text
"""

from utils.logger import get_logger
from utils.config import Config
import re

logger = get_logger('models.language_detection')

class LanguageDetector:
    """Language detection using FastText model"""
    
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load FastText language detection model"""
        try:
            logger.info("Loading FastText language detection model...")
            try:
                import fasttext
                if Config.LANG_DETECT_MODEL_PATH.exists():
                    logger.info(f"Loading FastText model from {Config.LANG_DETECT_MODEL_PATH}")
                    self.model = fasttext.load_model(str(Config.LANG_DETECT_MODEL_PATH))
                    logger.info("FastText model loaded successfully")
                else:
                    logger.warning(f"FastText model not found at {Config.LANG_DETECT_MODEL_PATH}, using script analysis")
                    self.model = "fasttext_mock"
            except ImportError:
                logger.warning("FastText not installed, using script-based detection")
                self.model = "fasttext_mock"
            except Exception as e:
                logger.error(f"Failed to load FastText model: {e}, using script analysis")
                self.model = "fasttext_mock"
            logger.info("FastText language detection model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load language detection model: {e}")
            raise
    
    def detect(self, text):
        """Detect language of the input text"""
        logger.info(f"Detecting language for text: {len(text)} characters")
        
        try:
            # Preprocess text
            cleaned_text = self._preprocess_text(text)
            
            if not cleaned_text:
                return {
                    'language': 'unknown',
                    'confidence': 0.0,
                    'script': 'unknown'
                }
            
            if self.model != "fasttext_mock":
                try:
                    # Real FastText detection
                    predictions = self.model.predict(cleaned_text, k=1)
                    lang_label = predictions[0][0].replace('__label__', '')
                    confidence = float(predictions[1][0])
                    
                    # Map FastText codes to our language names
                    lang_map = {'ne': 'nepali', 'si': 'sinhala', 'en': 'english'}
                    detected_lang = lang_map.get(lang_label, lang_label)
                    script = self._get_script_from_lang(detected_lang)
                    
                    logger.info(f"FastText detected: {detected_lang} (confidence: {confidence:.2f})")
                    
                    return {
                        'language': detected_lang,
                        'confidence': confidence,
                        'script': script,
                        'text_length': len(text)
                    }
                except Exception as e:
                    logger.error(f"FastText prediction failed: {e}, falling back to script analysis")
            
            # Fallback script analysis
            detected_lang, confidence, script = self._analyze_script(cleaned_text)
            
            return {
                'language': detected_lang,
                'confidence': confidence,
                'script': script,
                'text_length': len(text)
            }
            
        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            raise
    
    def _preprocess_text(self, text):
        """Preprocess text for language detection"""
        try:
            # Remove extra whitespace and normalize
            cleaned = re.sub(r'\s+', ' ', text.strip())
            
            # Remove numbers and punctuation for better detection
            cleaned = re.sub(r'[0-9\.\,\!\?\;\:\-\(\)\[\]\"\']+', ' ', cleaned)
            
            return cleaned.strip()
            
        except Exception as e:
            logger.error(f"Text preprocessing failed: {e}")
            return text
    
    def _analyze_script(self, text):
        """Analyze script to help with language detection"""
        try:
            # Devanagari script (Nepali)
            devanagari_chars = len(re.findall(r'[\u0900-\u097F]', text))
            
            # Sinhala script
            sinhala_chars = len(re.findall(r'[\u0D80-\u0DFF]', text))
            
            # Latin script (English)
            latin_chars = len(re.findall(r'[a-zA-Z]', text))
            
            total_chars = len(re.sub(r'\s', '', text))
            
            if total_chars == 0:
                return 'unknown', 0.0, 'unknown'
            
            # Calculate percentages
            devanagari_pct = devanagari_chars / total_chars
            sinhala_pct = sinhala_chars / total_chars
            latin_pct = latin_chars / total_chars
            
            # Determine language based on script dominance
            if devanagari_pct > 0.5:
                return 'nepali', min(0.95, devanagari_pct + 0.1), 'devanagari'
            elif sinhala_pct > 0.5:
                return 'sinhala', min(0.95, sinhala_pct + 0.1), 'sinhala'
            elif latin_pct > 0.7:
                return 'english', min(0.90, latin_pct), 'latin'
            else:
                return 'mixed', 0.5, 'mixed'
                
        except Exception as e:
            logger.error(f"Script analysis failed: {e}")
            return 'unknown', 0.0, 'unknown'
    
    def _get_script_from_lang(self, language):
        """Get script type from language name"""
        script_map = {
            'nepali': 'devanagari',
            'sinhala': 'sinhala',
            'english': 'latin'
        }
        return script_map.get(language, 'unknown')