#!/bin/bash

# Simple network check - wait a few seconds
echo "Waiting for network initialization..."
sleep 5

echo "Network should be ready"

# Install Chrome Driver (fallback)
if ! command -v chromedriver &> /dev/null; then
    echo "ChromeDriver not found, installing..."
    apt-get update && apt-get install -y chromium-driver
fi

# Check if yt-dlp is available
if ! command -v yt-dlp &> /dev/null; then
    echo "yt-dlp not found in PATH, installing via pip..."
    pip install yt-dlp
fi

# Create necessary directories
mkdir -p /app/logs
mkdir -p /app/downloads

# Start the application
echo "Starting Thunder Downloader..."
exec python -m thunder_downloader.main
