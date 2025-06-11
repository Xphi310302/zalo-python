# Zalo Automation Tool - Windows Installation Guide

This guide will help you install and run the Zalo Automation Tool on Windows.

## Installation Instructions

### Option 1: Using the Pre-packaged Executable (Recommended)

1. Extract the ZIP file to a location of your choice
2. Double-click on `run_zalo_app.bat` to start the application
3. A browser window will open automatically, and the Streamlit interface will load in your default web browser

### Option 2: Manual Installation (For Developers)

If you prefer to run the application from source:

1. Install Python 3.8 or newer from [python.org](https://www.python.org/downloads/)
2. Open Command Prompt as Administrator
3. Navigate to the extracted folder: `cd path\to\zalo-python`
4. Install the required packages: `pip install -r requirements.txt`
5. Run the application: `streamlit run zalo-gui.py`

## Usage Instructions

1. When the application starts, click "Initialize Browser" to open a browser window
2. Enter the phone numbers (one per line) in the text area
3. Enter your message template
4. Set the number of messages to send and wait time between messages
5. Click "Start Automation" to begin the process
6. The status of each phone number will be displayed in the Status tab

## Troubleshooting

### Browser Issues
- The application will try to use Firefox, Chrome, or Edge in that order
- Make sure you have at least one of these browsers installed
- If you encounter browser errors, try clicking "Reset Browser"

### WebDriver Issues
- The application automatically downloads the appropriate WebDriver
- If you encounter WebDriver errors, try restarting the application

### Automation Issues
- Make sure you're logged into Zalo in the browser that opens
- Allow sufficient time for the page to load before starting automation
- If messages aren't sending, try increasing the wait time between messages

## Support

If you encounter any issues, please contact support with the following information:
- Error messages from the application
- Your Windows version
- Browser version you're using
