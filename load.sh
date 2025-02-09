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
python tools/generate_placeholders.py

# Run the game
python main.py
