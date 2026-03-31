@echo off
REM Run this once as Administrator to add Tor to Windows Task Scheduler
TITLE Setting up Tor Auto-Start

schtasks /create /tn "TorHiddenService" /tr "\"C:\Users\Rudraksh\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe\" -f \"C:\Users\Rudraksh\Desktop\Tor_scrap\OnionSearch\torrc\"" /sc onlogon /rl limited /f

echo.
echo Tor has been added to Task Scheduler as "TorHiddenService"
echo It will start automatically when you log in to Windows.
echo.
pause
