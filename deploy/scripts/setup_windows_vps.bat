@echo off
echo ========================================
echo  Gold Trading Calculator - Windows VPS Setup
echo ========================================

echo Step 1: Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Step 2: Installing Python packages...
pip install --upgrade pip
pip install -r requirements.txt

echo Step 3: Checking MT5 installation...
if not exist "C:\Program Files\MetaTrader 5" (
    echo WARNING: MT5 not found in default location.
    echo Please install MT5 from your broker first.
)

echo Step 4: Creating config directory...
if not exist "config" mkdir config

echo Step 5: Setting up environment...
echo Creating .env file...
echo MT5_LOGIN=YOUR_MT5_LOGIN > .env
echo MT5_PASSWORD=YOUR_MT5_PASSWORD >> .env
echo MT5_SERVER=YOUR_BROKER_SERVER >> .env
echo FLASK_PORT=8080 >> .env

echo Step 6: Testing Flask server...
echo Starting test server...
python -c "
import sys
try:
    import flask
    import MetaTrader5 as mt5
    print('✅ All dependencies installed successfully!')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    sys.exit(1)
"

echo Step 7: Configuring Windows Firewall...
echo Adding firewall rule for port 8080...
netsh advfirewall firewall add rule name="Flask MT5 Server" dir=in action=allow protocol=TCP localport=8080

echo ========================================
echo ✅ Setup completed successfully!
echo ========================================
echo Next steps:
echo 1. Edit .env file with your MT5 credentials
echo 2. Run: python mt5_server.py
echo 3. Open browser: http://localhost:8080
echo ========================================
pause
