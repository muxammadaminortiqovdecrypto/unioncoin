#!/usr/bin/env python3
"""
UnionCoin Final Environment Configuration
Render.com PostgreSQL Database Setup
"""

import os
import sys
import subprocess
import webbrowser
from datetime import datetime

class FinalEnvConfig:
    def __init__(self):
        self.render_url = "https://render.com"
        self.github_repo = "https://github.com/muxammadaminortiqovdecrypto/unioncoin"
        
        # Database configuration from user
        self.db_host = "dpg-d6c9at15pdvs738si39g-a"
        self.db_host_external = "dpg-d6c9at15pdvs738si39g-a.oregon-postgres.render.com"
        self.db_name = "unioncoin"
        self.db_user = "unioncoin_user"
        self.db_password = "R0HqXLoceeHhqba1MokFvWhEDSBcecqd"
        self.db_port = "5432"
        
    def show_database_info(self):
        """Show database information"""
        print("🗄️ UnionCoin Database Information")
        print("=" * 70)
        print("📋 DATABASE CONFIGURATION:")
        print(f"🗄️ Database: {self.db_name}")
        print(f"👤 Username: {self.db_user}")
        print(f"🔐 Password: {self.db_password}")
        print(f"🌐 Internal Host: {self.db_host}")
        print(f"🌐 External Host: {self.db_host_external}")
        print(f"🔌 Port: {self.db_port}")
        print("")
        print("📋 DATABASE URLs:")
        print(f"🔗 Internal: postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}")
        print(f"🔗 External: postgresql://{self.db_user}:{self.db_password}@{self.db_host_external}/{self.db_name}")
        print("=" * 70)
        
        return True
    
    def create_final_env_file(self):
        """Create final environment file"""
        print("\n📝 CREATING FINAL ENVIRONMENT FILE")
        print("-" * 70)
        
        # Create database URLs
        internal_db_url = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
        external_db_url = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host_external}/{self.db_name}"
        
        env_content = f"""# UnionCoin Final Environment Configuration
# Render.com PostgreSQL Database Setup

# Database Configuration (CRITICAL)
DATABASE_URL={internal_db_url}
DATABASE_URL_EXTERNAL={external_db_url}
DATABASE_URL_INTERNAL={internal_db_url}
DB_HOST={self.db_host}
DB_HOST_EXTERNAL={self.db_host_external}
DB_PORT={self.db_port}
DB_NAME={self.db_name}
DB_USER={self.db_user}
DB_PASSWORD={self.db_password}

# Bot Configuration
BOT_TOKEN=8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTZom9_7A
ADMIN_TELEGRAM_ID=1685342390

# Domain Configuration
DOMAIN=unioncoin.onrender.com

# Security Configuration
TELEGRAM_AUTH_ONLY=true
WEB_REGISTRATION_DISABLED=true
ADMIN_ACCESS_TELEGRAM_ONLY=true
SECURITY_LEVEL=maximum

# Authentication Configuration
SECRET_KEY=unioncoin_secret_key_2026_secure
ADMIN_PASSWORD=unioncoin_admin_2026

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# CORS Configuration
ALLOWED_ORIGINS=https://unioncoin.onrender.com,http://localhost:8000,https://localhost:8000

# Logging Configuration
LOG_LEVEL=info
LOG_FILE=unioncoin.log

# Enhanced Features
USER_STATUS_CHECKING=true
INTELLIGENT_ERROR_HANDLING=true
LOADING_SPINNERS=true
CONTEXTUAL_HELP=true

# Application Configuration
APP_NAME=UnionCoin
APP_VERSION=4.0.0
AUTH_METHOD=telegram_only
REGISTRATION_METHOD=telegram_bot

# Database Connection Settings
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# Security Headers
X_FRAME_OPTIONS=DENY
X_CONTENT_TYPE_OPTIONS=nosniff
X_XSS_PROTECTION=1; mode=block
STRICT_TRANSPORT_SECURITY=max-age=31536000

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Session Configuration
SESSION_TIMEOUT=3600
SESSION_SECURE=true
SESSION_HTTP_ONLY=true

# Monitoring
MONITORING_ENABLED=true
HEALTH_CHECK_ENABLED=true
METRICS_ENABLED=true

# Backup Configuration
BACKUP_ENABLED=true
BACKUP_SCHEDULE=daily
BACKUP_RETENTION_DAYS=30
"""
        
        try:
            with open('.env', 'w') as f:
                f.write(env_content)
            print("✅ .env file created successfully!")
            
            # Show critical environment variables
            print("\n📋 CRITICAL ENVIRONMENT VARIABLES:")
            print(f"DATABASE_URL={internal_db_url}")
            print(f"BOT_TOKEN=8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTZom9_7A")
            print(f"ADMIN_TELEGRAM_ID=1685342390")
            print(f"TELEGRAM_AUTH_ONLY=true")
            print(f"WEB_REGISTRATION_DISABLED=true")
            print(f"ADMIN_ACCESS_TELEGRAM_ONLY=true")
            print(f"SECURITY_LEVEL=maximum")
            
            return True
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    
    def create_render_env_upload_script(self):
        """Create Render.com environment upload script"""
        print("\n📤 CREATING RENDER ENVIRONMENT UPLOAD SCRIPT")
        print("-" * 70)
        
        # Create database URLs
        internal_db_url = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
        
        script_content = f"""#!/usr/bin/env python3
"""
UnionCoin Render Environment Upload
Final Configuration with Real Database
"""

import os
import requests
import json
from datetime import datetime

class RenderEnvUploader:
    def __init__(self):
        self.api_key = "rnd_ZdEBDAplAik1ESge3UULwlYCxWbb"
        self.base_url = "https://api.render.com/v1"
        self.headers = {{
            "Authorization": f"Bearer {{self.api_key}}",
            "Content-Type": "application/json"
        }}
        
    def upload_final_env_vars(self, service_id):
        """Upload final environment variables"""
        env_vars = {{
            "envVars": [
                {{
                    "key": "DATABASE_URL",
                    "value": "{internal_db_url}"
                }},
                {{
                    "key": "DATABASE_URL_EXTERNAL",
                    "value": "postgresql://{self.db_user}:{self.db_password}@{self.db_host_external}/{self.db_name}"
                }},
                {{
                    "key": "DATABASE_URL_INTERNAL",
                    "value": "{internal_db_url}"
                }},
                {{
                    "key": "DB_HOST",
                    "value": "{self.db_host}"
                }},
                {{
                    "key": "DB_HOST_EXTERNAL",
                    "value": "{self.db_host_external}"
                }},
                {{
                    "key": "DB_PORT",
                    "value": "{self.db_port}"
                }},
                {{
                    "key": "DB_NAME",
                    "value": "{self.db_name}"
                }},
                {{
                    "key": "DB_USER",
                    "value": "{self.db_user}"
                }},
                {{
                    "key": "DB_PASSWORD",
                    "value": "{self.db_password}"
                }},
                {{
                    "key": "BOT_TOKEN",
                    "value": "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTZom9_7A"
                }},
                {{
                    "key": "ADMIN_TELEGRAM_ID",
                    "value": "1685342390"
                }},
                {{
                    "key": "DOMAIN",
                    "value": "unioncoin.onrender.com"
                }},
                {{
                    "key": "TELEGRAM_AUTH_ONLY",
                    "value": "true"
                }},
                {{
                    "key": "WEB_REGISTRATION_DISABLED",
                    "value": "true"
                }},
                {{
                    "key": "ADMIN_ACCESS_TELEGRAM_ONLY",
                    "value": "true"
                }},
                {{
                    "key": "SECURITY_LEVEL",
                    "value": "maximum"
                }},
                {{
                    "key": "SECRET_KEY",
                    "value": "unioncoin_secret_key_2026_secure"
                }},
                {{
                    "key": "ADMIN_PASSWORD",
                    "value": "unioncoin_admin_2026"
                }},
                {{
                    "key": "HOST",
                    "value": "0.0.0.0"
                }},
                {{
                    "key": "PORT",
                    "value": "8000"
                }},
                {{
                    "key": "DEBUG",
                    "value": "false"
                }},
                {{
                    "key": "USER_STATUS_CHECKING",
                    "value": "true"
                }},
                {{
                    "key": "INTELLIGENT_ERROR_HANDLING",
                    "value": "true"
                }},
                {{
                    "key": "LOADING_SPINNERS",
                    "value": "true"
                }},
                {{
                    "key": "CONTEXTUAL_HELP",
                    "value": "true"
                }}
            ]
        }}
        
        try:
            response = requests.patch(f"{{self.base_url}}/services/{{service_id}}/env-vars", headers=self.headers, json=env_vars)
            if response.status_code == 200:
                print("✅ Final environment variables uploaded successfully!")
                return True
            else:
                print(f"❌ Error uploading env vars: {{response.status_code}}")
                print(f"Response: {{response.text}}")
                return False
        except Exception as e:
            print(f"❌ Error: {{e}}")
            return False
    
    def get_services(self):
        """Get all services"""
        try:
            response = requests.get(f"{{self.base_url}}/services", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error getting services: {{response.status_code}}")
                return None
        except Exception as e:
            print(f"❌ Error: {{e}}")
            return None
    
    def find_service(self, service_name="unioncoin-web"):
        """Find specific service"""
        services = self.get_services()
        if not services:
            return None
        
        for service in services:
            if service.get('name') == service_name:
                return service
        
        print(f"❌ Service '{{service_name}}' not found")
        return None
    
    def restart_service(self, service_id):
        """Restart service"""
        try:
            response = requests.post(f"{{self.base_url}}/services/{{service_id}}/restart", headers=self.headers)
            if response.status_code == 200:
                print("✅ Service restarted successfully!")
                return True
            else:
                print(f"❌ Error restarting service: {{response.status_code}}")
                return False
        except Exception as e:
            print(f"❌ Error: {{e}}")
            return False
    
    def upload_final_environment(self):
        """Main upload process"""
        print("\\n🔍 FINDING SERVICE")
        print("-" * 40)
        
        service = self.find_service("unioncoin-web")
        if not service:
            print("❌ Service not found!")
            return False
        
        service_id = service['id']
        print(f"✅ Found service: {{service['name']}} (ID: {{service_id}})")
        
        print("\\n📤 UPLOADING FINAL ENVIRONMENT VARIABLES")
        print("-" * 60)
        
        if self.upload_final_env_vars(service_id):
            print("✅ Final environment variables uploaded!")
        else:
            print("❌ Failed to upload environment variables!")
            return False
        
        print("\\n🔄 RESTARTING SERVICE")
        print("-" * 30)
        
        if self.restart_service(service_id):
            print("✅ Service restarted!")
        else:
            print("❌ Failed to restart service!")
            return False
        
        return True

def main():
    """Main function"""
    print("📤 UnionCoin Final Environment Upload")
    print("=" * 60)
    print(f"📅 Upload Time: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
    print("=" * 60)
    
    uploader = RenderEnvUploader()
    
    print("\\n⚠️ WARNING: This will upload final environment variables!")
    confirm = input("👉 Type 'UPLOAD' to confirm: ").strip()
    if confirm == "UPLOAD":
        uploader.upload_final_environment()
    else:
        print("❌ Upload cancelled")

if __name__ == "__main__":
    main()
"""
        
        try:
            with open('render_final_env_upload.py', 'w') as f:
                f.write(script_content)
            print("✅ render_final_env_upload.py created successfully!")
            return True
        except Exception as e:
            print(f"❌ Error creating upload script: {e}")
            return False
    
    def show_render_manual_config(self):
        """Show Render.com manual configuration"""
        print("\n🌐 RENDER.COM MANUAL CONFIGURATION")
        print("=" * 80)
        
        # Create database URLs
        internal_db_url = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
        external_db_url = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host_external}/{self.db_name}"
        
        print("📋 MANUAL STEPS:")
        print("1. 🌐 Open: https://render.com")
        print("2. 🔍 Find: unioncoin-web service")
        print("3. ⚙️ Go to: Environment tab")
        print("4. 📤 Add/Update Environment Variables:")
        print("")
        
        critical_vars = [
            ("DATABASE_URL", internal_db_url),
            ("BOT_TOKEN", "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTZom9_7A"),
            ("ADMIN_TELEGRAM_ID", "1685342390"),
            ("TELEGRAM_AUTH_ONLY", "true"),
            ("WEB_REGISTRATION_DISABLED", "true"),
            ("ADMIN_ACCESS_TELEGRAM_ONLY", "true"),
            ("SECURITY_LEVEL", "maximum"),
            ("SECRET_KEY", "unioncoin_secret_key_2026_secure"),
            ("ADMIN_PASSWORD", "unioncoin_admin_2026"),
            ("DOMAIN", "unioncoin.onrender.com"),
            ("HOST", "0.0.0.0"),
            ("PORT", "8000"),
            ("DEBUG", "false")
        ]
        
        for i, (key, value) in enumerate(critical_vars, 1):
            print(f"   {i:2d}. {key} = {value}")
        
        print("")
        print("5. 💾 Save Changes")
        print("6. 🔄 Wait for automatic redeploy")
        print("7. 🧪 Test: https://unioncoin.onrender.com")
        print("8. 📱 Test: @tokenuchunku12bot")
        
        return True
    
    def show_database_connection_test(self):
        """Show database connection test"""
        print("\n🧪 DATABASE CONNECTION TEST")
        print("=" * 80)
        
        # Create database URLs
        internal_db_url = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
        external_db_url = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host_external}/{self.db_name}"
        
        print("📋 PSQL COMMANDS:")
        print(f"🔗 Internal: PASSWORD={self.db_password} psql -h {self.db_host} -U {self.db_user} {self.db_name}")
        print(f"🔗 External: PASSWORD={self.db_password} psql -h {self.db_host_external} -U {self.db_user} {self.db_name}")
        print("")
        print("📋 PYTHON TEST:")
        print("import psycopg2")
        print(f"conn = psycopg2.connect('{internal_db_url}')")
        print("print('✅ Database connected successfully!')")
        print("conn.close()")
        
        return True

def main():
    """Main function"""
    print("🔧 UnionCoin Final Environment Configuration")
    print("=" * 80)
    print(f"📅 Config Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    config = FinalEnvConfig()
    
    while True:
        print("\n📋 CONFIGURATION OPTIONS:")
        print("1. 🗄️ Show Database Information")
        print("2. 📝 Create Final .env File")
        print("3. 📤 Create Render Upload Script")
        print("4. 🌐 Render.com Manual Configuration")
        print("5. 🧪 Database Connection Test")
        print("6. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-6): ").strip()
        
        if choice == "1":
            config.show_database_info()
        elif choice == "2":
            config.create_final_env_file()
        elif choice == "3":
            config.create_render_env_upload_script()
        elif choice == "4":
            config.show_render_manual_config()
        elif choice == "5":
            config.show_database_connection_test()
        elif choice == "6":
            print("👋 Good luck with deployment!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
