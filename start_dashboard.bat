@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python fisens_dashboard.py
pause
