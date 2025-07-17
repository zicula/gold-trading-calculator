#!/bin/bash

# 🚀 Gold Trading Calculator Deployment Script
# Author: Zic Trading
# Date: July 17, 2025

echo "🚀 Starting Gold Trading Calculator Deployment..."
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "all_in_calculator_v4.html" ]; then
    echo -e "${RED}Error: all_in_calculator_v4.html not found. Please run this script from the Gold_Trading_Calculator directory.${NC}"
    exit 1
fi

echo -e "${BLUE}✅ Project files verified${NC}"

# Step 1: Initialize Git Repository
echo -e "${YELLOW}📦 Step 1: Initializing Git Repository...${NC}"
git init
git add .
git commit -m "🚀 Initial commit: Gold Trading Calculator V4 by Zic

Features:
- Binance Style Dark Theme  
- Responsive Design (Mobile/Tablet/Desktop)
- Auto RR Management
- Card System with Save Function
- Real-time Calculation
- Professional UI/UX

Version: 4.0.0
Author: Zic Trading"

echo -e "${GREEN}✅ Git repository initialized${NC}"

# Step 2: Add GitHub Remote
echo -e "${YELLOW}📡 Step 2: Adding GitHub Remote...${NC}"
git remote add origin https://github.com/zicula/gold-trading-calculator.git
git branch -M main

echo -e "${GREEN}✅ GitHub remote added${NC}"

# Step 3: Push to GitHub
echo -e "${YELLOW}🔄 Step 3: Pushing to GitHub...${NC}"
echo -e "${BLUE}Please make sure you've created the repository on GitHub first:${NC}"
echo -e "${BLUE}https://github.com/zicula/gold-trading-calculator${NC}"
echo ""
read -p "Press Enter to continue when repository is created..."

git push -u origin main

echo -e "${GREEN}✅ Code pushed to GitHub${NC}"

# Step 4: Deploy to Vercel
echo -e "${YELLOW}🚀 Step 4: Deploying to Vercel...${NC}"
echo -e "${BLUE}Installing Vercel CLI...${NC}"
npm install -g vercel

echo -e "${BLUE}Please login to Vercel when prompted...${NC}"
vercel login

echo -e "${BLUE}Deploying to production...${NC}"
vercel --prod

echo -e "${GREEN}✅ Deployed to Vercel${NC}"

# Step 5: Deploy to Netlify (Optional)
echo ""
echo -e "${YELLOW}📡 Step 5: Deploy to Netlify (Optional)${NC}"
read -p "Do you want to deploy to Netlify as well? (y/n): " deploy_netlify

if [[ $deploy_netlify == "y" || $deploy_netlify == "Y" ]]; then
    echo -e "${BLUE}Installing Netlify CLI...${NC}"
    npm install -g netlify-cli
    
    echo -e "${BLUE}Please login to Netlify when prompted...${NC}"
    netlify login
    
    echo -e "${BLUE}Deploying to Netlify...${NC}"
    netlify deploy --prod --dir=.
    
    echo -e "${GREEN}✅ Deployed to Netlify${NC}"
fi

# Step 6: Summary
echo ""
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo -e "${GREEN}=========================${NC}"
echo ""
echo -e "${BLUE}📊 Deployment Summary:${NC}"
echo -e "${BLUE}- GitHub Repository: https://github.com/zicula/gold-trading-calculator${NC}"
echo -e "${BLUE}- Vercel URL: Check the output above for your deployment URL${NC}"
if [[ $deploy_netlify == "y" || $deploy_netlify == "Y" ]]; then
    echo -e "${BLUE}- Netlify URL: Check the output above for your deployment URL${NC}"
fi
echo ""
echo -e "${YELLOW}🔧 Next Steps:${NC}"
echo -e "${YELLOW}1. Test your live application${NC}"
echo -e "${YELLOW}2. Set up custom domain (optional)${NC}"
echo -e "${YELLOW}3. Configure analytics${NC}"
echo -e "${YELLOW}4. Monitor performance${NC}"
echo ""
echo -e "${GREEN}✨ Your Gold Trading Calculator is now live!${NC}"
echo -e "${GREEN}Made with ❤️ by Zic Trading${NC}"
