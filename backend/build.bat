@echo off
REM Build script for creating standalone executable

echo Building Nepali ^& Sinhala Literature Translator Backend...

REM Check if virtual environment exists
if not exist "venv" (
    echo Error: Virtual environment not found. Run start.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install PyInstaller if not already installed
echo Installing PyInstaller...
pip install pyinstaller

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del *.spec

REM Create necessary directories for bundling
echo Creating directories...
if not exist "models" mkdir models
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp

REM Build the executable
echo Building executable...
pyinstaller app.py --onefile --name nepali-sinhala-backend ^
  --add-data "models;models" ^
  --add-data "logs;logs" ^
  --add-data "temp;temp" ^
  --hidden-import=paddleocr ^
  --hidden-import=transformers ^
  --hidden-import=torch ^
  --hidden-import=cv2 ^
  --hidden-import=numpy ^
  --hidden-import=PIL ^
  --hidden-import=flask ^
  --hidden-import=flask_cors ^
  --console ^
  --noconfirm

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Build completed successfully!
    echo Executable location: dist\nepali-sinhala-backend.exe
    echo.
    echo To test the executable:
    echo   cd dist
    echo   nepali-sinhala-backend.exe
    echo.
) else (
    echo.
    echo Build failed! Check the error messages above.
    echo.
)

pause