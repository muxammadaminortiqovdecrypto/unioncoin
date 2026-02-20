#!/usr/bin/env python3
"""
UnionCoin Render.com Terminal Deployment Script
Deploy UnionCoin to Render.com entirely via terminal/CLI
"""

import os
import sys
import subprocess
import requests
import json
import time
from datetime import datetime

class RenderTerminalDeployer:
    def __init__(self):
        self.render_api_key = "YOUR_RENDER_API_KEY"  # Render API key olish kerak
        self.github_repo = "https://github.com/muxammadaminortiqovdecrypto/unioncoin.git"
        self.service_name = "unioncoin"
        self.domain = "unioncoin.onrender.com"
        
    def get_render_api_key(self):
        """Get Render API key from user"""
        print("🔑 Render API Key kerak:")
        print("1. Render.com ga kirish: https://render.com")
        print("2. Account -> Settings -> API Keys")
        print("3. 'Create API Key' tugmasini bosing")
        print("4. Key nomini kiriting va 'Create' tugmasini bosing")
        print("5. API key ni nusxalab quyiga joylang")
        
        api_key = input("\n👉 Render API Key: ").strip()
        self.render_api_key = api_key
        
        # Save API key
        config = {
            'render_api_key': api_key,
            'github_repo': self.github_repo,
            'service_name': self.service_name,
            'domain': self.domain
        }
        
        with open('render_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ API key saqlandi")
        return api_key
    
    def create_database_service(self):
        """Create PostgreSQL database service via API"""
        print("🗄️ PostgreSQL database yaratilmoqda...")
        
        headers = {
            'Authorization': f'Bearer {self.render_api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'type': 'pserv',
            'name': f'{self.service_name}-db',
            'env': 'postgres',
            'plan': 'free',
            'region': 'oregon',
            'databaseName': 'unioncoin',
            'user': 'unioncoin_user',
            'password': 'unioncoin_password'
        }
        
        try:
            response = requests.post(
                'https://api.render.com/v1/services',
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                result = response.json()
                print("✅ Database service yaratildi")
                print(f"   📁 Service ID: {result.get('id')}")
                return result
            else:
                print(f"❌ Database yaratishda xatolik: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ API xatolik: {e}")
            return None
    
    def create_web_service(self, database_url):
        """Create web service via API"""
        print("🌐 Web service yaratilmoqda...")
        
        headers = {
            'Authorization': f'Bearer {self.render_api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'type': 'web',
            'name': f'{self.service_name}-web',
            'env': 'python',
            'plan': 'free',
            'region': 'oregon',
            'repo': self.github_repo,
            'branch': 'master',
            'buildCommand': 'pip install -r requirements_render.txt',
            'startCommand': 'gunicorn api_render:app --bind 0.0.0.0:$PORT',
            'healthCheckPath': '/verify',
            'autoDeploy': True,
            'envVars': [
                {
                    'key': 'DATABASE_URL',
                    'value': database_url
                },
                {
                    'key': 'BOT_TOKEN',
                    'value': '8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A'
                },
                {
                    'key': 'ADMIN_ID',
                    'value': '1685342390'
                },
                {
                    'key': 'SECRET_KEY',
                    'value': 'unioncoin_production_secret_key_2026'
                },
                {
                    'key': 'ADMIN_PASSWORD',
                    'value': 'unioncoin_admin_2026'
                },
                {
                    'key': 'HOST',
                    'value': '0.0.0.0'
                },
                {
                    'key': 'PORT',
                    'value': '8000'
                },
                {
                    'key': 'DEBUG',
                    'value': 'False'
                },
                {
                    'key': 'PYTHON_VERSION',
                    'value': '3.11'
                }
            ]
        }
        
        try:
            response = requests.post(
                'https://api.render.com/v1/services',
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                result = response.json()
                print("✅ Web service yaratildi")
                print(f"   🌐 URL: {result.get('url')}")
                return result
            else:
                print(f"❌ Web service yaratishda xatolik: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ API xatolik: {e}")
            return None
    
    def create_bot_service(self, database_url):
        """Create bot service via API"""
        print("🤖 Bot service yaratilmoqda...")
        
        headers = {
            'Authorization': f'Bearer {self.render_api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'type': 'worker',
            'name': f'{self.service_name}-bot',
            'env': 'python',
            'plan': 'free',
            'region': 'oregon',
            'repo': self.github_repo,
            'branch': 'master',
            'buildCommand': 'pip install -r requirements_render.txt',
            'startCommand': 'python bot.py',
            'envVars': [
                {
                    'key': 'DATABASE_URL',
                    'value': database_url
                },
                {
                    'key': 'BOT_TOKEN',
                    'value': '8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A'
                },
                {
                    'key': 'ADMIN_ID',
                    'value': '1685342390'
                },
                {
                    'key': 'SECRET_KEY',
                    'value': 'unioncoin_production_secret_key_2026'
                },
                {
                    'key': 'HOST',
                    'value': '0.0.0.0'
                },
                {
                    'key': 'PORT',
                    'value': '8000'
                },
                {
                    'key': 'DEBUG',
                    'value': 'False'
                },
                {
                    'key': 'PYTHON_VERSION',
                    'value': '3.11'
                }
            ]
        }
        
        try:
            response = requests.post(
                'https://api.render.com/v1/services',
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                result = response.json()
                print("✅ Bot service yaratildi")
                return result
            else:
                print(f"❌ Bot service yaratishda xatolik: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ API xatolik: {e}")
            return None
    
    def wait_for_service(self, service_id, service_name):
        """Wait for service to be ready"""
        print(f"⏳ {service_name} tayyorlanmoqda...")
        
        headers = {
            'Authorization': f'Bearer {self.render_api_key}',
            'Content-Type': 'application/json'
        }
        
        max_wait_time = 300  # 5 minutes
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            try:
                response = requests.get(
                    f'https://api.render.com/v1/services/{service_id}',
                    headers=headers
                )
                
                if response.status_code == 200:
                    service_data = response.json()
                    status = service_data.get('status', 'unknown')
                    
                    if status == 'live':
                        print(f"✅ {service_name} tayyor!")
                        return service_data
                    elif status == 'build_failed':
                        print(f"❌ {service_name} build failed!")
                        return service_data
                    else:
                        print(f"   🔄 Status: {status}")
                        time.sleep(10)
                else:
                    print(f"   ⚠️ API xatolik: {response.status_code}")
                    time.sleep(10)
                    
            except Exception as e:
                print(f"   ⚠️ Xatolik: {e}")
                time.sleep(10)
        
        print(f"❌ {service_name} tayyor bo'lmadi!")
        return None
    
    def test_deployment(self, web_url):
        """Test deployment"""
        print("🧪 Deployment test qilinmoqda...")
        
        test_urls = [
            (f"{web_url}", "Main page"),
            (f"{web_url}/health", "Health check"),
            (f"{web_url}/verify", "Blockchain verify"),
            (f"{web_url}/api/data?admin=unioncoin_admin_2026", "Admin panel")
        ]
        
        for url, description in test_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"   ✅ {description}: Working")
                else:
                    print(f"   ❌ {description}: {response.status_code}")
            except Exception as e:
                print(f"   ❌ {description}: {e}")
    
    def deploy_all_services(self):
        """Deploy all services"""
        print("🚀 UnionCoin Render.com Terminal Deployment")
        print("=" * 60)
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 1: Get API key
        if not self.render_api_key or self.render_api_key == "YOUR_RENDER_API_KEY":
            self.get_render_api_key()
        
        # Step 2: Create database
        print("\n📋 Step 1: PostgreSQL Database")
        print("-" * 40)
        database_service = self.create_database_service()
        
        if not database_service:
            print("❌ Database yaratish muvaffaqiyatsiz!")
            return False
        
        # Wait for database
        db_service_data = self.wait_for_service(database_service['id'], 'Database')
        if not db_service_data:
            print("❌ Database tayyor bo'lmadi!")
            return False
        
        # Get database URL
        database_url = f"postgresql://unioncoin_user:unioncoin_password@{database_service['id']}:5432/unioncoin"
        print(f"🗄️ Database URL: {database_url}")
        
        # Step 3: Create web service
        print("\n📋 Step 2: Web Service")
        print("-" * 40)
        web_service = self.create_web_service(database_url)
        
        if not web_service:
            print("❌ Web service yaratish muvaffaqiyatsiz!")
            return False
        
        # Wait for web service
        web_service_data = self.wait_for_service(web_service['id'], 'Web Service')
        if not web_service_data:
            print("❌ Web service tayyor bo'lmadi!")
            return False
        
        web_url = web_service_data.get('url', '')
        print(f"🌐 Web URL: {web_url}")
        
        # Step 4: Create bot service
        print("\n📋 Step 3: Bot Service")
        print("-" * 40)
        bot_service = self.create_bot_service(database_url)
        
        if not bot_service:
            print("❌ Bot service yaratish muvaffaqiyatsiz!")
            return False
        
        # Wait for bot service
        bot_service_data = self.wait_for_service(bot_service['id'], 'Bot Service')
        if not bot_service_data:
            print("❌ Bot service tayyor bo'lmadi!")
            return False
        
        # Step 5: Test deployment
        print("\n📋 Step 4: Testing Deployment")
        print("-" * 40)
        self.test_deployment(web_url)
        
        # Step 6: Show results
        print("\n🎉 Deployment Muvaffaqiyatli!")
        print("=" * 40)
        print(f"🌐 Web Interface: {web_url}")
        print(f"🔍 Health Check: {web_url}/health")
        print(f"📊 Blockchain Verify: {web_url}/verify")
        print(f"👑 Admin Panel: {web_url}/api/data?admin=unioncoin_admin_2026")
        print(f"🤖 Telegram Bot: @tokenuchunku12bot")
        print(f"📅 Deployed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
    
    def show_services_status(self):
        """Show current services status"""
        print("📊 Services Status")
        print("=" * 40)
        
        if not self.render_api_key or self.render_api_key == "YOUR_RENDER_API_KEY":
            print("❌ API key kerak!")
            return
        
        headers = {
            'Authorization': f'Bearer {self.render_api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(
                'https://api.render.com/v1/services',
                headers=headers
            )
            
            if response.status_code == 200:
                services = response.json()
                
                for service in services:
                    if self.service_name in service.get('name', ''):
                        name = service.get('name', 'Unknown')
                        status = service.get('status', 'unknown')
                        url = service.get('url', 'No URL')
                        service_type = service.get('type', 'unknown')
                        
                        print(f"📋 {name}")
                        print(f"   Type: {service_type}")
                        print(f"   Status: {status}")
                        print(f"   URL: {url}")
                        print()
            else:
                print(f"❌ API xatolik: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Xatolik: {e}")
    
    def delete_services(self):
        """Delete all services"""
        print("🗑️ Services o'chirilmoqda...")
        
        if not self.render_api_key or self.render_api_key == "YOUR_RENDER_API_KEY":
            print("❌ API key kerak!")
            return
        
        headers = {
            'Authorization': f'Bearer {self.render_api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(
                'https://api.render.com/v1/services',
                headers=headers
            )
            
            if response.status_code == 200:
                services = response.json()
                
                for service in services:
                    if self.service_name in service.get('name', ''):
                        service_id = service.get('id')
                        service_name = service.get('name')
                        
                        print(f"🗑️ {service_name} o'chirilmoqda...")
                        
                        delete_response = requests.delete(
                            f'https://api.render.com/v1/services/{service_id}',
                            headers=headers
                        )
                        
                        if delete_response.status_code == 204:
                            print(f"✅ {service_name} o'chirildi")
                        else:
                            print(f"❌ {service_name} o'chirilmadi: {delete_response.status_code}")
                
                print("✅ Barcha services o'chirildi!")
                
        except Exception as e:
            print(f"❌ Xatolik: {e}")

def main():
    """Main terminal deployment menu"""
    print("🚀 UnionCoin Render.com Terminal Deployment")
    print("=" * 60)
    
    deployer = RenderTerminalDeployer()
    
    # Load config if exists
    try:
        with open('render_config.json', 'r') as f:
            config = json.load(f)
            deployer.render_api_key = config.get('render_api_key', 'YOUR_RENDER_API_KEY')
            deployer.service_name = config.get('service_name', 'unioncoin')
            deployer.domain = config.get('domain', 'unioncoin.onrender.com')
    except FileNotFoundError:
        pass
    
    while True:
        print("\n📋 Terminal Deployment Options:")
        print("1. 🚀 Deploy All Services")
        print("2. 📊 Show Services Status")
        print("3. 🔧 Set API Key")
        print("4. 🗑️ Delete All Services")
        print("5. 🧪 Test Deployment")
        print("6. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-6): ").strip()
        
        if choice == "1":
            deployer.deploy_all_services()
        elif choice == "2":
            deployer.show_services_status()
        elif choice == "3":
            deployer.get_render_api_key()
        elif choice == "4":
            confirm = input("🗑️ Barcha services o'chirilsinmi? (yes/no): ").strip().lower()
            if confirm == 'yes':
                deployer.delete_services()
            else:
                print("❌ Bekor qilindi")
        elif choice == "5":
            web_url = input("🌐 Web URL kiriting: ").strip()
            if web_url:
                deployer.test_deployment(web_url)
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
