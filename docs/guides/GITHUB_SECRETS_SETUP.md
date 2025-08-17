# 🔐 GitHub Secrets Configuration Guide

## Required Secrets for DigitalOcean + GitHub Actions Integration

### 📋 GitHub Repository Secrets Setup

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add the following secrets:

### 🌊 DigitalOcean VPS Connection Secrets

#### `VPS_HOST`
```
Value: your.vps.ip.address
Example: 134.122.123.45
Description: The public IP address of your DigitalOcean VPS
```

#### `VPS_USERNAME`
```
Value: Administrator
Description: Windows VPS administrator username
```

#### `VPS_PASSWORD` (Alternative to SSH Key)
```
Value: your_strong_password_here
Description: Windows VPS administrator password
```

#### `VPS_SSH_PRIVATE_KEY` (Recommended over password)
```
Value: -----BEGIN OPENSSH PRIVATE KEY-----
       b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAAB...
       -----END OPENSSH PRIVATE KEY-----
Description: Your SSH private key for secure connection
```

#### `VPS_PORT`
```
Value: 22
Description: SSH port (usually 22)
```

---

## 🔑 How to Generate SSH Key Pair

### On your Mac/Local Machine:

```bash
# Generate new SSH key pair
ssh-keygen -t rsa -b 4096 -C "github-actions@yourdomain.com"

# Save as (when prompted):
~/.ssh/digitalocean_deploy_rsa

# Get the private key (for GitHub secret)
cat ~/.ssh/digitalocean_deploy_rsa

# Get the public key (for VPS)
cat ~/.ssh/digitalocean_deploy_rsa.pub
```

### On DigitalOcean VPS:

1. **RDP to your VPS**
2. **Open PowerShell as Administrator**
3. **Add your public key:**

```powershell
# Create .ssh directory
mkdir C:\Users\Administrator\.ssh

# Add your public key to authorized_keys
# Paste the content of digitalocean_deploy_rsa.pub
notepad C:\Users\Administrator\.ssh\authorized_keys

# Set correct permissions
icacls C:\Users\Administrator\.ssh /inheritance:r
icacls C:\Users\Administrator\.ssh /grant:r "Administrator:(OI)(CI)F"
icacls C:\Users\Administrator\.ssh\authorized_keys /inheritance:r
icacls C:\Users\Administrator\.ssh\authorized_keys /grant:r "Administrator:F"
```

---

## 🛠️ Alternative Setup (Password-based)

If you prefer password authentication (less secure):

### Required Secrets:
```yaml
VPS_HOST: your.vps.ip.address
VPS_USERNAME: Administrator  
VPS_PASSWORD: your_vps_password
VPS_PORT: 22
```

### Enable Password Authentication on VPS:
```powershell
# Install OpenSSH Server (if not already installed)
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Start SSH service
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

# Allow password authentication
$sshConfig = "C:\ProgramData\ssh\sshd_config"
(Get-Content $sshConfig) -replace '#PasswordAuthentication yes', 'PasswordAuthentication yes' | Set-Content $sshConfig

# Restart SSH service
Restart-Service sshd
```

---

## 🔧 GitHub Actions Workflow Secrets

### Environment Variables (Optional):
```yaml
FLASK_ENV: production
FLASK_PORT: 8080
SECRET_KEY: your-super-secret-key-here
```

### MT5 Configuration (Optional - can be set on VPS):
```yaml
MT5_LOGIN: your_mt5_login
MT5_PASSWORD: your_mt5_password  
MT5_SERVER: your_broker_server
```

---

## 📝 Complete Secrets Checklist

### ✅ Required for GitHub Actions:
- [ ] `VPS_HOST` - DigitalOcean VPS IP address
- [ ] `VPS_USERNAME` - Usually "Administrator"
- [ ] `VPS_SSH_PRIVATE_KEY` - SSH private key (recommended)
- [ ] `VPS_PORT` - SSH port (usually 22)

### ⚡ Optional for Enhanced Security:
- [ ] `VPS_PASSWORD` - VPS password (alternative to SSH key)
- [ ] `FLASK_SECRET_KEY` - Flask application secret
- [ ] `MT5_LOGIN` - MT5 account login
- [ ] `MT5_PASSWORD` - MT5 account password
- [ ] `MT5_SERVER` - Broker server name

---

## 🧪 Test Your Setup

### 1. Test SSH Connection Locally:
```bash
# Test SSH connection
ssh -i ~/.ssh/digitalocean_deploy_rsa Administrator@your.vps.ip.address

# If successful, you should get Windows command prompt
```

### 2. Test GitHub Actions:
```bash
# Push any change to trigger workflow
git add .
git commit -m "Test deployment"
git push origin main

# Check Actions tab in GitHub repository
```

### 3. Verify Application:
```bash
# After successful deployment, test the application
curl http://your.vps.ip.address:8080/status
```

---

## 🔍 Troubleshooting

### SSH Connection Issues:
```powershell
# On VPS, check SSH service status
Get-Service sshd

# Check SSH configuration
Get-Content C:\ProgramData\ssh\sshd_config | Select-String -Pattern "PasswordAuthentication|PubkeyAuthentication"

# Check firewall
Get-NetFirewallRule -DisplayName "*ssh*"
```

### GitHub Actions Failures:
```yaml
# Common issues:
1. Wrong VPS_HOST (IP address)
2. SSH key not properly formatted
3. SSH service not running on VPS
4. Firewall blocking SSH (port 22)
5. Wrong username (should be "Administrator")
```

### Application Issues:
```powershell
# On VPS, check service status
Get-Service "GoldTradingCalculator"

# Check if port 8080 is open
netstat -an | findstr :8080

# Check application logs
Get-EventLog -LogName Application -Source "Python"
```

---

## 🔒 Security Best Practices

### SSH Key Security:
```bash
# Use strong SSH keys
ssh-keygen -t ed25519 -C "github-actions@yourdomain.com"

# Restrict SSH access to specific IPs (on VPS)
# Add to C:\ProgramData\ssh\sshd_config:
# AllowUsers Administrator@github.actions.ip.range
```

### VPS Security:
```powershell
# Change default passwords
# Enable Windows Firewall
# Regular Windows Updates
# Limit RDP access to your IP only
```

### Application Security:
```yaml
# Use environment variables for secrets
# Enable HTTPS in production
# Implement API authentication
# Regular backup of trading data
```

---

## 🎯 Quick Setup Commands

### Copy-paste setup for GitHub Secrets:

1. **Generate SSH Key:**
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/digitalocean_deploy
```

2. **Copy Private Key (for GitHub Secret):**
```bash
cat ~/.ssh/digitalocean_deploy
```

3. **Copy Public Key (for VPS):**
```bash
cat ~/.ssh/digitalocean_deploy.pub
```

4. **Add to GitHub Secrets:**
   - Go to repository → Settings → Secrets → Actions
   - Add each secret with exact names above

5. **Configure VPS:**
   - RDP to VPS
   - Add public key to authorized_keys
   - Test SSH connection

---

## ✅ Verification Checklist

After setup, verify:

- [ ] SSH connection works from local machine
- [ ] GitHub Actions workflow runs successfully
- [ ] Application is accessible at http://VPS_IP:8080
- [ ] MT5 service is running
- [ ] Health checks pass
- [ ] Logs show no errors

---

## 📞 Need Help?

Common resources:
- **DigitalOcean SSH Guide**: https://docs.digitalocean.com/products/droplets/how-to/connect-with-ssh/
- **GitHub Actions Docs**: https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **Windows SSH Setup**: https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse

**Estimated Setup Time**: 30-45 minutes
**Security Level**: High (with SSH keys)
**Maintenance**: Automated
