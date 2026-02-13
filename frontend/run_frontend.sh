#!/bin/bash
echo "Starting Nepali & Sinhala Literature Translator Frontend"
echo "====================================================="

# Check if backend is running
echo "Checking backend status..."
if ! curl -s http://127.0.0.1:5005/health >/dev/null 2>&1; then
    echo
    echo "❌ Backend is not running!"
    echo "Please start the backend first:"
    echo "  cd ../backend"
    echo "  ./run.sh"
    echo
    exit 1
fi

echo "✅ Backend is running"

# Install frontend dependencies
echo "Installing frontend dependencies..."
pip install streamlit requests Pillow

# Start Streamlit app
echo
echo "Starting Streamlit frontend..."
echo "Frontend will open in your browser at: http://localhost:8501"
echo
streamlit run app.py