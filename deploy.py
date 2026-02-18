#!/usr/bin/env python3
"""
UnionCoin Production Deployment Script
Deploy to online server with automatic data backup
"""

import os
import sys
import requests
import sqlite3
import pandas as pd
from datetime import datetime
import subprocess
import shutil

class UnionCoinDeployer:
    def __init__(self):
        self.server_url = "YOUR_SERVER_URL"  # O'zgartiring
        self.server_ssh = "YOUR_SSH_SERVER"  # O'zgartiring
        self.server_user = "YOUR_USERNAME"  # O'zgartiring
        self.server_password = "YOUR_PASSWORD"  # O'zgartiring
        self.local_db_path = "unioncoin.db"
        self.backup_dir = "backups"
        
    def create_backup(self):
        """Create Excel backup of database"""
        try:
            print("📊 Creating database backup...")
            
            # Create backup directory
            os.makedirs(self.backup_dir, exist_ok=True)
            
            # Connect to database
            conn = sqlite3.connect(self.local_db_path)
            
            # Export users to Excel
            users_df = pd.read_sql_query("SELECT * FROM users", conn)
            users_file = f"{self.backup_dir}/users_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            users_df.to_excel(users_file, index=False, engine='openpyxl')
            
            # Export transactions to Excel
            transactions_df = pd.read_sql_query("""
                SELECT t.*, 
                       s.username as sender_name,
                       r.username as receiver_name
                FROM transactions t
                LEFT JOIN users s ON t.sender_id = s.id
                LEFT JOIN users r ON t.receiver_id = r.id
                ORDER BY t.id DESC
            """, conn)
            transactions_file = f"{self.backup_dir}/transactions_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            transactions_df.to_excel(transactions_file, index=False, engine='openpyxl')
            
            conn.close()
            
            print(f"✅ Backup created:")
            print(f"   📄 Users: {users_file}")
            print(f"   🔗 Transactions: {transactions_file}")
            
            return users_file, transactions_file
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return None, None
    
    def deploy_to_server(self):
        """Deploy application to online server"""
        try:
            print("🚀 Starting deployment to online server...")
            
            # Create deployment package
            print("📦 Creating deployment package...")
            deployment_files = [
                'api.py', 'bot.py', 'database.py', 'verify.py', 'view_data.py',
                'requirements.txt', 'Dockerfile', 'docker-compose.yml',
                'static/', 'templates/', '.env.example'
            ]
            
            # Create deployment script
            deploy_script = f"""#!/bin/bash
# UnionCoin Deployment Script
echo "🚀 UnionCoin Deployment Started at $(date)"

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx -y

# Create application directory
sudo mkdir -p /var/www/unioncoin
sudo chown $USER:$USER /var/www/unioncoin

# Copy application files
echo "📁 Copying application files..."
cp -r * /var/www/unioncoin/

# Install Python dependencies
cd /var/www/unioncoin
pip3 install -r requirements.txt

# Setup PostgreSQL
echo "🗄️ Setting up database..."
sudo -u postgres psql -c "CREATE DATABASE unioncoin;"
sudo -u postgres psql -c "CREATE USER unioncoin WITH PASSWORD 'secure_password_2026';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE unioncoin TO unioncoin;"

# Setup Nginx
echo "🌐 Setting up Nginx..."
sudo tee /etc/nginx/sites-available/unioncoin > /dev/null <<EOF
server {{
    listen 80;
    server_name YOUR_DOMAIN.com;
    
    location / {{
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
    
    location /static {{
        alias /var/www/unioncoin/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}
}}
EOF

sudo ln -s /etc/nginx/sites-available/unioncoin /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Setup SSL with Let's Encrypt
echo "🔒 Setting up SSL..."
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d YOUR_DOMAIN.com --non-interactive --agree-tos --email admin@YOUR_DOMAIN.com

# Create systemd services
echo "⚙️ Creating systemd services..."

# Web service
sudo tee /etc/systemd/system/unioncoin-web.service > /dev/null <<EOF
[Unit]
Description=UnionCoin Web Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/unioncoin
Environment=DATABASE_URL=postgresql://unioncoin:secure_password_2026@localhost/unioncoin
Environment=BOT_TOKEN=YOUR_BOT_TOKEN
Environment=ADMIN_ID=1685342390
ExecStart=/usr/bin/python3 api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Bot service
sudo tee /etc/systemd/system/unioncoin-bot.service > /dev/null <<EOF
[Unit]
Description=UnionCoin Telegram Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/unioncoin
Environment=DATABASE_URL=postgresql://unioncoin:secure_password_2026@localhost/unioncoin
Environment=BOT_TOKEN=YOUR_BOT_TOKEN
Environment=ADMIN_ID=1685342390
ExecStart=/usr/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable unioncoin-web
sudo systemctl enable unioncoin-bot
sudo systemctl start unioncoin-web
sudo systemctl start unioncoin-bot

# Setup firewall
echo "🔥 Setting up firewall..."
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

echo "✅ Deployment completed at $(date)"
echo "🌐 Web: http://YOUR_DOMAIN.com"
echo "🔒 HTTPS: https://YOUR_DOMAIN.com"
echo "📊 Admin: http://YOUR_DOMAIN.com/api/data?admin=unioncoin_admin_2026"
"""
            
            with open('deploy.sh', 'w') as f:
                f.write(deploy_script)
            
            print("✅ Deployment package created")
            return True
            
        except Exception as e:
            print(f"❌ Deployment preparation failed: {e}")
            return False
    
    def setup_auto_backup(self):
        """Setup automatic backup to admin"""
        try:
            print("🔄 Setting up automatic backup system...")
            
            # Create backup script
            backup_script = f"""#!/usr/bin/env python3
import sqlite3
import pandas as pd
import requests
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_backup_to_admin():
    try:
        # Create backup
        conn = sqlite3.connect('unioncoin.db')
        
        # Users data
        users_df = pd.read_sql_query("SELECT * FROM users", conn)
        users_excel = f"backup_users_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.xlsx"
        users_df.to_excel(users_excel, index=False, engine='openpyxl')
        
        # Transactions data
        transactions_df = pd.read_sql_query("""
            SELECT t.*, s.username as sender_name, r.username as receiver_name
            FROM transactions t
            LEFT JOIN users s ON t.sender_id = s.id
            LEFT JOIN users r ON t.receiver_id = r.id
            ORDER BY t.id DESC
        """, conn)
        transactions_excel = f"backup_transactions_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.xlsx"
        transactions_df.to_excel(transactions_excel, index=False, engine='openpyxl')
        
        conn.close()
        
        # Send to admin (you can implement email/telegram sending)
        print(f"📊 Backup created: {{users_excel}}, {{transactions_excel}}")
        
        # Optional: Send via Telegram bot to admin
        # You can implement this part
        
    except Exception as e:
        print(f"Backup error: {{e}}")

if __name__ == "__main__":
    send_backup_to_admin()
"""
            
            with open('auto_backup.py', 'w') as f:
                f.write(backup_script)
            
            # Create cron job
            cron_job = "0 */6 * * * * /usr/bin/python3 /var/www/unioncoin/auto_backup.py\n"
            
            print("✅ Auto backup system configured")
            print(f"📅 Backup schedule: Every 6 hours")
            
            return True
            
        except Exception as e:
            print(f"❌ Auto backup setup failed: {e}")
            return False
    
    def run_computer_as_server(self):
        """Setup current computer as server"""
        try:
            print("🖥️ Setting up current computer as server...")
            
            # Create server startup script
            server_script = f"""#!/usr/bin/env python3
import subprocess
import time
import os
from datetime import datetime

def start_services():
    print("🚀 Starting UnionCoin services...")
    
    # Start web server
    web_process = subprocess.Popen(['python', 'api.py'], 
                                  cwd=os.getcwd(),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    
    # Start bot
    bot_process = subprocess.Popen(['python', 'bot.py'], 
                                  cwd=os.getcwd(),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    
    print(f"✅ Services started at {{datetime.now()}}")
    print(f"🌐 Web: http://localhost:8000")
    print(f"📊 Admin: http://localhost:8000/api/data?admin=unioncoin_admin_2026")
    
    return web_process, bot_process

def monitor_services(web_process, bot_process):
    print("👀 Monitoring services...")
    
    while True:
        # Check if processes are running
        if web_process.poll() is not None:
            print("🔄 Web server stopped, restarting...")
            web_process = subprocess.Popen(['python', 'api.py'], 
                                          cwd=os.getcwd())
        
        if bot_process.poll() is not None:
            print("🔄 Bot stopped, restarting...")
            bot_process = subprocess.Popen(['python', 'bot.py'], 
                                          cwd=os.getcwd())
        
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    web_proc, bot_proc = start_services()
    try:
        monitor_services(web_proc, bot_proc)
    except KeyboardInterrupt:
        print("🛑 Services stopped by user")
"""
            
            with open('server_mode.py', 'w') as f:
                f.write(server_script)
            
            print("✅ Server mode script created")
            print("📝 Run: python server_mode.py")
            
            return True
            
        except Exception as e:
            print(f"❌ Server setup failed: {e}")
            return False
    
    def create_production_config(self):
        """Create production configuration"""
        try:
            print("⚙️ Creating production configuration...")
            
            config = f"""# UnionCoin Production Configuration
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Database Configuration
DATABASE_URL=postgresql://unioncoin:secure_password_2026@localhost/unioncoin

# Telegram Bot Configuration
BOT_TOKEN=8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A
ADMIN_ID=1685342390

# Security Configuration
SECRET_KEY=unioncoin_production_secret_key_2026
ADMIN_PASSWORD=unioncoin_admin_2026

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Domain Configuration
DOMAIN=YOUR_DOMAIN.com
SSL_EMAIL=admin@YOUR_DOMAIN.com

# Backup Configuration
BACKUP_ENABLED=True
BACKUP_INTERVAL=6  # hours
BACKUP_EMAIL=admin@YOUR_DOMAIN.com

# Monitoring Configuration
MONITORING_ENABLED=True
LOG_LEVEL=INFO
LOG_FILE=/var/log/unioncoin/unioncoin.log

# Performance Configuration
MAX_WORKERS=4
WORKER_CONNECTIONS=1000
KEEPALIVE_TIMEOUT=65

# Security Configuration
CORS_ORIGINS=https://YOUR_DOMAIN.com,https://www.YOUR_DOMAIN.com
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60  # seconds
"""
            
            with open('.env.production', 'w') as f:
                f.write(config)
            
            print("✅ Production configuration created")
            print("📝 File: .env.production")
            
            return True
            
        except Exception as e:
            print(f"❌ Config creation failed: {e}")
            return False

def main():
    """Main deployment menu"""
    print("🚀 UnionCoin Production Deployment")
    print("=" * 50)
    
    deployer = UnionCoinDeployer()
    
    while True:
        print("\n📋 Deployment Options:")
        print("1. 📊 Create Excel Backup")
        print("2. 🖥️ Setup Computer as Server")
        print("3. 🌐 Deploy to Online Server")
        print("4. ⚙️ Create Production Config")
        print("5. 🔄 Setup Auto Backup")
        print("6. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-6): ").strip()
        
        if choice == "1":
            users_file, transactions_file = deployer.create_backup()
            if users_file:
                print(f"📁 Backup files saved in {deployer.backup_dir}/")
        
        elif choice == "2":
            deployer.run_computer_as_server()
        
        elif choice == "3":
            deployer.deploy_to_server()
        
        elif choice == "4":
            deployer.create_production_config()
        
        elif choice == "5":
            deployer.setup_auto_backup()
        
        elif choice == "6":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
