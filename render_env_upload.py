#!/usr/bin/env python3
"""
UnionCoin Render.com Environment File Upload
Upload .env file to Render.com with proper format
"""

import os
import json
import webbrowser
import requests
from datetime import datetime

class RenderEnvUpload:
    def __init__(self):
        self.render_api_key = "YOUR_RENDER_API_KEY"
        self.service_name = "unioncoin-web"
        self.env_file_path = ".env"
        
    def find_env_file(self):
        """Find .env file in current directory"""
        print("🔍 Searching for .env file...")
        
        # Check current directory
        if os.path.exists(self.env_file_path):
            print(f"✅ Found {self.env_file_path} in current directory")
            return self.env_file_path
        
        # Check parent directories
        current_dir = os.getcwd()
        parent_dir = os.path.dirname(current_dir)
        
        while parent_dir != current_dir:
            env_path = os.path.join(parent_dir, self.env_file_path)
            if os.path.exists(env_path):
                print(f"✅ Found {self.env_file_path} in {parent_dir}")
                return env_path
            current_dir = parent_dir
            parent_dir = os.path.dirname(current_dir)
        
        print(f"❌ {self.env_file_path} not found!")
        return None
    
    def read_env_file(self, env_path):
        """Read and parse .env file"""
        print(f"📖 Reading {env_path}...")
        
        env_vars = {}
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        env_vars[key] = value
            
            print(f"✅ Read {len(env_vars)} environment variables:")
            for key, value in env_vars.items():
                # Hide sensitive values
                display_value = value[:10] + "..." if len(value) > 10 else value
                if 'TOKEN' in key or 'PASSWORD' in key or 'SECRET' in key:
                    display_value = "***HIDDEN***"
                print(f"   {key}: {display_value}")
            
            return env_vars
            
        except Exception as e:
            print(f"❌ Error reading .env file: {e}")
            return None
    
    def create_env_file(self):
        """Create .env file with UnionCoin configuration"""
        print("📝 Creating .env file...")
        
        env_content = """# UnionCoin Production Environment Configuration
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Database Configuration
DATABASE_URL=postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin

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

# CORS Configuration
ALLOWED_ORIGINS=https://unioncoin.onrender.com

# PostgreSQL Configuration (explicit)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=unioncoin
DB_USER=postgres
DB_PASSWORD=12345

# Performance Configuration
MAX_WORKERS=4
WORKER_CONNECTIONS=1000
KEEPALIVE_TIMEOUT=65

# Monitoring Configuration
MONITORING_ENABLED=True
LOG_LEVEL=INFO
LOG_FILE=/var/log/unioncoin/unioncoin.log

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
""".format(datetime=datetime.now())
        
        try:
            with open(self.env_file_path, 'w') as f:
                f.write(env_content)
            
            print(f"✅ Created {self.env_file_path}")
            print(f"📁 Location: {os.path.abspath(self.env_file_path)}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    
    def upload_env_to_render(self, env_vars, api_key):
        """Upload environment variables to Render.com"""
        print("🚀 Uploading environment variables to Render.com...")
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Get service ID
        try:
            response = requests.get(
                'https://api.render.com/v1/services',
                headers=headers
            )
            
            if response.status_code == 200:
                services = response.json()
                
                for service in services:
                    if service.get('name') == self.service_name:
                        service_id = service.get('id')
                        print(f"✅ Found service: {service_id}")
                        
                        # Prepare environment variables for new interface
                        env_groups = {}
                        
                        # Group variables by category
                        for key, value in env_vars.items():
                            group_name = self.get_group_name(key)
                            if group_name not in env_groups:
                                env_groups[group_name] = []
                            env_groups[group_name].append({
                                'key': key,
                                'value': value
                            })
                        
                        # Upload each group
                        for group_name, variables in env_groups.items():
                            env_data = {
                                'groupId': group_name,
                                'envVars': variables
                            }
                            
                            print(f"📦 Uploading group: {group_name}")
                            print(f"   Variables: {len(variables)}")
                            
                            # Add environment variables
                            add_response = requests.post(
                                f'https://api.render.com/v1/services/{service_id}/env-vars',
                                headers=headers,
                                json=env_data
                            )
                            
                            if add_response.status_code == 201:
                                print(f"✅ Group {group_name} uploaded successfully!")
                            else:
                                print(f"❌ Failed to upload group {group_name}: {add_response.status_code}")
                                print(f"   Error: {add_response.text}")
                        
                        # Trigger redeploy
                        print("🔄 Triggering redeploy...")
                        redeploy_response = requests.post(
                            f'https://api.render.com/v1/services/{service_id}/restart',
                            headers=headers
                        )
                        
                        if redeploy_response.status_code == 200:
                            print("✅ Service redeployed successfully!")
                            print("⏳ Wait 2-3 minutes for changes to take effect")
                            return True
                        else:
                            print(f"❌ Failed to redeploy: {redeploy_response.status_code}")
                            return False
                        
                print("❌ Service not found!")
                return False
                
        except Exception as e:
            print(f"❌ API error: {e}")
            return False
    
    def get_group_name(self, key):
        """Get group name for environment variable"""
        if 'DATABASE' in key or 'DB_' in key:
            return 'database'
        elif 'BOT_TOKEN' in key or 'ADMIN_ID' in key:
            return 'telegram'
        elif 'SECRET' in key or 'PASSWORD' in key:
            return 'security'
        elif 'HOST' in key or 'PORT' in key or 'DEBUG' in key:
            return 'server'
        elif 'CORS' in key or 'ALLOWED' in key:
            return 'cors'
        elif 'MAX_WORKERS' in key or 'WORKER' in key or 'KEEPALIVE' in key:
            return 'performance'
        elif 'MONITORING' in key or 'LOG' in key:
            return 'monitoring'
        elif 'RATE_LIMIT' in key:
            return 'rate-limit'
        else:
            return 'general'
    
    def show_env_file_location(self):
        """Show where .env file should be located"""
        print("📁 .env File Location Guide")
        print("=" * 40)
        
        current_dir = os.getcwd()
        print(f"\n📍 Current Directory: {current_dir}")
        print(f"🎯 Expected .env Location: {os.path.join(current_dir, '.env')}")
        
        print("\n📋 How to Create .env File:")
        print("1. 📝 Open text editor (Notepad, VS Code, etc.)")
        print("2. 📋 Copy the content below:")
        print("3. 💾 Save as '.env' in the current directory")
        print("4. 📁 Make sure it's in: D:\\unioncoin\\.env")
        
        print("\n📝 .env File Content:")
        print("-" * 30)
        print("DATABASE_URL=postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin")
        print("BOT_TOKEN=8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A")
        print("ADMIN_ID=1685342390")
        print("SECRET_KEY=unioncoin_production_secret_key_2026")
        print("ADMIN_PASSWORD=unioncoin_admin_2026")
        print("HOST=0.0.0.0")
        print("PORT=8000")
        print("DEBUG=False")
        print("ALLOWED_ORIGINS=https://unioncoin.onrender.com")
        
        return True
    
    def create_env_file_interactive(self):
        """Create .env file interactively"""
        print("📝 Create .env File Interactively")
        print("=" * 40)
        
        env_vars = {}
        
        # Database
        print("\n🗄️ Database Configuration:")
        env_vars['DATABASE_URL'] = input("DATABASE_URL (default: postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin): ").strip() or "postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin"
        
        # Telegram
        print("\n🤖 Telegram Configuration:")
        env_vars['BOT_TOKEN'] = input("BOT_TOKEN (default: 8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A): ").strip() or "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A"
        env_vars['ADMIN_ID'] = input("ADMIN_ID (default: 1685342390): ").strip() or "1685342390"
        
        # Security
        print("\n🔒 Security Configuration:")
        env_vars['SECRET_KEY'] = input("SECRET_KEY (default: unioncoin_production_secret_key_2026): ").strip() or "unioncoin_production_secret_key_2026"
        env_vars['ADMIN_PASSWORD'] = input("ADMIN_PASSWORD (default: unioncoin_admin_2026): ").strip() or "unioncoin_admin_2026"
        
        # Server
        print("\n🌐 Server Configuration:")
        env_vars['HOST'] = input("HOST (default: 0.0.0.0): ").strip() or "0.0.0.0"
        env_vars['PORT'] = input("PORT (default: 8000): ").strip() or "8000"
        env_vars['DEBUG'] = input("DEBUG (default: False): ").strip() or "False"
        
        # Write to file
        try:
            with open(self.env_file_path, 'w') as f:
                for key, value in env_vars.items():
                    f.write(f"{key}={value}\n")
            
            print(f"\n✅ Created {self.env_file_path}")
            print(f"📁 Location: {os.path.abspath(self.env_file_path)}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    
    def open_current_directory(self):
        """Open current directory in file explorer"""
        print("📁 Opening current directory...")
        current_dir = os.getcwd()
        
        if os.name == 'nt':  # Windows
            os.startfile(current_dir)
        elif os.name == 'posix':  # macOS/Linux
            if os.system('which xdg-open > /dev/null 2>&1') == 0:
                os.system(f'xdg-open "{current_dir}"')
            elif os.system('which open > /dev/null 2>&1') == 0:
                os.system(f'open "{current_dir}"')
        
        return True

def main():
    """Main environment upload menu"""
    print("🚀 UnionCoin Render.com Environment File Upload")
    print("=" * 60)
    
    uploader = RenderEnvUpload()
    
    while True:
        print("\n📋 Environment File Options:")
        print("1. 🔍 Find .env File")
        print("2. 📝 Create .env File")
        print("3. 📝 Create .env File Interactively")
        print("4. 📦 Upload .env to Render.com")
        print("5. 📁 Show .env File Location")
        print("6. 📁 Open Current Directory")
        print("7. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-7): ").strip()
        
        if choice == "1":
            env_path = uploader.find_env_file()
            if env_path:
                env_vars = uploader.read_env_file(env_path)
                if env_vars:
                    print("\n📦 Ready to upload to Render.com!")
        elif choice == "2":
            uploader.create_env_file()
        elif choice == "3":
            uploader.create_env_file_interactive()
        elif choice == "4":
            env_path = uploader.find_env_file()
            if env_path:
                env_vars = uploader.read_env_file(env_path)
                if env_vars:
                    api_key = input("🔑 Render API Key: ").strip()
                    if api_key:
                        uploader.upload_env_to_render(env_vars, api_key)
        elif choice == "5":
            uploader.show_env_file_location()
        elif choice == "6":
            uploader.open_current_directory()
        elif choice == "7":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
