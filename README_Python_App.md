# DYMO Label Printer - Python Desktop App

A standalone Python application that can **stay on top** and print DYMO labels with custom label types and SKUs.

## ✨ Features

- **Always Stay on Top**: Toggle button to keep the window above all other applications
- **Label Type Management**: Dropdown with saved label types + ability to add new ones
- **SKU Input**: Enter barcodes/SKUs that will be printed
- **Persistent Settings**: Your label types and preferences are saved automatically
- **Same Functionality**: Uses the exact same DYMO Connect API as the Chrome extension
- **Native Look**: Matches your Mac's system appearance

## 🚀 How to Run

### Option 1: Using the Shell Script
```bash
./run_dymo_app.sh
```

### Option 2: Direct Python Command
```bash
python3 dymo_label_printer.py
```

## 📋 Prerequisites

1. **Python 3**: Already installed on your Mac (macOS 10.15+)
2. **DYMO Connect**: Must be running (same as Chrome extension)
3. **DYMO Printer**: Connected and working

## 🎯 Usage

1. **Run the app** using one of the methods above
2. **Check "Always stay on top"** if you want the window to stay visible
3. **Select label type** from dropdown (CPU, MOBO, SCREEN) or add a new one
4. **Enter SKU** in the text field
5. **Click "Print Label"** or press Enter

## 💾 Data Storage

- Settings are saved to `~/.dymo_label_printer.json`
- Includes your custom label types and "always on top" preference
- Automatically loads when you restart the app

## 🔧 Technical Details

- **Framework**: tkinter (built into Python)
- **API**: DYMO Connect REST API (HTTPS on port 41951)
- **SSL**: Ignores certificate verification for localhost
- **Encoding**: Proper URL encoding to avoid XML issues

## 📁 Files

- `dymo_label_printer.py` - Main application
- `run_dymo_app.sh` - Launch script
- `README_Python_App.md` - This documentation

## 🆚 Python App vs Chrome Extension

| Feature | Chrome Extension | Python App |
|---------|------------------|------------|
| Stay on Top | ❌ No | ✅ Yes |
| Always Available | ❌ Popup closes | ✅ Always visible |
| System Integration | ❌ Browser only | ✅ Native app |
| Permissions | ⚠️ Browser security | ✅ Full system access |
| Installation | ✅ Easy (Chrome store ready) | ⚠️ Requires Python |

## 🔍 Troubleshooting

**"DYMO Connect is not running"**: Make sure DYMO Connect is started and shows "Started on Port 41951"

**App won't start**: Make sure Python 3 is installed:
```bash
python3 --version
```

**Window doesn't stay on top**: The checkbox might not be checked, or your window manager doesn't support it.

---

Enjoy your always-on-top DYMO label printer! 🏷️ 