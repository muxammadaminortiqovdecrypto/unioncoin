#!/usr/bin/env python3
"""
UnionCoin Complete Deployment Script
All-in-one deployment with environment variables
"""

import os
import sys
import subprocess
import webbrowser
import requests
import time
from datetime import datetime

class UnionCoinDeployer:
    def __init__(self):
        self.render_url = "https://render.com"
        self.github_repo = "https://github.com/muxammadaminortiqovdecrypto/unioncoin"
        
        # Environment Variables
        self.env_vars = {
            'DATABASE_URL': 'postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin',
            'BOT_TOKEN': '8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A',
            'ADMIN_ID': '1685342390',
            'SECRET_KEY': 'unioncoin_production_secret_key_2026',
            'ADMIN_PASSWORD': 'unioncoin_admin_2026',
            'HOST': '0.0.0.0',
            'PORT': '8000',
            'DEBUG': 'False',
            'PYTHON_VERSION': '3.11'
        }
        
    def show_banner(self):
        """Show deployment banner"""
        print("🚀 UnionCoin Complete Deployment Script")
        print("=" * 60)
        print("📅 Date:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("🌐 Repository:", self.github_repo)
        print("🔧 All-in-One Deployment Ready!")
        print("=" * 60)
        
    def deploy_to_render(self):
        """Deploy to Render.com"""
        print("\n🌐 DEPLOYING TO RENDER.COM")
        print("-" * 50)
        
        print("📋 STEP 1: Open Render Dashboard")
        print("1. 🌐 Opening Render dashboard...")
        webbrowser.open("https://render.com")
        input("👉 Press Enter after opening Render dashboard...")
        
        print("\n📋 STEP 2: Create Database")
        print("1. 🗄️ Click 'New +' → 'PostgreSQL'")
        print("2. 📝 Configure:")
        print("   • Name: unioncoin-db")
        print("   • Database: unioncoin")
        print("   • User: unioncoin_user")
        print("   • Password: unioncoin_password")
        print("3. ✅ Click 'Create Database'")
        input("👉 Press Enter after creating database...")
        
        print("\n📋 STEP 3: Create Web Service")
        print("1. 🌐 Click 'New +' → 'Web Service'")
        print("2. 🔗 Connect GitHub repository")
        print("3. 📁 Select: muxammadaminortiqovdecrypto/unioncoin")
        print("4. 📝 Configure:")
        print("   • Name: unioncoin-web")
        print("   • Environment: Python")
        print("   • Build: pip install -r requirements_render.txt")
        print("   • Start: gunicorn api_render:app --bind 0.0.0.0:$PORT")
        print("   • Health Check: /verify")
        input("👉 Press Enter after configuring web service...")
        
        print("\n📋 STEP 4: Add Environment Variables")
        print("1. ⚙️ Go to Environment tab")
        print("2. ➕ Click 'Add Environment Variable'")
        
        for key, value in self.env_vars.items():
            print(f"3. 📝 Add variable:")
            print(f"   • Group Name: unioncoin-admin")
            print(f"   • Variable Name: {key}")
            print(f"   • Variable Value: {value}")
            print(f"   • Type: Plain text")
            print("4. ✅ Click 'Save'")
            input("👉 Press Enter after adding variable...")
        
        print("\n📋 STEP 5: Create Bot Service")
        print("1. 🤖 Click 'New +' → 'Background Worker'")
        print("2. 📝 Configure:")
        print("   • Name: unioncoin-bot")
        print("   • Repository: muxammadaminortiqovdecrypto/unioncoin")
        print("   • Build: pip install -r requirements_render.txt")
        print("   • Start: python bot.py")
        input("👉 Press Enter after configuring bot service...")
        
        print("\n📋 STEP 6: Add Bot Environment Variables")
        for key, value in self.env_vars.items():
            print(f"1. 📝 Add variable to bot service:")
            print(f"   • Group Name: unioncoin-admin")
            print(f"   • Variable Name: {key}")
            print(f"   • Variable Value: {value}")
            print(f"   • Type: Plain text")
            print("2. ✅ Click 'Save'")
            input("👉 Press Enter after adding variable...")
        
        print("\n📋 STEP 7: Wait and Test")
        print("1. ⏳ Wait 5-10 minutes for deployment")
        print("2. 🧪 Test services:")
        print("   • Web: https://unioncoin.onrender.com")
        print("   • Admin: https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026")
        print("   • Bot: @tokenuchunku12bot")
        
        return True
    
    def deploy_to_heroku(self):
        """Deploy to Heroku"""
        print("\n🚀 DEPLOYING TO HEROKU")
        print("-" * 50)
        
        print("📋 STEP 1: Open Heroku Dashboard")
        print("1. 🌐 Opening Heroku dashboard...")
        webbrowser.open("https://heroku.com")
        input("👉 Press Enter after opening Heroku dashboard...")
        
        print("\n📋 STEP 2: Create App")
        print("1. ➕ Click 'Create new app'")
        print("2. 📝 Configure:")
        print("   • App name: unioncoin-app")
        print("   • Region: United States")
        input("👉 Press Enter after creating app...")
        
        print("\n📋 STEP 3: Connect GitHub")
        print("1. 🔗 Go to 'Deploy' tab")
        print("2. 📁 Click 'Connect to GitHub'")
        print("3. 🔍 Search: muxammadaminortiqovdecrypto/unioncoin")
        print("4. 🔗 Click 'Connect'")
        input("👉 Press Enter after connecting...")
        
        print("\n📋 STEP 4: Add Database")
        print("1. 🗄️ Go to 'Resources' tab")
        print("2. 🔍 Search: 'Heroku Postgres'")
        print("3. 📝 Select: 'Hobby Dev - Free'")
        print("4. ✅ Click 'Provision'")
        input("👉 Press Enter after adding database...")
        
        print("\n📋 STEP 5: Add Environment Variables")
        print("1. ⚙️ Go to 'Settings' tab")
        print("2. 🔍 Click 'Reveal Config Vars'")
        
        for key, value in self.env_vars.items():
            print(f"3. 📝 Add variable:")
            print(f"   • Key: {key}")
            print(f"   • Value: {value}")
            input("👉 Press Enter after adding variable...")
        
        return True
    
    def deploy_to_railway(self):
        """Deploy to Railway"""
        print("\n🚀 DEPLOYING TO RAILWAY")
        print("-" * 50)
        
        print("📋 STEP 1: Open Railway Dashboard")
        print("1. 🌐 Opening Railway dashboard...")
        webbrowser.open("https://railway.app")
        input("👉 Press Enter after opening Railway dashboard...")
        
        print("\n📋 STEP 2: Create Project")
        print("1. ➕ Click 'New Project'")
        print("2. 📁 Click 'Deploy from GitHub repo'")
        print("3. 🔍 Search: muxammadaminortiqovdecrypto/unioncoin")
        print("4. 🔗 Click 'Select'")
        input("👉 Press Enter after selecting...")
        
        print("\n📋 STEP 3: Configure Services")
        print("1. 📝 Railway will auto-detect services")
        print("2. ⚙️ Configure web service:")
        print("   • Name: unioncoin-web")
        print("   • Port: 8000")
        print("3. ⚙️ Configure database service:")
        print("   • Name: unioncoin-db")
        print("   • Type: PostgreSQL")
        input("👉 Press Enter after configuring...")
        
        print("\n📋 STEP 4: Add Environment Variables")
        for key, value in self.env_vars.items():
            print(f"1. 📝 Add variable:")
            print(f"   • Key: {key}")
            print(f"   • Value: {value}")
            input("👉 Press Enter after adding variable...")
        
        return True
    
    def deploy_to_vps(self):
        """Deploy to VPS"""
        print("\n🖥️ DEPLOYING TO VPS")
        print("-" * 50)
        
        print("📋 STEP 1: Get VPS Server")
        print("1. 🌐 Choose provider:")
        print("   • DigitalOcean: https://digitalocean.com")
        print("   • Vultr: https://vultr.com")
        print("   • Linode: https://linode.com")
        input("👉 Press Enter after choosing provider...")
        
        print("\n📋 STEP 2: Create Server")
        print("1. 🖥️ Create droplet/server:")
        print("   • OS: Ubuntu 20.04 LTS")
        print("   • Plan: $5/month (1GB RAM, 25GB SSD)")
        print("   • Region: Choose nearest to you")
        input("👉 Press Enter after creating server...")
        
        print("\n📋 STEP 3: Setup Server")
        print("1. 🔑 Get server IP and SSH key")
        print("2. 🖥️ Connect via SSH:")
        print("   • Windows: Use PuTTY")
        print("   • Mac/Linux: ssh root@SERVER_IP")
        print("3. 🔧 Update server:")
        print("   • apt update && apt upgrade -y")
        print("   • apt install python3 python3-pip postgresql nginx -y")
        input("👉 Press Enter after connecting...")
        
        print("\n📋 STEP 4: Deploy UnionCoin")
        print("1. 📁 Clone repository:")
        print("   • git clone https://github.com/muxammadaminortiqovdecrypto/unioncoin")
        print("   • cd unioncoin")
        print("2. 🐍 Setup Python:")
        print("   • python3 -m venv venv")
        print("   • source venv/bin/activate")
        print("   • pip install -r requirements.txt")
        print("3. 🗄️ Setup PostgreSQL:")
        print("   • sudo -u postgres createuser unioncoin_user")
        print("   • sudo -u postgres createdb unioncoin")
        print("   • sudo -u postgres psql -c \"ALTER USER unioncoin_user PASSWORD 'unioncoin_password';\"")
        print("4. 🚀 Start services:")
        print("   • gunicorn api:app --bind 0.0.0.0:8000 &")
        print("   • python bot.py &")
        input("👉 Press Enter after deploying...")
        
        return True
    
    def create_local_deployment(self):
        """Create local deployment"""
        print("\n🖥️ LOCAL DEPLOYMENT")
        print("-" * 50)
        
        print("📋 STEP 1: Start Web Server")
        print("1. 🚀 Starting web server on port 8000...")
        print("2. 🌐 Web Interface: http://localhost:8000")
        print("3. 📊 Admin Panel: http://localhost:8000/api/data?admin=unioncoin_admin_2026")
        
        # Start web server in background
        try:
            subprocess.Popen(['python', 'api.py'], 
                         creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            print("✅ Web server started!")
        except Exception as e:
            print(f"❌ Error starting web server: {e}")
        
        input("👉 Press Enter after starting web server...")
        
        print("\n📋 STEP 2: Start Telegram Bot")
        print("1. 🤖 Starting Telegram bot...")
        print("2. 📱 Bot Username: @tokenuchunku12bot")
        print("3. 💬 Commands: /start, /admin, /help")
        
        # Start bot in background
        try:
            subprocess.Popen(['python', 'bot.py'], 
                         creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            print("✅ Telegram bot started!")
        except Exception as e:
            print(f"❌ Error starting bot: {e}")
        
        return True
    
    def show_all_urls(self):
        """Show all deployment URLs"""
        print("\n🌐 ALL DEPLOYMENT URLS")
        print("-" * 50)
        
        urls = {
            "Local Web": "http://localhost:8000",
            "Local Admin": "http://localhost:8000/api/data?admin=unioncoin_admin_2026",
            "Render Web": "https://unioncoin.onrender.com",
            "Render Admin": "https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026",
            "GitHub": "https://github.com/muxammadaminortiqovdecrypto/unioncoin",
            "Render Dashboard": "https://render.com",
            "Heroku Dashboard": "https://heroku.com",
            "Railway Dashboard": "https://railway.app"
        }
        
        for name, url in urls.items():
            print(f"🌐 {name}: {url}")
        
        return True
    
    def show_environment_variables(self):
        """Show all environment variables"""
        print("\n🔑 ENVIRONMENT VARIABLES")
        print("-" * 50)
        
        for key, value in self.env_vars.items():
            print(f"📝 {key}: {value}")
        
        return True
    
    def create_backup_script(self):
        """Create backup script"""
        print("\n💾 CREATING BACKUP SCRIPT")
        
        backup_content = '''#!/bin/bash
# UnionCoin Backup Script
echo "🚀 UnionCoin Backup Script"
echo "========================"
echo "📅 Date: $(date)"

# Create backup directory
mkdir -p backups
cd backups

# Backup database
echo "🗄️ Backing up database..."
pg_dump unioncoin > unioncoin_backup_$(date +%Y%m%d_%H%M%S).sql

# Backup files
echo "📁 Backing up files..."
tar -czf unioncoin_files_$(date +%Y%m%d_%H%M%S).tar.gz ../unioncoin

# Create backup report
echo "📊 Backup Report:" > backup_report_$(date +%Y%m%d_%H%M%S).txt
echo "Date: $(date)" >> backup_report_$(date +%Y%m%d_%H%M%S).txt
echo "Database: unioncoin_backup_$(date +%Y%m%d_%H%M%S).sql" >> backup_report_$(date +%Y%m%d_%H%M%S).txt
echo "Files: unioncoin_files_$(date +%Y%m%d_%H%M%S).tar.gz" >> backup_report_$(date +%Y%m%d_%H%M%S).txt

echo "✅ Backup completed!"
echo "📁 Location: $(pwd)"
echo "📊 Report: backup_report_$(date +%Y%m%d_%H%M%S).txt"
'''
        
        with open('backup_script.sh', 'w') as f:
            f.write(backup_content)
        
        print("✅ Backup script created: backup_script.sh")
        return True
    
    def main_menu(self):
        """Main deployment menu"""
        while True:
            print("\n🚀 UNIONCOIN DEPLOYMENT MENU")
            print("=" * 50)
            print("1. 🌐 Deploy to Render.com (Recommended)")
            print("2. 🚀 Deploy to Heroku")
            print("3. 🚀 Deploy to Railway")
            print("4. 🖥️ Deploy to VPS (Production)")
            print("5. 🖥️ Local Deployment")
            print("6. 🌐 Show All URLs")
            print("7. 🔑 Show Environment Variables")
            print("8. 💾 Create Backup Script")
            print("9. ❌ Exit")
            
            choice = input("\n👉 Enter your choice (1-9): ").strip()
            
            if choice == "1":
                self.deploy_to_render()
            elif choice == "2":
                self.deploy_to_heroku()
            elif choice == "3":
                self.deploy_to_railway()
            elif choice == "4":
                self.deploy_to_vps()
            elif choice == "5":
                self.create_local_deployment()
            elif choice == "6":
                self.show_all_urls()
            elif choice == "7":
                self.show_environment_variables()
            elif choice == "8":
                self.create_backup_script()
            elif choice == "9":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please try again.")

def main():
    """Main function"""
    deployer = UnionCoinDeployer()
    deployer.show_banner()
    deployer.main_menu()

if __name__ == "__main__":
    main()
