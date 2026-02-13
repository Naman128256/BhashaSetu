@echo off
REM Start script for Windows

echo Starting Nepali ^& Sinhala Literature Translator Backend...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo Creating directories...
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp
if not exist "models" mkdir models

REM Start the Flask application
echo Starting Flask server...
set FLASK_APP=app.py
set FLASK_ENV=production
python app.py

pause