#!/bin/bash
# Start script for Linux/macOS

echo "Starting Nepali & Sinhala Literature Translator Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.13 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p logs temp models

# Start the Flask application
echo "Starting Flask server..."
export FLASK_APP=app.py
export FLASK_ENV=production
python app.py