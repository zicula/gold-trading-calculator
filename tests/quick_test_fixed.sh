#!/bin/bash
# 🧪 Quick Test Script - Fixed Version
# Essential Tests Only
# ทดสอบด่วนเฉพาะฟีเจอร์หลัก

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BASE_URL=${BASE_URL:-"http://localhost:8080"}
PASSED=0
FAILED=0
TOTAL=0

# Generate unique username for each test run
TIMESTAMP=$(date +%s)
TEST_USER="quicktest$TIMESTAMP"

echo -e "${BLUE}⚡ Quick Test - Gold Trading Calculator${NC}"
echo "========================================"

# Test function
quick_test() {
    local name="$1"
    local command="$2"
    TOTAL=$((TOTAL + 1))
    
    printf "[%d] %s... " "$TOTAL" "$name"
    
    if eval "$command" >/dev/null 2>&1; then
        echo -e "${GREEN}✅${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}❌${NC}"
        FAILED=$((FAILED + 1))
    fi
}

# Essential tests
quick_test "Server Health" "curl -s $BASE_URL/api/status | grep -q healthy"
quick_test "User Registration" "curl -s -X POST $BASE_URL/api/register -H 'Content-Type: application/json' -d '{\"username\":\"$TEST_USER\",\"email\":\"$TEST_USER@test.com\",\"password\":\"Test123!\"}' | grep -q successfully"
quick_test "User Login" "curl -s -X POST $BASE_URL/api/login -H 'Content-Type: application/json' -d '{\"username\":\"$TEST_USER\",\"password\":\"Test123!\"}' | grep -q token"

# Get token for authenticated tests
TOKEN=$(curl -s -X POST "$BASE_URL/api/login" -H "Content-Type: application/json" -d '{"username":"'$TEST_USER'","password":"Test123!"}' | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null || echo "")

if [ -n "$TOKEN" ]; then
    quick_test "Add MT5 Account" "curl -s -X POST $BASE_URL/api/accounts -H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json' -d '{\"account_name\":\"Quick Test\",\"login\":\"123\",\"password\":\"pass\",\"server\":\"demo\"}' | grep -q successfully"
    
    # Connect and get new token with account_id
    CONNECT_RESULT=$(curl -s -X POST $BASE_URL/api/accounts/1/connect -H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json' 2>/dev/null || echo "")
    quick_test "Connect MT5 Account" "echo '$CONNECT_RESULT' | grep -q successfully"
    
    # Get the new token from connection result
    NEW_TOKEN=$(echo "$CONNECT_RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null || echo "")
    
    if [ -n "$NEW_TOKEN" ]; then
        quick_test "Calculate Lot Size" "curl -s -X POST $BASE_URL/api/calculate -H 'Authorization: Bearer $NEW_TOKEN' -H 'Content-Type: application/json' -d '{\"symbol\":\"XAUUSD\",\"entryPrice1\":\"2000\",\"stopLoss\":\"1990\",\"portfolioSize\":\"10000\",\"riskPercent\":\"2\"}' | grep -q lotSize"
    else
        quick_test "Calculate Lot Size" "false"  # Force fail if no new token
    fi
fi

echo -e "\n📊 Results: ${GREEN}$PASSED passed${NC}, ${RED}$FAILED failed${NC} (${TOTAL} total)"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All essential features working!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some critical features failed${NC}"
    exit 1
fi
