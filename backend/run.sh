#!/bin/bash
# Comprehensive setup and run script for Nepali & Sinhala Literature Translator Backend
# This script handles everything: environment, dependencies, models, and startup

set -e  # Exit on any error

echo "🚀 NEPALI & SINHALA LITERATURE TRANSLATOR BACKEND"
echo "=================================================="
echo "Comprehensive setup and run script"
echo "This will set up everything from scratch and start the backend"
echo

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python() {
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        echo "❌ Python not found. Please install Python 3.10+ first."
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo "✅ Found Python $PYTHON_VERSION"
    
    # Check if version is 3.10+
    if [[ $(echo "$PYTHON_VERSION 3.10" | tr ' ' '\n' | sort -V | head -n1) != "3.10" ]]; then
        echo "⚠️  Python 3.10+ recommended, but continuing with $PYTHON_VERSION"
    fi
}

# Step 1: Check system requirements
echo "[1/8] Checking system requirements..."
check_python

if ! command_exists curl; then
    echo "❌ curl not found. Please install curl first."
    exit 1
fi
echo "✅ curl found"

if ! command_exists pip; then
    echo "❌ pip not found. Please install pip first."
    exit 1
fi
echo "✅ pip found"

# Step 2: Create and activate virtual environment
echo
echo "[2/8] Setting up virtual environment..."
if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "  ✅ Virtual environment created"
else
    echo "  ✅ Virtual environment already exists"
fi

echo "  Activating virtual environment..."
source venv/bin/activate
echo "  ✅ Virtual environment activated"

# Step 3: Upgrade pip and install basic tools
echo
echo "[3/8] Installing basic dependencies..."
pip install --upgrade pip setuptools wheel
pip install Flask==3.0.0 Flask-CORS==4.0.0 Werkzeug==3.0.1
pip install numpy==1.24.3 Pillow==10.1.0
echo "✅ Basic dependencies installed"

# Step 4: Install ML dependencies
echo
echo "[4/8] Installing ML dependencies..."
echo "  This may take several minutes..."

# Install PyTorch (CPU version for compatibility)
pip install torch==2.1.1 torchvision==0.16.1 --index-url https://download.pytorch.org/whl/cpu

# Install transformers and related
pip install transformers==4.35.2 tokenizers==0.15.0 sentencepiece==0.1.99

# Install FastText
pip install fasttext==0.9.2

# Install PaddleOCR and dependencies
pip install paddlepaddle==2.5.2 paddleocr==2.7.3 opencv-python==4.8.1.78

# Install additional dependencies
pip install requests==2.31.0 tqdm==4.66.1 packaging==23.2
echo "✅ ML dependencies installed"

# Step 5: Create directory structure
echo
echo "[5/8] Creating directory structure..."
mkdir -p logs temp
mkdir -p models/models/{paddleocr,nllb_model,fasttext,phi3}
echo "✅ Directories created"

# Step 6: Check existing models
echo
echo "[6/8] Checking existing models..."

# Check FastText model
if [ -f "models/models/fasttext/lid.176.bin" ]; then
    echo "  ✅ FastText model found"
elif [ -f "models/models/lid.176.ftz" ]; then
    echo "  ✅ FastText compressed model found"
    # Move to correct location
    mv models/models/lid.176.ftz models/models/fasttext/
    echo "  📁 Moved FastText model to correct location"
else
    echo "  📥 Downloading FastText language detection model..."
    curl -L -o models/models/fasttext/lid.176.bin \
        https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
    echo "  ✅ FastText model downloaded"
fi

# Check NLLB model
if [ -f "models/models/nllb_model/pytorch_model.bin" ]; then
    echo "  ✅ NLLB model weights found"
else
    echo "  ⚠️  NLLB model weights not found - translation will use fallback"
fi

# Step 7: Download missing NLLB tokenizer files
echo
echo "[7/8] Setting up NLLB translation model..."
cd models/models/nllb_model

NLLB_BASE_URL="https://huggingface.co/facebook/nllb-200-distilled-600M/resolve/main"

# Download missing files
files=("config.json" "tokenizer.json" "tokenizer_config.json" "sentencepiece.bpe.model" "special_tokens_map.json")

for file in "${files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "  📥 Downloading $file..."
        curl -L -o "$file" "$NLLB_BASE_URL/$file"
        echo "  ✅ $file downloaded"
    else
        echo "  ✅ $file already exists"
    fi
done

cd ../../..

# Check if we have complete NLLB model
if [ -f "models/models/nllb_model/pytorch_model.bin" ] && [ -f "models/models/nllb_model/config.json" ]; then
    echo "  ✅ NLLB model complete - real translation available"
else
    echo "  ⚠️  NLLB model incomplete - will use mock translation"
fi

# Step 8: Final verification and startup
echo
echo "[8/8] Final verification and startup..."

# Run setup check
echo "  Running setup verification..."
$PYTHON_CMD -c "
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

echo
echo "=================================================="
echo "🎉 SETUP COMPLETE - STARTING BACKEND SERVER"
echo "=================================================="
echo
echo "Backend features available:"
echo "  • Health check endpoints"
echo "  • Language detection (FastText or script-based)"
echo "  • Translation (NLLB or mock responses)"
echo "  • OCR processing (PaddleOCR or mock)"
echo "  • Text summarization (extractive)"
echo "  • File upload and processing"
echo
echo "Backend URL: http://127.0.0.1:5005"
echo "API Documentation: See README.md"
echo "Test with Postman: Import postman_collection.json"
echo
echo "Press Ctrl+C to stop the server"
echo "=================================================="
echo

# Start the backend
exec $PYTHON_CMD app.py