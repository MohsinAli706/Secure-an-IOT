#!/bin/bash

# Define the paths to your Python scripts
webuiScript="WebUI/manage.py runserver"
rpiApiScript="PiCode/rpi-api.py"

# Open a URL in the default web browser
xdg-open "http://127.0.0.1:8000"

# Start the Django WebUI + Server without displaying a terminal window
python3 "$webuiScript" > /dev/null 2>&1 &
echo "Django WebUI Started."

# Start the Flask RPi API without displaying a terminal window
python3 "$rpiApiScript" > /dev/null 2>&1 &
echo "Flask RPi API Started."

# Display a message and wait for user input to close both programs
read -p "Press Enter to stop Django WebUI & Flask RPi API..."

# Terminate all running Python processes
pkill -f "python3 $webuiScript"
pkill -f "python3 $rpiApiScript"

echo "Django WebUI & Flask API Stopped."

exit 0
