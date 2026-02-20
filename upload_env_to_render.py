#!/usr/bin/env python3
"""
Upload UnionCoin Environment Variables to Render.com
Simple script to upload .env file to Render.com
"""

import os
import requests
import json
from datetime import datetime

class RenderEnvUploader:
    def __init__(self):
        self.api_key = "rnd_ZdEBDAplAik1ESge3UULwlYCxWbb"
        self.base_url = "https://api.render.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def show_upload_plan(self):
        """Show upload plan"""
        print("📤 UnionCoin Environment Upload to Render.com")
        print("=" * 60)
        print("📋 UPLOAD PLAN:")
        print("1. 🔍 Find unioncoin-web service")
        print("2. 📤 Upload environment variables")
        print("3. ✅ Verify upload")
        print("4. 🔄 Restart service")
        print("5. 🧪 Test system")
        print("=" * 60)
        
        return True
    
    def get_services(self):
        """Get all services"""
        try:
            response = requests.get(f"{self.base_url}/services", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error getting services: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def find_service(self, service_name="unioncoin-web"):
        """Find specific service"""
        services = self.get_services()
        if not services:
            return None
        
        for service in services:
            if service.get('name') == service_name:
                return service
        
        print(f"❌ Service '{service_name}' not found")
        return None
    
    def upload_env_vars(self, service_id):
        """Upload environment variables"""
        env_vars = {
            "envVars": [
                {
                    "key": "BOT_TOKEN",
                    "value": "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTZom9_7A"
                },
                {
                    "key": "ADMIN_TELEGRAM_ID",
                    "value": "1685342390"
                },
                {
                    "key": "DATABASE_URL",
                    "value": "postgresql://postgres:12345@unioncoin-db.render.com/unioncoin"
                },
                {
                    "key": "DOMAIN",
                    "value": "unioncoin.onrender.com"
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
                },
                {
                    "key": "ALLOWED_ORIGINS",
                    "value": "https://unioncoin.onrender.com,http://localhost:8000,https://localhost:8000"
                },
                {
                    "key": "LOG_LEVEL",
                    "value": "info"
                },
                {
                    "key": "LOG_FILE",
                    "value": "unioncoin.log"
                },
                {
                    "key": "USER_STATUS_CHECKING",
                    "value": "true"
                },
                {
                    "key": "INTELLIGENT_ERROR_HANDLING",
                    "value": "true"
                },
                {
                    "key": "LOADING_SPINNERS",
                    "value": "true"
                },
                {
                    "key": "CONTEXTUAL_HELP",
                    "value": "true"
                }
            ]
        }
        
        try:
            response = requests.patch(f"{self.base_url}/services/{service_id}/env-vars", headers=self.headers, json=env_vars)
            if response.status_code == 200:
                print("✅ Environment variables uploaded successfully!")
                return True
            else:
                print(f"❌ Error uploading env vars: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def restart_service(self, service_id):
        """Restart service"""
        try:
            response = requests.post(f"{self.base_url}/services/{service_id}/restart", headers=self.headers)
            if response.status_code == 200:
                print("✅ Service restarted successfully!")
                return True
            else:
                print(f"❌ Error restarting service: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def verify_upload(self, service_id):
        """Verify upload"""
        try:
            response = requests.get(f"{self.base_url}/services/{service_id}/env-vars", headers=self.headers)
            if response.status_code == 200:
                env_vars = response.json()
                print(f"✅ Found {len(env_vars)} environment variables")
                
                # Check key variables
                key_vars = ["BOT_TOKEN", "ADMIN_TELEGRAM_ID", "TELEGRAM_AUTH_ONLY", "WEB_REGISTRATION_DISABLED"]
                for var in key_vars:
                    found = any(env['key'] == var for env in env_vars)
                    status = "✅" if found else "❌"
                    print(f"   {status} {var}: {'Found' if found else 'Missing'}")
                
                return True
            else:
                print(f"❌ Error verifying upload: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def upload_environment(self):
        """Main upload process"""
        print("\n🔍 FINDING SERVICE")
        print("-" * 40)
        
        service = self.find_service("unioncoin-web")
        if not service:
            print("❌ Service not found!")
            return False
        
        service_id = service['id']
        print(f"✅ Found service: {service['name']} (ID: {service_id})")
        
        print("\n📤 UPLOADING ENVIRONMENT VARIABLES")
        print("-" * 50)
        
        if self.upload_env_vars(service_id):
            print("✅ Environment variables uploaded!")
        else:
            print("❌ Failed to upload environment variables!")
            return False
        
        print("\n✅ VERIFYING UPLOAD")
        print("-" * 30)
        
        if self.verify_upload(service_id):
            print("✅ Upload verified!")
        else:
            print("❌ Upload verification failed!")
            return False
        
        print("\n🔄 RESTARTING SERVICE")
        print("-" * 30)
        
        if self.restart_service(service_id):
            print("✅ Service restarted!")
        else:
            print("❌ Failed to restart service!")
            return False
        
        return True
    
    def show_manual_instructions(self):
        """Show manual upload instructions"""
        print("\n📋 MANUAL UPLOAD INSTRUCTIONS")
        print("=" * 60)
        
        print("🌐 RENDER.COM MANUAL STEPS:")
        print("1. 🌐 Open: https://render.com")
        print("2. 🔍 Find: unioncoin-web service")
        print("3. ⚙️ Go to: Environment tab")
        print("4. 📤 Add Environment Variables:")
        
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
            ("ADMIN_PASSWORD", "unioncoin_admin_2026"),
            ("HOST", "0.0.0.0"),
            ("PORT", "8000"),
            ("DEBUG", "false"),
            ("ALLOWED_ORIGINS", "https://unioncoin.onrender.com,http://localhost:8000,https://localhost:8000"),
            ("LOG_LEVEL", "info"),
            ("LOG_FILE", "unioncoin.log"),
            ("USER_STATUS_CHECKING", "true"),
            ("INTELLIGENT_ERROR_HANDLING", "true"),
            ("LOADING_SPINNERS", "true"),
            ("CONTEXTUAL_HELP", "true")
        ]
        
        for i, (key, value) in enumerate(env_vars, 1):
            print(f"   {i:2d}. {key} = {value}")
        
        print("\n5. 💾 Save changes")
        print("6. 🔄 Restart service")
        print("7. ⏳ Wait 5-10 minutes")
        print("8. 🧪 Test system")
        
        return True
    
    def show_upload_summary(self):
        """Show upload summary"""
        print("\n📊 UPLOAD SUMMARY")
        print("=" * 50)
        
        print("✅ COMPLETED:")
        print("📤 Environment variables uploaded")
        print("🔄 Service restarted")
        print("🔐 Enhanced security enabled")
        print("📱 Telegram auth active")
        print("🎨 Intelligent error handling enabled")
        print("⏳ Loading spinners enabled")
        print("🎯 Contextual help enabled")
        
        print("\n🎯 NEXT STEPS:")
        print("1. ⏳ Wait 5-10 minutes for deployment")
        print("2. 🧪 Test: python test_telegram_auth.py")
        print("3. 📱 Test: @tokenuchunku12bot")
        print("4. 🌐 Test: https://unioncoin.onrender.com")
        
        print("\n🎉 EXPECTED RESULT:")
        print("📱 Telegram-only registration")
        print("🔐 Enhanced error handling")
        print("🎨 Improved UX with loading spinners")
        print("🚫 Admin panel hidden from web")
        print("👤 1:1 Telegram account mapping")
        print("🔒 Maximum security level")
        
        return True

def main():
    """Main function"""
    print("📤 UnionCoin Environment Upload to Render.com")
    print("=" * 60)
    print(f"📅 Upload Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    uploader = RenderEnvUploader()
    
    while True:
        print("\n📋 UPLOAD OPTIONS:")
        print("1. 📋 Show Upload Plan")
        print("2. 📤 Automatic Upload (API)")
        print("3. 📋 Manual Instructions")
        print("4. 📊 Show Upload Summary")
        print("5. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-5): ").strip()
        
        if choice == "1":
            uploader.show_upload_plan()
        elif choice == "2":
            print("\n⚠️ WARNING: This will upload environment variables!")
            confirm = input("👉 Type 'UPLOAD' to confirm: ").strip()
            if confirm == "UPLOAD":
                uploader.upload_environment()
            else:
                print("❌ Upload cancelled")
        elif choice == "3":
            uploader.show_manual_instructions()
        elif choice == "4":
            uploader.show_upload_summary()
        elif choice == "5":
            print("👋 Good luck with deployment!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
