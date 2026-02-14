# OneDrive Linux File Sanitizer

A Python GUI application to fix file and folder names that are incompatible with OneDrive on Linux.

## Features

- Scans mounted OneDrive directories for problematic files
- Fixes invalid characters (`< > : " / \ | ? *`)
- Removes trailing spaces and periods
- Handles Windows reserved names (CON, PRN, AUX, etc.)
- Preview changes before applying
- Batch rename with one click

## Requirements

- Python 3.6+
- tkinter

## Installation

```bash
# Install tkinter (Linux only)
# Debian/Ubuntu:
sudo apt-get install python3-tk

# Fedora/RHEL:
sudo dnf install python3-tkinter

# Arch:
sudo pacman -S tk

# Make executable
chmod +x main.py
```

## Usage

```bash
# Run the application
python3 main.py
# or
./main.py
```

1. Click "Browse" to select your mounted OneDrive directory
2. Click "Scan" to find problematic files
3. Review the issues in the table
4. Click "Fix All" to rename all files

## What Gets Fixed

- **Invalid characters**: Replaced with underscore `_`
- **Trailing spaces/periods**: Removed
- **Reserved names**: Prefixed with underscore `_`
- **Empty names**: Replaced with "unnamed"

## Safety

- Preview all changes before applying
- Confirmation dialog before fixing
- Processes deepest files first to avoid conflicts
