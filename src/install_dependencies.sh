#!/bin/bash

# Install Python pachages from requirements.txt file
pip install -r src/requirements.txt

# Check for errors
if [[ $? -ne 0]]; then
  echo "Failed to install Python packages. Exiting..."
  exit 1
fi

echo "Python packages installed successfully!"