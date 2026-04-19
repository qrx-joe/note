@echo off
cd /d %~dp0

set "PORT=5000"
:find_port
netstat -ano | findstr ":%PORT%" >nul
if errorlevel 1 goto :found_port
set /a PORT+=1
if %PORT% LEQ 5010 goto :find_port

echo [ERROR] 端口 5000~5010 均已被占用，请手动释放端口或设置 PORT 环境变量。
pause
exit /b 1

:found_port
echo 使用端口 %PORT%

.venv\Scripts\python.exe app.py
if errorlevel 1 (
    echo.
    echo [ERROR] Application failed to start!
    pause
)
pause
