"""
Document Processing Service - Handles OCR and document workflow
"""

from utils.logger import get_logger
from ocr.ocr_engine import OCREngine
from translation.translator import Translator
from language_detection.detector import LanguageDetector
from summarizer.summarizer import Summarizer
import threading
import time
import json

logger = get_logger(__name__)

class DocumentProcessor:
    """Handles document processing workflow"""
    
    def __init__(self):
        self.jobs = {}
        self.ocr_engine = OCREngine()
        self.translator = Translator()
        self.language_detector = LanguageDetector()
        self.summarizer = Summarizer()
    
    def process_document_async(self, job_id, file_path):
        """Start document processing in background thread"""
        logger.info(f"Starting async processing for job {job_id}")
        
        self.jobs[job_id] = {
            'status': 'processing',
            'progress': 0,
            'file_path': file_path,
            'start_time': time.time()
        }
        
        # Start processing in background thread
        thread = threading.Thread(
            target=self._process_document,
            args=(job_id, file_path)
        )
        thread.daemon = True
        thread.start()
    
    def _process_document(self, job_id, file_path):
        """Main document processing pipeline"""
        try:
            logger.info(f"Processing document for job {job_id}")
            
            # Step 1: OCR
            self._update_job_progress(job_id, 10, "Extracting text...")
            ocr_result = self.ocr_engine.extract_text(file_path)
            
            if not ocr_result or not ocr_result.get('text'):
                raise Exception("No text extracted from document")
            
            # Step 2: Language Detection
            self._update_job_progress(job_id, 30, "Detecting language...")
            detected_lang = self.language_detector.detect(ocr_result['text'])
            
            # Step 3: Translation
            self._update_job_progress(job_id, 50, "Translating text...")
            translation_result = self.translator.translate(
                ocr_result['text'],
                detected_lang['language'],
                'en'
            )
            
            # Step 4: Summarization
            self._update_job_progress(job_id, 80, "Generating summary...")
            summary_result = self.summarizer.summarize(translation_result['translated_text'])
            
            # Step 5: Complete
            self._update_job_progress(job_id, 100, "Completed")
            
            # Store final result
            self.jobs[job_id].update({
                'status': 'completed',
                'result': {
                    'original_text': ocr_result['text'],
                    'detected_language': detected_lang,
                    'translation': translation_result,
                    'summary': summary_result,
                    'processing_time': time.time() - self.jobs[job_id]['start_time']
                }
            })
            
            logger.info(f"Document processing completed for job {job_id}")
            
        except Exception as e:
            logger.error(f"Error processing document for job {job_id}: {e}")
            self.jobs[job_id].update({
                'status': 'failed',
                'error': str(e)
            })
    
    def _update_job_progress(self, job_id, progress, message):
        """Update job progress"""
        if job_id in self.jobs:
            self.jobs[job_id].update({
                'progress': progress,
                'message': message
            })
            logger.info(f"Job {job_id}: {progress}% - {message}")
    
    def get_job_status(self, job_id):
        """Get current job status"""
        if job_id not in self.jobs:
            return {'error': 'Job not found'}
        
        job = self.jobs[job_id]
        return {
            'job_id': job_id,
            'status': job['status'],
            'progress': job.get('progress', 0),
            'message': job.get('message', ''),
            'error': job.get('error')
        }
    
    def get_job_result(self, job_id):
        """Get job result if completed"""
        if job_id not in self.jobs:
            return None
        
        job = self.jobs[job_id]
        if job['status'] != 'completed':
            return None
        
        return job.get('result')