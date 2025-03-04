# WhatsApp Message Logger

A Python script that automatically logs WhatsApp Web messages, including deleted ones. The script runs in the background and captures both incoming and outgoing messages.

## Features

- Logs all WhatsApp messages before they can be deleted
- Runs in the background (headless mode)
- Captures both incoming and outgoing messages
- Automatically starts with Windows
- Stores messages with timestamps in JSON format
- Prevents duplicate message logging
- Works with WhatsApp Web

## Prerequisites

1. Windows OS
2. Python 3.7 or higher
3. Google Chrome browser
4. WhatsApp account
5. Internet connection

## Installation

1. Clone this repository:
```bash
git clone https://github.com/rbrusnicki/whatsapp-logger.git
cd whatsapp-logger
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Set the contact name to monitor:
   - Open `whatsapp_logger.py` in a text editor
   - Find this section:
     ```python
     # You can either use input to enter the contact name each time:
     # contact_name = input("Enter the contact name to monitor: ")
     
     # Or hardcode the contact name here (must match exactly as shown in WhatsApp):
     contact_name = "Example Contact"  # Replace with the exact name of the contact you want to monitor
     ```
   - Replace "Example Contact" with the exact name of the contact you want to monitor
   - The name must match exactly as it appears in WhatsApp (including emojis if any)
   - Save the file

4. Set up WhatsApp Web (First Time Only):
   - Comment out this line in `whatsapp_logger.py`:
     ```python
     chrome_options.add_argument("--headless=new")
     ```
   - Run the script:
     ```bash
     python whatsapp_logger.py
     ```
   - Scan the QR code with your WhatsApp mobile app
   - After successful login, close the script (Ctrl+C)
   - Uncomment the headless mode line you commented earlier

5. Set up auto-start with Windows:
   - Press `Windows + R`
   - Type `shell:startup` and press Enter
   - Create a shortcut to `run_hidden.vbs` in this folder
   - Or run this PowerShell command:
     ```powershell
     $WshShell = New-Object -comObject WScript.Shell
     $Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\WhatsAppLogger.lnk")
     $Shortcut.TargetPath = "C:\path\to\your\run_hidden.vbs"
     $Shortcut.WorkingDirectory = "C:\path\to\your\folder"
     $Shortcut.Save()
     ```

## File Structure

- `whatsapp_logger.py`: Main Python script that monitors WhatsApp Web
- `requirements.txt`: Python package dependencies
- `start_whatsapp_logger.bat`: Batch file to run the Python script
- `run_hidden.vbs`: VBS script to run the batch file in background
- `logs/`: Directory where message logs are stored (created automatically)

## Configuration

Before running the script, update these files with your correct paths:

1. In `run_hidden.vbs`:
```vbs
strWorkingDirectory = "C:\path\to\your\folder"
```

2. In `start_whatsapp_logger.bat`:
```batch
cd /d "C:\path\to\your\folder"
```

## Usage

The script will:
1. Run automatically when Windows starts
2. Monitor WhatsApp Web in the background
3. Save all messages to JSON files in the `logs` directory
4. Create separate log files for each contact

To view logged messages:
- Check the `logs` directory
- Files are named as `[contact_name]_messages.json`
- Each message entry contains:
  ```json
  {
    "timestamp": "YYYY-MM-DD HH:MM:SS",
    "contact": "Contact Name",
    "message": "Message content",
    "type": "received/sent"
  }
  ```

## Stopping the Logger

To stop the logger:
1. Open Task Manager
2. Find and end these processes:
   - `python.exe`
   - Background `chrome.exe` processes

To prevent auto-start:
1. Press `Windows + R`
2. Type `shell:startup`
3. Delete the "WhatsAppLogger" shortcut

## Troubleshooting

1. If the script doesn't start:
   - Check if Python is in your system PATH
   - Verify Chrome is installed
   - Check file paths in VBS and BAT files

2. If messages aren't being logged:
   - Delete the `chrome_profile` directory
   - Run the script without headless mode
   - Re-scan the WhatsApp Web QR code

3. If you get path errors:
   - Update the paths in both `run_hidden.vbs` and `start_whatsapp_logger.bat`
   - Make sure all files are in the correct directory

4. If contact's messages aren't being logged:
   - Verify the contact name matches exactly as shown in WhatsApp
   - Check for any special characters or emojis in the contact name
   - Try using the input method first to test the exact name

## Security Note

This tool is for personal use only. Please:
- Don't use it for unauthorized monitoring
- Respect privacy and consent
- Keep your logged messages secure
- Don't share your `chrome_profile` directory

## License

MIT License - See LICENSE file for details 