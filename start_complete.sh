#!/bin/bash
echo "🚀 COMPLETE NEPALI & SINHALA TRANSLATOR SETUP"
echo "============================================"
echo "Starting both Backend and Frontend"
echo

# Function to start backend in background
start_backend() {
    echo "[1/2] Starting Backend Server..."
    cd backend
    ./run.sh &
    BACKEND_PID=$!
    cd ..
    echo "Backend started with PID: $BACKEND_PID"
}

# Function to start frontend
start_frontend() {
    echo "[2/2] Starting Frontend UI..."
    echo "Waiting for backend to initialize..."
    sleep 15
    
    cd frontend
    ./run_frontend.sh
}

# Cleanup function
cleanup() {
    echo
    echo "Shutting down services..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "Backend stopped"
    fi
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Start services
start_backend
start_frontend

# Keep script running
wait