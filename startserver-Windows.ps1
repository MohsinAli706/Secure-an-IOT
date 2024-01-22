# Define the paths to your Python scripts
$webuiScript = "WebUI\manage.py runserver"
$rpiApiScript = "PiCode\rpi-api-simulation.py"

# Open a URL in the default web browser
Start-Process "http://127.0.0.1:8000"

# Start the Django WebUI + Server without displaying a terminal window
Start-Process -FilePath "python.exe" -ArgumentList "$webuiScript" -WindowStyle Hidden
Write-Host "Django WebUI Started."

# Start the Flask RPi API without displaying a terminal window
Start-Process -FilePath "python.exe" -ArgumentList "$rpiApiScript" -WindowStyle Hidden
Write-Host "Flask RPi API Started."

# Display a message and wait for user input to close both programs
Write-Host "Press Enter to stop Django WebUI & Flask RPi API..."
$null = Read-Host

# Terminate all running Python processes
Get-Process -Name "python" | ForEach-Object { Stop-Process -Id $_.Id -Force }

Write-Host "Django WebUI & Flask API Stopped."

exit