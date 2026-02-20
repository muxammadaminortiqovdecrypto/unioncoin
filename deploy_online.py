#!/usr/bin/env python3
"""
UnionCoin Online Deployment Script
Deploy to production server with full automation
"""

import os
import sys
import subprocess
import requests
import json
from datetime import datetime

class OnlineDeployer:
    def __init__(self):
        self.github_repo = "https://github.com/muxammadaminortiqovdecrypto/unioncoin.git"
        self.server_host = "YOUR_SERVER_IP"  # O'zgartiring
        self.server_user = "root"  # O'zgartiring
        self.server_password = "YOUR_PASSWORD"  # O'zgartiring
        self.domain = "YOUR_DOMAIN.com"  # O'zgartiring
        
    def deploy_to_server(self):
        """Deploy UnionCoin to online server"""
        print("🚀 Starting UnionCoin Online Deployment...")
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Step 1: Update server
            print("📦 Step 1: Updating server packages...")
            self.run_ssh_command("apt update && apt upgrade -y")
            
            # Step 2: Install dependencies
            print("🔧 Step 2: Installing dependencies...")
            self.run_ssh_command("""
                apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git curl certbot python3-certbot-nginx
            """)
            
            # Step 3: Clone from GitHub
            print("📥 Step 3: Cloning from GitHub...")
            self.run_ssh_command("""
                cd /var/www/
                if [ -d "unioncoin" ]; then
                    rm -rf unioncoin
                fi
                git clone https://github.com/muxammadaminortiqovdecrypto/unioncoin.git
            """)
            
            # Step 4: Setup Python environment
            print("🐍 Step 4: Setting up Python environment...")
            self.run_ssh_command("""
                cd /var/www/unioncoin
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt
            """)
            
            # Step 5: Setup PostgreSQL
            print("🗄️ Step 5: Setting up PostgreSQL...")
            self.run_ssh_command("""
                sudo -u postgres psql -c "DROP DATABASE IF EXISTS unioncoin;"
                sudo -u postgres psql -c "CREATE DATABASE unioncoin;"
                sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD '12345';"
                sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE unioncoin TO postgres;"
                sudo -u postgres psql -c "ALTER USER postgres CREATEDB;"
            """)
            
            # Step 6: Setup environment
            print("⚙️ Step 6: Setting up environment...")
            self.run_ssh_command("""
                cd /var/www/unioncoin
                cat > .env << EOF
DATABASE_URL=postgresql://postgres:12345@localhost/unioncoin
BOT_TOKEN=8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A
ADMIN_ID=1685342390
SECRET_KEY=unioncoin_production_secret_key_2026
ADMIN_PASSWORD=unioncoin_admin_2026
HOST=0.0.0.0
PORT=8000
DEBUG=False
ALLOWED_ORIGINS=https://""" + self.domain + """
EOF
            """)
            
            # Step 7: Initialize database
            print("🗄️ Step 7: Initializing database...")
            self.run_ssh_command("""
                cd /var/www/unioncoin
                source venv/bin/activate
                python database.py
            """)
            
            # Step 8: Setup systemd services
            print("⚙️ Step 8: Setting up systemd services...")
            self.run_ssh_command("""
                cat > /etc/systemd/system/unioncoin-web.service << EOF
[Unit]
Description=UnionCoin Web Server
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/unioncoin
Environment=PATH=/usr/bin:/usr/local/bin
EnvironmentFile=/var/www/unioncoin/.env
ExecStart=/var/www/unioncoin/venv/bin/python /var/www/unioncoin/api.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

                cat > /etc/systemd/system/unioncoin-bot.service << EOF
[Unit]
Description=UnionCoin Telegram Bot
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/unioncoin
Environment=PATH=/usr/bin:/usr/local/bin
EnvironmentFile=/var/www/unioncoin/.env
ExecStart=/var/www/unioncoin/venv/bin/python /var/www/unioncoin/bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
            """)
            
            # Step 9: Setup Nginx
            print("🌐 Step 9: Setting up Nginx...")
            self.run_ssh_command(f"""
                cat > /etc/nginx/sites-available/unioncoin << EOF
server {{
    listen 80;
    server_name {self.domain};
    return 301 https://$server_name$request_uri;
}}

server {{
    listen 443 ssl http2;
    server_name {self.domain};
    
    ssl_certificate /etc/letsencrypt/live/{self.domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{self.domain}/privkey.pem;
    
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

                ln -sf /etc/nginx/sites-available/unioncoin /etc/nginx/sites-enabled/
                nginx -t
                systemctl reload nginx
            """)
            
            # Step 10: Setup SSL
            print("🔒 Step 10: Setting up SSL...")
            self.run_ssh_command(f"""
                certbot --nginx -d {self.domain} --non-interactive --agree-tos --email admin@{self.domain}
            """)
            
            # Step 11: Start services
            print("🚀 Step 11: Starting services...")
            self.run_ssh_command("""
                systemctl daemon-reload
                systemctl enable unioncoin-web unioncoin-bot
                systemctl restart unioncoin-web unioncoin-bot
                systemctl restart postgresql
                systemctl restart nginx
            """)
            
            # Step 12: Setup firewall
            print("🔥 Step 12: Setting up firewall...")
            self.run_ssh_command("""
                ufw allow 22
                ufw allow 80
                ufw allow 443
                ufw --force enable
            """)
            
            # Step 13: Setup monitoring
            print("📊 Step 13: Setting up monitoring...")
            self.run_ssh_command("""
                mkdir -p /var/log/unioncoin
                mkdir -p /var/www/unioncoin/backups
                
                # Create backup script
                cat > /var/www/unioncoin/backup.sh << 'EOF'
#!/bin/bash
cd /var/www/unioncoin
python -c "
import sqlite3
import pandas as pd
from datetime import datetime
import os

# Create backup
conn = sqlite3.connect('unioncoin.db')
users_df = pd.read_sql_query('SELECT * FROM users', conn)
transactions_df = pd.read_sql_query('SELECT t.*, s.username as sender_name, r.username as receiver_name FROM transactions t LEFT JOIN users s ON t.sender_id = s.id LEFT JOIN users r ON t.receiver_id = r.id ORDER BY t.id DESC', conn)

backup_dir = f'backups/{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}'
os.makedirs(backup_dir, exist_ok=True)

users_df.to_excel(f'{backup_dir}/users.xlsx', index=False)
transactions_df.to_excel(f'{backup_dir}/transactions.xlsx', index=False)
conn.close()
print(f'Backup created: {backup_dir}')
"
EOF

                chmod +x /var/www/unioncoin/backup.sh
                
                # Add to crontab
                (crontab -l 2>/dev/null; echo "0 */6 * * * /var/www/unioncoin/backup.sh") | crontab -
            """)
            
            print("\n✅ UnionCoin deployment completed successfully!")
            print(f"🌐 Web Interface: https://{self.domain}")
            print(f"📊 Admin Panel: https://{self.domain}/api/data?admin=unioncoin_admin_2026")
            print(f"🤖 Telegram Bot: @tokenuchunku12bot")
            print(f"📅 Deployed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            return False
    
    def run_ssh_command(self, command):
        """Run SSH command on server"""
        try:
            import paramiko
            
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.server_host, username=self.server_user, password=self.server_password)
            
            stdin, stdout, stderr = ssh.exec_command(command)
            
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            ssh.close()
            
            if error:
                print(f"⚠️ SSH Warning: {error}")
            
            return output
            
        except ImportError:
            print("❌ paramiko not installed. Install with: pip install paramiko")
            return None
        except Exception as e:
            print(f"❌ SSH Error: {e}")
            return None
    
    def test_deployment(self):
        """Test deployment"""
        print("🧪 Testing deployment...")
        
        try:
            # Test web interface
            response = requests.get(f"https://{self.domain}", timeout=10)
            if response.status_code == 200:
                print("✅ Web interface: Working")
            else:
                print(f"❌ Web interface: {response.status_code}")
            
            # Test API
            response = requests.get(f"https://{self.domain}/verify", timeout=10)
            if response.status_code == 200:
                print("✅ API: Working")
            else:
                print(f"❌ API: {response.status_code}")
            
            # Test admin panel
            response = requests.get(f"https://{self.domain}/api/data?admin=unioncoin_admin_2026", timeout=10)
            if response.status_code == 200:
                print("✅ Admin panel: Working")
            else:
                print(f"❌ Admin panel: {response.status_code}")
            
            return True
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False
    
    def get_server_info(self):
        """Get server configuration from user"""
        print("\n🌐 Server Configuration")
        print("=" * 50)
        
        self.server_host = input("👉 Server IP Address: ").strip()
        self.server_user = input("👉 SSH Username (default: root): ").strip() or "root"
        self.server_password = input("👉 SSH Password: ").strip()
        self.domain = input("👉 Domain Name: ").strip()
        
        # Save configuration
        config = {
            'server_host': self.server_host,
            'server_user': self.server_user,
            'domain': self.domain,
            'github_repo': self.github_repo,
            'deployed_at': datetime.now().isoformat()
        }
        
        with open('server_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n✅ Configuration saved to server_config.json")
        return config

def main():
    """Main deployment menu"""
    print("🚀 UnionCoin Online Deployment")
    print("=" * 50)
    
    deployer = OnlineDeployer()
    
    while True:
        print("\n📋 Deployment Options:")
        print("1. 🔧 Configure Server Settings")
        print("2. 🚀 Deploy to Online Server")
        print("3. 🧪 Test Deployment")
        print("4. 📊 Show Server Info")
        print("5. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-5): ").strip()
        
        if choice == "1":
            deployer.get_server_info()
        elif choice == "2":
            if not deployer.server_host:
                print("❌ Please configure server settings first (option 1)")
                continue
            deployer.deploy_to_server()
        elif choice == "3":
            if not deployer.domain:
                print("❌ Please configure server settings first (option 1)")
                continue
            deployer.test_deployment()
        elif choice == "4":
            try:
                with open('server_config.json', 'r') as f:
                    config = json.load(f)
                    print(f"\n📊 Current Server Configuration:")
                    print(f"   Host: {config.get('server_host', 'Not set')}")
                    print(f"   User: {config.get('server_user', 'Not set')}")
                    print(f"   Domain: {config.get('domain', 'Not set')}")
                    print(f"   GitHub: {config.get('github_repo', 'Not set')}")
            except FileNotFoundError:
                print("❌ No server configuration found. Run option 1 first.")
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
