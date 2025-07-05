# DYMO Label Printer Chrome Extension

This Chrome extension allows you to print DYMO labels with custom label types and SKUs using your existing DYMO label template.

## Features

- **Dropdown for Label Types**: Select from previously used label types (CPU, MOBO, Screen) or add new ones
- **SKU Input**: Enter the SKU/barcode text that will be printed
- **Persistent Storage**: Your custom label types are saved and remembered
- **Direct DYMO Printing**: Communicates directly with DYMO Connect software

## Setup Instructions

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

## Usage

1. **Open the Extension**: Click on the extension icon in Chrome's toolbar

2. **Select Label Type**: 
   - Choose from existing types (CPU, MOBO, Screen)
   - Or select "+ Add New Label Type" to create a custom one

3. **Enter SKU**: Type the SKU/barcode text in the second field

4. **Print**: Click "Print Label" to send the label to your DYMO printer

## Technical Details

- The extension uses your existing `Address Asset-SSD-PCI E Card.label` template
- It replaces `{{LABEL_TYPE}}` with your selected label type
- It replaces `{{SKU}}` with your entered SKU
- Label types are stored in Chrome's local storage and persist between sessions

## Troubleshooting

- **"DYMO Connect not running"**: Make sure DYMO Connect software is installed and running
- **"No DYMO printers found"**: Check that your DYMO label writer is connected and recognized by DYMO Connect
- **Print fails**: Ensure your printer has labels loaded and is ready to print

## Files

- `manifest.json`: Extension configuration
- `popup.html`: User interface
- `popup.js`: Main functionality
- `Address Asset-SSD-PCI E Card.label`: Original DYMO label template
- `README.md`: This documentation file 