#!/usr/bin/env python3
"""
UnionCoin Simple Deployment
Easy deployment for Render.com with step-by-step guidance
"""

import os
import webbrowser
import requests
import time
from datetime import datetime

class SimpleDeployer:
    def __init__(self):
        self.render_url = "https://render.com"
        self.github_repo = "https://github.com/muxammadaminortiqovdecrypto/unioncoin"
        
    def show_current_status(self):
        """Show current deployment status"""
        print("🚀 UnionCoin Deployment Status")
        print("=" * 50)
        
        print("\n✅ WORKING:")
        print("• GitHub Repository: https://github.com/muxammadaminortiqovdecrypto/unioncoin")
        print("• Web Interface: https://unioncoin.onrender.com")
        print("• Health Check: https://unioncoin.onrender.com/health")
        print("• Blockchain Verify: https://unioncoin.onrender.com/verify")
        
        print("\n❌ NEEDS FIX:")
        print("• Admin Panel: https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026")
        print("• Bot Service: Not deployed as background worker")
        print("• Environment Variables: Missing ADMIN_PASSWORD")
        
        return True
    
    def show_simple_fix_steps(self):
        """Show simple step-by-step fix"""
        print("🔧 SIMPLE FIX STEPS")
        print("=" * 50)
        
        print("\n📋 STEP 1: Open Render Dashboard")
        print("1. 🌐 Go to: https://render.com")
        print("2. 👤 Login with your email/password")
        print("3. 📊 Find 'unioncoin-web' service")
        print("4. 🖱️ Click on service name")
        
        print("\n📋 STEP 2: Add Environment Variable")
        print("1. ⚙️ Click 'Environment' tab")
        print("2. ➕ Click 'Add Environment Variable'")
        print("3. 📝 Fill in:")
        print("   • Group Name: unioncoin-admin")
        print("   • Variable Name: ADMIN_PASSWORD")
        print("   • Variable Value: unioncoin_admin_2026")
        print("   • Type: Plain text")
        print("4. ✅ Click 'Save'")
        
        print("\n📋 STEP 3: Add Bot Service")
        print("1. 🌐 Go back to Render dashboard")
        print("2. ➕ Click 'New +' → 'Background Worker'")
        print("3. 📝 Configure:")
        print("   • Name: unioncoin-bot")
        print("   • Repository: muxammadaminortiqovdecrypto/unioncoin")
        print("   • Branch: master")
        print("   • Build Command: pip install -r requirements_render.txt")
        print("   • Start Command: python bot.py")
        print("4. ⚙️ Add Environment Variables:")
        print("   • DATABASE_URL: postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin")
        print("   • BOT_TOKEN: 8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A")
        print("   • ADMIN_ID: 1685342390")
        print("   • SECRET_KEY: unioncoin_production_secret_key_2026")
        print("   • HOST: 0.0.0.0")
        print("   • PORT: 8000")
        print("   • DEBUG: False")
        print("5. ✅ Click 'Create Background Worker'")
        
        print("\n📋 STEP 4: Test Everything")
        print("1. ⏳ Wait 5-10 minutes for services to start")
        print("2. 🧪 Test admin panel: https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026")
        print("3. 🤖 Test bot: @tokenuchunku12bot")
        print("4. 🌐 Test web: https://unioncoin.onrender.com")
        
        return True
    
    def test_current_deployment(self):
        """Test current deployment status"""
        print("🧪 Testing Current Deployment...")
        print("=" * 50)
        
        urls = [
            ("Main Page", "https://unioncoin.onrender.com"),
            ("Health Check", "https://unioncoin.onrender.com/health"),
            ("Blockchain Verify", "https://unioncoin.onrender.com/verify"),
            ("Admin Panel", "https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026")
        ]
        
        for name, url in urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"✅ {name}: Working")
                elif response.status_code == 401:
                    print(f"❌ {name}: 401 - Access Denied (needs admin password)")
                else:
                    print(f"❌ {name}: {response.status_code}")
            except Exception as e:
                print(f"❌ {name}: Error - {str(e)[:50]}")
        
        return True
    
    def create_env_file(self):
        """Create .env file for reference"""
        print("📝 Creating .env file for reference...")
        
        env_content = """# UnionCoin Environment Variables
# Copy these to Render.com Environment section

DATABASE_URL=postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin
BOT_TOKEN=8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A
ADMIN_ID=1685342390
SECRET_KEY=unioncoin_production_secret_key_2026
ADMIN_PASSWORD=unioncoin_admin_2026
HOST=0.0.0.0
PORT=8000
DEBUG=False
"""
        
        with open('render_env.txt', 'w') as f:
            f.write(env_content)
        
        print("✅ Created render_env.txt with all environment variables")
        return True
    
    def open_render_dashboard(self):
        """Open Render dashboard"""
        print("🌐 Opening Render dashboard...")
        webbrowser.open("https://render.com")
        return True
    
    def open_github_repo(self):
        """Open GitHub repository"""
        print("📁 Opening GitHub repository...")
        webbrowser.open("https://github.com/muxammadaminortiqovdecrypto/unioncoin")
        return True
    
    def show_quick_commands(self):
        """Show quick reference commands"""
        print("⚡ QUICK REFERENCE")
        print("=" * 50)
        
        print("\n🔑 Environment Variables:")
        print("• ADMIN_PASSWORD: unioncoin_admin_2026")
        print("• BOT_TOKEN: 8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A")
        print("• DATABASE_URL: postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin")
        
        print("\n🌐 URLs:")
        print("• Render: https://render.com")
        print("• Web: https://unioncoin.onrender.com")
        print("• Admin: https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026")
        
        print("\n📋 Service Names:")
        print("• Web Service: unioncoin-web")
        print("• Database: unioncoin-db")
        print("• Bot Service: unioncoin-bot")
        
        return True
    
    def show_alternative_solutions(self):
        """Show alternative deployment solutions"""
        print("🔄 ALTERNATIVE SOLUTIONS")
        print("=" * 50)
        
        print("\n1️⃣ LOCAL WINDOWS SERVICE:")
        print("• Run on your computer 24/7")
        print("• Use: python windows_service.py")
        print("• Pros: Full control, no limits")
        print("• Cons: Computer must stay on")
        
        print("\n2️⃣ CUSTOM SERVER (VPS):")
        print("• Rent a server (DigitalOcean, Vultr, etc.)")
        print("• Use: python deploy_online.py")
        print("• Pros: Full control, dedicated resources")
        print("• Cons: Monthly cost (~$5-10)")
        
        print("\n3️⃣ DOCKER DEPLOYMENT:")
        print("• Container-based deployment")
        print("• Use: docker-compose up")
        print("• Pros: Portable, scalable")
        print("• Cons: More complex setup")
        
        return True

def main():
    """Main simple deployment menu"""
    print("🚀 UnionCoin Simple Deployment")
    print("=" * 50)
    
    deployer = SimpleDeployer()
    
    while True:
        print("\n📋 Simple Deployment Options:")
        print("1. 📊 Show Current Status")
        print("2. 🔧 Show Fix Steps")
        print("3. 🧪 Test Current Deployment")
        print("4. 📝 Create Environment File")
        print("5. 🌐 Open Render Dashboard")
        print("6. 📁 Open GitHub Repository")
        print("7. ⚡ Quick Reference")
        print("8. 🔄 Alternative Solutions")
        print("9. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-9): ").strip()
        
        if choice == "1":
            deployer.show_current_status()
        elif choice == "2":
            deployer.show_simple_fix_steps()
        elif choice == "3":
            deployer.test_current_deployment()
        elif choice == "4":
            deployer.create_env_file()
        elif choice == "5":
            deployer.open_render_dashboard()
        elif choice == "6":
            deployer.open_github_repo()
        elif choice == "7":
            deployer.show_quick_commands()
        elif choice == "8":
            deployer.show_alternative_solutions()
        elif choice == "9":
            print("👋 Good luck with deployment!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
