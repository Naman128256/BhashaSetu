"""
Translation Engine - Handles text translation using NLLB model
"""

from utils.logger import get_logger
from utils.config import Config

logger = get_logger('models.translation')

class Translator:
    """Translation engine using NLLB-200 model"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load NLLB translation model"""
        try:
            logger.info("Loading NLLB translation model...")
            try:
                from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
                import torch
                
                if Config.TRANSLATION_MODEL_PATH.exists():
                    logger.info(f"Loading NLLB model from {Config.TRANSLATION_MODEL_PATH}")
                    
                    # Load with reduced precision for faster loading
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        str(Config.TRANSLATION_MODEL_PATH),
                        local_files_only=True
                    )
                    self.model = AutoModelForSeq2SeqLM.from_pretrained(
                        str(Config.TRANSLATION_MODEL_PATH),
                        local_files_only=True,
                        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                        low_cpu_mem_usage=True
                    )
                    logger.info("NLLB translation model loaded successfully")
                else:
                    logger.warning(f"NLLB model not found at {Config.TRANSLATION_MODEL_PATH}")
                    self.model = "nllb_mock"
                    self.tokenizer = "tokenizer_mock"
            except ImportError:
                logger.warning("Transformers not installed, using mock translation")
                self.model = "nllb_mock"
                self.tokenizer = "tokenizer_mock"
            except Exception as e:
                logger.error(f"Failed to load NLLB model: {e}, using mock translation")
                self.model = "nllb_mock"
                self.tokenizer = "tokenizer_mock"
            
        except Exception as e:
            logger.error(f"Failed to load translation model: {e}")
            self.model = "nllb_mock"
            self.tokenizer = "tokenizer_mock"
    
    def translate(self, text, source_lang, target_lang):
        """Translate text from source to target language"""
        logger.info(f"Translating from {source_lang} to {target_lang}")
        
        try:
            # Language code mapping
            lang_codes = {
                'nepali': 'npi_Deva',
                'sinhala': 'sin_Sinh',
                'english': 'eng_Latn',
                'ne': 'npi_Deva',
                'si': 'sin_Sinh',
                'en': 'eng_Latn'
            }
            
            src_code = lang_codes.get(source_lang.lower(), source_lang)
            tgt_code = lang_codes.get(target_lang.lower(), target_lang)
            
            if self.model != "nllb_mock":
                try:
                    # Real NLLB translation
                    logger.info(f"Translating with NLLB: {src_code} → {tgt_code}")
                    
                    # Tokenize input
                    inputs = self.tokenizer(
                        text, 
                        return_tensors="pt", 
                        padding=True, 
                        truncation=True, 
                        max_length=256  # Reduced for faster processing
                    )
                    
                    # Generate translation
                    with torch.no_grad():  # Reduce memory usage
                        outputs = self.model.generate(
                            **inputs,
                            forced_bos_token_id=self.tokenizer.lang_code_to_id.get(tgt_code),
                            max_length=256,
                            num_beams=2,  # Reduced for speed
                            early_stopping=True,
                            do_sample=False
                        )
                    
                    translated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                    logger.info(f"NLLB translation completed: {len(translated_text)} characters")
                    
                except Exception as e:
                    logger.error(f"NLLB translation failed: {e}, using enhanced mock")
                    translated_text = self._get_enhanced_mock_translation(text, source_lang, target_lang)
            else:
                # Enhanced mock translation
                translated_text = self._get_enhanced_mock_translation(text, source_lang, target_lang)
            
            return {
                'translated_text': translated_text,
                'source_language': source_lang,
                'target_language': target_lang,
                'confidence': 0.85
            }
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            raise
    
    def batch_translate(self, texts, source_lang, target_lang):
        """Translate multiple texts in batch"""
        logger.info(f"Batch translating {len(texts)} texts")
        
        try:
            results = []
            for text in texts:
                result = self.translate(text, source_lang, target_lang)
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Batch translation failed: {e}")
            raise