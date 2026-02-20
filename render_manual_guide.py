#!/usr/bin/env python3
"""
UnionCoin Render.com Manual Deployment Guide
Step-by-step guide for successful deployment
"""

import webbrowser
import os

class RenderManualGuide:
    def __init__(self):
        self.github_repo = "https://github.com/muxammadaminortiqovdecrypto/unioncoin"
        self.render_url = "https://render.com"
        
    def show_manual_guide(self):
        """Show step-by-step manual deployment guide"""
        print("🚀 UnionCoin Render.com Manual Deployment Guide")
        print("=" * 60)
        
        print("\n📋 PREPARATION STEPS:")
        print("=" * 30)
        
        print("\n1️⃣ GitHub Repository Check:")
        print(f"   📁 Repository: {self.github_repo}")
        print("   ✅ Make sure all files are pushed to GitHub")
        print("   🔍 Check: https://github.com/muxammadaminortiqovdecrypto/unioncoin")
        
        print("\n2️⃣ Render.com Account:")
        print("   🌐 Go to: https://render.com")
        print("   👤 Sign up or login")
        print("   📧 Verify email address")
        
        print("\n📋 DEPLOYMENT STEPS:")
        print("=" * 30)
        
        print("\n🗄️ STEP 1: Create PostgreSQL Database")
        print("-" * 40)
        print("1. Go to Render dashboard")
        print("2. Click 'New +' → 'PostgreSQL'")
        print("3. Configure database:")
        print("   • Name: unioncoin-db")
        print("   • Database: unioncoin")
        print("   • User: unioncoin_user")
        print("   • Password: unioncoin_password")
        print("4. Click 'Create Database'")
        print("5. Wait for database to be ready (green checkmark)")
        print("6. Copy the Internal Database URL")
        
        print("\n🌐 STEP 2: Create Web Service")
        print("-" * 40)
        print("1. Click 'New +' → 'Web Service'")
        print("2. Connect GitHub:")
        print("   • Choose 'Connect a repository'")
        print("   • Select GitHub")
        print("   • Authorize Render")
        print("   • Select 'muxammadaminortiqovdecrypto/unioncoin'")
        print("   • Choose branch: master")
        print("3. Configure service:")
        print("   • Name: unioncoin-web")
        print("   • Environment: Python")
        print("   • Region: Oregon (or nearest)")
        print("   • Branch: master")
        print("   • Root Directory: ./")
        print("   • Build Command: pip install -r requirements_render.txt")
        print("   • Start Command: gunicorn api_render:app --bind 0.0.0.0:$PORT")
        print("4. Click 'Advanced Settings'")
        print("5. Add Environment Variables:")
        
        env_vars = [
            ("DATABASE_URL", "postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin"),
            ("BOT_TOKEN", "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A"),
            ("ADMIN_ID", "1685342390"),
            ("SECRET_KEY", "unioncoin_production_secret_key_2026"),
            ("ADMIN_PASSWORD", "unioncoin_admin_2026"),
            ("HOST", "0.0.0.0"),
            ("PORT", "8000"),
            ("DEBUG", "False"),
            ("PYTHON_VERSION", "3.11")
        ]
        
        for key, value in env_vars:
            print(f"   • {key}: {value}")
        
        print("6. Click 'Create Web Service'")
        print("7. Wait for deployment to complete")
        
        print("\n🤖 STEP 3: Create Bot Service")
        print("-" * 40)
        print("1. Click 'New +' → 'Background Worker'")
        print("2. Connect same GitHub repository")
        print("3. Configure worker:")
        print("   • Name: unioncoin-bot")
        print("   • Environment: Python")
        print("   • Branch: master")
        print("   • Build Command: pip install -r requirements_render.txt")
        print("   • Start Command: python bot.py")
        print("4. Add same Environment Variables as web service")
        print("5. Click 'Create Background Worker'")
        
        print("\n🔧 STEP 4: Configure Services")
        print("-" * 40)
        print("1. Wait for both services to be ready")
        print("2. Check service logs for any errors")
        print("3. Test web service: https://unioncoin.onrender.com/verify")
        print("4. Test admin panel: https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026")
        print("5. Check bot service logs for Telegram connection")
        
        print("\n🔍 TROUBLESHOOTING:")
        print("=" * 30)
        
        print("\n❌ Common Issues and Solutions:")
        print("-" * 40)
        
        print("\n1️⃣ Build Failed:")
        print("   • Check requirements_render.txt syntax")
        print("   • Verify all dependencies are available")
        print("   • Check Python version compatibility")
        
        print("\n2️⃣ Database Connection Error:")
        print("   • Verify database is running")
        print("   • Check DATABASE_URL format")
        print("   • Ensure database name matches")
        print("   • Check user/password are correct")
        
        print("\n3️⃣ Bot Not Starting:")
        print("   • Verify BOT_TOKEN is correct")
        print("   • Check bot.py syntax")
        print("   • Ensure aiogram is installed")
        print("   • Check Telegram bot permissions")
        
        print("\n4️⃣ Web Service Not Responding:")
        print("   • Check gunicorn command")
        print("   • Verify PORT environment variable")
        print("   • Check health check path")
        print("   • Ensure api_render.py exists")
        
        print("\n5️⃣ Environment Variables Not Working:")
        print("   • Check variable names (case-sensitive)")
        print("   • Verify no extra spaces")
        print("   • Ensure all required variables are added")
        print("   • Restart service after adding variables")
        
        print("\n📋 VERIFICATION STEPS:")
        print("=" * 30)
        
        print("\n✅ After Deployment, Test:")
        print("-" * 40)
        print("1. Web Interface: https://unioncoin.onrender.com")
        print("2. Health Check: https://unioncoin.onrender.com/health")
        print("3. Blockchain Verify: https://unioncoin.onrender.com/verify")
        print("4. Admin Panel: https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026")
        print("5. Check logs in Render dashboard")
        print("6. Test Telegram bot: @tokenuchunku12bot")
        
        print("\n📊 MONITORING:")
        print("=" * 30)
        print("• Service logs in Render dashboard")
        print("• Health check status")
        print("• Database connection status")
        print("• Bot service activity")
        print("• Error tracking")
        
        print("\n🔧 MAINTENANCE:")
        print("=" * 30)
        print("• Automatic restarts on failure")
        print("• GitHub auto-deployment")
        print("• Environment variable management")
        print("• Log rotation")
        print("• Database backups")
        
        return True
    
    def open_render_dashboard(self):
        """Open Render dashboard"""
        print("\n🌐 Opening Render dashboard...")
        webbrowser.open(self.render_url)
        return True
    
    def open_github_repo(self):
        """Open GitHub repository"""
        print("\n📁 Opening GitHub repository...")
        webbrowser.open(self.github_repo)
        return True
    
    def show_quick_commands(self):
        """Show quick reference commands"""
        print("\n⚡ QUICK REFERENCE:")
        print("=" * 30)
        
        print("\n🔧 Build Command:")
        print("pip install -r requirements_render.txt")
        
        print("\n🚀 Web Start Command:")
        print("gunicorn api_render:app --bind 0.0.0.0:$PORT")
        
        print("\n🤖 Bot Start Command:")
        print("python bot.py")
        
        print("\n🗄️ Database URL:")
        print("postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin")
        
        print("\n🔑 Admin Password:")
        print("unioncoin_admin_2026")
        
        print("\n📱 Telegram Bot:")
        print("@tokenuchunku12bot")
        
        print("\n🌐 Web URLs:")
        print("• Main: https://unioncoin.onrender.com")
        print("• Health: https://unioncoin.onrender.com/health")
        print("• Verify: https://unioncoin.onrender.com/verify")
        print("• Admin: https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026")
        
        return True

def main():
    """Main menu"""
    print("🚀 UnionCoin Render.com Manual Deployment")
    print("=" * 60)
    
    guide = RenderManualGuide()
    
    while True:
        print("\n📋 Manual Deployment Options:")
        print("1. 📖 Show Complete Guide")
        print("2. 🌐 Open Render Dashboard")
        print("3. 📁 Open GitHub Repository")
        print("4. ⚡ Quick Reference")
        print("5. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-5): ").strip()
        
        if choice == "1":
            guide.show_manual_guide()
        elif choice == "2":
            guide.open_render_dashboard()
        elif choice == "3":
            guide.open_github_repo()
        elif choice == "4":
            guide.show_quick_commands()
        elif choice == "5":
            print("👋 Good luck with deployment!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
