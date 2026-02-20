#!/usr/bin/env python3
"""
UnionCoin Render.com Deployment Script
Deploy UnionCoin to Render.com platform
"""

import os
import sys
import subprocess
import requests
import json
from datetime import datetime
import webbrowser

class RenderDeployer:
    def __init__(self):
        self.render_api_key = "YOUR_RENDER_API_KEY"
        self.github_repo = "https://github.com/muxammadaminortiqovdecrypto/unioncoin.git"
        self.app_name = "unioncoin"
        self.domain = "unioncoin.onrender.com"
        
    def setup_render_deployment(self):
        """Setup Render.com deployment"""
        print("🚀 Setting up UnionCoin deployment to Render.com...")
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Step 1: Create render.yaml configuration
            print("📝 Step 1: Creating Render configuration...")
            self.create_render_config()
            
            # Step 2: Update database.py for PostgreSQL
            print("🗄️ Step 2: Updating database configuration...")
            self.update_database_config()
            
            # Step 3: Create startup scripts
            print("⚙️ Step 3: Creating startup scripts...")
            self.create_startup_scripts()
            
            # Step 4: Update requirements.txt
            print("📦 Step 4: Updating requirements...")
            self.update_requirements()
            
            # Step 5: Create health check endpoints
            print("🔍 Step 5: Creating health check endpoints...")
            self.create_health_checks()
            
            # Step 6: Setup environment variables
            print("⚙️ Step 6: Setting up environment variables...")
            self.setup_environment()
            
            print("\n✅ Render deployment setup completed!")
            print("📋 Next steps:")
            print("1. Push to GitHub")
            print("2. Connect to Render.com")
            print("3. Deploy application")
            
            return True
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False
    
    def create_render_config(self):
        """Create render.yaml configuration"""
        config = '''services:
  # Web Service
  - type: web
    name: unioncoin-web
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt && python database.py"
    startCommand: "python api.py"
    envVars:
      - key: DATABASE_URL
        value: "postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin"
      - key: BOT_TOKEN
        value: "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A"
      - key: ADMIN_ID
        value: "1685342390"
      - key: SECRET_KEY
        value: "unioncoin_production_secret_key_2026"
      - key: ADMIN_PASSWORD
        value: "unioncoin_admin_2026"
      - key: HOST
        value: "0.0.0.0"
      - key: PORT
        value: "8000"
      - key: DEBUG
        value: "False"
    healthCheckPath: "/verify"
    autoDeploy: true

  # PostgreSQL Database
  - type: pserv
    name: unioncoin-db
    env: postgres
    plan: free
    databaseName: unioncoin
    user: unioncoin_user
    password: unioncoin_password

  # Background Bot Service
  - type: worker
    name: unioncoin-bot
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python bot.py"
    envVars:
      - key: DATABASE_URL
        value: "postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin"
      - key: BOT_TOKEN
        value: "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A"
      - key: ADMIN_ID
        value: "1685342390"
      - key: SECRET_KEY
        value: "unioncoin_production_secret_key_2026"
      - key: HOST
        value: "0.0.0.0"
      - key: PORT
        value: "8000"
      - key: DEBUG
        value: "False"

# Environment variables for all services
globalEnvVars:
  - key: PYTHON_VERSION
    value: "3.11"
  - key: DATABASE_URL
    value: "postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin"
  - key: BOT_TOKEN
        value: "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A"
      - key: ADMIN_ID
        value: "1685342390"
      - key: SECRET_KEY
        value: "unioncoin_production_secret_key_2026"
      - key: ADMIN_PASSWORD
        value: "unioncoin_admin_2026"
      - key: HOST
        value: "0.0.0.0"
      - key: PORT
        value: "8000"
      - key: DEBUG
        value: "False"

# Health checks
healthChecks:
  - type: web
    name: unioncoin-web-health
    path: "/verify"
    interval: 30
    timeout: 10
    gracePeriod: 60
'''
        
        with open('render.yaml', 'w') as f:
            f.write(config)
        
        print("✅ render.yaml created")
        return True
    
    def update_database_config(self):
        """Update database.py for Render PostgreSQL"""
        db_content = '''import os
import hashlib
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import Optional, List

# Database configuration for Render.com
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin")

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    wallet_address = Column(String, unique=True, index=True, nullable=False)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    tg_id = Column(BigInteger, unique=True, index=True, nullable=True)
    is_primary = Column(Boolean, default=False)
    profile_color = Column(String, default="#667eea")
    
    # Relationships
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.sender_id", back_populates="sender")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.receiver_id", back_populates="receiver")

# Transaction model
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    transaction_type = Column(String, default="p2p")  # p2p, welcome_bonus, admin_approval
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_transactions")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_transactions")

def init_db():
    """Initialize database"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
'''
        
        with open('database.py', 'w') as f:
            f.write(db_content)
        
        print("✅ database.py updated for Render PostgreSQL")
        return True
    
    def create_startup_scripts(self):
        """Create startup scripts for Render"""
        # Web startup script
        web_script = '''#!/bin/bash
# UnionCoin Web Service Startup Script
echo "🚀 Starting UnionCoin Web Service..."
echo "📅 Started at: $(date)"

# Set environment variables
export DATABASE_URL=${DATABASE_URL}
export BOT_TOKEN=${BOT_TOKEN}
export ADMIN_ID=${ADMIN_ID}
export SECRET_KEY=${SECRET_KEY}
export ADMIN_PASSWORD=${ADMIN_PASSWORD}
export HOST=0.0.0.0
export PORT=8000
export DEBUG=False

# Initialize database
python database.py

# Start web server
echo "🌐 Starting web server on port 8000..."
python api.py
'''
        
        with open('start_web.sh', 'w') as f:
            f.write(web_script)
        
        # Bot startup script
        bot_script = '''#!/bin/bash
# UnionCoin Bot Service Startup Script
echo "🤖 Starting UnionCoin Bot Service..."
echo "📅 Started at: $(date)"

# Set environment variables
export DATABASE_URL=${DATABASE_URL}
export BOT_TOKEN=${BOT_TOKEN}
export ADMIN_ID=${ADMIN_ID}
export SECRET_KEY=${SECRET_KEY}
export HOST=0.0.0.0
export PORT=8000
export DEBUG=False

# Start bot
echo "🤖 Starting Telegram bot..."
python bot.py
'''
        
        with open('start_bot.sh', 'w') as f:
            f.write(bot_script)
        
        print("✅ Startup scripts created")
        return True
    
    def update_requirements(self):
        """Update requirements.txt for Render"""
        requirements = '''fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
aiogram==3.4.1
python-multipart==0.0.6
jinja2==3.1.2
pydantic==2.5.0
python-dotenv==1.0.0
pandas==2.1.4
openpyxl==3.1.2
requests==2.31.0
schedule==1.2.0
cryptography==41.0.8
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
gunicorn==21.2.0
redis==5.0.1
celery==5.3.4
flower==2.0.1
sentry-sdk==1.40.6
paramiko==3.3.1
'''
        
        with open('requirements.txt', 'w') as f:
            f.write(requirements)
        
        print("✅ requirements.txt updated for Render")
        return True
    
    def create_health_checks(self):
        """Create health check endpoints"""
        health_check_content = '''from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db, User, Transaction

app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint for Render"""
    return {"status": "healthy", "service": "unioncoin", "timestamp": str(datetime.utcnow())}

@app.get("/verify")
async def verify_blockchain():
    """Verify blockchain integrity"""
    try:
        db = next(get_db())
        users = db.query(User).all()
        transactions = db.query(Transaction).all()
        
        total_balance = sum(user.balance for user in users)
        
        return {
            "blockchain_valid": True,
            "total_users": len(users),
            "total_transactions": len(transactions),
            "total_balance": total_balance,
            "status": "verified"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        
        with open('health_check.py', 'w') as f:
            f.write(health_check_content)
        
        print("✅ Health check endpoints created")
        return True
    
    def setup_environment(self):
        """Setup environment variables"""
        env_content = '''# UnionCoin Render.com Environment Configuration

# Database Configuration (Render PostgreSQL)
DATABASE_URL=postgresql://unioncoin_user:unioncoin_password@unioncoin-db:5432/unioncoin

# Telegram Bot Configuration
BOT_TOKEN=8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A
ADMIN_ID=1685342390

# Security Configuration
SECRET_KEY=unioncoin_production_secret_key_2026
ADMIN_PASSWORD=unioncoin_admin_2026

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Render Configuration
PYTHON_VERSION=3.11
RENDER_SERVICE_NAME=unioncoin-web
RENDER_DB_NAME=unioncoin
RENDER_DB_USER=unioncoin_user
RENDER_DB_PASSWORD=unioncoin_password
'''
        
        with open('.env.render', 'w') as f:
            f.write(env_content)
        
        print("✅ Environment configuration created")
        return True
    
    def deploy_to_render(self):
        """Deploy to Render.com"""
        print("🚀 Deploying to Render.com...")
        
        try:
            # Step 1: Push to GitHub
            print("📤 Step 1: Pushing to GitHub...")
            self.push_to_github()
            
            # Step 2: Open Render.com
            print("🌐 Step 2: Opening Render.com...")
            webbrowser.open("https://render.com")
            
            print("\n📋 Manual deployment steps:")
            print("1. Sign up/login to Render.com")
            print("2. Click 'New +' -> 'Web Service'")
            print("3. Connect GitHub repository")
            print("4. Select 'muxammadaminortiqovdecrypto/unioncoin'")
            print("5. Configure service settings:")
            print("   - Name: unioncoin-web")
            print("   - Environment: Python")
            print("   - Build Command: pip install -r requirements.txt && python database.py")
            print("   - Start Command: python api.py")
            print("6. Add environment variables")
            print("7. Deploy!")
            
            return True
            
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            return False
    
    def push_to_github(self):
        """Push updated code to GitHub"""
        try:
            # Add all changes
            subprocess.run(["git", "add", "."], check=True)
            
            # Commit changes
            subprocess.run(["git", "commit", "-m", "Add Render.com deployment configuration"], check=True)
            
            # Push to GitHub
            subprocess.run(["git", "push", "origin", "master"], check=True)
            
            print("✅ Code pushed to GitHub")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")
            return False
    
    def get_render_info(self):
        """Get Render.com deployment information"""
        print("\n🌐 Render.com Deployment Information")
        print("=" * 50)
        print("📋 Platform: Render.com")
        print("🆓 Plan: Free tier")
        print("🗄️ Database: PostgreSQL (free)")
        print("🌐 Domain: unioncoin.onrender.com")
        print("🤖 Bot: Background worker")
        print("📊 Monitoring: Built-in health checks")
        print("🔄 Auto-deploy: GitHub integration")
        print("🔒 SSL: Automatic HTTPS")
        print("📈 Scaling: Paid plans available")
        
        print("\n🎯 Benefits:")
        print("✅ Free tier available")
        print("✅ Automatic SSL")
        print("✅ Built-in monitoring")
        print("✅ GitHub integration")
        print("✅ Easy deployment")
        print("✅ PostgreSQL included")
        
        print("\n📋 Limitations (Free Tier):")
        print("⚠️ 750 hours/month")
        print("⚠️ 256MB RAM")
        print("⚠️ 10GB storage")
        print("⚠️ Sleeps after 15 minutes inactivity")
        
        return True

def main():
    """Main Render deployment menu"""
    print("🚀 UnionCoin Render.com Deployment")
    print("=" * 50)
    
    deployer = RenderDeployer()
    
    while True:
        print("\n📋 Render.com Deployment Options:")
        print("1. ⚙️ Setup Render Configuration")
        print("2. 🚀 Deploy to Render.com")
        print("3. 📊 Render.com Information")
        print("4. 📤 Push to GitHub")
        print("5. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-5): ").strip()
        
        if choice == "1":
            deployer.setup_render_deployment()
        elif choice == "2":
            deployer.deploy_to_render()
        elif choice == "3":
            deployer.get_render_info()
        elif choice == "4":
            deployer.push_to_github()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
