#!/usr/bin/env python3
"""
UnionCoin Server Upload Package
Prepare and upload UnionCoin to online server
"""

import os
import sys
import zipfile
import requests
import json
from datetime import datetime
import subprocess

class UnionCoinUploader:
    def __init__(self):
        self.server_url = "YOUR_SERVER_URL"  # O'zgartiring
        self.server_user = "YOUR_USERNAME"  # O'zgartiring
        self.server_password = "YOUR_PASSWORD"  # O'zgartiring
        self.server_path = "/var/www/unioncoin"  # Serverdagi path
        self.package_name = f"unioncoin_deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
    def create_deployment_package(self):
        """Create deployment package"""
        print("📦 Creating deployment package...")
        
        # Files to include in deployment
        files_to_include = [
            'api.py', 'bot.py', 'database.py', 'verify.py', 'view_data.py',
            'server_mode.py', 'requirements.txt', 'Dockerfile', 'docker-compose.yml',
            '.env.example', 'static/', 'templates/'
        ]
        
        # Create ZIP package
        with zipfile.ZipFile(self.package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files_to_include:
                if os.path.exists(file_path):
                    if os.path.isdir(file_path):
                        for root, dirs, files in os.walk(file_path):
                            for file in files:
                                file_full_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_full_path, os.path.dirname(file_path))
                                zipf.write(file_full_path, arcname)
                    else:
                        zipf.write(file_path, os.path.basename(file_path))
                        print(f"   📄 Added: {file_path}")
                else:
                    print(f"   ⚠️  Missing: {file_path}")
        
        print(f"✅ Package created: {self.package_name}")
        print(f"📊 Package size: {os.path.getsize(self.package_name) / 1024 / 1024:.2f} MB")
        
        return self.package_name
    
    def upload_to_server(self):
        """Upload package to server via FTP/SSH"""
        print(f"🚀 Uploading to server: {self.server_url}")
        
        try:
            # Method 1: Using requests (if server has HTTP upload endpoint)
            upload_url = f"{self.server_url}/upload"
            
            with open(self.package_name, 'rb') as f:
                files = {'file': (self.package_name, f, 'application/zip')}
                data = {
                    'deploy_key': 'unioncoin_deploy_2026',
                    'timestamp': datetime.now().isoformat()
                }
                
                response = requests.post(upload_url, files=files, data=data, timeout=300)
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Upload successful!")
                    print(f"   📁 Server path: {result.get('path', 'Unknown')}")
                    print(f"   🔗 Access URL: {result.get('url', 'Unknown')}")
                    return True
                else:
                    print(f"❌ Upload failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return False
    
    def deploy_via_ssh(self):
        """Deploy via SSH commands"""
        print("🔐 Deploying via SSH...")
        
        ssh_commands = f"""
# UnionCoin SSH Deployment Script
echo "🚀 Starting UnionCoin deployment at $(date)"

# Create backup of current version
if [ -d "{self.server_path}" ]; then
    echo "📊 Creating backup of current version..."
    cd {self.server_path}
    tar -czf ../unioncoin_backup_$(date +%Y%m%d_%H%M%S).tar.gz .
    echo "✅ Backup created"
fi

# Extract new version
echo "📦 Extracting new version..."
cd /var/www/
mkdir -p {self.server_path}
tar -xzf /tmp/{self.package_name} -C {self.server_path}
echo "✅ Extraction complete"

# Install dependencies
echo "📦 Installing Python dependencies..."
cd {self.server_path}
pip3 install -r requirements.txt
echo "✅ Dependencies installed"

# Setup database
echo "🗄️ Setting up database..."
sudo -u postgres psql -c "DROP DATABASE IF EXISTS unioncoin;"
sudo -u postgres psql -c "CREATE DATABASE unioncoin;"
sudo -u postgres psql -c "CREATE USER unioncoin WITH PASSWORD 'secure_password_2026';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE unioncoin TO unioncoin;"
echo "✅ Database setup complete"

# Setup environment
echo "⚙️ Setting up environment..."
cp .env.example .env
sed -i 's/YOUR_BOT_TOKEN/8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A/g' .env
sed -i 's/YOUR_ADMIN_ID/1685342390/g' .env
sed -i 's|sqlite:///./unioncoin.db|postgresql://unioncoin:secure_password_2026@localhost/unioncoin|g' .env
echo "✅ Environment configured"

# Setup systemd services
echo "⚙️ Creating systemd services..."
sudo tee /etc/systemd/system/unioncoin-web.service > /dev/null <<EOF
[Unit]
Description=UnionCoin Web Server
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory={self.server_path}
Environment=PATH=/usr/bin:/usr/local/bin
EnvironmentFile={self.server_path}/.env
ExecStart=/usr/bin/python3 {self.server_path}/api.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/unioncoin-bot.service > /dev/null <<EOF
[Unit]
Description=UnionCoin Telegram Bot
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory={self.server_path}
Environment=PATH=/usr/bin:/usr/local/bin
EnvironmentFile={self.server_path}/.env
ExecStart=/usr/bin/python3 {self.server_path}/bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Enable and start services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable unioncoin-web unioncoin-bot
sudo systemctl restart unioncoin-web unioncoin-bot

# Setup Nginx
echo "🌐 Setting up Nginx..."
sudo tee /etc/nginx/sites-available/unioncoin > /dev/null <<EOF
server {{
    listen 80;
    server_name YOUR_DOMAIN.com;
    return 301 https://$server_name$request_uri;
}}

server {{
    listen 443 ssl http2;
    server_name YOUR_DOMAIN.com;
    
    ssl_certificate /etc/letsencrypt/live/YOUR_DOMAIN.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/YOUR_DOMAIN.com/privkey.pem;
    
    location / {{
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
    }}
    
    location /static {{
        alias {self.server_path}/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}
}}
EOF

sudo ln -sf /etc/nginx/sites-available/unioncoin /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Setup SSL
echo "🔒 Setting up SSL..."
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d YOUR_DOMAIN.com --non-interactive --agree-tos --email admin@YOUR_DOMAIN.com

# Setup firewall
echo "🔥 Setting up firewall..."
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

echo "✅ Deployment completed at $(date)"
echo "🌐 HTTP: http://YOUR_DOMAIN.com"
echo "🔒 HTTPS: https://YOUR_DOMAIN.com"
echo "📊 Admin: https://YOUR_DOMAIN.com/api/data?admin=unioncoin_admin_2026"
echo "🤖 Bot: @tokenuchunku12bot"
"""
        
        try:
            # Use paramiko for SSH (install with: pip install paramiko)
            import paramiko
            
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.server_url, username=self.server_user, password=self.server_password)
            
            # Upload package
            sftp = ssh.open_sftp()
            sftp.put(self.package_name, f'/tmp/{self.package_name}')
            
            # Execute deployment commands
            stdin, stdout, stderr = ssh.exec_command(ssh_commands)
            
            print("📋 SSH Output:")
            print(stdout.read().decode())
            
            if stderr:
                print("❌ SSH Errors:")
                print(stderr.read().decode())
            
            ssh.close()
            print("✅ SSH deployment completed!")
            return True
            
        except ImportError:
            print("⚠️ paramiko not installed. Install with: pip install paramiko")
            return False
        except Exception as e:
            print(f"❌ SSH deployment failed: {e}")
            return False
    
    def create_server_config(self):
        """Create server configuration files"""
        print("⚙️ Creating server configuration files...")
        
        # Nginx config
        nginx_config = f"""
# UnionCoin Nginx Configuration
server {{
    listen 80;
    server_name YOUR_DOMAIN.com;
    return 301 https://$server_name$request_uri;
}}

server {{
    listen 443 ssl http2;
    server_name YOUR_DOMAIN.com;
    
    ssl_certificate /etc/letsencrypt/live/YOUR_DOMAIN.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/YOUR_DOMAIN.com/privkey.pem;
    
    location / {{
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
    
    location /static {{
        alias {self.server_path}/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}
}}
"""
        
        with open('nginx.conf', 'w') as f:
            f.write(nginx_config)
        
        # Systemd service files
        web_service = """[Unit]
Description=UnionCoin Web Server
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/unioncoin
Environment=PATH=/usr/bin:/usr/local/bin
EnvironmentFile=/var/www/unioncoin/.env
ExecStart=/usr/bin/python3 /var/www/unioncoin/api.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target"""
        
        bot_service = """[Unit]
Description=UnionCoin Telegram Bot
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/unioncoin
Environment=PATH=/usr/bin:/usr/local/bin
EnvironmentFile=/var/www/unioncoin/.env
ExecStart=/usr/bin/python3 /var/www/unioncoin/bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target"""
        
        with open('unioncoin-web.service', 'w') as f:
            f.write(web_service)
        
        with open('unioncoin-bot.service', 'w') as f:
            f.write(bot_service)
        
        print("✅ Server configuration files created:")
        print("   📄 nginx.conf")
        print("   ⚙️ unioncoin-web.service")
        print("   🤖 unioncoin-bot.service")
        
        return True
    
    def get_server_info(self):
        """Get server information from user"""
        print("\n🌐 Server Configuration")
        print("=" * 40)
        
        server_url = input("👉 Server URL/IP: ").strip()
        server_user = input("👉 SSH Username: ").strip()
        server_password = input("👉 SSH Password: ").strip()
        domain = input("👉 Domain Name: ").strip()
        email = input("👉 Email (for SSL): ").strip()
        
        # Update configuration
        self.server_url = server_url
        self.server_user = server_user
        self.server_password = server_password
        
        # Save config
        config = {
            'server_url': server_url,
            'server_user': server_user,
            'domain': domain,
            'email': email,
            'updated_at': datetime.now().isoformat()
        }
        
        with open('server_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n✅ Configuration saved to server_config.json")
        return config
    
    def run_interactive_deployment(self):
        """Interactive deployment menu"""
        print("🚀 UnionCoin Online Server Deployment")
        print("=" * 50)
        
        while True:
            print("\n📋 Deployment Options:")
            print("1. 🔧 Configure Server Settings")
            print("2. 📦 Create Deployment Package")
            print("3. 🚀 Upload to Server")
            print("4. 🔐 Deploy via SSH")
            print("5. ⚙️ Create Server Config Files")
            print("6. 📊 Show Server Info")
            print("7. ❌ Exit")
            
            choice = input("\n👉 Enter your choice (1-7): ").strip()
            
            if choice == "1":
                self.get_server_info()
            elif choice == "2":
                self.create_deployment_package()
            elif choice == "3":
                if self.create_deployment_package():
                    self.upload_to_server()
            elif choice == "4":
                if self.create_deployment_package():
                    self.deploy_via_ssh()
            elif choice == "5":
                self.create_server_config()
            elif choice == "6":
                try:
                    with open('server_config.json', 'r') as f:
                        config = json.load(f)
                        print(f"\n📊 Current Server Configuration:")
                        print(f"   URL: {config.get('server_url', 'Not set')}")
                        print(f"   User: {config.get('server_user', 'Not set')}")
                        print(f"   Domain: {config.get('domain', 'Not set')}")
                        print(f"   Email: {config.get('email', 'Not set')}")
                except FileNotFoundError:
                    print("❌ No server configuration found. Run option 1 first.")
            elif choice == "7":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please try again.")

def main():
    """Main deployment menu"""
    uploader = UnionCoinUploader()
    uploader.run_interactive_deployment()

if __name__ == "__main__":
    main()
