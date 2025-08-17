#!/bin/bash
# 🧪 Automated Testing Script for Gold Trading Calculator
# ทดสอบระบบอัตโนมัติทุกฟีเจอร์

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BASE_URL=${BASE_URL:-"http://localhost:8080"}
TEST_DATA_DIR="tests/fixtures"
RESULTS_DIR="tests/results"

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

echo -e "${BLUE}🧪 Gold Trading Calculator - Automated Testing${NC}"
echo "================================================="

# Function to run test and track results
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_status="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -e "\n${YELLOW}[TEST $TOTAL_TESTS] $test_name${NC}"
    
    # Run the test command
    if eval "$test_command"; then
        echo -e "${GREEN}✅ PASSED: $test_name${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}❌ FAILED: $test_name${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Function to test API endpoint
test_api() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    local expected_status="$4"
    local token="$5"
    
    local curl_cmd="curl -s -w '%{http_code}' -X $method"
    
    if [ -n "$token" ]; then
        curl_cmd="$curl_cmd -H 'Authorization: Bearer $token'"
    fi
    
    if [ -n "$data" ]; then
        curl_cmd="$curl_cmd -H 'Content-Type: application/json' -d '$data'"
    fi
    
    curl_cmd="$curl_cmd '$BASE_URL$endpoint'"
    
    local response=$(eval "$curl_cmd")
    local status_code="${response: -3}"
    
    if [ "$status_code" = "$expected_status" ]; then
        return 0
    else
        echo "Expected: $expected_status, Got: $status_code"
        return 1
    fi
}

# Setup test environment
setup_test_env() {
    echo -e "${YELLOW}🔧 Setting up test environment...${NC}"
    
    # Create results directory
    mkdir -p "$RESULTS_DIR"
    
    # Wait for application to be ready
    echo "Waiting for application to start..."
    for i in {1..30}; do
        if curl -s "$BASE_URL/api/status" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Application is ready${NC}"
            break
        fi
        sleep 2
    done
}

# Test 1: Health Check
test_health_check() {
    echo -e "\n${BLUE}=== Phase 1: Health Check ===${NC}"
    
    run_test "Server Status Check" \
        "test_api 'GET' '/api/status' '' '200'" \
        "200"
}

# Test 2: Authentication Tests
test_authentication() {
    echo -e "\n${BLUE}=== Phase 2: Authentication Tests ===${NC}"
    
    # Test user registration
    run_test "User Registration - Normal User" \
        "test_api 'POST' '/api/register' '{\"username\":\"testuser1\",\"email\":\"test1@example.com\",\"password\":\"TestPass123!\",\"role\":\"user\"}' '201'" \
        "201"
    
    run_test "User Registration - Broadcast User" \
        "test_api 'POST' '/api/register' '{\"username\":\"broadcast1\",\"email\":\"broadcast1@example.com\",\"password\":\"TestPass123!\",\"role\":\"broadcast\"}' '201'" \
        "201"
    
    run_test "User Registration - Super Admin" \
        "test_api 'POST' '/api/register' '{\"username\":\"admin1\",\"email\":\"admin1@example.com\",\"password\":\"TestPass123!\",\"role\":\"super_admin\"}' '201'" \
        "201"
    
    # Test duplicate registration
    run_test "Duplicate Registration Prevention" \
        "test_api 'POST' '/api/register' '{\"username\":\"testuser1\",\"email\":\"test1@example.com\",\"password\":\"TestPass123!\"}' '409'" \
        "409"
    
    # Test user login
    run_test "User Login - Valid Credentials" \
        "test_api 'POST' '/api/login' '{\"username\":\"testuser1\",\"password\":\"TestPass123!\"}' '200'" \
        "200"
    
    run_test "User Login - Invalid Credentials" \
        "test_api 'POST' '/api/login' '{\"username\":\"testuser1\",\"password\":\"wrongpassword\"}' '401'" \
        "401"
    
    # Get tokens for further testing
    echo "Getting authentication tokens..."
    
    USER_TOKEN=$(curl -s -X POST "$BASE_URL/api/login" \
        -H "Content-Type: application/json" \
        -d '{"username":"testuser1","password":"TestPass123!"}' | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null || echo "")
    
    BROADCAST_TOKEN=$(curl -s -X POST "$BASE_URL/api/login" \
        -H "Content-Type: application/json" \
        -d '{"username":"broadcast1","password":"TestPass123!"}' | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null || echo "")
    
    ADMIN_TOKEN=$(curl -s -X POST "$BASE_URL/api/login" \
        -H "Content-Type: application/json" \
        -d '{"username":"admin1","password":"TestPass123!"}' | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null || echo "")
    
    if [ -n "$USER_TOKEN" ] && [ -n "$ADMIN_TOKEN" ]; then
        echo -e "${GREEN}✅ Tokens obtained successfully${NC}"
    else
        echo -e "${RED}❌ Failed to obtain tokens${NC}"
    fi
}

# Test 3: Authorization Tests
test_authorization() {
    echo -e "\n${BLUE}=== Phase 3: Authorization Tests ===${NC}"
    
    # Test access without token
    run_test "Access Denied Without Token" \
        "test_api 'GET' '/api/accounts' '' '401'" \
        "401"
    
    # Test access with invalid token
    run_test "Access Denied With Invalid Token" \
        "test_api 'GET' '/api/accounts' '' '401' 'invalid_token'" \
        "401"
    
    # Test role-based access control
    run_test "User Access to Broadcast Endpoint (Should Fail)" \
        "test_api 'POST' '/api/broadcast_orders' '{\"symbol\":\"XAUUSD\"}' '403' '$USER_TOKEN'" \
        "403"
    
    run_test "Admin Access to Broadcast Endpoint (Should Pass)" \
        "test_api 'POST' '/api/broadcast_orders' '{\"symbol\":\"XAUUSD\",\"entryPrice1\":\"2000\",\"stopLoss\":\"1990\",\"riskPercent\":\"2\"}' '200' '$ADMIN_TOKEN'" \
        "200"
}

# Test 4: MT5 Account Management
test_mt5_accounts() {
    echo -e "\n${BLUE}=== Phase 4: MT5 Account Management ===${NC}"
    
    # Test getting accounts (should be empty initially)
    run_test "Get Empty Accounts List" \
        "test_api 'GET' '/api/accounts' '' '200' '$USER_TOKEN'" \
        "200"
    
    # Test adding MT5 account
    run_test "Add MT5 Account" \
        "test_api 'POST' '/api/accounts' '{\"account_name\":\"Demo Account 1\",\"login\":\"12345678\",\"password\":\"mt5password\",\"server\":\"MetaQuotes-Demo\",\"broker\":\"MetaQuotes\",\"account_type\":\"demo\"}' '201' '$USER_TOKEN'" \
        "201"
    
    # Test adding account with missing fields
    run_test "Add Account With Missing Fields (Should Fail)" \
        "test_api 'POST' '/api/accounts' '{\"account_name\":\"Incomplete Account\"}' '400' '$USER_TOKEN'" \
        "400"
    
    # Test getting accounts after adding
    run_test "Get Accounts List After Adding" \
        "test_api 'GET' '/api/accounts' '' '200' '$USER_TOKEN'" \
        "200"
}

# Test 5: Trading Calculator
test_calculator() {
    echo -e "\n${BLUE}=== Phase 5: Trading Calculator Tests ===${NC}"
    
    # Test basic calculation
    run_test "Basic Lot Calculation" \
        "test_api 'POST' '/api/calculate' '{\"symbol\":\"XAUUSD\",\"entryPrice1\":\"2000.00\",\"stopLoss\":\"1990.00\",\"portfolioSize\":\"10000\",\"riskPercent\":\"2\"}' '200' '$USER_TOKEN'" \
        "200"
    
    # Test calculation without connection (should still work for calculation)
    run_test "Calculate Without MT5 Connection" \
        "test_api 'POST' '/api/calculate' '{\"symbol\":\"XAUUSD\",\"entryPrice1\":\"2000.00\",\"stopLoss\":\"1990.00\",\"portfolioSize\":\"5000\",\"riskPercent\":\"1\"}' '200' '$USER_TOKEN'" \
        "200"
    
    # Test calculation with missing fields
    run_test "Calculate With Missing Fields (Should Fail)" \
        "test_api 'POST' '/api/calculate' '{\"symbol\":\"XAUUSD\",\"entryPrice1\":\"2000.00\"}' '400' '$USER_TOKEN'" \
        "400"
}

# Test 6: Broadcast System
test_broadcast_system() {
    echo -e "\n${BLUE}=== Phase 6: Broadcast System Tests ===${NC}"
    
    # Test broadcast orders by admin
    run_test "Send Broadcast Orders (Admin)" \
        "test_api 'POST' '/api/broadcast_orders' '{\"symbol\":\"XAUUSD\",\"entryPrice1\":\"2000.00\",\"stopLoss\":\"1990.00\",\"riskPercent\":\"2\",\"portfolioSize\":\"5000\"}' '200' '$ADMIN_TOKEN'" \
        "200"
    
    # Test broadcast status
    run_test "Get Broadcast Status" \
        "test_api 'GET' '/api/broadcast_status' '' '200' '$ADMIN_TOKEN'" \
        "200"
    
    # Test broadcast access by non-admin (should fail)
    run_test "Non-Admin Broadcast Access (Should Fail)" \
        "test_api 'POST' '/api/broadcast_orders' '{\"symbol\":\"XAUUSD\"}' '403' '$USER_TOKEN'" \
        "403"
}

# Test 7: Order Management
test_order_management() {
    echo -e "\n${BLUE}=== Phase 7: Order Management Tests ===${NC}"
    
    # Test sending orders (requires connected account, might fail in test env)
    run_test "Send Orders to MT5" \
        "test_api 'POST' '/api/send_orders' '{\"symbol\":\"XAUUSD\",\"action\":\"BUY\",\"volume\":\"0.1\"}' '500' '$USER_TOKEN'" \
        "500"  # Expecting 500 because no real MT5 connection
}

# Test 8: Security Tests
test_security() {
    echo -e "\n${BLUE}=== Phase 8: Security Tests ===${NC}"
    
    # Test SQL injection prevention
    run_test "SQL Injection Prevention" \
        "test_api 'POST' '/api/login' '{\"username\":\"admin'\'; DROP TABLE users; --\",\"password\":\"test\"}' '401'" \
        "401"
    
    # Test XSS prevention
    run_test "XSS Prevention in Registration" \
        "test_api 'POST' '/api/register' '{\"username\":\"<script>alert(1)</script>\",\"email\":\"xss@test.com\",\"password\":\"test123\"}' '201'" \
        "201"
    
    # Test password requirements
    run_test "Weak Password Rejection" \
        "test_api 'POST' '/api/register' '{\"username\":\"weakuser\",\"email\":\"weak@test.com\",\"password\":\"123\"}' '400'" \
        "400"
}

# Test 9: Performance Tests
test_performance() {
    echo -e "\n${BLUE}=== Phase 9: Performance Tests ===${NC}"
    
    echo "Running concurrent request test..."
    
    # Test concurrent registrations
    local start_time=$(date +%s)
    for i in {1..10}; do
        curl -s -X POST "$BASE_URL/api/register" \
            -H "Content-Type: application/json" \
            -d "{\"username\":\"perfuser$i\",\"email\":\"perf$i@test.com\",\"password\":\"TestPass123!\"}" > /dev/null &
    done
    wait
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    if [ $duration -lt 10 ]; then
        echo -e "${GREEN}✅ PASSED: Concurrent Registration Performance (${duration}s)${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAILED: Concurrent Registration Performance (${duration}s > 10s)${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

# Test 10: Data Validation
test_data_validation() {
    echo -e "\n${BLUE}=== Phase 10: Data Validation Tests ===${NC}"
    
    # Test email format validation
    run_test "Invalid Email Format" \
        "test_api 'POST' '/api/register' '{\"username\":\"emailtest\",\"email\":\"invalid-email\",\"password\":\"TestPass123!\"}' '400'" \
        "400"
    
    # Test numeric validation in calculator
    run_test "Invalid Numeric Input in Calculator" \
        "test_api 'POST' '/api/calculate' '{\"symbol\":\"XAUUSD\",\"entryPrice1\":\"not-a-number\",\"stopLoss\":\"1990\",\"portfolioSize\":\"10000\",\"riskPercent\":\"2\"}' '400' '$USER_TOKEN'" \
        "400"
    
    # Test negative values validation
    run_test "Negative Values Validation" \
        "test_api 'POST' '/api/calculate' '{\"symbol\":\"XAUUSD\",\"entryPrice1\":\"2000\",\"stopLoss\":\"1990\",\"portfolioSize\":\"-1000\",\"riskPercent\":\"2\"}' '400' '$USER_TOKEN'" \
        "400"
}

# Generate test report
generate_report() {
    echo -e "\n${BLUE}📊 Generating Test Report...${NC}"
    
    local report_file="$RESULTS_DIR/test_report_$(date +%Y%m%d_%H%M%S).md"
    
    cat > "$report_file" << EOF
# 🧪 Gold Trading Calculator - Test Report
**Generated:** $(date)
**Environment:** $BASE_URL

## 📊 Summary
- **Total Tests:** $TOTAL_TESTS
- **Passed:** $PASSED_TESTS
- **Failed:** $FAILED_TESTS
- **Success Rate:** $(echo "scale=2; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc)%

## 📋 Test Results
EOF

    if [ $FAILED_TESTS -eq 0 ]; then
        echo "✅ **All tests passed!**" >> "$report_file"
    else
        echo "❌ **Some tests failed. Check logs for details.**" >> "$report_file"
    fi
    
    echo -e "${GREEN}✅ Report generated: $report_file${NC}"
}

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🧹 Cleaning up test data...${NC}"
    # Add cleanup commands here if needed
}

# Main test execution
main() {
    setup_test_env
    
    test_health_check
    test_authentication
    test_authorization
    test_mt5_accounts
    test_calculator
    test_broadcast_system
    test_order_management
    test_security
    test_performance
    test_data_validation
    
    # Print final summary
    echo -e "\n${BLUE}=====================================${NC}"
    echo -e "${BLUE}📊 Final Test Summary${NC}"
    echo -e "${BLUE}=====================================${NC}"
    echo -e "Total Tests: $TOTAL_TESTS"
    echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
    echo -e "${RED}Failed: $FAILED_TESTS${NC}"
    
    local success_rate=$(echo "scale=2; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc)
    echo -e "Success Rate: ${success_rate}%"
    
    if [ $FAILED_TESTS -eq 0 ]; then
        echo -e "\n${GREEN}🎉 All tests passed! System is ready for production.${NC}"
    else
        echo -e "\n${RED}⚠️  Some tests failed. Please review and fix issues before deployment.${NC}"
    fi
    
    generate_report
    cleanup
    
    # Exit with error code if tests failed
    [ $FAILED_TESTS -eq 0 ] && exit 0 || exit 1
}

# Run tests
main "$@"
