#!/bin/bash
# Build script for creating standalone executable

echo "Building Nepali & Sinhala Literature Translator Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Run start.sh first."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install PyInstaller if not already installed
echo "Installing PyInstaller..."
pip install pyinstaller

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist *.spec

# Create necessary directories for bundling
echo "Creating directories..."
mkdir -p models logs temp

# Build the executable
echo "Building executable..."
pyinstaller app.py --onefile --name nepali-sinhala-backend \
  --add-data "models:models" \
  --add-data "logs:logs" \
  --add-data "temp:temp" \
  --hidden-import=paddleocr \
  --hidden-import=transformers \
  --hidden-import=torch \
  --hidden-import=cv2 \
  --hidden-import=numpy \
  --hidden-import=PIL \
  --hidden-import=flask \
  --hidden-import=flask_cors \
  --console \
  --noconfirm

if [ $? -eq 0 ]; then
    echo ""
    echo "Build completed successfully!"
    echo "Executable location: dist/nepali-sinhala-backend"
    echo ""
    echo "To test the executable:"
    echo "  cd dist"
    echo "  ./nepali-sinhala-backend"
    echo ""
else
    echo ""
    echo "Build failed! Check the error messages above."
    echo ""
fi