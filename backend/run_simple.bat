@echo off
echo Starting Nepali ^& Sinhala Literature Translator Backend
echo =====================================================

REM Create virtual environment if not exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install only essential packages that work with Python 3.13
echo Installing essential packages...
pip install Flask Flask-CORS Werkzeug
pip install numpy Pillow requests

REM Try to install optional ML packages (ignore errors)
echo Installing optional ML packages...
pip install --no-deps transformers || echo Warning: transformers failed
pip install torch --index-url https://download.pytorch.org/whl/cpu || echo Warning: torch failed
pip install fasttext-wheel || echo Warning: fasttext failed
pip install paddleocr || echo Warning: paddleocr failed

REM Create directories
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp

echo.
echo Starting Flask backend...
python app.py