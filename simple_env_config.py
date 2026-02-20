#!/usr/bin/env python3
"""
UnionCoin Simple Environment Configuration
Render.com PostgreSQL Database Setup
"""

import os
import subprocess
from datetime import datetime

# Database configuration from user
db_host = "dpg-d6c9at15pdvs738si39g-a"
db_host_external = "dpg-d6c9at15pdvs738si39g-a.oregon-postgres.render.com"
db_name = "unioncoin"
db_user = "unioncoin_user"
db_password = "R0HqXLoceeHhqba1MokFvWhEDSBcecqd"
db_port = "5432"

def show_database_info():
    """Show database information"""
    print("🗄️ UnionCoin Database Information")
    print("=" * 70)
    print("📋 DATABASE CONFIGURATION:")
    print(f"🗄️ Database: {db_name}")
    print(f"👤 Username: {db_user}")
    print(f"🔐 Password: {db_password}")
    print(f"🌐 Internal Host: {db_host}")
    print(f"🌐 External Host: {db_host_external}")
    print(f"🔌 Port: {db_port}")
    print("")
    
    # Create database URLs
    internal_db_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    external_db_url = f"postgresql://{db_user}:{db_password}@{db_host_external}/{db_name}"
    
    print("📋 DATABASE URLs:")
    print(f"🔗 Internal: {internal_db_url}")
    print(f"🔗 External: {external_db_url}")
    print("=" * 70)
    
    return internal_db_url, external_db_url

def create_env_file():
    """Create environment file"""
    print("\n📝 CREATING ENVIRONMENT FILE")
    print("-" * 70)
    
    # Create database URLs
    internal_db_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    external_db_url = f"postgresql://{db_user}:{db_password}@{db_host_external}/{db_name}"
    
    env_content = f"""# UnionCoin Environment Configuration
# Render.com PostgreSQL Database Setup

# Database Configuration (CRITICAL)
DATABASE_URL={internal_db_url}
DATABASE_URL_EXTERNAL={external_db_url}
DATABASE_URL_INTERNAL={internal_db_url}
DB_HOST={db_host}
DB_HOST_EXTERNAL={db_host_external}
DB_PORT={db_port}
DB_NAME={db_name}
DB_USER={db_user}
DB_PASSWORD={db_password}

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

def show_render_manual_config():
    """Show Render.com manual configuration"""
    print("\n🌐 RENDER.COM MANUAL CONFIGURATION")
    print("=" * 80)
    
    # Create database URLs
    internal_db_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    
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

def show_database_connection_test():
    """Show database connection test"""
    print("\n🧪 DATABASE CONNECTION TEST")
    print("=" * 80)
    
    print("📋 PSQL COMMANDS:")
    print(f"🔗 Internal: PASSWORD={db_password} psql -h {db_host} -U {db_user} {db_name}")
    print(f"🔗 External: PASSWORD={db_password} psql -h {db_host_external} -U {db_user} {db_name}")
    print("")
    print("📋 PYTHON TEST:")
    internal_db_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    print("import psycopg2")
    print(f"conn = psycopg2.connect('{internal_db_url}')")
    print("print('✅ Database connected successfully!')")
    print("conn.close()")
    
    return True

def create_quick_deploy_script():
    """Create quick deploy script"""
    print("\n🚀 CREATING QUICK DEPLOY SCRIPT")
    print("-" * 70)
    
    internal_db_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    
    script_content = f"""#!/bin/bash
# UnionCoin Quick Deploy Script
# Render.com PostgreSQL Database Setup

echo "🚀 UnionCoin Quick Deploy"
echo "========================"

# Install dependencies
echo "📦 Installing dependencies..."
pip install fastapi uvicorn sqlalchemy aiogram python-dotenv psycopg2-binary requests passlib python-jose

# Set environment variables
echo "🔧 Setting environment variables..."
export DATABASE_URL="{internal_db_url}"
export BOT_TOKEN="8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTZom9_7A"
export ADMIN_TELEGRAM_ID="1685342390"
export TELEGRAM_AUTH_ONLY="true"
export WEB_REGISTRATION_DISABLED="true"
export ADMIN_ACCESS_TELEGRAM_ONLY="true"
export SECURITY_LEVEL="maximum"
export SECRET_KEY="unioncoin_secret_key_2026_secure"
export ADMIN_PASSWORD="unioncoin_admin_2026"
export DOMAIN="unioncoin.onrender.com"
export HOST="0.0.0.0"
export PORT="8000"
export DEBUG="false"

# Start application
echo "🚀 Starting UnionCoin..."
python enhanced_telegram_auth.py
"""
    
    try:
        with open('quick_deploy.sh', 'w') as f:
            f.write(script_content)
        print("✅ quick_deploy.sh created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating deploy script: {e}")
        return False

def main():
    """Main function"""
    print("🔧 UnionCoin Simple Environment Configuration")
    print("=" * 80)
    print(f"📅 Config Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    while True:
        print("\n📋 CONFIGURATION OPTIONS:")
        print("1. 🗄️ Show Database Information")
        print("2. 📝 Create .env File")
        print("3. 🌐 Render.com Manual Configuration")
        print("4. 🧪 Database Connection Test")
        print("5. 🚀 Create Quick Deploy Script")
        print("6. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-6): ").strip()
        
        if choice == "1":
            show_database_info()
        elif choice == "2":
            create_env_file()
        elif choice == "3":
            show_render_manual_config()
        elif choice == "4":
            show_database_connection_test()
        elif choice == "5":
            create_quick_deploy_script()
        elif choice == "6":
            print("👋 Good luck with deployment!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
