from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome import service
import json
from datetime import datetime
import os
import time
import sys
import subprocess
import glob
import tempfile

class WhatsAppLogger:
    def __init__(self, target_contact):
        self.target_contact = target_contact
        self.logged_messages = []
        self.setup_driver()
        
    def get_chrome_version(self):
        try:
            # Try to get Chrome version using Windows registry
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            version, _ = winreg.QueryValueEx(key, "version")
            return version
        except:
            try:
                # Alternative method using PowerShell
                cmd = 'powershell -command "&{(Get-Item \'C:\Program Files\Google\Chrome\Application\chrome.exe\').VersionInfo.FileVersion}"'
                version = subprocess.check_output(cmd, shell=True).decode().strip()
                return version
            except:
                print("Could not determine Chrome version. Please make sure Chrome is installed.")
                return None

    def find_chromedriver(self, base_path):
        # Look for chromedriver.exe in the directory
        driver_pattern = os.path.join(base_path, '**', 'chromedriver.exe')
        drivers = glob.glob(driver_pattern, recursive=True)
        if drivers:
            return drivers[0]
        return None

    def setup_driver(self):
        try:
            chrome_version = self.get_chrome_version()
            if not chrome_version:
                sys.exit(1)
                
            print(f"Detected Chrome version: {chrome_version}")
            
            # Create a temporary directory for Chrome
            temp_dir = tempfile.mkdtemp()
            user_data_dir = os.path.join(os.getcwd(), 'chrome_profile')
            
            chrome_options = Options()
            # Headless mode configuration
            chrome_options.add_argument("--headless=new")     ### comment this line if you want to see the browser
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
            chrome_options.add_argument(f"--remote-debugging-port=9222")
            chrome_options.add_argument(f"--temp-directory={temp_dir}")
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
            chrome_options.add_argument("--disable-site-isolation-trials")
            # Additional headless mode settings
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            # Add user agent to avoid detection
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")
            
            # Get ChromeDriver
            driver_manager = ChromeDriverManager()
            base_path = driver_manager.install()
            driver_path = self.find_chromedriver(os.path.dirname(base_path))
            
            if not driver_path:
                print("Could not find chromedriver.exe. Downloading specific version...")
                driver_path = ChromeDriverManager(version=chrome_version).install()
            
            print(f"Using ChromeDriver path: {driver_path}")
            
            # Create service with increased start timeout
            chrome_service = service.Service(
                executable_path=driver_path,
                start_error_message="Chrome failed to start. Please check if Chrome is properly installed.",
                service_args=['--verbose']
            )
            
            print("Initializing Chrome WebDriver in headless mode...")
            self.driver = webdriver.Chrome(
                service=chrome_service,
                options=chrome_options
            )
            print("Chrome WebDriver initialized successfully!")
            
        except Exception as e:
            print(f"\nError setting up Chrome WebDriver: {str(e)}")
            print("\nDetailed troubleshooting steps:")
            print("1. Verify Chrome installation:")
            print("   - Open Chrome manually to confirm it works")
            print("   - If Chrome isn't installed, download it from: https://www.google.com/chrome/")
            print("2. Try these steps:")
            print("   - Close all Chrome windows")
            print("   - Delete the chrome_profile directory if it exists")
            print("   - Delete the contents of %TEMP% directory")
            print("   - Run: pip uninstall selenium webdriver-manager")
            print("   - Run: pip install selenium==4.18.1 webdriver-manager==4.0.1")
            print("3. If error persists, try running:")
            print("   python -m pip install --upgrade pip")
            sys.exit(1)
        
    def start_logging(self):
        # Open WhatsApp Web
        print("Opening WhatsApp Web in background...")
        self.driver.get("https://web.whatsapp.com")
        print("\nIMPORTANT: You need to scan the QR code once to set up WhatsApp Web.")
        print("To do this, run the script once without headless mode:")
        print("1. Close this script (Ctrl+C)")
        print("2. Delete the chrome_profile directory")
        print("3. Comment out the '--headless=new' line in the code")
        print("4. Run the script again, scan the QR code")
        print("5. After successful login, restore the '--headless=new' line")
        print("\nWaiting for WhatsApp Web to load (60 seconds timeout)...")
        
        try:
            # Wait for the contact search box to be present (indicating successful login)
            search_box = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            
            # Search for the target contact
            search_box.clear()
            search_box.send_keys(self.target_contact)
            time.sleep(2)
            
            # Click on the contact
            contact = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//span[@title="{self.target_contact}"]'))
            )
            contact.click()
            #print(f"Started monitoring messages from {self.target_contact} in background")
            print(f"Started monitoring in background")
            #print("Messages will be saved to logs/{self.target_contact}_messages.json")
            print("You can minimize this window. Press Ctrl+C to stop monitoring.")
            self.monitor_messages()
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            self.driver.quit()
            
    def get_message_history(self):
        try:
            filename = f"logs/{self.target_contact}_messages.json"
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"\nError reading message history: {str(e)}")
            return []

    def is_message_logged(self, message_text, message_type, messages_history):
        # Check if message is already in history
        for msg in messages_history:
            if msg["message"] == message_text and msg["type"] == message_type:
                return True
        return False

    def monitor_messages(self):
        last_incoming_count = 0
        last_outgoing_count = 0
        messages_logged = 0
        
        print("\nMonitoring messages... (Press Ctrl+C to stop)")
        
        while True:
            try:
                # Get message history
                messages_history = self.get_message_history()
                
                # Get all incoming messages in the chat
                incoming_messages = self.driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')
                # Get all outgoing messages in the chat
                outgoing_messages = self.driver.find_elements(By.XPATH, '//div[contains(@class, "message-out")]')
                
                # Check for new incoming messages
                if len(incoming_messages) > last_incoming_count:
                    # Get the last few messages to check for missed ones
                    start_index = max(0, len(incoming_messages) - 5)  # Check last 5 messages
                    messages_to_check = incoming_messages[start_index:]
                    
                    for message in messages_to_check:
                        try:
                            message_text = message.find_element(By.CSS_SELECTOR, 'span.selectable-text').text
                            
                            # Only process if message isn't already logged
                            if not self.is_message_logged(message_text, "received", messages_history):
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                
                                message_data = {
                                    "timestamp": timestamp,
                                    "contact": self.target_contact,
                                    "message": message_text,
                                    "type": "received"
                                }
                                
                                self.logged_messages.append(message_data)
                                self.save_to_file(message_data)
                                messages_logged += 1
                                print(f"\rTotal messages logged: {messages_logged}", end="")
                            
                        except Exception as e:
                            print(f"\nError processing incoming message: {str(e)}")
                            continue
                    
                    last_incoming_count = len(incoming_messages)
                
                # Check for new outgoing messages
                if len(outgoing_messages) > last_outgoing_count:
                    # Get the last few messages to check for missed ones
                    start_index = max(0, len(outgoing_messages) - 5)  # Check last 5 messages
                    messages_to_check = outgoing_messages[start_index:]
                    
                    for message in messages_to_check:
                        try:
                            message_text = message.find_element(By.CSS_SELECTOR, 'span.selectable-text').text
                            
                            # Only process if message isn't already logged
                            if not self.is_message_logged(message_text, "sent", messages_history):
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                
                                message_data = {
                                    "timestamp": timestamp,
                                    "contact": "You",
                                    "message": message_text,
                                    "type": "sent"
                                }
                                
                                self.logged_messages.append(message_data)
                                self.save_to_file(message_data)
                                messages_logged += 1
                                print(f"\rTotal messages logged: {messages_logged}", end="")
                            
                        except Exception as e:
                            print(f"\nError processing outgoing message: {str(e)}")
                            continue
                    
                    last_outgoing_count = len(outgoing_messages)
                
                time.sleep(1)  # Check for new messages every second
                
            except Exception as e:
                print(f"\nError monitoring messages: {str(e)}")
                time.sleep(5)  # Wait before retrying
                
    def save_to_file(self, message_data):
        filename = f"logs/{self.target_contact}_messages.json"
        os.makedirs("logs", exist_ok=True)
        
        try:
            # Read existing messages
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    messages = json.load(f)
            else:
                messages = []
            
            # Append new message
            messages.append(message_data)
            
            # Save updated messages
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(messages, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving to file: {str(e)}")

if __name__ == "__main__":
    print("WhatsApp Message Logger (Background Mode)")
    print("---------------------------------------")
    print("Make sure Google Chrome is installed and up to date.")
    #contact_name = input("Enter the contact name to monitor: ")
    contact_name = "GaAng"
    logger = WhatsAppLogger(contact_name)
    logger.start_logging() 

# The setup is now complete! Here's what we've done:
# Created start_whatsapp_logger.bat - A batch file that runs the Python script
# Created run_hidden.vbs - A VBS script that runs the batch file without showing a window
# Created a shortcut in your Windows Startup folder
# The script will now automatically:
# Start when Windows boots
# Run in the background without showing any windows
# Log all WhatsApp messages as before
# To test it:
# Restart your computer
# The script should start automatically
# Check the logs folder to verify it's working
# If you want to stop the script from running at startup:
# Press Windows + R
# Type shell:startup
# Delete the "WhatsAppLogger" shortcut
# Additional tips:
# You can check if the script is running by looking in Task Manager for "python.exe" or "chrome.exe" processes
# The logs will continue to be saved in the logs folder
# If you need to stop the script, you can use Task Manager to end the Python process