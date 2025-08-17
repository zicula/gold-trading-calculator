# PowerShell script for automated VPS setup
# Run as Administrator on Windows VPS

param(
    [string]$GitHubRepo = "https://github.com/zicula/gold-trading-calculator.git",
    [string]$AppDir = "C:\TradingCalculator",
    [string]$ServiceName = "GoldTradingCalculator"
)

Write-Host "🌊 DigitalOcean VPS Setup for Gold Trading Calculator" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Function to check if running as administrator
function Test-Administrator {
    $user = [Security.Principal.WindowsIdentity]::GetCurrent();
    (New-Object Security.Principal.WindowsPrincipal $user).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}

if (-not (Test-Administrator)) {
    Write-Error "❌ This script must be run as Administrator!"
    Write-Host "Right-click PowerShell and select 'Run as Administrator'"
    exit 1
}

Write-Host "✅ Running as Administrator" -ForegroundColor Green

# Step 1: Install Chocolatey
Write-Host "`n📦 Installing Chocolatey package manager..." -ForegroundColor Yellow
try {
    Get-Command choco -ErrorAction Stop | Out-Null
    Write-Host "✅ Chocolatey already installed" -ForegroundColor Green
} catch {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    Write-Host "✅ Chocolatey installed successfully" -ForegroundColor Green
}

# Step 2: Install required software
Write-Host "`n🐍 Installing Python..." -ForegroundColor Yellow
choco install python -y --force

Write-Host "`n📂 Installing Git..." -ForegroundColor Yellow
choco install git -y --force

Write-Host "`n🔧 Installing Visual C++ Redistributable..." -ForegroundColor Yellow
choco install vcredist2019 -y --force

Write-Host "`n🛠️ Installing NSSM (Service Manager)..." -ForegroundColor Yellow
choco install nssm -y --force

# Refresh environment variables
Write-Host "`n🔄 Refreshing environment..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Step 3: Create application directory
Write-Host "`n📁 Creating application directory..." -ForegroundColor Yellow
if (Test-Path $AppDir) {
    Write-Host "⚠️ Directory already exists: $AppDir" -ForegroundColor Yellow
    $response = Read-Host "Do you want to remove and recreate it? (y/N)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Remove-Item $AppDir -Recurse -Force
        Write-Host "🗑️ Removed existing directory" -ForegroundColor Yellow
    } else {
        Write-Host "ℹ️ Using existing directory" -ForegroundColor Blue
    }
}

if (-not (Test-Path $AppDir)) {
    New-Item -ItemType Directory -Path $AppDir -Force | Out-Null
    Write-Host "✅ Created directory: $AppDir" -ForegroundColor Green
}

# Step 4: Clone repository
Write-Host "`n📥 Cloning GitHub repository..." -ForegroundColor Yellow
Set-Location $AppDir
try {
    if (Test-Path ".git") {
        Write-Host "📂 Repository already exists, pulling latest changes..." -ForegroundColor Blue
        git pull origin main
    } else {
        git clone $GitHubRepo .
    }
    Write-Host "✅ Repository cloned/updated successfully" -ForegroundColor Green
} catch {
    Write-Error "❌ Failed to clone repository: $_"
    exit 1
}

# Step 5: Install Python dependencies
Write-Host "`n📋 Installing Python dependencies..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    Write-Host "✅ Python dependencies installed" -ForegroundColor Green
} catch {
    Write-Error "❌ Failed to install Python dependencies: $_"
    exit 1
}

# Step 6: Configure Windows Firewall
Write-Host "`n🔥 Configuring Windows Firewall..." -ForegroundColor Yellow
try {
    New-NetFirewallRule -DisplayName "Flask MT5 Server" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow -ErrorAction SilentlyContinue
    Write-Host "✅ Firewall rule added for port 8080" -ForegroundColor Green
} catch {
    Write-Warning "⚠️ Could not add firewall rule: $_"
}

# Step 7: Create environment file
Write-Host "`n⚙️ Creating environment configuration..." -ForegroundColor Yellow
$envContent = @"
# MT5 Configuration
MT5_LOGIN=YOUR_MT5_LOGIN
MT5_PASSWORD=YOUR_MT5_PASSWORD
MT5_SERVER=YOUR_BROKER_SERVER

# Flask Configuration
FLASK_PORT=8080
FLASK_HOST=0.0.0.0
FLASK_ENV=production

# Security
SECRET_KEY=your-secret-key-here
"@

$envPath = Join-Path $AppDir ".env"
$envContent | Out-File -FilePath $envPath -Encoding UTF8
Write-Host "✅ Environment file created: $envPath" -ForegroundColor Green
Write-Host "⚠️  Please edit .env file with your MT5 credentials!" -ForegroundColor Yellow

# Step 8: Create deployment script
Write-Host "`n🚀 Creating deployment script..." -ForegroundColor Yellow
$deployScript = @"
@echo off
echo 🚀 Starting deployment...
cd $AppDir

echo 🛑 Stopping existing server...
taskkill /F /IM python.exe /T 2>nul || echo No Python processes found

echo 📥 Pulling latest changes...
git pull origin main

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo 🎯 Starting server...
start /B python mt5_server.py

echo ✅ Deployment complete!
echo 🌐 Server should be available at: http://localhost:8080
"@

$deployPath = Join-Path $AppDir "deploy.bat"
$deployScript | Out-File -FilePath $deployPath -Encoding ASCII
Write-Host "✅ Deployment script created: $deployPath" -ForegroundColor Green

# Step 9: Create Windows Service
Write-Host "`n🔧 Creating Windows Service..." -ForegroundColor Yellow
try {
    # Stop existing service if it exists
    if (Get-Service $ServiceName -ErrorAction SilentlyContinue) {
        Stop-Service $ServiceName -Force
        & nssm remove $ServiceName confirm
    }
    
    # Create new service
    & nssm install $ServiceName python
    & nssm set $ServiceName AppDirectory $AppDir
    & nssm set $ServiceName AppParameters mt5_server.py
    & nssm set $ServiceName DisplayName "Gold Trading Calculator MT5 Server"
    & nssm set $ServiceName Description "Automated trading calculator with MT5 integration"
    & nssm set $ServiceName Start SERVICE_AUTO_START
    
    Write-Host "✅ Windows Service created: $ServiceName" -ForegroundColor Green
} catch {
    Write-Warning "⚠️ Could not create Windows Service: $_"
}

# Step 10: Create health check script
Write-Host "`n🏥 Creating health check script..." -ForegroundColor Yellow
$healthCheckScript = @"
`$url = "http://localhost:8080/status"
try {
    `$response = Invoke-WebRequest -Uri `$url -TimeoutSec 10
    if (`$response.StatusCode -eq 200) {
        Write-Host "✅ Server is healthy" -ForegroundColor Green
        exit 0
    }
} catch {
    Write-Host "❌ Server is down, restarting..." -ForegroundColor Red
    try {
        Restart-Service "$ServiceName" -ErrorAction Stop
        Write-Host "✅ Service restarted" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to restart service: `$_" -ForegroundColor Red
    }
    exit 1
}
"@

$healthCheckPath = Join-Path $AppDir "health_check.ps1"
$healthCheckScript | Out-File -FilePath $healthCheckPath -Encoding UTF8
Write-Host "✅ Health check script created: $healthCheckPath" -ForegroundColor Green

# Step 11: Schedule health check
Write-Host "`n⏰ Scheduling health check..." -ForegroundColor Yellow
try {
    # Remove existing task if it exists
    Unregister-ScheduledTask -TaskName "TradingCalculatorHealthCheck" -Confirm:$false -ErrorAction SilentlyContinue
    
    # Create new scheduled task
    $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)
    $action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$healthCheckPath`""
    $settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 2)
    
    Register-ScheduledTask -TaskName "TradingCalculatorHealthCheck" -Trigger $trigger -Action $action -Settings $settings -User "SYSTEM" | Out-Null
    Write-Host "✅ Health check scheduled (every 5 minutes)" -ForegroundColor Green
} catch {
    Write-Warning "⚠️ Could not schedule health check: $_"
}

# Step 12: Performance optimization
Write-Host "`n⚡ Applying performance optimizations..." -ForegroundColor Yellow
try {
    # Set high performance power plan
    powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
    Write-Host "✅ High performance power plan activated" -ForegroundColor Green
} catch {
    Write-Warning "⚠️ Could not set power plan: $_"
}

# Step 13: Test installation
Write-Host "`n🧪 Testing installation..." -ForegroundColor Yellow
try {
    python --version
    git --version
    python -c "import flask; print('✅ Flask:', flask.__version__)"
    python -c "import MetaTrader5; print('✅ MT5 API available')" 2>$null || Write-Host "⚠️ MT5 API not available (will use mock mode)" -ForegroundColor Yellow
    Write-Host "✅ All dependencies verified" -ForegroundColor Green
} catch {
    Write-Warning "⚠️ Some dependencies may not be properly installed: $_"
}

# Final summary
Write-Host "`n🎉 Setup Complete!" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green
Write-Host "📁 Application Directory: $AppDir" -ForegroundColor Cyan
Write-Host "🔧 Windows Service: $ServiceName" -ForegroundColor Cyan
Write-Host "🌐 Server URL: http://localhost:8080" -ForegroundColor Cyan
Write-Host "📝 Logs: Check Windows Event Viewer" -ForegroundColor Cyan

Write-Host "`n📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your MT5 credentials"
Write-Host "2. Install MT5 terminal from your broker"
Write-Host "3. Start the service: Start-Service $ServiceName"
Write-Host "4. Test the application: http://localhost:8080"
Write-Host "5. Configure GitHub Actions for auto-deployment"

Write-Host "`n⚠️  Important Notes:" -ForegroundColor Red
Write-Host "• Update .env file with real MT5 credentials"
Write-Host "• Install MT5 terminal from your broker"
Write-Host "• Configure DigitalOcean firewall for port 8080"
Write-Host "• Test MT5 API connection before trading"

Write-Host "`n🚀 To start the server manually:" -ForegroundColor Cyan
Write-Host "cd $AppDir"
Write-Host "python mt5_server.py"

Write-Host "`n✅ VPS Setup Complete! Happy Trading! 📈" -ForegroundColor Green
