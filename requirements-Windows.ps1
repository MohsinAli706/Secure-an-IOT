# Check if 'requirements.txt' file exists
if (Test-Path -Path ".\requirements.txt") {
    # Activate your Python virtual environment (if you have one)
    # .\venv\Scripts\Activate
    
    # Install Python dependencies from requirements.txt
    pip install -r .\requirements.txt

    # Deactivate your Python virtual environment (if you activated one)
    # deactivate
}
else {
    Write-Host "Error: 'requirements.txt' file not found."
}
