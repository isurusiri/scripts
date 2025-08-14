#!/bin/bash
# Spotify Playlist Creator Setup Script
# This script helps you set up the Spotify playlist creator tool

set -e

echo "Spotify Playlist Creator Setup"
echo "=================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "pip3 found: $(pip3 --version)"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "Dependencies installed successfully!"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from template..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo ".env file created from env.example"
        echo "Please edit .env file with your Spotify API credentials"
    else
        echo "env.example not found. Please create .env file manually with:"
        echo "   SPOTIFY_CLIENT_ID=your_client_id"
        echo "   SPOTIFY_CLIENT_SECRET=your_client_secret"
    fi
else
    echo ".env file already exists"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Spotify API credentials"
echo "2. Run: python3 create_playlist.py --help"
echo "3. Create your first playlist: python3 create_playlist.py"
echo ""
echo "For more information, see README.md"
