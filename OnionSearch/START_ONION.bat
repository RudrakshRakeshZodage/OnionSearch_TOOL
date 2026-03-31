@echo off
TITLE Tor Onion Site Launcher
echo ============================================
echo   Starting Permanent Tor Hidden Service
echo ============================================
echo.

REM --- Find Tor Expert Bundle (update path if needed) ---
set TOR_EXE=C:\Users\Rudraksh\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe
set TORRC=C:\Users\Rudraksh\Desktop\Tor_scrap\OnionSearch\torrc

REM --- Start Tor in background ---
echo [1/3] Starting Tor daemon...
start "Tor Daemon" /min "%TOR_EXE%" -f "%TORRC%"
timeout /t 5 /nobreak >nul

REM --- Start Node servers via PM2 ---
echo [2/3] Starting Node.js servers with PM2...
cd /d C:\Users\Rudraksh\Desktop\Tor_scrap\OnionSearch
pm2 start pm2.config.js

echo.
echo [3/3] Saving PM2 process list...
pm2 save

echo.
echo ============================================
echo   DONE! Your .onion site is now LIVE:
echo   http://4mlr2pcgoopag7wip2mkhgj3fozwwvtyegqcmyfcahtvnj6u25pewdid.onion
echo ============================================
echo.
echo Run "pm2 status" to check server health
echo Run "pm2 logs" to view live logs
pause
