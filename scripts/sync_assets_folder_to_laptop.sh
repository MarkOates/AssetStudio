#!/bin/bash

# Specify the correct computer name
CORRECT_COMPUTER_NAME="Mark’s MacBook Pro"  # Replace with your desired computer name

# Get the current computer name
CURRENT_COMPUTER_NAME=$(scutil --get ComputerName)

# Check if the current computer name matches the correct name
if [ "$CURRENT_COMPUTER_NAME" == "$CORRECT_COMPUTER_NAME" ]; then
    echo "Computer name matches. Starting rsync..."
    rsync -av --progress --ignore-existing --verbose --exclude='*.zip' /Volumes/markoates/Assets/ /Users/markoates/Assets/
else
    echo "Error: This script can only be run on $CORRECT_COMPUTER_NAME. Current computer name is $CURRENT_COMPUTER_NAME."
fi

