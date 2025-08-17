#!/bin/bash
# MT5 Integration Setup Script
# Gold Trading Calculator by Zic

echo "🟡 Gold Trading Calculator - MT5 Integration Setup"
echo "=================================================="
echo ""

# Check if Python is installed
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    echo "📥 Download from: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "✅ Python $PYTHON_VERSION found"

# Check if pip is installed
echo "🔍 Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi
echo "✅ pip3 found"

# Install Python packages
echo ""
echo "📦 Installing required Python packages..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ All packages installed successfully"
else
    echo "❌ Failed to install packages. Please check your internet connection and try again."
    exit 1
fi

# Create start script
echo ""
echo "📝 Creating start script..."
cat > start_mt5_server.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting MT5 Integration Server..."
echo "🔗 Server URL: http://localhost:8080"
echo "⚠️  Make sure MT5 is running and Auto Trading is enabled"
echo ""
echo "To stop the server, press Ctrl+C"
echo "=================================================="
python3 mt5_server.py
EOF

chmod +x start_mt5_server.sh
echo "✅ Start script created: start_mt5_server.sh"

# Create Windows batch file
cat > start_mt5_server.bat << 'EOF'
@echo off
echo 🚀 Starting MT5 Integration Server...
echo 🔗 Server URL: http://localhost:8080
echo ⚠️  Make sure MT5 is running and Auto Trading is enabled
echo.
echo To stop the server, press Ctrl+C
echo ==================================================
python mt5_server.py
pause
EOF

echo "✅ Windows start script created: start_mt5_server.bat"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Open MetaTrader 5"
echo "2. Login to your ConnextFX account"
echo "3. Enable Auto Trading (Tools → Options → Expert Advisors → Allow automated trading)"
echo "4. Run the server:"
echo "   - On Mac/Linux: ./start_mt5_server.sh"
echo "   - On Windows: start_mt5_server.bat"
echo "5. Open mt5_integration.html in your browser"
echo ""
echo "🔗 Server will be available at: http://localhost:8080"
echo "🌐 Web interface: file://$(pwd)/mt5_integration.html"
