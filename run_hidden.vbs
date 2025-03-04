Set WshShell = CreateObject("WScript.Shell")
strWorkingDirectory = "C:\Users\Administrator\Documents\watslog"
WshShell.CurrentDirectory = strWorkingDirectory
WshShell.Run chr(34) & strWorkingDirectory & "\start_whatsapp_logger.bat" & chr(34), 0
Set WshShell = Nothing 