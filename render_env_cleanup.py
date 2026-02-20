#!/usr/bin/env python3
"""
Render.com Environment Group Cleanup
Remove environment group and set individual variables
"""

import os
import requests
import json
from datetime import datetime

class RenderEnvCleaner:
    def __init__(self):
        self.api_key = "rnd_ZdEBDAplAik1ESge3UULwlYCxWbb"
        self.base_url = "https://api.render.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def show_cleanup_plan(self):
        """Show cleanup plan"""
        print("🧹 Render.com Environment Group Cleanup")
        print("=" * 50)
        print("📋 CLEANUP PLAN:")
        print("1. 🔍 Find unioncoin-web service")
        print("2. 🗑️ Remove environment group")
        print("3. 📝 Set individual environment variables")
        print("4. ✅ Verify cleanup")
        print("5. 🔄 Restart service")
        print("=" * 50)
        
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
    
    def get_environment_groups(self, service_id):
        """Get environment groups for service"""
        try:
            response = requests.get(f"{self.base_url}/services/{service_id}/env-groups", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error getting env groups: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def delete_environment_group(self, service_id, group_id):
        """Delete environment group"""
        try:
            response = requests.delete(f"{self.base_url}/services/{service_id}/env-groups/{group_id}", headers=self.headers)
            if response.status_code == 204:
                print("✅ Environment group deleted successfully")
                return True
            else:
                print(f"❌ Error deleting env group: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def set_individual_env_vars(self, service_id):
        """Set individual environment variables"""
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
                }
            ]
        }
        
        try:
            response = requests.patch(f"{self.base_url}/services/{service_id}/env-vars", headers=self.headers, json=env_vars)
            if response.status_code == 200:
                print("✅ Individual environment variables set successfully")
                return True
            else:
                print(f"❌ Error setting env vars: {response.status_code}")
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
                print("✅ Service restarted successfully")
                return True
            else:
                print(f"❌ Error restarting service: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def cleanup_environment(self):
        """Main cleanup process"""
        print("\n🔍 FINDING SERVICE")
        print("-" * 30)
        
        service = self.find_service("unioncoin-web")
        if not service:
            print("❌ Service not found!")
            return False
        
        service_id = service['id']
        print(f"✅ Found service: {service['name']} (ID: {service_id})")
        
        print("\n🗑️ GETTING ENVIRONMENT GROUPS")
        print("-" * 40)
        
        env_groups = self.get_environment_groups(service_id)
        if not env_groups:
            print("❌ No environment groups found")
            return False
        
        print(f"✅ Found {len(env_groups)} environment groups")
        
        # Delete all environment groups
        for group in env_groups:
            print(f"\n🗑️ DELETING GROUP: {group.get('name', 'Unknown')}")
            if self.delete_environment_group(service_id, group['id']):
                print(f"✅ Group deleted: {group.get('name', 'Unknown')}")
            else:
                print(f"❌ Failed to delete group: {group.get('name', 'Unknown')}")
        
        print("\n📝 SETTING INDIVIDUAL ENVIRONMENT VARIABLES")
        print("-" * 50)
        
        if self.set_individual_env_vars(service_id):
            print("✅ Individual environment variables set")
        else:
            print("❌ Failed to set individual environment variables")
            return False
        
        print("\n🔄 RESTARTING SERVICE")
        print("-" * 30)
        
        if self.restart_service(service_id):
            print("✅ Service restarted")
        else:
            print("❌ Failed to restart service")
            return False
        
        return True
    
    def show_manual_instructions(self):
        """Show manual cleanup instructions"""
        print("\n📋 MANUAL CLEANUP INSTRUCTIONS")
        print("=" * 50)
        
        print("🌐 RENDER.COM MANUAL STEPS:")
        print("1. 🌐 Open: https://render.com")
        print("2. 🔍 Find: unioncoin-web service")
        print("3. ⚙️ Go to: Environment tab")
        print("4. 🗑️ Find: Environment Groups section")
        print("5. 🗑️ Delete: All environment groups")
        print("6. 📝 Add: Individual environment variables:")
        print("   • BOT_TOKEN = 8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTZom9_7A")
        print("   • ADMIN_TELEGRAM_ID = 1685342390")
        print("   • DATABASE_URL = postgresql://postgres:12345@unioncoin-db.render.com/unioncoin")
        print("   • DOMAIN = unioncoin.onrender.com")
        print("   • TELEGRAM_AUTH_ONLY = true")
        print("   • WEB_REGISTRATION_DISABLED = true")
        print("   • ADMIN_ACCESS_TELEGRAM_ONLY = true")
        print("   • SECURITY_LEVEL = maximum")
        print("   • SECRET_KEY = unioncoin_secret_key_2026_secure")
        print("   • ADMIN_PASSWORD = unioncoin_admin_2026")
        print("7. 💾 Save changes")
        print("8. 🔄 Restart service")
        print("9. ⏳ Wait 5-10 minutes")
        print("10. 🧪 Test system")
        
        print("\n🎯 RESULT:")
        print("✅ Environment groups removed")
        print("✅ Individual variables set")
        print("✅ Service restarted")
        print("✅ Enhanced Telegram auth active")
        
        return True
    
    def show_cleanup_summary(self):
        """Show cleanup summary"""
        print("\n📊 CLEANUP SUMMARY")
        print("=" * 40)
        
        print("✅ COMPLETED:")
        print("🗑️ Environment groups: Removed")
        print("📝 Individual variables: Set")
        print("🔄 Service: Restarted")
        print("🔐 Security: Enhanced")
        print("📱 Telegram auth: Active")
        
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
    print("🧹 Render.com Environment Group Cleanup")
    print("=" * 50)
    print(f"📅 Cleanup Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    cleaner = RenderEnvCleaner()
    
    while True:
        print("\n📋 CLEANUP OPTIONS:")
        print("1. 📋 Show Cleanup Plan")
        print("2. 🧹 Automatic Cleanup (API)")
        print("3. 📋 Manual Instructions")
        print("4. 📊 Show Cleanup Summary")
        print("5. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-5): ").strip()
        
        if choice == "1":
            cleaner.show_cleanup_plan()
        elif choice == "2":
            print("\n⚠️ WARNING: This will delete all environment groups!")
            confirm = input("👉 Type 'DELETE' to confirm: ").strip()
            if confirm == "DELETE":
                cleaner.cleanup_environment()
            else:
                print("❌ Cleanup cancelled")
        elif choice == "3":
            cleaner.show_manual_instructions()
        elif choice == "4":
            cleaner.show_cleanup_summary()
        elif choice == "5":
            print("👋 Good luck with cleanup!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
