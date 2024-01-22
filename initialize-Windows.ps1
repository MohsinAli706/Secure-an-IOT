# Set the relative file path
$file_path = "WebUI\authsysproject\settings.py"

# Prompt the user for input
$new_mail = Read-Host "Enter your Gmail Address (Gmail ONLY)"
$new_pass = Read-Host "Enter your Generated App Password"

# Use PowerShell to replace the content of the .py file
(Get-Content -Path $file_path) -replace 'example@gmail.com', $new_mail | Set-Content -Path $file_path
(Get-Content -Path $file_path) -replace 'examplepass', $new_pass | Set-Content -Path $file_path

Write-Host "Email updated successfully!"

