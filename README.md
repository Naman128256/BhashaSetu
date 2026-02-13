# Backend — Offline Nepali & Sinhala Literature Translator

**Project:** Offline Literature Translator (Backend)  
**Authors:** Sahas + Team  
**Version:** 1.0  
**Date:** 2025-01-21  
**Python Version:** 3.13  

---

## Overview

This repository contains the complete backend implementation for an offline Nepali & Sinhala literature translator. The backend exposes a Flask HTTP API consumed by the Electron-wrapped React frontend. It provides:

- OCR (PaddleOCR)  
- Offline translation (NLLB-200)  
- Language detection (FastText)  
- Text summarization  

All processing happens locally on the user's machine.

---

## Quick Start

### Prerequisites

- Python 3.13 (or 3.10+)  
- pip 23+  
- 8–16 GB RAM (recommended)  
- 10+ GB free disk space (for models)  

---

## Installation & Setup

### Option 1: Quick Start (Minimal Setup)

```bash
# Windows
cd backend
quick_start.bat

# Python-based (all platforms)
cd backend
python start_minimal.py
```

---

### Option 2: Complete System Setup (Backend + Frontend)

```bash
# Windows
start_complete.bat

# Linux/macOS  
chmod +x start_complete.sh
./start_complete.sh
```

---

### Option 3: Full Backend Setup

```bash
# Windows
cd backend
run_simple.bat

# Linux/macOS  
cd backend
chmod +x run.sh
./run.sh
```

---

### Auto-Fix Missing Components

```cmd
# Windows
cd backend
fix_missing.bat
```

```bash
# Linux/macOS
cd backend
chmod +x fix_missing.sh
./fix_missing.sh
```

---

### Manual Setup

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

Backend:  
`http://127.0.0.1:5005`

Frontend:  
`http://localhost:8501`

---

## Verify Setup

```bash
python check_setup.py
curl http://127.0.0.1:5005/health
```

---

# Folder Structure

```
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── run.sh / run.bat
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── ocr/
│   ├── translation/
│   ├── language_detection/
│   ├── summarizer/
│   ├── models/
│   ├── logs/
│   └── temp/
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── README.md
├── ARCHITECTURE.md
├── MODELS.md
├── MISSING.md
└── postman_collection.json
```

---

# API Endpoints

## Health Check

### GET /health

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

---

### GET /version

```bash
curl http://127.0.0.1:5005/version
```

---

### GET /models/status

```bash
curl http://127.0.0.1:5005/models/status
```

---

# Document Processing

### POST /upload

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

---

### GET /status/<job_id>

```bash
curl http://127.0.0.1:5005/status/uuid-string
```

---

### GET /result/<job_id>

```bash
curl http://127.0.0.1:5005/result/uuid-string
```

---

# Translation Endpoints

### POST /translate

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"नमस्ते","source_lang":"auto","target_lang":"en"}' \
  http://127.0.0.1:5005/translate
```

---

### POST /detect-language

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"नमस्ते"}' \
  http://127.0.0.1:5005/detect-language
```

---

### POST /summarize

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"Long text to summarize...","max_length":150}' \
  http://127.0.0.1:5005/summarize
```

---

# Model Setup Status

## Available Models

1. FastText Language Detection (126 MB)  
2. NLLB Translation Weights (600 MB)  
3. PaddleOCR (auto-download)  
4. Dynamic Translation System  

---

# Logging System

Log files:

- `logs/app.log`
- `logs/error.log`
- `logs/model.log`

Log Levels:

- DEBUG  
- INFO  
- WARNING  
- ERROR  
- CRITICAL  

---

# PyInstaller Build

```bash
pip install pyinstaller

pyinstaller app.py --onefile --name nepali-sinhala-backend \
  --add-data "models;models" \
  --add-data "logs;logs" \
  --hidden-import=paddleocr \
  --hidden-import=transformers \
  --hidden-import=torch
```

---

# Performance Requirements

## Minimum

- 4 core CPU  
- 8 GB RAM  
- 20 GB Storage  

## Recommended

- 8 core CPU  
- 16 GB RAM  
- SSD Storage  

---

# Testing

```bash
pip install pytest pytest-cov
python -m pytest tests/ -v
```

---

# Troubleshooting

### Port Conflict

```bash
netstat -ano | findstr :5005
```

### Memory Issues

- Close heavy apps  
- Use quantized models  

---

# Security

- Fully offline processing  
- File validation  
- Secure path handling  
- No external network calls  

---

# License

MIT License  

---

# Quick Commands

```bash
quick_start.bat
python start_minimal.py
python check_setup.py
python app.py
curl http://127.0.0.1:5005/health
```

---

## Current Working Features

### Dynamic Translation System

- Nepali → English (context-aware)  
- Sinhala → English (cultural nuance preserved)  
- Real-time Language Detection  
- Intelligent fallback system  
- Cultural context preservation  

---

**Note:**  
This backend provides intelligent, culturally-aware translations preserving meaning and context across Nepali, Sinhala, and English languages with dynamic content analysis.
