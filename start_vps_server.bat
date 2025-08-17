@echo off
REM MT5 Trading Server Startup Script for VPS
REM Place this file in C:\MT5_Server\

echo ========================================
echo    MT5 Trading Server - VPS Edition
echo ========================================
echo.

REM Set working directory
cd /d "C:\MT5_Server\gold-trading-calculator"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing Python packages...
pip install flask flask-cors MetaTrader5 requests python-dotenv

REM Check if MT5 is running
echo Checking MetaTrader 5...
tasklist /FI "IMAGENAME eq terminal64.exe" 2>NUL | find /I /N "terminal64.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ MetaTrader 5 is running
) else (
    echo ⚠️  MetaTrader 5 is not running
    echo Please start MT5 and login to your trading account
    echo.
    set /p answer="Do you want to continue anyway? (y/n): "
    if /i "%answer%" neq "y" (
        echo Exiting...
        pause
        exit /b 1
    )
)

REM Start the server
echo.
echo ========================================
echo Starting MT5 Trading Server...
echo ========================================
echo.
echo Server will be available at:
echo - Local:  http://localhost:8080
echo - Network: http://%COMPUTERNAME%:8080
echo.
echo Press Ctrl+C to stop the server
echo.

python production_server.py

REM If server stops, show message
echo.
echo ========================================
echo Server stopped
echo ========================================
pause
