@echo off
cd /d "C:\Users\Administrator\Documents\watslog"
if not exist "whatsapp_logger.py" (
    echo Error: whatsapp_logger.py not found in C:\Users\Administrator\Documents\watslog
    echo Please check if the file exists and the path is correct
    pause
    exit /b 1
)
python whatsapp_logger.py
if errorlevel 1 (
    echo Error running Python script
    pause
) 