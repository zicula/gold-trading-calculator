#!/bin/bash
# 🐳 DigitalOcean VPS Docker Deployment Script
# Gold Trading Calculator - One-click deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="gold-trading-calculator"
DOMAIN=${DOMAIN:-"yourdomain.com"}
EMAIL=${EMAIL:-"admin@yourdomain.com"}
BACKUP_ENABLED=${BACKUP_ENABLED:-"true"}

echo -e "${BLUE}🐳 Gold Trading Calculator - DigitalOcean Docker Deployment${NC}"
echo "========================================================"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}❌ This script should not be run as root${NC}"
   exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Docker if not exists
install_docker() {
    echo -e "${YELLOW}📦 Installing Docker...${NC}"
    
    # Update package index
    sudo apt-get update
    
    # Install required packages
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Set up stable repository
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker Engine
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    
    echo -e "${GREEN}✅ Docker installed successfully${NC}"
}

# Install Docker Compose if not exists
install_docker_compose() {
    echo -e "${YELLOW}📦 Installing Docker Compose...${NC}"
    
    # Download Docker Compose
    DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
    sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    
    # Make it executable
    sudo chmod +x /usr/local/bin/docker-compose
    
    echo -e "${GREEN}✅ Docker Compose installed successfully${NC}"
}

# Setup firewall
setup_firewall() {
    echo -e "${YELLOW}🔥 Configuring firewall...${NC}"
    
    # Install ufw if not exists
    sudo apt-get install -y ufw
    
    # Configure firewall rules
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    sudo ufw allow ssh
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    
    # Enable firewall
    sudo ufw --force enable
    
    echo -e "${GREEN}✅ Firewall configured${NC}"
}

# Generate SSL certificates using Let's Encrypt
setup_ssl() {
    echo -e "${YELLOW}🔒 Setting up SSL certificates...${NC}"
    
    # Install certbot
    sudo apt-get install -y certbot
    
    # Generate certificates
    sudo certbot certonly --standalone \
        --email $EMAIL \
        --agree-tos \
        --no-eff-email \
        -d $DOMAIN
    
    # Copy certificates to nginx directory
    sudo mkdir -p ./deploy/docker/nginx/ssl
    sudo cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem ./deploy/docker/nginx/ssl/cert.pem
    sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem ./deploy/docker/nginx/ssl/key.pem
    sudo chown $USER:$USER ./deploy/docker/nginx/ssl/*
    
    echo -e "${GREEN}✅ SSL certificates configured${NC}"
}

# Create environment file
create_env_file() {
    echo -e "${YELLOW}⚙️ Creating environment configuration...${NC}"
    
    # Generate secure keys
    SECRET_KEY=$(openssl rand -hex 32)
    JWT_SECRET_KEY=$(openssl rand -hex 32)
    ENCRYPTION_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
    REDIS_PASSWORD=$(openssl rand -hex 16)
    
    cat > .env << EOF
# Gold Trading Calculator Environment Configuration
# Generated on $(date)

# Security Keys
SECRET_KEY=${SECRET_KEY}
JWT_SECRET_KEY=${JWT_SECRET_KEY}
ENCRYPTION_KEY=${ENCRYPTION_KEY}
REDIS_PASSWORD=${REDIS_PASSWORD}

# Application Settings
FLASK_ENV=production
CORS_ORIGINS=https://${DOMAIN}
DATABASE_PATH=/app/data/trading_accounts.db

# Backup Settings
BACKUP_INTERVAL=3600

# Domain Configuration
DOMAIN=${DOMAIN}
EMAIL=${EMAIL}
EOF

    echo -e "${GREEN}✅ Environment file created${NC}"
}

# Deploy application
deploy_app() {
    echo -e "${YELLOW}🚀 Deploying application...${NC}"
    
    # Stop existing containers if any
    docker-compose -f deploy/docker/docker-compose.yml down 2>/dev/null || true
    
    # Build and start services
    docker-compose -f deploy/docker/docker-compose.yml up -d --build
    
    # Wait for services to be ready
    echo -e "${YELLOW}⏳ Waiting for services to start...${NC}"
    sleep 30
    
    # Check if services are running
    if docker-compose -f deploy/docker/docker-compose.yml ps | grep -q "Up"; then
        echo -e "${GREEN}✅ Application deployed successfully${NC}"
    else
        echo -e "${RED}❌ Deployment failed${NC}"
        docker-compose -f deploy/docker/docker-compose.yml logs
        exit 1
    fi
}

# Setup monitoring
setup_monitoring() {
    echo -e "${YELLOW}📊 Setting up monitoring...${NC}"
    
    # Create monitoring script
    cat > monitor.sh << 'EOF'
#!/bin/bash
# Simple monitoring script

while true; do
    echo "$(date): Checking application health..."
    
    # Check if containers are running
    if ! docker-compose -f deploy/docker/docker-compose.yml ps | grep -q "Up"; then
        echo "$(date): Some containers are down, restarting..."
        docker-compose -f deploy/docker/docker-compose.yml up -d
    fi
    
    # Check application endpoint
    if ! curl -f http://localhost:8080/api/status >/dev/null 2>&1; then
        echo "$(date): Application not responding, restarting..."
        docker-compose -f deploy/docker/docker-compose.yml restart gold-trading-app
    fi
    
    sleep 300  # Check every 5 minutes
done
EOF
    
    chmod +x monitor.sh
    
    # Create systemd service for monitoring
    sudo tee /etc/systemd/system/gold-trading-monitor.service > /dev/null << EOF
[Unit]
Description=Gold Trading Calculator Monitor
After=docker.service
Requires=docker.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/monitor.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    # Enable and start monitoring service
    sudo systemctl daemon-reload
    sudo systemctl enable gold-trading-monitor.service
    sudo systemctl start gold-trading-monitor.service
    
    echo -e "${GREEN}✅ Monitoring configured${NC}"
}

# Main deployment process
main() {
    echo -e "${BLUE}Starting deployment process...${NC}\n"
    
    # Check and install Docker
    if ! command_exists docker; then
        install_docker
        echo -e "${YELLOW}⚠️ Please log out and log back in to apply Docker group changes${NC}"
        echo -e "${YELLOW}Then run this script again${NC}"
        exit 0
    fi
    
    # Check and install Docker Compose
    if ! command_exists docker-compose; then
        install_docker_compose
    fi
    
    # Setup firewall
    setup_firewall
    
    # Create environment file
    create_env_file
    
    # Setup SSL (optional, comment out if not using domain)
    # setup_ssl
    
    # Deploy application
    deploy_app
    
    # Setup monitoring
    setup_monitoring
    
    echo -e "\n${GREEN}🎉 Deployment completed successfully!${NC}"
    echo -e "${BLUE}📋 Post-deployment information:${NC}"
    echo -e "   • Application URL: http://localhost (or https://$DOMAIN if SSL configured)"
    echo -e "   • API Status: http://localhost/api/status"
    echo -e "   • Container Status: docker-compose -f deploy/docker/docker-compose.yml ps"
    echo -e "   • Logs: docker-compose -f deploy/docker/docker-compose.yml logs -f"
    echo -e "   • Stop: docker-compose -f deploy/docker/docker-compose.yml down"
    echo -e "\n${YELLOW}📝 Next steps:${NC}"
    echo -e "   1. Configure your domain DNS to point to this server"
    echo -e "   2. Run SSL setup if using custom domain"
    echo -e "   3. Create admin user account"
    echo -e "   4. Test the application functionality"
}

# Run main function
main "$@"
