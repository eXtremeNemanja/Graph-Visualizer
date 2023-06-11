#!/bin/bash

if [ -d "venv" ]; then
    echo "Removing existing venv..."
    rm -rf venv
fi

echo "Creating new venv..."
python3 -m venv venv

echo "Activating venv..."
source venv/bin/activate

echo "venv activated."
