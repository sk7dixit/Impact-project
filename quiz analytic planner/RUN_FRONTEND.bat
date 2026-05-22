@echo off
title Frontend - Port 5173
cd /d "%~dp0frontend"

echo Installing frontend packages...
call npm install
if errorlevel 1 goto error

echo.
echo Starting frontend...
echo Keep this window OPEN.
echo Open the URL shown below in your browser (usually http://localhost:5173)
echo.
call npm run dev
goto end

:error
echo.
echo ERROR: npm install failed. Install Node.js from https://nodejs.org
pause
exit /b 1

:end
pause
