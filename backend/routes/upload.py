"""
File upload and document processing routes
"""

from flask import Blueprint, request, jsonify
from flask import send_file
from services.pdf_generator import generate_translation_pdf
from werkzeug.utils import secure_filename
from services.document_processor import DocumentProcessor
from utils.logger import get_logger
from utils.config import Config
import os
import uuid

upload_bp = Blueprint('upload', __name__)
logger = get_logger(__name__)
processor = DocumentProcessor()

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and initiate processing"""
    logger.info("File upload requested")
    
    if 'file' not in request.files:
        logger.warning("No file provided in upload request")
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        logger.warning("Empty filename in upload request")
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        logger.warning(f"Invalid file type: {file.filename}")
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = Config.TEMP_DIR / f"{job_id}_{filename}"
        file.save(str(file_path))
        
        logger.info(f"File uploaded successfully: {filename}, Job ID: {job_id}")
        
        # Initialize document processor
        # processor = DocumentProcessor()
        
        # Start processing (async)
        processor.process_document_async(job_id, str(file_path))
        
        return jsonify({
            'job_id': job_id,
            'status': 'processing',
            'filename': filename
        })
        
    except Exception as e:
        logger.error(f"Error during file upload: {e}")
        return jsonify({'error': str(e)}), 500

@upload_bp.route('/status/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get processing status for a job"""
    logger.info(f"Status check for job: {job_id}")
    
    try:
        # processor = DocumentProcessor()
        status = processor.get_job_status(job_id)
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Error getting job status: {e}")
        return jsonify({'error': str(e)}), 500

@upload_bp.route('/result/<job_id>', methods=['GET'])
def get_result(job_id):
    """Get processing result for a completed job"""
    logger.info(f"Result requested for job: {job_id}")
    
    try:
        # processor = DocumentProcessor()
        result = processor.get_job_result(job_id)
        
        if result is None:
            return jsonify({'error': 'Job not found or not completed'}), 404
            
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error getting job result: {e}")
        return jsonify({'error': str(e)}), 500




@upload_bp.route('/download/<job_id>', methods=['GET'])
def download_translation_pdf(job_id):
    """Generate and download translated text as a PDF."""

    logger.info(f"PDF download requested for job: {job_id}")

    try:
        result = processor.get_job_result(job_id)

        if result is None:
            return jsonify({
                'error': 'Job not found or not completed'
            }), 404

        translation_info = result.get('translation', {})
        translated_text = translation_info.get('translated_text', '')

        if not translated_text.strip():
            return jsonify({
                'error': 'No translated text available'
            }), 404

        pdf_buffer = generate_translation_pdf(translated_text)

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'BhashaSetu_Translation_{job_id[:8]}.pdf'
        )

    except Exception as e:
        logger.error(f"Error generating translation PDF: {e}")
        return jsonify({'error': str(e)}), 500
