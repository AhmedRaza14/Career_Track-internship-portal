#!/bin/bash

echo "========================================"
echo "Starting CareerTrack Backend Server"
echo "========================================"
echo ""

echo "Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run './setup.sh' first to set up the environment."
    exit 1
fi
echo ""

echo "Checking for .env file..."
if [ ! -f .env ]; then
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and configure your settings."
    exit 1
fi
echo ""

echo "Starting FastAPI server on port 8001..."
echo "Server will be available at: http://localhost:8001"
echo "API Documentation: http://localhost:8001/docs"
echo ""
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
