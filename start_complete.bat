@echo off
echo 🚀 COMPLETE NEPALI ^& SINHALA TRANSLATOR SETUP
echo ============================================
echo Starting both Backend and Frontend
echo.

REM Step 1: Start Backend
echo [1/2] Starting Backend Server...
cd backend
start "Backend Server" cmd /k "run.bat"

REM Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 10 /nobreak >nul

REM Step 2: Start Frontend
echo [2/2] Starting Frontend UI...
cd ..\frontend
start "Frontend UI" cmd /k "run_frontend.bat"

echo.
echo ============================================
echo 🎉 COMPLETE SYSTEM STARTED!
echo ============================================
echo.
echo Backend: http://127.0.0.1:5005
echo Frontend: http://localhost:8501
echo.
echo Both services are running in separate windows.
echo Close the command windows to stop the services.
echo.
pause