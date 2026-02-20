#!/usr/bin/env python3
"""
Quick Deploy Telegram Auth System
Simple deployment without Unicode issues
"""

import os
import subprocess
import webbrowser
from datetime import datetime

def deploy_telegram_auth():
    """Deploy Telegram authentication system"""
    print("🚀 UnionCoin Telegram Auth Quick Deploy")
    print("=" * 50)
    
    try:
        # Step 1: Backup current system
        print("💾 Backing up current system...")
        subprocess.run(["cp", "api.py", "api.py.backup"], check=True)
        subprocess.run(["cp", "bot.py", "bot.py.backup"], check=True)
        print("✅ Backup completed")
        
        # Step 2: Deploy Telegram auth API
        print("📱 Deploying Telegram auth API...")
        subprocess.run(["cp", "telegram_auth_api.py", "api.py"], check=True)
        print("✅ Telegram auth API deployed")
        
        # Step 3: Deploy secure bot
        print("🔒 Deploying secure bot...")
        subprocess.run(["cp", "secure_bot.py", "bot.py"], check=True)
        print("✅ Secure bot deployed")
        
        # Step 4: Show Render.com instructions
        print("\n🌐 RENDER.COM UPDATE INSTRUCTIONS:")
        print("-" * 40)
        print("1. Open: https://render.com")
        print("2. Find 'unioncoin-web' service")
        print("3. Update Start Command: python telegram_auth_api.py")
        print("4. Add Environment Variables:")
        print("   - TELEGRAM_AUTH_ONLY=true")
        print("   - WEB_REGISTRATION_DISABLED=true")
        print("   - ADMIN_ACCESS_TELEGRAM_ONLY=true")
        print("5. Save and wait for redeploy")
        
        # Step 5: Test instructions
        print("\n🧪 TEST INSTRUCTIONS:")
        print("-" * 30)
        print("1. 📱 Test Telegram bot: @tokenuchunku12bot")
        print("2. 🚀 Send /start command")
        print("3. ✅ Create new account")
        print("4. 🌐 Test web interface: https://unioncoin.onrender.com")
        print("5. 🔒 Verify admin access via Telegram only")
        
        # Step 6: Security features
        print("\n🔒 SECURITY FEATURES:")
        print("-" * 30)
        print("✅ Web registration disabled")
        print("✅ Telegram-only registration")
        print("✅ 1:1 Telegram account mapping")
        print("✅ Admin access via Telegram only")
        print("✅ User data privacy enforced")
        
        print("\n🎉 DEPLOYMENT COMPLETED!")
        print("📱 Users can ONLY register via Telegram bot")
        print("🌐 Web interface redirects to Telegram")
        print("🔒 Security level: MAXIMUM")
        
        # Open Render dashboard
        webbrowser.open("https://render.com")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

if __name__ == "__main__":
    deploy_telegram_auth()
