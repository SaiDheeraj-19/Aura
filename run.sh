#!/bin/bash

# AURA Setup & Run Script
# This script automates the setup and launch process

echo "🎙️ AURA Setup & Launch"
echo "=========================================="
echo ""

# Check Python version
echo "📌 Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check FFmpeg
echo ""
echo "📌 Checking FFmpeg installation..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg found: $(ffmpeg -version | head -n 1)"
else
    echo "⚠️  FFmpeg not found!"
    echo "Please install FFmpeg:"
    echo "  macOS: brew install ffmpeg"
    echo "  Ubuntu: sudo apt-get install ffmpeg"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "📦 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys before running the app!"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to exit..."
fi

# Launch Streamlit app
echo ""
echo "🚀 Launching AURA..."
echo "=========================================="
echo ""
streamlit run app.py
