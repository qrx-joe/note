@echo off
chcp 65001 >nul
title Momerandum
cd /d %~dp0
.venv\Scripts\python.exe app.py
pause