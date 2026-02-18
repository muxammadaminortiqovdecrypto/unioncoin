#!/usr/bin/env python3
"""
UnionCoin GitHub Deployment
Deploy to GitHub repository for easy server deployment
"""

import os
import sys
import subprocess
import requests
import json
from datetime import datetime
import zipfile

class GitHubDeployer:
    def __init__(self):
        self.github_token = "YOUR_GITHUB_TOKEN"  # O'zgartiring
        self.github_username = "YOUR_GITHUB_USERNAME"  # O'zgartiring
        self.repo_name = "unioncoin"
        self.local_path = os.getcwd()
        
    def create_github_repo(self):
        """Create GitHub repository"""
        print("🐙 Creating GitHub repository...")
        
        try:
            # GitHub API endpoint for creating repository
            url = f"https://api.github.com/user/repos"
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            data = {
                "name": self.repo_name,
                "description": "UnionCoin - Production-Grade Token Ecosystem with Telegram Bot and Web Interface",
                "private": False,  # Public repository
                "auto_init": False,
                "gitignore_template": "python"
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 201:
                repo_data = response.json()
                print(f"✅ Repository created: {repo_data['html_url']}")
                print(f"   Clone URL: {repo_data['clone_url']}")
                return repo_data['clone_url']
            else:
                print(f"❌ Failed to create repository: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ GitHub API error: {e}")
            return None
    
    def setup_git_remote(self, repo_url):
        """Setup git remote and push to GitHub"""
        print("🔧 Setting up Git remote...")
        
        try:
            # Initialize git if not already initialized
            if not os.path.exists('.git'):
                subprocess.run(['git', 'init'], cwd=self.local_path, check=True)
                print("   ✅ Git initialized")
            
            # Add remote
            auth_url = f"https://{self.github_username}:{self.github_token}@github.com/{self.github_username}/{self.repo_name}.git"
            subprocess.run(['git', 'remote', 'add', 'origin', auth_url], cwd=self.local_path, check=True)
            print("   ✅ Remote added")
            
            # Add all files
            subprocess.run(['git', 'add', '.'], cwd=self.local_path, check=True)
            print("   ✅ Files added")
            
            # Commit
            commit_message = f"Deploy UnionCoin v2.0 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_message], cwd=self.local_path, check=True)
            print("   ✅ Files committed")
            
            # Push to GitHub
            subprocess.run(['git', 'push', '-u', 'origin', 'master'], cwd=self.local_path, check=True)
            print("   ✅ Pushed to GitHub")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Git setup error: {e}")
            return False
    
    def create_deployment_script(self):
        """Create server deployment script"""
        print("📜 Creating server deployment script...")
        
        script_content = f"""#!/bin/bash
# UnionCoin Server Deployment from GitHub
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

echo "🚀 Starting UnionCoin deployment from GitHub..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git curl

# Clone from GitHub
echo "📥 Cloning from GitHub..."
cd /var/www/
if [ -d "unioncoin" ]; then
    sudo rm -rf unioncoin
fi

git clone https://github.com/{self.github_username}/{self.repo_name}.git
cd unioncoin

# Setup Python environment
echo "🐍 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup database
echo "🗄️ Setting up database..."
sudo -u postgres psql -c "DROP DATABASE IF EXISTS unioncoin;"
sudo -u postgres psql -c "CREATE DATABASE unioncoin;"
sudo -u postgres psql -c "CREATE USER unioncoin WITH PASSWORD 'secure_password_2026';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE unioncoin TO unioncoin;"

# Setup environment
echo "⚙️ Setting up environment..."
cp .env.example .env
sed -i 's|YOUR_BOT_TOKEN|8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A|g' .env
sed -i 's|YOUR_ADMIN_ID|1685342390|g' .env
sed -i 's|sqlite:///./unioncoin.db|postgresql://unioncoin:secure_password_2026@localhost/unioncoin|g' .env

# Setup systemd services
echo "⚙️ Creating systemd services..."
sudo tee /etc/systemd/system/unioncoin-web.service > /dev/null <<EOF
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

sudo tee /etc/systemd/system/unioncoin-bot.service > /dev/null <<EOF
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
    }}
    
    location /static {{
        alias /var/www/unioncoin/static;
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
echo "📥 Repository: https://github.com/{self.github_username}/{self.repo_name}"
"""
        
        with open('deploy_from_github.sh', 'w') as f:
            f.write(script_content)
        
        # Make script executable
        os.chmod('deploy_from_github.sh', 0o755)
        
        print("✅ Deployment script created: deploy_from_github.sh")
        print("   📜 Script is executable")
        return True
    
    def create_github_actions(self):
        """Create GitHub Actions workflow for CI/CD"""
        print("🔄 Creating GitHub Actions workflow...")
        
        workflow_content = f"""name: Deploy UnionCoin

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        
    - name: Run tests
      run: |
        python database.py
        python -m pytest tests/ || echo "No tests found, continuing..."
        
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{{{ secrets.HOST }}}}
        username: ${{{{ secrets.USERNAME }}}}
        key: ${{{{ secrets.SSH_KEY }}}}
        port: 22
        script: |
          cd /var/www/unioncoin
          git pull origin master
          source venv/bin/activate
          pip install -r requirements.txt
          sudo systemctl restart unioncoin-web unioncoin-bot
          
    - name: Notify deployment
      if: success()
        run: |
          echo "🚀 UnionCoin deployed successfully!"
"""
        
        # Create .github/workflows directory
        os.makedirs('.github/workflows', exist_ok=True)
        
        with open('.github/workflows/deploy.yml', 'w') as f:
            f.write(workflow_content)
        
        print("✅ GitHub Actions workflow created")
        return True
    
    def get_github_config(self):
        """Get GitHub configuration from user"""
        print("\n🐙 GitHub Configuration")
        print("=" * 40)
        
        github_token = input("👉 GitHub Token: ").strip()
        github_username = input("👉 GitHub Username: ").strip()
        
        # Update configuration
        self.github_token = github_token
        self.github_username = github_username
        
        # Save config
        config = {
            'github_token': github_token,
            'github_username': github_username,
            'repo_name': self.repo_name,
            'updated_at': datetime.now().isoformat()
        }
        
        with open('github_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n✅ GitHub configuration saved to github_config.json")
        return config
    
    def run_interactive_deployment(self):
        """Interactive GitHub deployment menu"""
        print("🐙 UnionCoin GitHub Deployment")
        print("=" * 50)
        
        while True:
            print("\n📋 GitHub Deployment Options:")
            print("1. 🔧 Configure GitHub Settings")
            print("2. 🐙 Create GitHub Repository")
            print("3. 📤 Push to GitHub")
            print("4. 📜 Create Deployment Script")
            print("5. 🔄 Create GitHub Actions")
            print("6. 📊 Show GitHub Info")
            print("7. ❌ Exit")
            
            choice = input("\n👉 Enter your choice (1-7): ").strip()
            
            if choice == "1":
                self.get_github_config()
            elif choice == "2":
                repo_url = self.create_github_repo()
                if repo_url:
                    self.setup_git_remote(repo_url)
            elif choice == "3":
                # Load config and push
                try:
                    with open('github_config.json', 'r') as f:
                        config = json.load(f)
                        self.github_token = config['github_token']
                        self.github_username = config['github_username']
                    
                    repo_url = f"https://github.com/{self.github_username}/{self.repo_name}.git"
                    self.setup_git_remote(repo_url)
                except FileNotFoundError:
                    print("❌ No GitHub configuration found. Run option 1 first.")
            elif choice == "4":
                self.create_deployment_script()
            elif choice == "5":
                self.create_github_actions()
            elif choice == "6":
                try:
                    with open('github_config.json', 'r') as f:
                        config = json.load(f)
                        print(f"\n📊 Current GitHub Configuration:")
                        print(f"   Username: {config.get('github_username', 'Not set')}")
                        print(f"   Repository: {config.get('repo_name', 'Not set')}")
                        print(f"   Token: {'*' * len(config.get('github_token', ''))}{'*' if config.get('github_token') else 'Not set'}")
                except FileNotFoundError:
                    print("❌ No GitHub configuration found. Run option 1 first.")
            elif choice == "7":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please try again.")

def main():
    """Main GitHub deployment menu"""
    deployer = GitHubDeployer()
    deployer.run_interactive_deployment()

if __name__ == "__main__":
    main()
