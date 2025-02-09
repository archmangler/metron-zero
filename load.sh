#!/bin/bash

# Exit on error
set -e

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade pip and requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

# Only generate placeholders if assets directory is empty
if [ ! "$(ls -A assets/images 2>/dev/null)" ]; then
    echo "No assets found. Generating placeholders..."
    python tools/generate_placeholders.py
else
    echo "Using existing game assets from assets/images/"
fi

# Run the game
python main.py
