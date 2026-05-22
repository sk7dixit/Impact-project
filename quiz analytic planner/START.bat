@echo off
title AI Exam Prep - Starting...
cd /d "%~dp0"

echo Installing dependencies (if needed)...
call npm run install:all
if errorlevel 1 (
  echo Install failed. Make sure Node.js is installed.
  pause
  exit /b 1
)

echo.
echo Starting Backend (port 5000) and Frontend (port 5173)...
echo Open browser: http://localhost:5173
echo Press Ctrl+C to stop both servers.
echo.

call npm run dev

pause
