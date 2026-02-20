#!/usr/bin/env python3
"""
UnionCoin Render.com Environment Variable Fix
Fix environment variable format for new Render.com interface
"""

import webbrowser
import requests
import json
import time

class RenderEnvFix:
    def __init__(self):
        self.render_api_key = "YOUR_RENDER_API_KEY"
        self.service_name = "unioncoin-web"
        self.admin_url = "https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026"
        
    def show_new_interface_guide(self):
        """Show guide for new Render.com interface"""
        print("🔧 Render.com New Interface Guide")
        print("=" * 60)
        
        print("\n📋 NEW RENDER.COM INTERFACE:")
        print("=" * 40)
        
        print("\n🔍 WHAT'S DIFFERENT:")
        print("• Old interface: Simple key-value pairs")
        print("• New interface: Groups with multiple variables")
        print("• Group name: Required field")
        print("• Variable name: Required field")
        print("• Variable value: Required field")
        
        print("\n📝 HOW TO ADD ADMIN_PASSWORD:")
        print("=" * 40)
        
        print("\n🎯 METHOD 1: Via Web Interface")
        print("-" * 40)
        print("1. 🌐 Go to: https://render.com")
        print("2. 👤 Login to your account")
        print("3. 📊 Find 'unioncoin-web' service")
        print("4. ⚙️ Click on service name")
        print("5. 📋 Go to 'Environment' tab")
        print("6. ➕ Click 'Add Environment Variable'")
        print("7. 📝 Fill in the form:")
        print("   • Group Name: unioncoin-admin")
        print("   • Variable Name: ADMIN_PASSWORD")
        print("   • Variable Value: unioncoin_admin_2026")
        print("   • Type: Plain text")
        print("8. ✅ Click 'Save'")
        print("9. ⏳ Wait 2-3 minutes for restart")
        
        print("\n🎯 METHOD 2: Via API (Recommended)")
        print("-" * 40)
        print("1. 🔑 Get your Render API key")
        print("   • Go to: https://render.com")
        print("   • Account → Settings → API Keys")
        print("   • Click 'Create API Key'")
        print("2. 🚀 Run this script with API key")
        print("   • python render_env_fix.py")
        print("   • Choose option 2 (API Method)")
        print("3. ✅ Automatic fix")
        
        print("\n📋 ENVIRONMENT VARIABLE FORMAT:")
        print("=" * 40)
        print("\n🔑 Required Format:")
        print("• Group Name: unioncoin-admin")
        print("• Variable Name: ADMIN_PASSWORD")
        print("• Variable Value: unioncoin_admin_2026")
        print("• Type: Plain text")
        
        print("\n📝 Example:")
        print("Group Name: unioncoin-admin")
        print("├── Variable Name: ADMIN_PASSWORD")
        print("│   └── Variable Value: unioncoin_admin_2026")
        print("├── Variable Name: BOT_TOKEN")
        print("│   └── Variable Value: 8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A")
        print("└── Variable Name: DATABASE_URL")
        print("    └── Variable Value: postgresql://...")
        
        return True
    
    def fix_via_api(self, api_key):
        """Fix environment variables via API"""
        print("🔧 Fixing environment variables via API...")
        
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
                        
                        # Delete existing ADMIN_PASSWORD if exists
                        self.delete_existing_env_var(service_id, headers)
                        
                        # Add new environment variable with group
                        env_data = {
                            'groupId': 'unioncoin-admin',
                            'envVars': [
                                {
                                    'key': 'ADMIN_PASSWORD',
                                    'value': 'unioncoin_admin_2026'
                                },
                                {
                                    'key': 'BOT_TOKEN',
                                    'value': '8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A'
                                },
                                {
                                    'key': 'DATABASE_URL',
                                    'value': 'postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin'
                                }
                            ]
                        }
                        
                        # Add environment variables
                        add_response = requests.post(
                            f'https://api.render.com/v1/services/{service_id}/env-vars',
                            headers=headers,
                            json=env_data
                        )
                        
                        if add_response.status_code == 201:
                            print("✅ Environment variables added successfully!")
                            print("📋 Added variables:")
                            print("   • Group: unioncoin-admin")
                            print("   • ADMIN_PASSWORD: unioncoin_admin_2026")
                            print("   • BOT_TOKEN: [HIDDEN]")
                            print("   • DATABASE_URL: [HIDDEN]")
                            
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
                        else:
                            print(f"❌ Failed to add env vars: {add_response.status_code}")
                            print(f"   Error: {add_response.text}")
                            return False
                        
                print("❌ Service not found!")
                return False
                
        except Exception as e:
            print(f"❌ API error: {e}")
            return False
    
    def delete_existing_env_var(self, service_id, headers):
        """Delete existing ADMIN_PASSWORD environment variable"""
        try:
            # Get existing env vars
            response = requests.get(
                f'https://api.render.com/v1/services/{service_id}/env-vars',
                headers=headers
            )
            
            if response.status_code == 200:
                env_vars = response.json()
                
                for env_var in env_vars:
                    if env_var.get('key') == 'ADMIN_PASSWORD':
                        env_id = env_var.get('id')
                        
                        # Delete existing
                        delete_response = requests.delete(
                            f'https://api.render.com/v1/services/{service_id}/env-vars/{env_id}',
                            headers=headers
                        )
                        
                        if delete_response.status_code == 204:
                            print("🗑️ Deleted existing ADMIN_PASSWORD")
                        else:
                            print(f"⚠️ Failed to delete existing: {delete_response.status_code}")
                        
                        break
                        
        except Exception as e:
            print(f"⚠️ Error checking existing env vars: {e}")
    
    def test_admin_panel(self):
        """Test admin panel access"""
        print("🧪 Testing admin panel...")
        
        try:
            response = requests.get(self.admin_url, timeout=10)
            
            if response.status_code == 200:
                print("✅ Admin panel working!")
                data = response.json()
                print(f"   👥 Users: {data.get('total_users', 0)}")
                print(f"   🔗 Transactions: {data.get('total_transactions', 0)}")
                print(f"   💰 Total Balance: {data.get('total_balance', 0)}")
                return True
            else:
                print(f"❌ Admin panel error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False
    
    def open_render_dashboard(self):
        """Open Render dashboard"""
        print("🌐 Opening Render dashboard...")
        webbrowser.open("https://render.com")
        return True
    
    def show_api_key_help(self):
        """Show how to get API key"""
        print("🔑 How to Get Render API Key:")
        print("=" * 40)
        
        print("\n1️⃣ Go to Render.com:")
        print("   🌐 https://render.com")
        
        print("\n2️⃣ Navigate to Account Settings:")
        print("   👤 Click on your avatar (top right)")
        print("   ⚙️ Click 'Account Settings'")
        
        print("\n3️⃣ Go to API Keys:")
        print("   🔑 Scroll down to 'API Keys' section")
        print("   ➕ Click 'Create API Key'")
        
        print("\n4️⃣ Create API Key:")
        print("   📝 Name: unioncoin-deployment")
        print("   📅 Expiration: 90 days (recommended)")
        print("   ✅ Click 'Create API Key'")
        
        print("\n5️⃣ Copy API Key:")
        print("   📋 Click 'Copy' button")
        print("   📝 Save it securely")
        
        print("\n⚠️ IMPORTANT:")
        print("• Keep API key secret!")
        print("• Don't share it with anyone!")
        print("• Store it securely!")
        
        return True
    
    def show_quick_reference(self):
        """Show quick reference"""
        print("\n⚡ QUICK REFERENCE:")
        print("=" * 30)
        
        print("\n🔑 Environment Variables:")
        print("Group Name: unioncoin-admin")
        print("├── ADMIN_PASSWORD: unioncoin_admin_2026")
        print("├── BOT_TOKEN: 8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A")
        print("└── DATABASE_URL: postgresql://...")
        
        print("\n🌐 URLs:")
        print("• Render: https://render.com")
        print("• Admin: https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026")
        print("• Health: https://unioncoin.onrender.com/health")
        
        return True

def main():
    """Main environment fix menu"""
    print("🔧 UnionCoin Render.com Environment Variable Fix")
    print("=" * 60)
    
    fixer = RenderEnvFix()
    
    while True:
        print("\n📋 Environment Variable Fix Options:")
        print("1. 📖 Show New Interface Guide")
        print("2. 🔧 Fix via API (Recommended)")
        print("3. 🧪 Test Admin Panel")
        print("4. 🌐 Open Render Dashboard")
        print("5. 🔑 API Key Help")
        print("6. ⚡ Quick Reference")
        print("7. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-7): ").strip()
        
        if choice == "1":
            fixer.show_new_interface_guide()
        elif choice == "2":
            api_key = input("🔑 Render API Key: ").strip()
            if api_key:
                fixer.fix_via_api(api_key)
        elif choice == "3":
            fixer.test_admin_panel()
        elif choice == "4":
            fixer.open_render_dashboard()
        elif choice == "5":
            fixer.show_api_key_help()
        elif choice == "6":
            fixer.show_quick_reference()
        elif choice == "7":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
