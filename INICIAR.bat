@echo off
cd /d "%~dp0"
echo Abriendo la IA...
where py >nul 2>nul && (py -3 main.py) || (python main.py)
if errorlevel 1 pause