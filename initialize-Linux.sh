#!/bin/bash

# Set the relative file path
file_path="WebUI/authsysproject/settings.py"

# Prompt the user for input
read -p "Enter your Gmail Address (Gmail ONLY): " new_mail
read -p "Enter your Generated App Password: " new_pass

# Use sed to replace the content of the .py file
sed -i "s/example@gmail.com/$new_mail/g" "$file_path"
sed -i "s/examplepass/$new_pass/g" "$file_path"

echo "Email updated successfully!"
