@echo off
REM Fiber Optic Sensing Logger - Single 60-Second Session
REM Click this batch file each time you want to run a 60-second session

cd /d "%~dp0"

echo ========================================
echo Fiber Optic Sensing Logger - Single Run
echo This session will run for 60 seconds
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the logger once (60 seconds)
echo Starting logging session...
python Fiber_optic_sensing_60sec.py

echo.
echo ========================================
echo Session complete!
echo.
echo To run another session, just double-click
echo this batch file again!
echo ========================================
echo.

pause
exit /b 0