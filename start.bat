@echo off
cd /d %~dp0

netstat -ano | findstr ":5000" >nul
if not errorlevel 1 (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000"') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    echo Port 5000 released.
)

.venv\Scripts\python.exe app.py
if errorlevel 1 (
    echo.
    echo [ERROR] Application failed to start!
    pause
)
pause
