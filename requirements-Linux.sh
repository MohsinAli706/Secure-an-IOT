#!/bin/bash

# Check if 'requirements.txt' file exists
if [ -f "requirements.txt" ]; then
    # Activate your Python virtual environment (if you have one)
    # source venv/bin/activate
    
    # Install Python dependencies from requirements.txt
    pip install -r requirements.txt

    # Deactivate your Python virtual environment (if you activated one)
    # deactivate
else
    echo "Error: 'requirements.txt' file not found."
fi
