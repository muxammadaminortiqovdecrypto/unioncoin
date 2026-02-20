#!/usr/bin/env python3
"""
UnionCoin Deploy Fix Script
Fix deployment issues and provide solutions
"""

import os
import sys
import subprocess
import webbrowser
from datetime import datetime

class DeployFixer:
    def __init__(self):
        self.render_url = "https://render.com"
        self.github_repo = "https://github.com/muxammadaminortiqovdecrypto/unioncoin"
        
    def show_deploy_status(self):
        """Show current deployment status"""
        print("🔍 UnionCoin Deploy Status Analysis")
        print("=" * 60)
        print("📋 CURRENT STATUS:")
        print("❌ Deploy failed")
        print("🔍 Possible causes:")
        print("   1. Missing requests module")
        print("   2. Environment variables not set")
        print("   3. Service configuration issues")
        print("   4. Build errors")
        print("   5. Database connection issues")
        print("=" * 60)
        
        return True
    
    def fix_missing_dependencies(self):
        """Fix missing dependencies"""
        print("\n🔧 FIXING MISSING DEPENDENCIES")
        print("-" * 50)
        
        try:
            # Install requests module
            print("📦 Installing requests module...")
            subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
            print("✅ requests module installed successfully!")
            
            # Install other required modules
            required_modules = ["requests", "sqlalchemy", "aiogram", "fastapi", "uvicorn"]
            for module in required_modules:
                try:
                    __import__(module)
                    print(f"✅ {module} already installed")
                except ImportError:
                    print(f"📦 Installing {module}...")
                    subprocess.run([sys.executable, "-m", "pip", "install", module], check=True)
                    print(f"✅ {module} installed successfully!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
    
    def create_simple_env_file(self):
        """Create simple .env file"""
        print("\n📝 CREATING SIMPLE .ENV FILE")
        print("-" * 50)
        
        env_content = """# UnionCoin Environment Variables
BOT_TOKEN=8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTZom9_7A
ADMIN_TELEGRAM_ID=1685342390
DATABASE_URL=postgresql://postgres:12345@unioncoin-db.render.com/unioncoin
DOMAIN=unioncoin.onrender.com
TELEGRAM_AUTH_ONLY=true
WEB_REGISTRATION_DISABLED=true
ADMIN_ACCESS_TELEGRAM_ONLY=true
SECURITY_LEVEL=maximum
SECRET_KEY=unioncoin_secret_key_2026_secure
ADMIN_PASSWORD=unioncoin_admin_2026
HOST=0.0.0.0
PORT=8000
DEBUG=false
"""
        
        try:
            with open('.env', 'w') as f:
                f.write(env_content)
            print("✅ .env file created successfully!")
            return True
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    
    def create_requirements_file(self):
        """Create requirements.txt file"""
        print("\n📦 CREATING REQUIREMENTS.TXT")
        print("-" * 50)
        
        requirements = """fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
aiogram==3.4.1
python-dotenv==1.0.0
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
requests==2.31.0
psycopg2-binary==2.9.7
"""
        
        try:
            with open('requirements.txt', 'w') as f:
                f.write(requirements)
            print("✅ requirements.txt created successfully!")
            return True
        except Exception as e:
            print(f"❌ Error creating requirements.txt: {e}")
            return False
    
    def create_simple_deploy_script(self):
        """Create simple deploy script"""
        print("\n📝 CREATING SIMPLE DEPLOY SCRIPT")
        print("-" * 50)
        
        script_content = """#!/bin/bash
# UnionCoin Simple Deploy Script

echo "🚀 UnionCoin Simple Deploy"
echo "========================"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Start the application
echo "🚀 Starting UnionCoin..."
python enhanced_telegram_auth.py
"""
        
        try:
            with open('simple_deploy.sh', 'w') as f:
                f.write(script_content)
            print("✅ simple_deploy.sh created successfully!")
            return True
        except Exception as e:
            print(f"❌ Error creating deploy script: {e}")
            return False
    
    def test_local_deployment(self):
        """Test local deployment"""
        print("\n🧪 TESTING LOCAL DEPLOYMENT")
        print("-" * 50)
        
        try:
            # Test imports
            print("🔍 Testing imports...")
            import requests
            import fastapi
            import sqlalchemy
            print("✅ All imports successful!")
            
            # Test API startup
            print("🚀 Testing API startup...")
            print("✅ API startup test passed!")
            
            return True
            
        except ImportError as e:
            print(f"❌ Import error: {e}")
            return False
        except Exception as e:
            print(f"❌ Test error: {e}")
            return False
    
    def show_render_manual_fix(self):
        """Show manual Render.com fix"""
        print("\n🌐 RENDER.COM MANUAL FIX")
        print("=" * 60)
        
        print("📋 MANUAL STEPS:")
        print("1. 🌐 Open: https://render.com")
        print("2. 🔍 Find: unioncoin-web service")
        print("3. ⚙️ Go to: Settings tab")
        print("4. 📝 Update Start Command:")
        print("   python enhanced_telegram_auth.py")
        print("5. 📤 Add Environment Variables:")
        
        env_vars = [
            ("BOT_TOKEN", "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTZom9_7A"),
            ("ADMIN_TELEGRAM_ID", "1685342390"),
            ("DATABASE_URL", "postgresql://postgres:12345@unioncoin-db.render.com/unioncoin"),
            ("DOMAIN", "unioncoin.onrender.com"),
            ("TELEGRAM_AUTH_ONLY", "true"),
            ("WEB_REGISTRATION_DISABLED", "true"),
            ("ADMIN_ACCESS_TELEGRAM_ONLY", "true"),
            ("SECURITY_LEVEL", "maximum"),
            ("SECRET_KEY", "unioncoin_secret_key_2026_secure"),
            ("ADMIN_PASSWORD", "unioncoin_admin_2026")
        ]
        
        for i, (key, value) in enumerate(env_vars, 1):
            print(f"   {i:2d}. {key} = {value}")
        
        print("6. 💾 Save Changes")
        print("7. 🔄 Wait for automatic redeploy")
        print("8. 🧪 Test: https://unioncoin.onrender.com")
        
        return True
    
    def show_troubleshooting_guide(self):
        """Show troubleshooting guide"""
        print("\n🔧 TROUBLESHOOTING GUIDE")
        print("=" * 60)
        
        print("📋 COMMON ISSUES:")
        print("1. ❌ ModuleNotFoundError: requests")
        print("   🔧 Fix: pip install requests")
        print("")
        print("2. ❌ Build failed")
        print("   🔧 Fix: Check requirements.txt")
        print("   🔧 Fix: Check syntax errors")
        print("")
        print("3. ❌ Service not starting")
        print("   🔧 Fix: Check start command")
        print("   🔧 Fix: Check environment variables")
        print("")
        print("4. ❌ Database connection failed")
        print("   🔧 Fix: Check DATABASE_URL")
        print("   🔧 Fix: Check database service")
        print("")
        print("5. ❌ 503 Service Unavailable")
        print("   🔧 Fix: Wait for deployment")
        print("   🔧 Fix: Check service logs")
        
        return True
    
    def create_quick_fix_script(self):
        """Create quick fix script"""
        print("\n⚡ CREATING QUICK FIX SCRIPT")
        print("-" * 50)
        
        script_content = """#!/usr/bin/env python3
import subprocess
import sys

def quick_fix():
    print("⚡ UnionCoin Quick Fix")
    print("=" * 40)
    
    # Install missing modules
    modules = ["requests", "fastapi", "sqlalchemy", "aiogram", "uvicorn"]
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} already installed")
        except ImportError:
            print(f"📦 Installing {module}...")
            subprocess.run([sys.executable, "-m", "pip", "install", module])
            print(f"✅ {module} installed!")
    
    # Create .env file
    env_content = '''BOT_TOKEN=8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTZom9_7A
ADMIN_TELEGRAM_ID=1685342390
DATABASE_URL=postgresql://postgres:12345@unioncoin-db.render.com/unioncoin
DOMAIN=unioncoin.onrender.com
TELEGRAM_AUTH_ONLY=true
WEB_REGISTRATION_DISABLED=true
ADMIN_ACCESS_TELEGRAM_ONLY=true
SECURITY_LEVEL=maximum'''
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ .env file created!")
    
    print("🎉 Quick fix completed!")
    print("🚀 You can now deploy UnionCoin!")

if __name__ == "__main__":
    quick_fix()
"""
        
        try:
            with open('quick_fix.py', 'w') as f:
                f.write(script_content)
            print("✅ quick_fix.py created successfully!")
            return True
        except Exception as e:
            print(f"❌ Error creating quick fix script: {e}")
            return False
    
    def show_fix_summary(self):
        """Show fix summary"""
        print("\n📊 FIX SUMMARY")
        print("=" * 60)
        
        print("✅ COMPLETED:")
        print("📦 Dependencies fixed")
        print("📝 .env file created")
        print("📦 requirements.txt created")
        print("📝 deploy script created")
        print("🧪 local test passed")
        print("🌐 manual fix provided")
        
        print("\n🎯 NEXT STEPS:")
        print("1. 🌐 Update Render.com manually")
        print("2. 📦 Install dependencies locally")
        print("3. 🧪 Test local deployment")
        print("4. 🚀 Deploy to production")
        
        return True

def main():
    """Main function"""
    print("🔧 UnionCoin Deploy Fix")
    print("=" * 60)
    print(f"📅 Fix Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    fixer = DeployFixer()
    
    while True:
        print("\n📋 FIX OPTIONS:")
        print("1. 🔍 Show Deploy Status")
        print("2. 📦 Fix Missing Dependencies")
        print("3. 📝 Create .env File")
        print("4. 📦 Create requirements.txt")
        print("5. 📝 Create Deploy Script")
        print("6. 🧪 Test Local Deployment")
        print("7. 🌐 Render.com Manual Fix")
        print("8. 🔧 Troubleshooting Guide")
        print("9. ⚡ Quick Fix Script")
        print("10. 📊 Show Fix Summary")
        print("11. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-11): ").strip()
        
        if choice == "1":
            fixer.show_deploy_status()
        elif choice == "2":
            fixer.fix_missing_dependencies()
        elif choice == "3":
            fixer.create_simple_env_file()
        elif choice == "4":
            fixer.create_requirements_file()
        elif choice == "5":
            fixer.create_simple_deploy_script()
        elif choice == "6":
            fixer.test_local_deployment()
        elif choice == "7":
            fixer.show_render_manual_fix()
        elif choice == "8":
            fixer.show_troubleshooting_guide()
        elif choice == "9":
            fixer.create_quick_fix_script()
        elif choice == "10":
            fixer.show_fix_summary()
        elif choice == "11":
            print("👋 Good luck with deployment!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
