#!/bin/bash

# 🍎 MT5 Setup Script for macOS
# This script helps set up MT5 integration on macOS

echo "🍎 MT5 Setup for macOS - Gold Trading Calculator"
echo "=================================================="

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is designed for macOS only"
    exit 1
fi

echo ""
echo "📋 MT5 Integration Options for macOS:"
echo ""
echo "1. 🔧 Parallels Desktop + Windows VM (Recommended)"
echo "2. 🐳 Docker Desktop + Windows Container"
echo "3. ☁️  Remote VPS Setup"
echo "4. 🍷 Wine (Experimental)"
echo ""

read -p "Choose an option (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🔧 Setting up Parallels Desktop method..."
        echo ""
        echo "📥 Steps to follow:"
        echo "1. Download Parallels Desktop: https://www.parallels.com/"
        echo "2. Install Windows 11 in Parallels"
        echo "3. Download and install MT5 in Windows VM"
        echo "4. Install Python in Windows VM"
        echo ""
        echo "📋 Commands to run in Windows VM:"
        echo "   pip install MetaTrader5 Flask flask-cors"
        echo "   git clone https://github.com/zicula/gold-trading-calculator.git"
        echo "   cd gold-trading-calculator"
        echo "   python mt5_server.py"
        echo ""
        echo "🔗 Then update MT5_SERVER_URL in mt5_integration.html to your VM IP"
        ;;
    2)
        echo ""
        echo "🐳 Setting up Docker method..."
        echo ""
        echo "❗ Note: Windows containers on macOS require specific setup"
        echo ""
        echo "📥 Steps:"
        echo "1. Install Docker Desktop for Mac"
        echo "2. Enable Windows containers (if supported)"
        echo "3. Build Windows container with MT5"
        echo ""
        echo "⚠️  This method is complex and may not work reliably"
        ;;
    3)
        echo ""
        echo "☁️  Setting up Remote VPS method..."
        echo ""
        echo "📥 Recommended VPS providers:"
        echo "- AWS EC2 Windows"
        echo "- Google Cloud Windows"
        echo "- Azure Windows VM"
        echo "- Vultr Windows"
        echo ""
        echo "📋 Steps:"
        echo "1. Create Windows VPS"
        echo "2. Install MT5 on VPS"
        echo "3. Install Python and dependencies"
        echo "4. Upload project files"
        echo "5. Run mt5_server.py"
        echo "6. Update MT5_SERVER_URL to VPS IP"
        echo ""
        echo "💰 Estimated cost: $10-30/month"
        ;;
    4)
        echo ""
        echo "🍷 Setting up Wine method (Experimental)..."
        echo ""
        echo "⚠️  Warning: This method is unreliable and not recommended"
        echo ""
        if command -v brew &> /dev/null; then
            echo "📦 Installing Wine via Homebrew..."
            brew install --cask wine-stable
            echo "✅ Wine installed"
            echo ""
            echo "📋 Next steps:"
            echo "1. Download MT5 Windows installer"
            echo "2. Run: wine mt5setup.exe"
            echo "3. Install Python in Wine environment"
            echo "4. Install MetaTrader5 library"
            echo ""
            echo "❗ Note: Wine support for MT5 is limited and buggy"
        else
            echo "❌ Homebrew not found. Please install Homebrew first:"
            echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        fi
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "📚 Additional Resources:"
echo "- MT5 Documentation: https://www.metatrader5.com/en/terminal/help"
echo "- Python API Docs: https://www.mql5.com/en/docs/integration/python_metatrader5"
echo "- Project Repository: https://github.com/zicula/gold-trading-calculator"
echo ""
echo "🔧 For development/testing, the server includes mock MT5 implementation"
echo "   You can test the web interface without actual MT5 connection"
echo ""

# Check if we're in the project directory
if [[ -f "mt5_server.py" ]]; then
    echo "📍 You're in the project directory"
    echo ""
    echo "🧪 To test with mock MT5 (no real trading):"
    echo "   python3 mt5_server.py"
    echo ""
    echo "🌐 Then open: http://localhost:8080/status"
    echo ""
    read -p "Start mock server now? (y/n): " start_mock
    if [[ $start_mock == "y" || $start_mock == "Y" ]]; then
        echo "🚀 Starting mock MT5 server..."
        python3 mt5_server.py
    fi
else
    echo "📂 Navigate to project directory first:"
    echo "   cd /path/to/gold-trading-calculator"
    echo "   ./setup_mt5_macos.sh"
fi

echo ""
echo "✅ Setup guide completed!"
echo "📞 Need help? Check README_MT5_MACOS.md for detailed instructions"
