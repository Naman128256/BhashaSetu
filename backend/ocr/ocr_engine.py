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
        """Initialize Tesseract OCR"""
        try:
            import pytesseract

            self.model = pytesseract
            logger.info("Tesseract OCR initialized successfully")

        except ImportError:
            logger.error("pytesseract is not installed")
            self.model = None


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
        """Extract Nepali, Sinhala and English text from an image"""
        logger.info(f"Processing image: {image_path}")

        try:
            from PIL import Image

            if self.model is None:
                raise RuntimeError("Tesseract OCR is unavailable")

            image = Image.open(image_path).convert("RGB")

            # Recognize Nepali, Sinhala and English together
            result = self.model.image_to_data(
                image,
                lang="nep+sin+eng",
                config="--oem 1 --psm 6",
                output_type=self.model.Output.DICT
            )

            blocks = []
            extracted_lines = []
            confidences = []

            for i, text in enumerate(result["text"]):
                text = text.strip()

                if not text:
                    continue

                try:
                    confidence = float(result["conf"][i])
                except (ValueError, TypeError):
                    continue

                if confidence < 0:
                    continue

                blocks.append({
                    "text": text,
                    "bbox": [
                        result["left"][i],
                        result["top"][i],
                        result["left"][i] + result["width"][i],
                        result["top"][i] + result["height"][i]
                    ],
                    "confidence": confidence / 100
                })

                extracted_lines.append(text)
                confidences.append(confidence / 100)

            return {
                "text": " ".join(extracted_lines),
                "confidence": (
                    sum(confidences) / len(confidences)
                    if confidences else 0
                ),
                "blocks": blocks
            }

        except Exception as e:
            logger.error(f"Image OCR failed: {e}")
            raise


    def _extract_from_pdf(self, pdf_path):
        """Extract text from digital and scanned PDF pages"""
        import fitz
        from PIL import Image
        import io

        logger.info(f"Processing PDF: {pdf_path}")

        if self.model is None:
            raise RuntimeError("Tesseract OCR is unavailable")

        extracted_pages = []
        all_blocks = []
        confidences = []

        try:
            doc = fitz.open(pdf_path)

            for page_number, page in enumerate(doc, start=1):

                # First try extracting embedded digital text
                page_text = page.get_text("text").strip()

                if len(page_text) >= 20:
                    extracted_pages.append(page_text)

                    all_blocks.append({
                        "text": page_text,
                        "page": page_number,
                        "bbox": list(page.rect),
                        "confidence": 1.0
                    })

                    confidences.append(1.0)
                    continue

                # If no usable text exists, perform OCR
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)

                image = Image.open(
                    io.BytesIO(pix.tobytes("png"))
                ).convert("RGB")

                result = self.model.image_to_data(
                    image,
                    lang="nep+sin+eng",
                    config="--oem 1 --psm 6",
                    output_type=self.model.Output.DICT
                )

                page_lines = []

                for i, word in enumerate(result["text"]):
                    word = word.strip()

                    if not word:
                        continue

                    try:
                        confidence = float(result["conf"][i])
                    except (ValueError, TypeError):
                        continue

                    if confidence < 0:
                        continue

                    confidence = confidence / 100

                    all_blocks.append({
                        "text": word,
                        "page": page_number,
                        "bbox": [
                            result["left"][i],
                            result["top"][i],
                            result["left"][i] + result["width"][i],
                            result["top"][i] + result["height"][i]
                        ],
                        "confidence": confidence
                    })

                    page_lines.append(word)
                    confidences.append(confidence)

                extracted_pages.append(" ".join(page_lines))

            doc.close()

            return {
                "text": "\n\n".join(extracted_pages).strip(),
                "confidence": (
                    sum(confidences) / len(confidences)
                    if confidences else 0
                ),
                "pages": len(extracted_pages),
                "blocks": all_blocks
            }

        except Exception as e:
            logger.exception(f"PDF OCR failed: {e}")
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