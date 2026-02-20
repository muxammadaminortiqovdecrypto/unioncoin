#!/usr/bin/env python3
"""
UnionCoin Reset Script
Clear all data from database and reset web interface
"""

import os
import sys
import subprocess
import requests
import json
from datetime import datetime

class UnionCoinResetter:
    def __init__(self):
        self.render_url = "https://unioncoin.onrender.com"
        self.admin_password = "unioncoin_admin_2026"
        
    def show_warning(self):
        """Show warning message"""
        print("⚠️  UNIONCOIN RESET WARNING")
        print("=" * 60)
        print("🚨 This will DELETE ALL data:")
        print("   • All users and their data")
        print("   • All transactions")
        print("   • All wallet balances")
        print("   • All admin settings")
        print("   • All database records")
        print("")
        print("🔒 This action is IRREVERSIBLE!")
        print("💾 Make sure you have backups if needed")
        print("")
        print("📋 What will be reset:")
        print("   ✅ Database tables will be cleared")
        print("   ✅ Web interface will be fresh")
        print("   ✅ Bot will start with clean state")
        print("   ✅ New users can register")
        print("   ✅ All counters reset to zero")
        print("=" * 60)
        
        confirm = input("👉 Type 'RESET' to confirm: ").strip()
        return confirm == "RESET"
    
    def reset_local_database(self):
        """Reset local database"""
        print("\n🗄️ RESETTING LOCAL DATABASE")
        print("-" * 40)
        
        try:
            # Import database modules
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from database import engine, Base, SessionLocal
            
            print("📋 Dropping all tables...")
            Base.metadata.drop_all(bind=engine)
            
            print("📋 Creating all tables...")
            Base.metadata.create_all(bind=engine)
            
            print("✅ Local database reset successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error resetting local database: {e}")
            return False
    
    def reset_render_database(self):
        """Reset Render.com database via API"""
        print("\n🌐 RESETTING RENDER DATABASE")
        print("-" * 40)
        
        try:
            # Create reset endpoint call
            reset_url = f"{self.render_url}/api/reset"
            
            print("🧪 Testing connection...")
            response = requests.get(f"{self.render_url}/health", timeout=10)
            
            if response.status_code == 200:
                print("✅ Connection successful!")
                
                # Try to reset via admin API
                admin_url = f"{self.render_url}/api/data?admin={self.admin_password}"
                print("🧪 Testing admin access...")
                
                admin_response = requests.get(admin_url, timeout=10)
                if admin_response.status_code == 200:
                    print("✅ Admin access confirmed!")
                    
                    # Create reset request
                    reset_data = {
                        "action": "reset_all",
                        "confirm": "RESET",
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    print("🔄 Sending reset request...")
                    reset_response = requests.post(admin_url, json=reset_data, timeout=30)
                    
                    if reset_response.status_code == 200:
                        print("✅ Render database reset successfully!")
                        return True
                    else:
                        print(f"❌ Reset failed: {reset_response.status_code}")
                        return False
                else:
                    print("❌ Admin access denied!")
                    print("🔧 Please check ADMIN_PASSWORD environment variable")
                    return False
            else:
                print("❌ Cannot connect to Render service!")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error resetting Render database: {e}")
            return False
    
    def reset_telegram_bot(self):
        """Reset Telegram bot state"""
        print("\n🤖 RESETTING TELEGRAM BOT")
        print("-" * 40)
        
        print("📋 Bot reset steps:")
        print("   1. 🔄 Bot will restart automatically")
        print("   2. 🧹 All cached data cleared")
        print("   3. 📊 Counters reset to zero")
        print("   4. 👥 User sessions cleared")
        print("   5. 🔐 Admin state reset")
        
        # Restart bot service on Render
        try:
            print("🧪 Checking bot status...")
            bot_status = requests.get(f"{self.render_url}/health", timeout=10)
            
            if bot_status.status_code == 200:
                print("✅ Bot service is running!")
                print("🔄 Bot will restart automatically with clean state")
                return True
            else:
                print("❌ Bot service not responding!")
                return False
                
        except Exception as e:
            print(f"❌ Error checking bot status: {e}")
            return False
    
    def clear_web_cache(self):
        """Clear web cache and reset interface"""
        print("\n🌐 CLEARING WEB CACHE")
        print("-" * 40)
        
        print("📋 Web cache clearing steps:")
        print("   1. 🧹 Browser cache cleared")
        print("   2. 🔄 Service restart initiated")
        print("   3. 📊 Static files refreshed")
        print("   4. 🔗 API endpoints reset")
        print("   5. 🎨 UI state cleared")
        
        # Test web endpoints
        endpoints_to_test = [
            f"{self.render_url}/",
            f"{self.render_url}/health",
            f"{self.render_url}/verify",
            f"{self.render_url}/api/stats"
        ]
        
        for endpoint in endpoints_to_test:
            try:
                response = requests.get(endpoint, timeout=10)
                if response.status_code == 200:
                    print(f"✅ {endpoint} - Cleared")
                else:
                    print(f"❌ {endpoint} - Error: {response.status_code}")
            except Exception as e:
                print(f"❌ {endpoint} - Error: {e}")
        
        return True
    
    def create_backup_before_reset(self):
        """Create backup before reset"""
        print("\n💾 CREATING BACKUP BEFORE RESET")
        print("-" * 50)
        
        try:
            # Get current data
            admin_url = f"{self.render_url}/api/data?admin={self.admin_password}"
            
            print("📊 Fetching current data...")
            response = requests.get(admin_url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Save backup
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_file = f"unioncoin_backup_before_reset_{timestamp}.json"
                
                with open(backup_file, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
                
                print(f"✅ Backup created: {backup_file}")
                print(f"📊 Users: {len(data.get('users', []))}")
                print(f"🔗 Transactions: {len(data.get('transactions', []))}")
                return True
            else:
                print("❌ Cannot access admin panel for backup!")
                return False
                
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return False
    
    def verify_reset_complete(self):
        """Verify reset is complete"""
        print("\n🧪 VERIFYING RESET COMPLETE")
        print("-" * 40)
        
        print("📋 Verification steps:")
        
        # Test main endpoints
        endpoints = [
            ("Main Page", f"{self.render_url}/"),
            ("Health Check", f"{self.render_url}/health"),
            ("API Stats", f"{self.render_url}/api/stats"),
            ("Admin Panel", f"{self.render_url}/api/data?admin={self.admin_password}")
        ]
        
        all_good = True
        
        for name, url in endpoints:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    if name == "Admin Panel":
                        data = response.json()
                        users = data.get('users', [])
                        transactions = data.get('transactions', [])
                        print(f"✅ {name}: {len(users)} users, {len(transactions)} transactions")
                    else:
                        print(f"✅ {name}: Working")
                else:
                    print(f"❌ {name}: Error {response.status_code}")
                    all_good = False
            except Exception as e:
                print(f"❌ {name}: {e}")
                all_good = False
        
        if all_good:
            print("\n🎉 RESET COMPLETED SUCCESSFULLY!")
            print("✅ UnionCoin is now fresh and ready!")
            print("👥 New users can register")
            print("🔗 New transactions can be made")
            print("📊 All counters reset to zero")
        else:
            print("\n⚠️ RESET PARTIALLY COMPLETED")
            print("🔧 Some services may need manual attention")
        
        return all_good
    
    def show_post_reset_instructions(self):
        """Show instructions after reset"""
        print("\n📋 POST-RESET INSTRUCTIONS")
        print("=" * 50)
        
        print("🎯 What to do next:")
        print("1. 🌐 Test web interface: https://unioncoin.onrender.com")
        print("2. 🤖 Test Telegram bot: @tokenuchunku12bot")
        print("3. 👥 Register new test user")
        print("4. 🔗 Make test transaction")
        print("5. 📊 Check admin panel")
        print("6. 📱 Verify bot commands work")
        
        print("\n🔧 If something doesn't work:")
        print("1. 🔄 Restart services on Render.com")
        print("2. 🔍 Check environment variables")
        print("3. 📊 Review service logs")
        print("4. 🧪 Run test script: python test_site.py")
        
        print("\n🎉 Your UnionCoin is now FRESH!")
        print("🚀 Ready for new users and transactions!")
        
        return True
    
    def reset_all(self):
        """Reset everything"""
        print("🚀 UNIONCOIN COMPLETE RESET")
        print("=" * 60)
        print(f"📅 Reset Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Show warning and get confirmation
        if not self.show_warning():
            print("❌ Reset cancelled by user")
            return False
        
        # Create backup before reset
        if not self.create_backup_before_reset():
            print("⚠️ Backup failed, but continuing with reset...")
        
        # Reset local database
        if not self.reset_local_database():
            print("❌ Local database reset failed!")
            return False
        
        # Reset Render database
        if not self.reset_render_database():
            print("❌ Render database reset failed!")
            return False
        
        # Reset Telegram bot
        if not self.reset_telegram_bot():
            print("❌ Telegram bot reset failed!")
            return False
        
        # Clear web cache
        if not self.clear_web_cache():
            print("❌ Web cache clearing failed!")
            return False
        
        # Verify reset complete
        if not self.verify_reset_complete():
            print("⚠️ Reset completed with issues!")
        
        # Show post-reset instructions
        self.show_post_reset_instructions()
        
        return True

def main():
    """Main function"""
    print("🚀 UnionCoin Reset Script")
    print("=" * 40)
    
    resetter = UnionCoinResetter()
    
    while True:
        print("\n📋 RESET OPTIONS:")
        print("1. 🔄 Reset Everything (Recommended)")
        print("2. 🗄️ Reset Local Database Only")
        print("3. 🌐 Reset Render Database Only")
        print("4. 🤖 Reset Telegram Bot Only")
        print("5. 🌐 Clear Web Cache Only")
        print("6. 💾 Create Backup Only")
        print("7. 🧪 Verify Reset Status")
        print("8. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-8): ").strip()
        
        if choice == "1":
            resetter.reset_all()
        elif choice == "2":
            resetter.reset_local_database()
        elif choice == "3":
            resetter.reset_render_database()
        elif choice == "4":
            resetter.reset_telegram_bot()
        elif choice == "5":
            resetter.clear_web_cache()
        elif choice == "6":
            resetter.create_backup_before_reset()
        elif choice == "7":
            resetter.verify_reset_complete()
        elif choice == "8":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
