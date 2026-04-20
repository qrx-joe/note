@echo off
cd /d %~dp0

set "PORT=5000"
:find_port
netstat -ano | findstr ":%PORT%" >nul
if errorlevel 1 goto :found_port
set /a PORT+=1
if %PORT% LEQ 5010 goto :find_port

echo [ERROR] Port 5000~5010 all occupied, set PORT env var manually.
pause
exit /b 1

:found_port
echo Using port %PORT%

.venv\Scripts\python.exe app.py
pause
