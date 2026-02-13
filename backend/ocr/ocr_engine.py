"""
OCR Engine - Handles text extraction from images and PDFs
"""

from utils.logger import get_logger
from utils.config import Config
from pathlib import Path

try:
    import numpy as np
except ImportError:
    np = None

try:
    import cv2
except ImportError:
    cv2 = None

logger = get_logger('models.ocr')

class OCREngine:
    """OCR engine using PaddleOCR for text extraction"""
    
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load PaddleOCR model"""
        try:
            logger.info("Loading PaddleOCR model...")
            try:
                from paddleocr import PaddleOCR
                self.model = PaddleOCR(use_angle_cls=True, lang='en')
                logger.info("PaddleOCR model loaded successfully")
            except ImportError:
                logger.warning("PaddleOCR not installed, using mock model")
                self.model = "paddleocr_mock"
            
        except Exception as e:
            logger.error(f"Failed to load OCR model: {e}")
            self.model = "paddleocr_mock"
    
    def extract_text(self, file_path):
        """Extract text from image or PDF file"""
        logger.info(f"Extracting text from: {file_path}")
        
        try:
            file_path = Path(file_path)
            
            if file_path.suffix.lower() == '.pdf':
                return self._extract_from_pdf(file_path)
            else:
                return self._extract_from_image(file_path)
                
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            raise
    
    def _extract_from_image(self, image_path):
        """Extract text from image file"""
        logger.info(f"Processing image: {image_path}")
        
        try:
            if self.model != "paddleocr_mock":
                # Real PaddleOCR processing
                result = self.model.ocr(str(image_path), cls=True)
                
                extracted_text = ""
                blocks = []
                
                if result and result[0]:
                    for line in result[0]:
                        if line[1][0]:  # Check if text exists
                            text = line[1][0]
                            confidence = line[1][1]
                            bbox = line[0]
                            
                            extracted_text += text + " "
                            blocks.append({
                                'text': text,
                                'bbox': bbox,
                                'confidence': confidence
                            })
                
                return {
                    'text': extracted_text.strip(),
                    'confidence': sum(b['confidence'] for b in blocks) / len(blocks) if blocks else 0,
                    'blocks': blocks
                }
            else:
                # Mock result
                extracted_text = f"Sample extracted text from {Path(image_path).name}"
                return {
                    'text': extracted_text,
                    'confidence': 0.95,
                    'blocks': [{
                        'text': extracted_text,
                        'bbox': [0, 0, 100, 50],
                        'confidence': 0.95
                    }]
                }
            
        except Exception as e:
            logger.error(f"Image OCR failed: {e}")
            raise
    
    def _extract_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        logger.info(f"Processing PDF: {pdf_path}")
        
        try:
            # Placeholder for PDF processing
            # import fitz  # PyMuPDF
            # doc = fitz.open(pdf_path)
            
            # Mock result for now
            extracted_text = f"Sample extracted text from PDF {pdf_path.name}"
            
            return {
                'text': extracted_text,
                'confidence': 0.90,
                'pages': 1,
                'blocks': [
                    {
                        'text': extracted_text,
                        'page': 1,
                        'bbox': [0, 0, 100, 50],
                        'confidence': 0.90
                    }
                ]
            }
            
        except Exception as e:
            logger.error(f"PDF OCR failed: {e}")
            raise
    
    def _preprocess_image(self, image):
        """Preprocess image for better OCR results"""
        try:
            if cv2 is not None:
                # Convert to grayscale
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                # Denoise
                denoised = cv2.fastNlMeansDenoising(gray)
                
                # Threshold
                _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                
                return thresh
            else:
                return image
            
        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            return image