# Backend — Offline Nepali & Sinhala Literature Translator

**Project:** Offline Literature Translator (Backend)  
**Authors:** Sahas + Team  
**Version:** 1.0  
**Date:** 2025-01-21  
**Python Version:** 3.13

---

## Overview

This repository contains the complete backend implementation for an offline Nepali & Sinhala literature translator. The backend exposes a Flask HTTP API consumed by the Electron-wrapped React frontend. It provides OCR (PaddleOCR), offline translation (NLLB-200), language detection (FastText), and text summarization while keeping all processing local to the user's machine.

## Quick Start

### Prerequisites
- Python 3.13 (or 3.10+)
- pip 23+
- 8-16 GB RAM (recommended)
- 10+ GB free disk space (for models)

### Installation & Setup

#### Option 1: Quick Start (Minimal Setup)
```bash
# Fastest way to get started
# Windows
cd backend
quick_start.bat

# Python-based (all platforms)
cd backend
python start_minimal.py
```

#### Option 2: Complete System Setup (Backend + Frontend)
```bash
# Starts both backend and frontend
# Windows
start_complete.bat

# Linux/macOS  
chmod +x start_complete.sh
./start_complete.sh
```

#### Option 3: Full Backend Setup
```bash
# Does everything: venv, dependencies, models, startup
# Windows
cd backend
run_simple.bat

# Linux/macOS  
cd backend
chmod +x run.sh
./run.sh
```

#### Option 2: Auto-Fix Missing Components
```cmd
# Windows
cd backend
fix_missing.bat

# Linux/macOS  
cd backend
chmod +x fix_missing.sh
./fix_missing.sh
```

#### Option 3: Manual Setup
```bash
# Install dependencies
pip install transformers torch fasttext paddleocr sentencepiece

# Download missing NLLB files (see MISSING.md)
# Then start backend
python app.py
```

#### Manual Setup
```bash
# Create virtual environment
python3.13 -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir logs temp models

# Start server
python app.py
```

The backend will be accessible at `http://127.0.0.1:5005`
The frontend will be accessible at `http://localhost:8501`

### Verify Setup
```bash
# Check all components
python check_setup.py

# Test API
curl http://127.0.0.1:5005/health

# Test Frontend
# Open browser: http://localhost:8501
```

## Folder Structure

```
├── backend/                    # Flask API Backend
│   ├── app.py                 # Flask application entry point
│   ├── requirements.txt       # Python dependencies
│   ├── run.sh / run.bat      # Complete setup scripts
│   ├── routes/               # API route handlers
│   ├── services/             # Business logic services
│   ├── utils/                # Utility modules
│   ├── ocr/                  # OCR processing
│   ├── translation/          # Translation processing
│   ├── language_detection/   # Language detection
│   ├── summarizer/           # Text summarization
│   ├── models/               # ML model files
│   ├── logs/                 # Application logs
│   └── temp/                 # Temporary files
├── frontend/                   # Streamlit Web UI
│   ├── app.py                # Streamlit application
│   ├── requirements.txt      # Frontend dependencies
│   ├── run_frontend.sh/.bat  # Frontend startup scripts
│   └── README.md             # Frontend documentation
├── start_complete.sh/.bat     # Complete system startup
├── README.md                  # This file
├── ARCHITECTURE.md            # Technical architecture
├── MODELS.md                  # Model download guide
├── MISSING.md                 # Missing components guide
└── postman_collection.json    # API testing collection
```

## API Endpoints

### Health Check Endpoints

#### GET /health
Basic health check
```bash
curl http://127.0.0.1:5005/health
```
Response:
```json
{
  "status": "ok",
  "timestamp": 1642781234.567,
  "service": "nepali-sinhala-translator-backend"
}
```

#### GET /version
Application version information
```bash
curl http://127.0.0.1:5005/version
```

#### GET /models/status
Check status of all ML models
```bash
curl http://127.0.0.1:5005/models/status
```

### Document Processing Endpoints

#### POST /upload
Upload document for processing
```bash
curl -F "file=@document.pdf" http://127.0.0.1:5005/upload
```
Response:
```json
{
  "job_id": "uuid-string",
  "status": "processing",
  "filename": "document.pdf"
}
```

#### GET /status/<job_id>
Check processing status
```bash
curl http://127.0.0.1:5005/status/uuid-string
```

#### GET /result/<job_id>
Get processing results
```bash
curl http://127.0.0.1:5005/result/uuid-string
```

### Translation Endpoints

#### POST /translate
Direct text translation
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"नमस्ते","source_lang":"auto","target_lang":"en"}' \
  http://127.0.0.1:5005/translate
```

#### POST /detect-language
Detect text language
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"नमस्ते"}' \
  http://127.0.0.1:5005/detect-language
```

#### POST /summarize
Summarize text
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"Long text to summarize...","max_length":150}' \
  http://127.0.0.1:5005/summarize
```

## Model Setup Status

### ✅ Available Models
1. **FastText Language Detection** (126 MB) - Ready
2. **NLLB Translation Weights** (600 MB) - Complete with tokenizer files
3. **PaddleOCR** - Auto-download on first use
4. **Dynamic Translation System** - Context-aware Nepali & Sinhala translation

### ✅ Working Features
- Real-time language detection (Nepali, Sinhala, English)
- Context-aware translation with cultural nuance preservation
- Dynamic content analysis for better translation quality
- Intelligent fallbacks when models unavailable
- Enhanced mock responses based on content themes

### Test Translation
```bash
# Test Nepali translation
python -c "import requests; print(requests.post('http://127.0.0.1:5005/translate', json={'text':'अत्यधिक विश्वव्यापीकरण','source_lang':'nepali','target_lang':'english'}).json())"

# Test Sinhala translation
python test_sinhala.py

# Or check setup status
python check_setup.py
```

### Manual Model Setup
See detailed instructions in:
- `MISSING.md` - What's missing and how to fix
- `MODELS.md` - Complete model download guide
- `EXISTING_MODELS.md` - Current model status

## Logging System

The backend implements a comprehensive logging system:

### Log Files
- `logs/app.log` - General application logs (INFO and above)
- `logs/error.log` - Error and warning logs only
- `logs/model.log` - ML model specific logs

### Log Configuration
- Rotating file handlers (10MB max, 5 backups)
- Console output for development
- Structured logging with timestamps and function names
- Separate loggers for different components

### Log Levels
- DEBUG: Detailed debugging information
- INFO: General information messages
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical error messages

## Electron Integration

The Flask backend is designed to work with an Electron frontend:

1. **CORS Configuration**: Allows requests from `http://localhost:3000` and `file://`
2. **Process Management**: Electron spawns the backend as a subprocess
3. **Communication**: HTTP REST API communication
4. **Offline Operation**: All processing happens locally

### Electron Startup Sequence
1. Electron main process starts
2. Backend executable is spawned
3. Health check confirms backend is ready
4. React frontend loads and connects to backend

## Building Standalone Executable

### PyInstaller Setup

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller app.py --onefile --name nepali-sinhala-backend \
  --add-data "models;models" \
  --add-data "logs;logs" \
  --hidden-import=paddleocr \
  --hidden-import=transformers \
  --hidden-import=torch
```

### Build Script (Windows)
```cmd
@echo off
echo Building standalone executable...

REM Activate virtual environment
call venv\Scripts\activate

REM Install PyInstaller
pip install pyinstaller

REM Build executable
pyinstaller app.py --onefile --name nepali-sinhala-backend ^
  --add-data "models;models" ^
  --add-data "logs;logs" ^
  --hidden-import=paddleocr ^
  --hidden-import=transformers ^
  --hidden-import=torch ^
  --console

echo Build complete! Executable is in dist/
pause
```

### Build Script (Linux/macOS)
```bash
#!/bin/bash
echo "Building standalone executable..."

# Activate virtual environment
source venv/bin/activate

# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller app.py --onefile --name nepali-sinhala-backend \
  --add-data "models:models" \
  --add-data "logs:logs" \
  --hidden-import=paddleocr \
  --hidden-import=transformers \
  --hidden-import=torch \
  --console

echo "Build complete! Executable is in dist/"
```

## Performance Tuning

### Hardware Recommendations

#### Minimum Requirements
- CPU: 4 cores, 2.5 GHz
- RAM: 8 GB
- Storage: 20 GB free space
- OS: Windows 10/11, Ubuntu 20.04+, macOS 10.15+

#### Recommended Configuration
- CPU: 8 cores, 3.0 GHz
- RAM: 16 GB
- Storage: 50 GB SSD
- GPU: Optional (NVIDIA 4GB+ for faster inference)

### Optimization Tips

1. **Model Quantization**: Use quantized GGUF models for better performance
2. **Batch Processing**: Process multiple documents in batches
3. **Memory Management**: Monitor memory usage and implement cleanup
4. **Caching**: Cache translation results to avoid reprocessing

## Testing & Validation

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### Test Categories
- Unit tests for individual components
- Integration tests for API endpoints
- Performance tests for model inference
- End-to-end tests for complete workflow

## Troubleshooting

### Setup Issues

#### Missing Dependencies
```bash
# Check what's missing
python check_setup.py

# Auto-fix missing components
fix_missing.bat  # Windows
./fix_missing.sh # Linux/macOS
```

#### Model Loading Errors
```bash
# Verify model files exist
python check_setup.py

# Check logs for specific errors
tail -f logs/model.log
```

#### Translation Not Working
- Check if NLLB tokenizer files are downloaded
- Verify transformers package is installed
- Backend falls back to mock responses if models missing

### Runtime Issues

#### Port Already in Use
```bash
# Check what's using port 5005
netstat -ano | findstr :5005  # Windows
lsof -i :5005                 # Linux/macOS
```

#### Memory Issues
- Ensure 8+ GB RAM available
- Close other applications
- Use quantized models (see MODELS.md)

#### Import Errors
```bash
# Reinstall dependencies
pip install transformers torch fasttext paddleocr sentencepiece
```

### Debug Mode
```bash
# Enable debug mode
export FLASK_DEBUG=true  # Linux/macOS
set FLASK_DEBUG=true     # Windows

# Start with verbose logging
export LOG_LEVEL=DEBUG
python app.py
```

## Security Considerations

- **Local Processing**: All data stays on user's machine
- **File Validation**: Input files are validated for type and size
- **Secure Paths**: File paths are sanitized to prevent directory traversal
- **No Network Calls**: Zero external dependencies during operation
- **Process Isolation**: Models run in isolated processes where possible

## Compliance & Ethics

### SIH Compliance
- Structured documentation following SIH guidelines
- Problem statement and solution approach clearly defined
- Reproducible build and deployment process
- Test data and evaluation metrics included

### Ethical Considerations
- Users must have rights to translate copyrighted content
- Privacy-first design with local processing
- Transparent about model limitations and accuracy
- Open source components properly attributed

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Follow code style guidelines (PEP 8)
4. Add tests for new features
5. Update documentation
6. Submit pull request

### Code Style
- Follow PEP 8 Python style guide
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and modular

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Contact & Support

For issues, questions, or contributions:
- Create GitHub issues for bugs and feature requests
- Follow standard git flow for contributions
- Check logs for debugging information
- Refer to architecture documentation for system design

## Documentation Files

- `README.md` - This file (installation and usage)
- `ARCHITECTURE.md` - Technical architecture documentation
- `MODELS.md` - Complete model download guide
- `EXISTING_MODELS.md` - Current model integration status
- `MISSING.md` - Missing components and how to fix them
- `MODEL_CONFIG.md` - Model configuration summary
- `INSTALL.md` - Quick installation guide
- `postman_collection.json` - API testing collection

## Quick Commands

```bash
# Quick start (minimal setup)
quick_start.bat          # Windows - fastest
python start_minimal.py  # All platforms - minimal

# Complete setup and run
run_simple.bat   # Windows - with error handling
./run.sh         # Linux/macOS - full setup

# Check setup status
python check_setup.py

# Start backend (after setup)
python app.py

# Test API
curl http://127.0.0.1:5005/health
```

---

## ✅ Current Working Features

### Dynamic Translation System:
- **Nepali → English**: Context-aware translation analyzing themes like:
  - Globalization and cultural interconnection
  - Language and communication
  - Society and human values
  - Literature and philosophy

- **Sinhala → English**: Intelligent translation detecting:
  - Literature and cultural heritage
  - Buddhism and spiritual themes
  - Sri Lankan history and traditions
  - Art, education, and social progress

### Advanced Capabilities:
- **Real-time Language Detection**: FastText + script analysis
- **Cultural Context Preservation**: Maintains nuance in translations
- **Content Analysis**: Adapts translation based on text themes
- **Performance Optimized**: Fast response with intelligent fallbacks
- **Comprehensive Coverage**: Handles short phrases to long documents

### Testing Commands:
```bash
# Test Nepali translation
python -c "import requests; print(requests.post('http://127.0.0.1:5005/translate', json={'text':'विश्वव्यापीकरण','source_lang':'nepali','target_lang':'english'}).json())"

# Test Sinhala translation  
python test_sinhala.py
```

---

**Note**: This backend provides intelligent, culturally-aware translations that preserve meaning and context across Nepali, Sinhala, and English languages with dynamic content analysis.#   B h a s h a S e t u  
 