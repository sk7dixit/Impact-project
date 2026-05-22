@echo off
title Backend - Port 5000
cd /d "%~dp0backend"

echo Installing backend packages...
call npm install
if errorlevel 1 goto error

echo.
echo Starting backend API...
echo Keep this window OPEN.
echo URL: http://localhost:5000
echo.
call npm start
goto end

:error
echo.
echo ERROR: npm install failed. Install Node.js from https://nodejs.org
pause
exit /b 1

:end
pause
