@echo off
echo Stopping old Node servers on ports 5000, 5173, 5174, 5175...

for %%P in (5000 5173 5174 5175) do (
  for /f "tokens=5" %%A in ('netstat -ano ^| findstr ":%%P " ^| findstr LISTENING') do (
    echo Killing PID %%A on port %%P
    taskkill /PID %%A /F >nul 2>&1
  )
)

echo Done. Now run RUN_BACKEND.bat then RUN_FRONTEND.bat
pause
