#!/usr/bin/env python3
"""
UnionCoin Database Connection Fix
Fix database host name issue
"""

import os
import subprocess
from datetime import datetime

def show_database_issue():
    """Show database issue"""
    print("🔍 UnionCoin Database Connection Issue")
    print("=" * 70)
    print("📋 ERROR ANALYSIS:")
    print("❌ could not translate host name 'unioncoin-db.render.com'")
    print("❌ Name or service not known")
    print("❌ Application exited early")
    print("")
    print("🎯 ROOT CAUSE:")
    print("❌ WRONG DATABASE HOST!")
    print("❌ You're using: unioncoin-db.render.com")
    print("❌ Correct host: dpg-d6c9at15pdvs738si39g-a")
    print("")
    print("📋 CORRECT DATABASE CONFIGURATION:")
    print("✅ Host: dpg-d6c9at15pdvs738si39g-a")
    print("✅ External: dpg-d6c9at15pdvs738si39g-a.oregon-postgres.render.com")
    print("✅ Database: unioncoin")
    print("✅ User: unioncoin_user")
    print("✅ Password: R0HqXLoceeHhqba1MokFvWhEDSBcecqd")
    print("=" * 70)

def create_fixed_env_file():
    """Create fixed environment file"""
    print("\n📝 CREATING FIXED ENVIRONMENT FILE")
    print("-" * 70)
    
    # CORRECT database URLs
    internal_db_url = "postgresql://unioncoin_user:R0HqXLoceeHhqba1MokFvWhEDSBcecqd@dpg-d6c9at15pdvs738si39g-a/unioncoin"
    external_db_url = "postgresql://unioncoin_user:R0HqXLoceeHhqba1MokFvWhEDSBcecqd@dpg-d6c9at15pdvs738si39g-a.oregon-postgres.render.com/unioncoin"
    
    env_content = f"""# UnionCoin FIXED Environment Configuration
# CORRECT DATABASE HOST - NO MORE ERRORS!

# Database Configuration (FIXED)
DATABASE_URL={internal_db_url}
DATABASE_URL_EXTERNAL={external_db_url}
DATABASE_URL_INTERNAL={internal_db_url}
DB_HOST=dpg-d6c9at15pdvs738si39g-a
DB_HOST_EXTERNAL=dpg-d6c9at15pdvs738si39g-a.oregon-postgres.render.com
DB_PORT=5432
DB_NAME=unioncoin
DB_USER=unioncoin_user
DB_PASSWORD=R0HqXLoceeHhqba1MokFvWhEDSBcecqd

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
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ FIXED .env file created successfully!")
        
        # Show the critical fix
        print("\n🔧 CRITICAL FIX:")
        print("❌ OLD: postgresql://unioncoin_user:password@unioncoin-db.render.com/unioncoin")
        print("✅ NEW: postgresql://unioncoin_user:R0HqXLoceeHhqba1MokFvWhEDSBcecqd@dpg-d6c9at15pdvs738si39g-a/unioncoin")
        print("")
        print("🎯 KEY DIFFERENCE:")
        print("❌ OLD HOST: unioncoin-db.render.com (WRONG)")
        print("✅ NEW HOST: dpg-d6c9at15pdvs738si39g-a (CORRECT)")
        
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def create_render_fix_script():
    """Create Render.com fix script"""
    print("\n📤 CREATING RENDER.COM FIX SCRIPT")
    print("-" * 70)
    
    script_content = """#!/usr/bin/env python3
"""
UnionCoin Render.com Database Fix
Fix database host name issue
"""

import requests
import json

# Render.com API
API_KEY = "rnd_ZdEBDAplAik1ESge3UULwlYCxWbb"
BASE_URL = "https://api.render.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def fix_database_host():
    """Fix database host in Render.com"""
    print("🔧 Fixing database host in Render.com...")
    
    # CORRECT environment variables
    env_vars = {
        "envVars": [
            {
                "key": "DATABASE_URL",
                "value": "postgresql://unioncoin_user:R0HqXLoceeHhqba1MokFvWhEDSBcecqd@dpg-d6c9at15pdvs738si39g-a/unioncoin"
            },
            {
                "key": "DATABASE_URL_EXTERNAL",
                "value": "postgresql://unioncoin_user:R0HqXLoceeHhqba1MokFvWhEDSBcecqd@dpg-d6c9at15pdvs738si39g-a.oregon-postgres.render.com/unioncoin"
            },
            {
                "key": "DATABASE_URL_INTERNAL",
                "value": "postgresql://unioncoin_user:R0HqXLoceeHhqba1MokFvWhEDSBcecqd@dpg-d6c9at15pdvs738si39g-a/unioncoin"
            },
            {
                "key": "DB_HOST",
                "value": "dpg-d6c9at15pdvs738si39g-a"
            },
            {
                "key": "DB_HOST_EXTERNAL",
                "value": "dpg-d6c9at15pdvs738si39g-a.oregon-postgres.render.com"
            },
            {
                "key": "DB_PORT",
                "value": "5432"
            },
            {
                "key": "DB_NAME",
                "value": "unioncoin"
            },
            {
                "key": "DB_USER",
                "value": "unioncoin_user"
            },
            {
                "key": "DB_PASSWORD",
                "value": "R0HqXLoceeHhqba1MokFvWhEDSBcecqd"
            },
            {
                "key": "BOT_TOKEN",
                "value": "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTZom9_7A"
            },
            {
                "key": "ADMIN_TELEGRAM_ID",
                "value": "1685342390"
            },
            {
                "key": "TELEGRAM_AUTH_ONLY",
                "value": "true"
            },
            {
                "key": "WEB_REGISTRATION_DISABLED",
                "value": "true"
            },
            {
                "key": "ADMIN_ACCESS_TELEGRAM_ONLY",
                "value": "true"
            },
            {
                "key": "SECURITY_LEVEL",
                "value": "maximum"
            },
            {
                "key": "SECRET_KEY",
                "value": "unioncoin_secret_key_2026_secure"
            },
            {
                "key": "ADMIN_PASSWORD",
                "value": "unioncoin_admin_2026"
            },
            {
                "key": "DOMAIN",
                "value": "unioncoin.onrender.com"
            },
            {
                "key": "HOST",
                "value": "0.0.0.0"
            },
            {
                "key": "PORT",
                "value": "8000"
            },
            {
                "key": "DEBUG",
                "value": "false"
            }
        ]
    }
    
    try:
        # Get services
        response = requests.get(f"{BASE_URL}/services", headers=HEADERS)
        if response.status_code == 200:
            services = response.json()
            
            # Find unioncoin-web service
            for service in services:
                if service.get('name') == 'unioncoin-web':
                    service_id = service['id']
                    print(f"✅ Found service: {service['name']} (ID: {service_id})")
                    
                    # Update environment variables
                    response = requests.patch(f"{BASE_URL}/services/{service_id}/env-vars", headers=HEADERS, json=env_vars)
                    if response.status_code == 200:
                        print("✅ Environment variables updated successfully!")
                        
                        # Restart service
                        response = requests.post(f"{BASE_URL}/services/{service_id}/restart", headers=HEADERS)
                        if response.status_code == 200:
                            print("✅ Service restarted successfully!")
                            return True
                        else:
                            print(f"❌ Error restarting service: {response.status_code}")
                            return False
                    else:
                        print(f"❌ Error updating env vars: {response.status_code}")
                        print(f"Response: {response.text}")
                        return False
        
        print("❌ Service 'unioncoin-web' not found!")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🔧 UnionCoin Render.com Database Fix")
    print("=" * 60)
    
    print("\\n⚠️ WARNING: This will fix the database host issue!")
    confirm = input("👉 Type 'FIX' to confirm: ").strip()
    if confirm == "FIX":
        if fix_database_host():
            print("\\n🎉 Database host fixed successfully!")
            print("🔄 Wait 5-10 minutes for redeploy...")
            print("🧪 Test: https://unioncoin.onrender.com")
        else:
            print("\\n❌ Failed to fix database host!")
    else:
        print("❌ Fix cancelled")

if __name__ == "__main__":
    main()
"""
    
    try:
        with open('render_database_fix.py', 'w') as f:
            f.write(script_content)
        print("✅ render_database_fix.py created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating fix script: {e}")
        return False

def show_manual_render_fix():
    """Show manual Render.com fix"""
    print("\n🌐 MANUAL RENDER.COM FIX")
    print("=" * 70)
    
    print("📋 STEP-BY-STEP FIX:")
    print("1. 🌐 Open: https://render.com")
    print("2. 🔍 Find: unioncoin-web service")
    print("3. ⚙️ Go to: Environment tab")
    print("4. 🗑️ DELETE ALL existing environment variables")
    print("5. 📤 ADD NEW environment variables:")
    print("")
    
    # Show the critical fix
    print("🔧 CRITICAL DATABASE FIX:")
    print("❌ DELETE: DATABASE_URL=postgresql://...@unioncoin-db.render.com/...")
    print("✅ ADD: DATABASE_URL=postgresql://unioncoin_user:R0HqXLoceeHhqba1MokFvWhEDSBcecqd@dpg-d6c9at15pdvs738si39g-a/unioncoin")
    print("")
    
    critical_vars = [
        ("DATABASE_URL", "postgresql://unioncoin_user:R0HqXLoceeHhqba1MokFvWhEDSBcecqd@dpg-d6c9at15pdvs738si39g-a/unioncoin"),
        ("BOT_TOKEN", "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTZom9_7A"),
        ("ADMIN_TELEGRAM_ID", "1685342390"),
        ("TELEGRAM_AUTH_ONLY", "true"),
        ("WEB_REGISTRATION_DISABLED", "true"),
        ("ADMIN_ACCESS_TELEGRAM_ONLY", "true"),
        ("SECURITY_LEVEL", "maximum"),
        ("SECRET_KEY", "unioncoin_secret_key_2026_secure"),
        ("ADMIN_PASSWORD", "unioncoin_admin_2026"),
        ("DOMAIN", "unioncoin.onrender.com")
    ]
    
    for i, (key, value) in enumerate(critical_vars, 1):
        print(f"   {i:2d}. {key} = {value}")
    
    print("")
    print("6. 💾 Save Changes")
    print("7. 🔄 Wait for redeploy")
    print("8. 🧪 Test: https://unioncoin.onrender.com")
    print("9. 📱 Test: @tokenuchunku12bot")
    
    return True

def show_quick_fix():
    """Show quick fix"""
    print("\n⚡ QUICK FIX")
    print("=" * 70)
    
    print("🎯 ONE-LINE SOLUTION:")
    print("🔧 CHANGE DATABASE_HOST FROM 'unioncoin-db.render.com' TO 'dpg-d6c9at15pdvs738si39g-a'")
    print("")
    print("❌ WRONG: DATABASE_URL=postgresql://unioncoin_user:password@unioncoin-db.render.com/unioncoin")
    print("✅ CORRECT: DATABASE_URL=postgresql://unioncoin_user:R0HqXLoceeHhqba1MokFvWhEDSBcecqd@dpg-d6c9at15pdvs738si39g-a/unioncoin")
    print("")
    print("🌐 RENDER.COM STEPS:")
    print("1. Open: https://render.com")
    print("2. Find: unioncoin-web service")
    print("3. Go to: Environment tab")
    print("4. Update: DATABASE_URL")
    print("5. Save: Changes")
    print("6. Wait: Redeploy")
    print("7. Test: https://unioncoin.onrender.com")
    
    return True

def main():
    """Main function"""
    print("🔧 UnionCoin Database Connection Fix")
    print("=" * 70)
    print(f"📅 Fix Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    while True:
        print("\n📋 FIX OPTIONS:")
        print("1. 🔍 Show Database Issue")
        print("2. 📝 Create Fixed .env File")
        print("3. 📤 Create Render Fix Script")
        print("4. 🌐 Manual Render.com Fix")
        print("5. ⚡ Quick Fix")
        print("6. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-6): ").strip()
        
        if choice == "1":
            show_database_issue()
        elif choice == "2":
            create_fixed_env_file()
        elif choice == "3":
            create_render_fix_script()
        elif choice == "4":
            show_manual_render_fix()
        elif choice == "5":
            show_quick_fix()
        elif choice == "6":
            print("👋 Good luck with database fix!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
