#!/usr/bin/env python3
"""
UnionCoin Render.com Admin Panel Fix
Fix admin panel access by setting environment variables
"""

import webbrowser
import os

class RenderAdminFix:
    def __init__(self):
        self.render_url = "https://render.com"
        self.service_name = "unioncoin-web"
        
    def show_admin_fix_guide(self):
        """Show step-by-step admin panel fix guide"""
        print("🔧 UnionCoin Admin Panel Fix Guide")
        print("=" * 50)
        
        print("\n📋 PROBLEM:")
        print("❌ Admin panel returns 401 - Access denied")
        print("🔍 REASON: ADMIN_PASSWORD environment variable not set correctly")
        
        print("\n📋 SOLUTION:")
        print("=" * 30)
        
        print("\n1️⃣ Open Render Dashboard:")
        print("   🌐 Go to: https://render.com")
        print("   👤 Login to your account")
        print("   📊 Go to Dashboard")
        
        print("\n2️⃣ Find UnionCoin Web Service:")
        print("   🔍 Look for 'unioncoin-web' service")
        print("   📋 Click on the service name")
        print("   ⚙️ Go to 'Environment' tab")
        
        print("\n3️⃣ Add Environment Variable:")
        print("   ➕ Click 'Add Environment Variable'")
        print("   🔑 Fill in:")
        print("      • Key: ADMIN_PASSWORD")
        print("      • Value: unioncoin_admin_2026")
        print("      • Type: Plain text")
        print("   ✅ Click 'Save'")
        
        print("\n4️⃣ Restart Service:")
        print("   🔄 Go back to service dashboard")
        print("   ⚠️ Wait for service to restart")
        print("   ✅ Service will restart automatically")
        
        print("\n5️⃣ Test Admin Panel:")
        print("   🧪 Open: https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026")
        print("   🔑 Should show admin data now")
        
        print("\n📋 ALTERNATIVE: API Method")
        print("=" * 30)
        
        print("\n🔧 Alternative Fix via Render API:")
        print("1. Get your Render API key")
        print("2. Run this script with API key")
        
        return True
    
    def fix_via_api(self, api_key):
        """Fix admin panel via Render API"""
        print("🔧 Fixing admin panel via Render API...")
        
        import requests
        import json
        
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
                        
                        # Get current env vars
                        env_response = requests.get(
                            f'https://api.render.com/v1/services/{service_id}/env-vars',
                            headers=headers
                        )
                        
                        current_env_vars = env_response.json() if env_response.status_code == 200 else []
                        
                        # Check if ADMIN_PASSWORD exists
                        admin_password_exists = any(
                            env.get('key') == 'ADMIN_PASSWORD' 
                            for env in current_env_vars
                        )
                        
                        if admin_password_exists:
                            print("✅ ADMIN_PASSWORD already exists")
                            # Update it
                            for env in current_env_vars:
                                if env.get('key') == 'ADMIN_PASSWORD':
                                    env_id = env.get('id')
                                    
                                    update_response = requests.patch(
                                        f'https://api.render.com/v1/services/{service_id}/env-vars/{env_id}',
                                        headers=headers,
                                        json={'value': 'unioncoin_admin_2026'}
                                    )
                                    
                                    if update_response.status_code == 200:
                                        print("✅ ADMIN_PASSWORD updated successfully!")
                                    else:
                                        print(f"❌ Failed to update: {update_response.status_code}")
                                    break
                        else:
                            print("➕ Adding ADMIN_PASSWORD...")
                            
                            # Add new env var
                            add_response = requests.post(
                                f'https://api.render.com/v1/services/{service_id}/env-vars',
                                headers=headers,
                                json={
                                    'key': 'ADMIN_PASSWORD',
                                    'value': 'unioncoin_admin_2026'
                                }
                            )
                            
                            if add_response.status_code == 201:
                                print("✅ ADMIN_PASSWORD added successfully!")
                            else:
                                print(f"❌ Failed to add: {add_response.status_code}")
                        
                        # Trigger redeploy
                        print("🔄 Triggering redeploy...")
                        redeploy_response = requests.post(
                            f'https://api.render.com/v1/services/{service_id}/restart',
                            headers=headers
                        )
                        
                        if redeploy_response.status_code == 200:
                            print("✅ Service redeployed successfully!")
                        else:
                            print(f"❌ Failed to redeploy: {redeploy_response.status_code}")
                        
                        return True
                        
                print("❌ Service not found!")
                return False
                
        except Exception as e:
            print(f"❌ API error: {e}")
            return False
    
    def test_admin_panel(self):
        """Test admin panel access"""
        print("🧪 Testing admin panel access...")
        
        import requests
        
        test_url = "https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026"
        
        try:
            response = requests.get(test_url, timeout=10)
            
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
    
    def show_quick_commands(self):
        """Show quick reference commands"""
        print("\n⚡ QUICK REFERENCE:")
        print("=" * 30)
        
        print("\n🔑 Admin Password:")
        print("unioncoin_admin_2026")
        
        print("\n🌐 Admin Panel URL:")
        print("https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026")
        
        print("\n📊 Other URLs:")
        print("• Main: https://unioncoin.onrender.com")
        print("• Health: https://unioncoin.onrender.com/health")
        print("• Verify: https://unioncoin.onrender.com/verify")
        
        print("\n🔧 Environment Variable:")
        print("Key: ADMIN_PASSWORD")
        print("Value: unioncoin_admin_2026")
        
        return True
    
    def get_api_key_and_fix(self):
        """Get API key and fix admin panel"""
        print("🔑 Getting API key to fix admin panel...")
        
        api_key = input("👉 Render API Key: ").strip()
        
        if api_key:
            if self.fix_via_api(api_key):
                print("\n✅ Admin panel fixed via API!")
                print("🧪 Testing admin panel...")
                self.test_admin_panel()
            else:
                print("\n❌ Failed to fix admin panel via API!")
        else:
            print("\n❌ No API key provided!")
        
        return True

def main():
    """Main admin fix menu"""
    print("🔧 UnionCoin Admin Panel Fix")
    print("=" * 50)
    
    fixer = RenderAdminFix()
    
    while True:
        print("\n📋 Admin Panel Fix Options:")
        print("1. 📖 Show Fix Guide")
        print("2. 🔧 Fix via API")
        print("3. 🧪 Test Admin Panel")
        print("4. 🌐 Open Render Dashboard")
        print("5. ⚡ Quick Reference")
        print("6. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-6): ").strip()
        
        if choice == "1":
            fixer.show_admin_fix_guide()
        elif choice == "2":
            fixer.get_api_key_and_fix()
        elif choice == "3":
            fixer.test_admin_panel()
        elif choice == "4":
            fixer.open_render_dashboard()
        elif choice == "5":
            fixer.show_quick_commands()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
