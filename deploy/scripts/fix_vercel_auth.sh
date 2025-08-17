#!/bin/bash

# 🔧 Vercel Account Setup Helper
# This script helps resolve the "Account not found" error

echo "🚀 Vercel Account Setup Helper"
echo "================================"
echo ""

# Check if user has Vercel account
echo "Step 1: Check if you have a Vercel account"
echo "🌐 Please open: https://vercel.com"
echo "👤 If you don't have an account, click 'Continue with GitHub'"
echo "✅ Complete the account setup process"
echo ""
read -p "Press Enter when you have a Vercel account..."

# Clear existing credentials
echo "Step 2: Clear any existing credentials"
echo "🧹 Removing old authentication data..."
rm -rf ~/.config/vercel ~/.vercel 2>/dev/null || true
echo "✅ Cleared old credentials"
echo ""

# Fresh login
echo "Step 3: Fresh login attempt"
echo "🔐 Starting fresh Vercel login..."
echo "⚠️  When prompted, choose 'Continue with GitHub'"
echo "🌐 A browser window will open for authentication"
echo ""
read -p "Press Enter to start login process..."

# Attempt login
vercel login

# Check if login was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Login successful!"
    echo "✅ You can now deploy with: vercel --prod"
else
    echo ""
    echo "❌ Login failed. Alternative options:"
    echo "1. 🌐 Use Vercel Dashboard (recommended)"
    echo "2. 🌐 Try GitHub Pages (simplest)"
    echo "3. 🌐 Use Netlify (alternative)"
    echo ""
    echo "📖 Check DEPLOYMENT_GUIDE.md for detailed instructions"
fi

echo ""
echo "🚀 Happy deploying!"
