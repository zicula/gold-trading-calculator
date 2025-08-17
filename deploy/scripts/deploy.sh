#!/bin/bash

# 🚀 Gold Trading Calculator Deployment Script v2.0
# Author: Zic Trading
# Date: August 16, 2025

echo "🚀 Starting Gold Trading Calculator Deployment..."
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "risk_calculator.html" ]; then
    echo -e "${RED}Error: risk_calculator.html not found. Please run this script from the Gold_Trading_Calculator directory.${NC}"
    exit 1
fi

echo -e "${BLUE}✅ Project files verified${NC}"

# Step 1: Check Git Status
echo -e "${YELLOW}📦 Step 1: Checking Git Status...${NC}"

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  Found uncommitted changes. Committing...${NC}"
    git add .
    git commit -m "� Auto-commit before deployment $(date '+%Y-%m-%d %H:%M:%S')

Updated Features:
- Enhanced Risk Calculator with MM System
- Mobile Responsive Design (iPhone optimized)
- MT5 Integration Support
- Dual-Zone Trading Strategy
- Professional UI/UX Improvements"
fi

echo -e "${GREEN}✅ Git status checked${NC}"

# Step 2: Push to GitHub
echo -e "${YELLOW}📡 Step 2: Pushing to GitHub...${NC}"

git push origin main

echo -e "${GREEN}✅ Code pushed to GitHub${NC}"

# Step 3: Deploy to Vercel
echo -e "${YELLOW}� Step 3: Deploying to Vercel...${NC}"
if command -v vercel &> /dev/null; then
    echo -e "${BLUE}Deploying to production...${NC}"
    vercel --prod
    echo -e "${GREEN}✅ Deployed to Vercel${NC}"
else
    echo -e "${YELLOW}⚠️  Vercel CLI not found. Installing...${NC}"
    npm install -g vercel
    echo -e "${BLUE}Please login to Vercel and redeploy...${NC}"
    vercel login
    vercel --prod
fi

# Step 4: Deploy to Netlify (Optional)
echo ""
echo -e "${YELLOW}📡 Step 4: Deploy to Netlify (Optional)${NC}"
read -p "Do you want to deploy to Netlify as well? (y/n): " deploy_netlify

if [[ $deploy_netlify == "y" || $deploy_netlify == "Y" ]]; then
    if command -v netlify &> /dev/null; then
        echo -e "${BLUE}Deploying to Netlify...${NC}"
        netlify deploy --prod --dir=.
        echo -e "${GREEN}✅ Deployed to Netlify${NC}"
    else
        echo -e "${YELLOW}⚠️  Netlify CLI not found. Installing...${NC}"
        npm install -g netlify-cli
        echo -e "${BLUE}Please login to Netlify and redeploy...${NC}"
        netlify login
        netlify deploy --prod --dir=.
    fi
fi

# Step 5: Summary
echo ""
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo -e "${GREEN}=========================${NC}"
echo ""
echo -e "${BLUE}📊 Your Gold Trading Calculator Features:${NC}"
echo -e "${BLUE}🧮 All-In Calculator v4${NC}"
echo -e "${BLUE}📊 Risk Calculator with MM System${NC}"
echo -e "${BLUE}🔗 MT5 Integration Support${NC}"
echo -e "${BLUE}📱 Mobile Responsive Design${NC}"
echo -e "${BLUE}💰 Dual-Zone Trading Strategy${NC}"
echo ""
echo -e "${BLUE}📱 Access Routes:${NC}"
echo -e "${BLUE}   /           → Main page${NC}"
echo -e "${BLUE}   /calculator → All-In Calculator${NC}"
echo -e "${BLUE}   /risk       → Risk Calculator${NC}"
echo -e "${BLUE}   /risk-mt5   → Risk Calculator MT5${NC}"
echo -e "${BLUE}   /mt5        → MT5 Integration${NC}"
echo ""
echo -e "${YELLOW}🔧 Next Steps:${NC}"
echo -e "${YELLOW}1. Test all calculators on mobile and desktop${NC}"
echo -e "${YELLOW}2. Verify MM calculations work correctly${NC}"
echo -e "${YELLOW}3. Test MT5 integration features${NC}"
echo -e "${YELLOW}4. Set up custom domain (optional)${NC}"
echo ""
echo -e "${GREEN}✨ Your Advanced Trading Calculator Suite is now live!${NC}"
echo -e "${GREEN}Made with ❤️ by Zic Trading${NC}"
