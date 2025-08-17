"""
VPS Health Monitor for MT5 Trading Server
Monitors server health and automatically restarts if needed
"""

import requests
import time
import logging
import subprocess
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('health_monitor.log'),
        logging.StreamHandler()
    ]
)

class VPSHealthMonitor:
    def __init__(self):
        self.server_url = "http://localhost:8080"
        self.check_interval = 60  # seconds
        self.max_failures = 3
        self.consecutive_failures = 0
        self.last_alert_time = 0
        self.alert_cooldown = 3600  # 1 hour
        
    def check_server_health(self):
        """Check if server is responding"""
        try:
            response = requests.get(f"{self.server_url}/status", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check MT5 connection
                if data.get('mt5_connected', False):
                    logging.info("✅ Server and MT5 both healthy")
                    self.consecutive_failures = 0
                    return True
                else:
                    logging.warning("⚠️  Server OK but MT5 disconnected")
                    self.consecutive_failures += 1
                    return False
            else:
                logging.error(f"❌ Server returned status code: {response.status_code}")
                self.consecutive_failures += 1
                return False
                
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Connection failed: {e}")
            self.consecutive_failures += 1
            return False
    
    def restart_server(self):
        """Restart the MT5 server"""
        try:
            logging.info("🔄 Attempting to restart server...")
            
            # Kill existing Python processes
            subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                          capture_output=True, text=True)
            
            time.sleep(5)
            
            # Start server again
            server_path = os.path.join(os.getcwd(), 'start_vps_server.bat')
            subprocess.Popen([server_path], shell=True)
            
            logging.info("🚀 Server restart initiated")
            time.sleep(30)  # Give server time to start
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to restart server: {e}")
            return False
    
    def send_alert(self, message):
        """Send alert notification"""
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_alert_time < self.alert_cooldown:
            return
        
        try:
            # Log alert
            logging.critical(f"🚨 ALERT: {message}")
            
            # Send email if configured
            self.send_email_alert(message)
            
            # Send Telegram if configured
            self.send_telegram_alert(message)
            
            self.last_alert_time = current_time
            
        except Exception as e:
            logging.error(f"Failed to send alert: {e}")
    
    def send_email_alert(self, message):
        """Send email alert"""
        try:
            # Configure with your email settings
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            email_user = "your_email@gmail.com"  # Replace with your email
            email_password = "your_app_password"  # Replace with your app password
            alert_email = "your_alert_email@gmail.com"  # Replace with alert email
            
            if email_user == "your_email@gmail.com":
                return  # Skip if not configured
            
            msg = MIMEText(f"""
MT5 Trading Server Alert

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Message: {message}

Server URL: {self.server_url}
Consecutive Failures: {self.consecutive_failures}

Please check your VPS and MT5 setup.
            """)
            
            msg['Subject'] = f"🚨 MT5 Server Alert: {message}"
            msg['From'] = email_user
            msg['To'] = alert_email
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_user, email_password)
                server.send_message(msg)
                
            logging.info("📧 Email alert sent successfully")
            
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
    
    def send_telegram_alert(self, message):
        """Send Telegram alert"""
        try:
            bot_token = "your_bot_token"  # Replace with your bot token
            chat_id = "your_chat_id"     # Replace with your chat ID
            
            if bot_token == "your_bot_token":
                return  # Skip if not configured
            
            telegram_message = f"""
🚨 *MT5 Server Alert*

📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
❌ Issue: {message}
🔢 Failures: {self.consecutive_failures}

Please check your VPS server.
            """
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': telegram_message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                logging.info("📱 Telegram alert sent successfully")
            else:
                logging.error(f"Telegram alert failed: {response.status_code}")
                
        except Exception as e:
            logging.error(f"Failed to send Telegram alert: {e}")
    
    def run(self):
        """Main monitoring loop"""
        logging.info("🔍 Starting VPS Health Monitor")
        logging.info(f"Monitoring: {self.server_url}")
        logging.info(f"Check interval: {self.check_interval} seconds")
        
        while True:
            try:
                is_healthy = self.check_server_health()
                
                if not is_healthy:
                    if self.consecutive_failures >= self.max_failures:
                        # Send alert
                        alert_msg = f"Server unhealthy for {self.consecutive_failures} consecutive checks"
                        self.send_alert(alert_msg)
                        
                        # Try to restart
                        if self.restart_server():
                            self.consecutive_failures = 0
                            self.send_alert("Server restarted successfully")
                        else:
                            self.send_alert("Failed to restart server - manual intervention required")
                
                # Sleep until next check
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logging.info("🛑 Monitor stopped by user")
                break
            except Exception as e:
                logging.error(f"Monitor error: {e}")
                time.sleep(self.check_interval)

if __name__ == "__main__":
    monitor = VPSHealthMonitor()
    monitor.run()
