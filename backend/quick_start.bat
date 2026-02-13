@echo off
echo Quick Start - Nepali ^& Sinhala Translator
echo ========================================

REM Install minimal requirements
pip install Flask Flask-CORS numpy Pillow requests

REM Create directories
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp

REM Start backend
echo Starting backend...
python app.py

pause