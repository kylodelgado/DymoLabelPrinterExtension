#!/bin/bash
# DYMO Label Printer App Launcher

echo "Starting DYMO Label Printer App..."

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    python3 dymo_label_printer.py
elif command -v python &> /dev/null; then
    python dymo_label_printer.py
else
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python 3 from https://python.org"
    exit 1
fi 