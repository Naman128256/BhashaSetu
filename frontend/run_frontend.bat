@echo off
echo Starting Nepali ^& Sinhala Literature Translator Frontend
echo =====================================================

REM Check if backend is running
echo Checking backend status...
curl -s http://127.0.0.1:5005/health >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Backend is not running!
    echo Please start the backend first:
    echo   cd ../backend
    echo   run.bat
    echo.
    pause
    exit /b 1
)

echo ✅ Backend is running

REM Install frontend dependencies
echo Installing frontend dependencies...
pip install streamlit requests Pillow

REM Start Streamlit app
echo.
echo Starting Streamlit frontend...
echo Frontend will open in your browser at: http://localhost:8501
echo.
streamlit run app.py