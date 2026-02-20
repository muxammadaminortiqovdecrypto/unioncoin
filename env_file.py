#!/usr/bin/env python3
"""
UnionCoin Environment File Creator
Create .env file with all required variables
"""

import os
from datetime import datetime

def create_env_file():
    """Create .env file with all environment variables"""
    print("🔑 Creating UnionCoin Environment File")
    print("=" * 50)
    
    # Environment variables
    env_vars = {
        'DATABASE_URL': 'postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin',
        'BOT_TOKEN': '8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A',
        'ADMIN_ID': '1685342390',
        'SECRET_KEY': 'unioncoin_production_secret_key_2026',
        'ADMIN_PASSWORD': 'unioncoin_admin_2026',
        'HOST': '0.0.0.0',
        'PORT': '8000',
        'DEBUG': 'False',
        'PYTHON_VERSION': '3.11',
        'ALLOWED_ORIGINS': 'https://unioncoin.onrender.com',
        'DB_HOST': 'localhost',
        'DB_PORT': '5432',
        'DB_NAME': 'unioncoin',
        'DB_USER': 'postgres',
        'DB_PASSWORD': '12345',
        'MAX_WORKERS': '4',
        'WORKER_CONNECTIONS': '1000',
        'KEEPALIVE_TIMEOUT': '65',
        'MONITORING_ENABLED': 'True',
        'LOG_LEVEL': 'INFO',
        'LOG_FILE': '/var/log/unioncoin/unioncoin.log',
        'RATE_LIMIT_ENABLED': 'True',
        'RATE_LIMIT_REQUESTS': '100',
        'RATE_LIMIT_WINDOW': '60'
    }
    
    # Create .env content
    env_content = f"""# UnionCoin Production Environment Configuration
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Database Configuration
DATABASE_URL={env_vars['DATABASE_URL']}
DB_HOST={env_vars['DB_HOST']}
DB_PORT={env_vars['DB_PORT']}
DB_NAME={env_vars['DB_NAME']}
DB_USER={env_vars['DB_USER']}
DB_PASSWORD={env_vars['DB_PASSWORD']}

# Telegram Bot Configuration
BOT_TOKEN={env_vars['BOT_TOKEN']}
ADMIN_ID={env_vars['ADMIN_ID']}

# Security Configuration
SECRET_KEY={env_vars['SECRET_KEY']}
ADMIN_PASSWORD={env_vars['ADMIN_PASSWORD']}

# Server Configuration
HOST={env_vars['HOST']}
PORT={env_vars['PORT']}
DEBUG={env_vars['DEBUG']}
PYTHON_VERSION={env_vars['PYTHON_VERSION']}
ALLOWED_ORIGINS={env_vars['ALLOWED_ORIGINS']}

# Performance Configuration
MAX_WORKERS={env_vars['MAX_WORKERS']}
WORKER_CONNECTIONS={env_vars['WORKER_CONNECTIONS']}
KEEPALIVE_TIMEOUT={env_vars['KEEPALIVE_TIMEOUT']}

# Monitoring Configuration
MONITORING_ENABLED={env_vars['MONITORING_ENABLED']}
LOG_LEVEL={env_vars['LOG_LEVEL']}
LOG_FILE={env_vars['LOG_FILE']}

# Rate Limiting Configuration
RATE_LIMIT_ENABLED={env_vars['RATE_LIMIT_ENABLED']}
RATE_LIMIT_REQUESTS={env_vars['RATE_LIMIT_REQUESTS']}
RATE_LIMIT_WINDOW={env_vars['RATE_LIMIT_WINDOW']}

# CORS Configuration
CORS_ORIGINS=https://unioncoin.onrender.com,http://localhost:8000

# SSL Configuration
SSL_CERT_PATH=/etc/ssl/certs/unioncoin.crt
SSL_KEY_PATH=/etc/ssl/private/unioncoin.key

# Backup Configuration
BACKUP_ENABLED=True
BACKUP_INTERVAL=6  # hours
BACKUP_PATH=/var/backups/unioncoin
BACKUP_RETENTION=30  # days

# Redis Configuration (if using Redis)
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=

# Email Configuration (if using email notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=True

# Telegram Bot Additional Settings
BOT_WEBHOOK_URL=
BOT_PARSE_MODE=html
BOT_DISABLE_NOTIFICATIONS=False

# API Configuration
API_PREFIX=/api/v1
API_DOCS_URL=https://unioncoin.onrender.com/docs
API_RATE_LIMIT=100/minute

# Frontend Configuration
FRONTEND_URL=https://unioncoin.onrender.com
FRONTEND_BUILD_PATH=./static
FRONTEND_ASSETS_PATH=./static/assets

# Security Headers
SECURITY_HEADERS_ENABLED=True
SECURITY_HEADERS_X_FRAME_OPTIONS=DENY
SECURITY_HEADERS_X_CONTENT_TYPE_OPTIONS=nosniff
SECURITY_HEADERS_X_XSS_PROTECTION=1; mode=block

# Session Configuration
SESSION_SECRET_KEY={env_vars['SECRET_KEY']}
SESSION_TIMEOUT=3600  # seconds
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True

# Database Pool Configuration
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# Monitoring and Analytics
ANALYTICS_ENABLED=False
GOOGLE_ANALYTICS_ID=
SENTRY_DSN=

# Feature Flags
FEATURE_REGISTRATION_ENABLED=True
FEATURE_LOGIN_WITH_TELEGRAM=True
FEATURE_EMAIL_VERIFICATION=False
FEATURE_2FA_ENABLED=False
FEATURE_API_DOCS=True
FEATURE_ADMIN_PANEL=True

# Development/Production Flags
ENVIRONMENT=production
MAINTENANCE_MODE=False
DEBUG_SQL=False
"""
    
    # Write to .env file
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ .env file created successfully!")
        print(f"📁 Location: {os.path.abspath('.env')}")
        print("\n📋 Environment Variables Created:")
        print("-" * 40)
        
        for key, value in env_vars.items():
            print(f"📝 {key}: {value}")
        
        print("\n🎯 NEXT STEPS:")
        print("1. 📁 Copy .env file to your deployment location")
        print("2. 🚀 Run your deployment script")
        print("3. 🌐 Test your application")
        print("4. 📊 Monitor your services")
        
        print("\n🔑 IMPORTANT:")
        print("• Keep this file secure and private")
        print("• Don't commit .env to version control")
        print("• Update variables as needed for your environment")
        print("• Test all services after deployment")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def show_env_file_location():
    """Show where .env file should be located"""
    print("📁 .env File Location Guide")
    print("=" * 40)
    
    current_dir = os.getcwd()
    env_path = os.path.join(current_dir, '.env')
    
    print(f"\n📍 Current Directory: {current_dir}")
    print(f"🎯 Expected .env Location: {env_path}")
    
    print("\n📋 How to Use:")
    print("1. 📝 The .env file has been created in current directory")
    print("2. 📁 Copy this file to your deployment location")
    print("3. 🚀 Use it with your deployment script")
    print("4. 🌐 Test your application")
    
    print("\n🔑 Security Notes:")
    print("• Never share this file publicly")
    print("• Add .env to .gitignore")
    print("• Use different values for production")
    print("• Update tokens and passwords regularly")
    
    return True

def create_render_env_upload():
    """Create Render.com environment upload script"""
    print("🚀 Creating Render.com Environment Upload Script")
    print("=" * 60)
    
    upload_script = '''#!/bin/bash
# UnionCoin Render.com Environment Upload Script
echo "🚀 UnionCoin Render.com Environment Upload"
echo "===================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "📝 Please run: python env_file.py"
    exit 1
fi

echo "📁 Found .env file"
echo "🌐 Opening Render dashboard..."

# Open Render dashboard
if command -v xdg-open > /dev/null; then
    xdg-open "https://render.com"
elif command -v open > /dev/null; then
    open "https://render.com"
else
    echo "🌐 Please open: https://render.com"
fi

echo ""
echo "📋 STEPS TO UPLOAD ENVIRONMENT:"
echo "1. 🔗 Go to your unioncoin-web service"
echo "2. ⚙️ Click on 'Environment' tab"
echo "3. ➕ Click 'Add Environment Variable'"
echo "4. 📝 Add variables from .env file:"
echo ""

# Read and display .env variables
while IFS='=' read -r key value; do
    if [[ $key != \#* ]]; then
        echo "   • $key: $value"
    fi
done < .env

echo ""
echo "5. ✅ Click 'Save' after each variable"
echo "6. 🔄 Service will restart automatically"
echo "7. 🧪 Test your admin panel: https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026"
echo ""
echo "🎉 Environment upload completed!"
'''
    
    with open('render_env_upload.sh', 'w') as f:
        f.write(upload_script)
    
    print("✅ Render environment upload script created: render_env_upload.sh")
    return True

def main():
    """Main function"""
    print("🔑 UnionCoin Environment File Creator")
    print("=" * 50)
    
    while True:
        print("\n📋 ENVIRONMENT FILE OPTIONS:")
        print("1. 🔧 Create .env File")
        print("2. 📁 Show .env File Location")
        print("3. 🚀 Create Render Upload Script")
        print("4. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-4): ").strip()
        
        if choice == "1":
            create_env_file()
        elif choice == "2":
            show_env_file_location()
        elif choice == "3":
            create_render_env_upload()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
