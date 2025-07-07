# DYMO Label Printer Chrome Extension & Desktop App

This project provides both a Chrome extension and a Python desktop application for printing DYMO labels with custom label types and SKUs using your existing DYMO label template.

## Features

- **Dropdown for Label Types**: Select from previously used label types (CPU, MOBO, SCREEN) or add new ones
- **SKU Input**: Enter the SKU/barcode text that will be printed
- **Quantity Selection**: Print 1-99 labels at once (Python app only)
- **Always on Top**: Keep the app window visible above other applications (Python app only)
- **Persistent Storage**: Your custom label types are saved and remembered
- **Direct DYMO Printing**: Communicates directly with DYMO Connect software

## Chrome Extension Setup

### Prerequisites

1. **DYMO Connect Software**: Make sure you have DYMO Connect installed and running
   - Download from [DYMO's website](https://www.dymo.com/connect)
   - The extension communicates with DYMO Connect via HTTP on port 41951

2. **DYMO Label Writer**: Have your DYMO label writer connected and set up

### Installation

1. **Add Icons**: Create the following icon files in the extension directory:
   - `icon16.png` (16x16 pixels)
   - `icon48.png` (48x48 pixels)
   - `icon128.png` (128x128 pixels)

2. **Load the Extension**:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select the folder containing these extension files

### Usage

1. **Open the Extension**: Click on the extension icon in Chrome's toolbar
2. **Select Label Type**: Choose from existing types or add a new one
3. **Enter SKU**: Type the SKU/barcode text in the second field
4. **Print**: Click "Print Label" to send the label to your DYMO printer

## Python Desktop App

The Python desktop app (`dymo_label_printer.py`) provides additional features not available in Chrome extensions, such as "always on top" functionality and quantity printing.

### Running the Python App

1. **Prerequisites**: Ensure Python 3.6+ is installed with tkinter support
2. **DYMO Connect**: Make sure DYMO Connect software is running
3. **Run the Script**: Execute `python3 dymo_label_printer.py`

### Compiling to Standalone Mac Application

For a more convenient experience, you can compile the Python app into a standalone Mac application that doesn't require Python to be installed.

#### Setup PyInstaller

```bash
# Install pipx (if not already installed)
brew install pipx

# Install PyInstaller
pipx install pyinstaller

# Add pipx to PATH
pipx ensurepath

# Reload shell configuration
source ~/.zshrc
```

#### Create Mac App

```bash
# Navigate to your project directory
cd /path/to/your/Extension\ Dymo

# Build the Mac application
pyinstaller --windowed --onedir --name "DYMO Label Printer" --add-data "*.label:." dymo_label_printer.py
```

#### Install the App

```bash
# Copy to Applications folder
cp -R "dist/DYMO Label Printer.app" /Applications/
```

#### Launch the App

- **From Finder**: Applications → "DYMO Label Printer"
- **From Terminal**: `open "/Applications/DYMO Label Printer.app"`
- **Security Note**: On first launch, macOS may show a security warning. Go to System Settings → Privacy & Security → Allow the app to run.

### Mac App Features

✅ **Standalone**: No Python installation required  
✅ **Always on Top**: Optional window behavior  
✅ **Quantity Printing**: Print 1-99 labels at once  
✅ **Persistent Settings**: Remembers preferences  
✅ **Native Mac App**: Integrates with macOS  

## Technical Details

- Both versions use your existing `Address Asset-SSD-PCI E Card.label` template
- Template variables are replaced: `{{LABEL_TYPE}}` and `{{SKU}}`
- Settings are stored locally (Chrome storage for extension, JSON file for Python app)
- Communication with DYMO Connect via HTTP API on port 41951

## Troubleshooting

- **"DYMO Connect not running"**: Make sure DYMO Connect software is installed and running
- **"No DYMO printers found"**: Check that your DYMO label writer is connected and recognized by DYMO Connect
- **Print fails**: Ensure your printer has labels loaded and is ready to print
- **Mac app won't open**: Check System Settings → Privacy & Security and allow the app to run

## Files

### Chrome Extension
- `manifest.json`: Extension configuration
- `popup.html`: User interface
- `popup.js`: Main functionality
- `icons/`: Extension icons

### Python Desktop App
- `dymo_label_printer.py`: Desktop application
- `run_dymo_app.sh`: Launch script
- `README_Python_App.md`: Detailed Python app documentation

### Shared
- `Address Asset-SSD-PCI E Card.label`: Original DYMO label template
- `README.md`: This documentation file 