@echo off
set webuiScript=WebUI\manage.py runserver
set rpiApiScript=PiCode\rpi-api-simulation.py

:: Open a URL in the default web browser
start http://127.0.0.1:8000

:: Start the Django WebUI + Server without displaying a terminal window
start "" python.exe "%webuiScript%" /B
echo Django WebUI Started.

:: Start the Flask RPi API without displaying a terminal window
start "" python.exe "%rpiApiScript%" /B
echo Flask RPi API Started.

:: Display a message and wait for user input to close both programs
echo Press Enter to stop Django WebUI & Flask RPi API...
set /p dummyVar=
taskkill /f /im python.exe > nul 2>&1

echo Django WebUI & Flask API Stopped.
exit /b 0