@echo off
setlocal enabledelayedexpansion

REM Comprehensive setup and run script for Nepali & Sinhala Literature Translator Backend
REM This script handles everything: environment, dependencies, models, and startup

echo 🚀 NEPALI ^& SINHALA LITERATURE TRANSLATOR BACKEND
echo ==================================================
echo Comprehensive setup and run script
echo This will set up everything from scratch and start the backend
echo.

REM Step 1: Check system requirements
echo [1/8] Checking system requirements...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.10+ first.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Found Python %PYTHON_VERSION%

pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found. Please install pip first.
    pause
    exit /b 1
)
echo ✅ pip found

curl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ curl not found. Please install curl first.
    pause
    exit /b 1
)
echo ✅ curl found

REM Step 2: Create and activate virtual environment
echo.
echo [2/8] Setting up virtual environment...
if not exist "venv" (
    echo   Creating virtual environment...
    python -m venv venv
    echo   ✅ Virtual environment created
) else (
    echo   ✅ Virtual environment already exists
)

echo   Activating virtual environment...
call venv\Scripts\activate
echo   ✅ Virtual environment activated

REM Step 3: Upgrade pip and install basic tools
echo.
echo [3/8] Installing basic dependencies...
pip install --upgrade pip setuptools wheel
pip install Flask==3.0.0 Flask-CORS==4.0.0 Werkzeug==3.0.1
pip install numpy==1.24.3 Pillow==10.1.0
echo ✅ Basic dependencies installed

REM Step 4: Install ML dependencies
echo.
echo [4/8] Installing ML dependencies...
echo   This may take several minutes...

REM Install PyTorch (CPU version for compatibility)
pip install torch==2.1.1 torchvision==0.16.1 --index-url https://download.pytorch.org/whl/cpu

REM Install transformers and related
pip install transformers==4.35.2 tokenizers==0.15.0 sentencepiece==0.1.99

REM Install FastText
pip install fasttext==0.9.2

REM Install PaddleOCR and dependencies
pip install paddlepaddle==2.5.2 paddleocr==2.7.3 opencv-python==4.8.1.78

REM Install additional dependencies
pip install requests==2.31.0 tqdm==4.66.1 packaging==23.2
echo ✅ ML dependencies installed

REM Step 5: Create directory structure
echo.
echo [5/8] Creating directory structure...
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp
if not exist "models\models\paddleocr" mkdir models\models\paddleocr
if not exist "models\models\nllb_model" mkdir models\models\nllb_model
if not exist "models\models\fasttext" mkdir models\models\fasttext
if not exist "models\models\phi3" mkdir models\models\phi3
echo ✅ Directories created

REM Step 6: Check existing models
echo.
echo [6/8] Checking existing models...

REM Check FastText model
if exist "models\models\fasttext\lid.176.bin" (
    echo   ✅ FastText model found
) else if exist "models\models\lid.176.ftz" (
    echo   ✅ FastText compressed model found
    echo   📁 Moving FastText model to correct location...
    move models\models\lid.176.ftz models\models\fasttext\
) else (
    echo   📥 Downloading FastText language detection model...
    curl -L -o models\models\fasttext\lid.176.bin ^
        https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
    echo   ✅ FastText model downloaded
)

REM Check NLLB model
if exist "models\models\nllb_model\pytorch_model.bin" (
    echo   ✅ NLLB model weights found
) else (
    echo   ⚠️  NLLB model weights not found - translation will use fallback
)

REM Step 7: Download missing NLLB tokenizer files
echo.
echo [7/8] Setting up NLLB translation model...
cd models\models\nllb_model

set NLLB_BASE_URL=https://huggingface.co/facebook/nllb-200-distilled-600M/resolve/main

REM Download missing files
set files=config.json tokenizer.json tokenizer_config.json sentencepiece.bpe.model special_tokens_map.json

for %%f in (%files%) do (
    if not exist "%%f" (
        echo   📥 Downloading %%f...
        curl -L -o "%%f" "%NLLB_BASE_URL%/%%f"
        echo   ✅ %%f downloaded
    ) else (
        echo   ✅ %%f already exists
    )
)

cd ..\..\..

REM Check if we have complete NLLB model
if exist "models\models\nllb_model\pytorch_model.bin" (
    if exist "models\models\nllb_model\config.json" (
        echo   ✅ NLLB model complete - real translation available
    ) else (
        echo   ⚠️  NLLB model incomplete - will use mock translation
    )
) else (
    echo   ⚠️  NLLB model incomplete - will use mock translation
)

REM Step 8: Final verification and startup
echo.
echo [8/8] Final verification and startup...

echo   Running setup verification...
python -c "
import sys
print(f'Python: {sys.version}')

# Check critical imports
try:
    import flask
    print('✅ Flask available')
except ImportError:
    print('❌ Flask missing')

try:
    import transformers
    print('✅ Transformers available')
except ImportError:
    print('⚠️  Transformers missing - translation fallback')

try:
    import fasttext
    print('✅ FastText available')
except ImportError:
    print('⚠️  FastText missing - language detection fallback')

try:
    import paddleocr
    print('✅ PaddleOCR available')
except ImportError:
    print('⚠️  PaddleOCR missing - OCR fallback')

print('Setup verification complete')
"

echo.
echo ==================================================
echo 🎉 SETUP COMPLETE - STARTING BACKEND SERVER
echo ==================================================
echo.
echo Backend features available:
echo   • Health check endpoints
echo   • Language detection (FastText or script-based)
echo   • Translation (NLLB or mock responses)
echo   • OCR processing (PaddleOCR or mock)
echo   • Text summarization (extractive)
echo   • File upload and processing
echo.
echo Backend URL: http://127.0.0.1:5005
echo API Documentation: See README.md
echo Test with Postman: Import postman_collection.json
echo.
echo Press Ctrl+C to stop the server
echo ==================================================
echo.

REM Start the backend
python app.py