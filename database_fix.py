#!/usr/bin/env python3
"""
UnionCoin Database Connection Fix
Fix database connection issues for Render.com deployment
"""

import os
import sys
import subprocess
import webbrowser
from datetime import datetime

class DatabaseFixer:
    def __init__(self):
        self.render_url = "https://render.com"
        self.github_repo = "https://github.com/muxammadaminortiqovdecrypto/unioncoin"
        
    def show_database_error_analysis(self):
        """Analyze database connection errors"""
        print("🔍 UnionCoin Database Connection Error Analysis")
        print("=" * 80)
        print("📋 ERROR IDENTIFIED:")
        print("❌ (psycopg2.OperationalError) could not translate host name")
        print("❌ 'unioncoin-db.render.com' to address: Name or service not known")
        print("❌ Application exited early")
        print("")
        print("🎯 ROOT CAUSES:")
        print("1. 🗄️ Database service not created")
        print("2. 🔧 Incorrect database URL")
        print("3. 🌐 Database service not running")
        print("4. 🔐 Database credentials wrong")
        print("5. 🌐 Network connectivity issues")
        print("6. 🔧 Environment variables not loaded")
        print("")
        print("📋 SOLUTION NEEDED:")
        print("1. 🗄️ Create PostgreSQL service on Render.com")
        print("2. 🔧 Update DATABASE_URL with correct credentials")
        print("3. 🌐 Ensure database service is running")
        print("4. 🔐 Verify database credentials")
        print("5. 🔧 Load environment variables properly")
        print("=" * 80)
        
        return True
    
    def create_database_config(self):
        """Create database configuration"""
        print("\n🗄️ CREATING DATABASE CONFIGURATION")
        print("-" * 70)
        
        # Multiple database URL options
        database_configs = {
            "render_internal": {
                "name": "Render Internal Database",
                "url": "postgresql://postgres:12345@unioncoin-db:5432/unioncoin",
                "description": "Internal Render database connection"
            },
            "render_external": {
                "name": "Render External Database",
                "url": "postgresql://postgres:12345@unioncoin-db.render.com:5432/unioncoin",
                "description": "External Render database connection"
            },
            "localhost": {
                "name": "Local Database",
                "url": "postgresql://postgres:12345@localhost:5432/unioncoin",
                "description": "Local development database"
            },
            "sqlite": {
                "name": "SQLite Database",
                "url": "sqlite:///unioncoin.db",
                "description": "SQLite fallback database"
            }
        }
        
        # Create database config file
        config_content = """# UnionCoin Database Configuration
# Multiple database connection options

# Render Internal Database (Recommended)
DATABASE_URL_INTERNAL=postgresql://postgres:12345@unioncoin-db:5432/unioncoin

# Render External Database
DATABASE_URL_EXTERNAL=postgresql://postgres:12345@unioncoin-db.render.com:5432/unioncoin

# Local Database
DATABASE_URL_LOCAL=postgresql://postgres:12345@localhost:5432/unioncoin

# SQLite Fallback
DATABASE_URL_SQLITE=sqlite:///unioncoin.db

# Current Active Database
DATABASE_URL=postgresql://postgres:12345@unioncoin-db:5432/unioncoin

# Database Configuration
DB_HOST=unioncoin-db
DB_PORT=5432
DB_NAME=unioncoin
DB_USER=postgres
DB_PASSWORD=12345
"""
        
        try:
            with open('database_config.txt', 'w') as f:
                f.write(config_content)
            print("✅ database_config.txt created successfully!")
            
            # Show database options
            print("\n📋 DATABASE OPTIONS:")
            for key, config in database_configs.items():
                print(f"   {key}: {config['name']}")
                print(f"   URL: {config['url']}")
                print(f"   Description: {config['description']}")
                print("")
            
            return True
        except Exception as e:
            print(f"❌ Error creating database config: {e}")
            return False
    
    def create_enhanced_database_py(self):
        """Create enhanced database.py with fallback"""
        print("\n🗄️ CREATING ENHANCED DATABASE.PY")
        print("-" * 70)
        
        database_py_content = '''"""
UnionCoin Enhanced Database Module
With database connection fallback and error handling
"""

import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URLs in order of preference
DATABASE_URLS = [
    os.getenv("DATABASE_URL_INTERNAL", "postgresql://postgres:12345@unioncoin-db:5432/unioncoin"),
    os.getenv("DATABASE_URL_EXTERNAL", "postgresql://postgres:12345@unioncoin-db.render.com:5432/unioncoin"),
    os.getenv("DATABASE_URL_LOCAL", "postgresql://postgres:12345@localhost:5432/unioncoin"),
    os.getenv("DATABASE_URL_SQLITE", "sqlite:///unioncoin.db"),
    os.getenv("DATABASE_URL", "sqlite:///unioncoin.db")  # Fallback
]

# Global variables
engine = None
SessionLocal = None
current_database_url = None

def create_database_engine():
    """Create database engine with fallback"""
    global engine, SessionLocal, current_database_url
    
    for i, database_url in enumerate(DATABASE_URLS):
        try:
            logger.info(f"Attempting to connect to database {i+1}/{len(DATABASE_URLS)}: {database_url}")
            
            # Create engine
            engine = create_engine(
                database_url,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=False
            )
            
            # Test connection
            with engine.connect() as connection:
                connection.execute("SELECT 1")
            
            # Create session factory
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            current_database_url = database_url
            
            logger.info(f"✅ Successfully connected to database: {database_url}")
            return True
            
        except Exception as e:
            logger.warning(f"❌ Failed to connect to database {i+1}: {database_url}")
            logger.warning(f"Error: {e}")
            continue
    
    # If all connections fail, use SQLite as last resort
    try:
        logger.info("🔄 Falling back to SQLite database...")
        engine = create_engine("sqlite:///unioncoin.db", echo=False)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        current_database_url = "sqlite:///unioncoin.db"
        logger.info("✅ Successfully connected to SQLite fallback database")
        return True
        
    except Exception as e:
        logger.error(f"❌ Critical: Failed to connect to any database: {e}")
        return False

# Initialize database engine
if not create_database_engine():
    logger.error("❌ CRITICAL: Could not establish database connection")
    raise Exception("Database connection failed")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    wallet_address = Column(String, unique=True, index=True, nullable=False)
    balance = Column(Float, default=1000.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_banned = Column(Boolean, default=False)
    is_inactive = Column(Boolean, default=False)
    is_suspended = Column(Boolean, default=False)
    tg_id = Column(Integer, unique=True, index=True, nullable=True)
    
    # Relationships
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.sender_id", back_populates="sender")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.receiver_id", back_populates="receiver")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    transaction_type = Column(String, default="transfer")
    tx_hash = Column(String, unique=True, index=True, nullable=True)
    current_hash = Column(String, nullable=True)
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_transactions")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_transactions")

def get_db():
    """Get database session"""
    if SessionLocal is None:
        raise Exception("Database not initialized")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")
        return False

def check_database_connection():
    """Check database connection status"""
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection check failed: {e}")
        return False

def get_database_info():
    """Get current database information"""
    return {
        "database_url": current_database_url,
        "engine_type": "postgresql" if "postgresql" in current_database_url else "sqlite",
        "connection_status": check_database_connection(),
        "tables": ["users", "transactions"]
    }

def create_transaction(db: Session, sender_id: int = None, receiver_id: int = None, amount: float = 0.0, tx_type: str = "transfer"):
    """Create a new transaction"""
    try:
        import random
        import string
        
        # Generate transaction hash
        tx_hash = ''.join(random.choices(string.ascii_uppercase + string.digits, k=64))
        
        transaction = Transaction(
            sender_id=sender_id,
            receiver_id=receiver_id,
            amount=amount,
            transaction_type=tx_type,
            tx_hash=tx_hash
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        logger.info(f"✅ Transaction created: {tx_hash}")
        return transaction
        
    except Exception as e:
        logger.error(f"❌ Error creating transaction: {e}")
        db.rollback()
        return None

def get_password_hash(password: str) -> str:
    """Generate password hash"""
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    except ImportError:
        # Fallback if passlib not available
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)
    except ImportError:
        # Fallback if passlib not available
        import hashlib
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def generate_mnemonic() -> str:
    """Generate mnemonic phrase"""
    try:
        import mnemonic
        mnemo = mnemonic.Mnemonic("english")
        return mnemo.generate(strength=128)
    except ImportError:
        # Fallback if mnemonic not available
        import random
        import string
        words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew"]
        return ' '.join(random.choices(words, k=12))

# Initialize database on import
try:
    init_db()
    logger.info("✅ Database initialized successfully")
except Exception as e:
    logger.error(f"❌ Database initialization failed: {e}")
'''
        
        try:
            with open('database_enhanced.py', 'w') as f:
                f.write(database_py_content)
            print("✅ database_enhanced.py created successfully!")
            return True
        except Exception as e:
            print(f"❌ Error creating enhanced database.py: {e}")
            return False
    
    def create_database_service_guide(self):
        """Create database service setup guide"""
        print("\n🗄️ CREATING DATABASE SERVICE GUIDE")
        print("-" * 70)
        
        guide_content = """# UnionCoin Database Service Setup Guide
# Render.com PostgreSQL Service Setup

## 🎯 PROBLEM:
- Database connection failed
- 'unioncoin-db.render.com' not found
- Application exited early

## 🔧 SOLUTION: Create PostgreSQL Service

### Step 1: Create PostgreSQL Service
1. 🌐 Open: https://render.com
2. ➕ Click: "New +" button
3. 🗄️ Select: "PostgreSQL"
4. 📝 Service Name: unioncoin-db
5. 🗄️ Database Name: unioncoin
6. 👤 User: postgres
7. 🔐 Password: 12345
8. 🌐 Region: Oregon (or closest)
9. 💰 Plan: Free
10. ✅ Click: "Create PostgreSQL Database"

### Step 2: Get Database Connection Details
1. ⏳ Wait for database to be ready (2-3 minutes)
2. 🔍 Go to: unioncoin-db service
3. 🔗 Copy: Internal Database URL
4. 📝 Format: postgresql://postgres:12345@unioncoin-db:5432/unioncoin

### Step 3: Update Environment Variables
1. 🔍 Go to: unioncoin-web service
2. ⚙️ Go to: Environment tab
3. 📤 Add/Update DATABASE_URL:
   DATABASE_URL=postgresql://postgres:12345@unioncoin-db:5432/unioncoin
4. 💾 Save Changes
5. 🔄 Wait for redeploy

### Step 4: Alternative Database URLs
If internal URL doesn't work, try these:

#### Internal URL (Recommended):
DATABASE_URL=postgresql://postgres:12345@unioncoin-db:5432/unioncoin

#### External URL:
DATABASE_URL=postgresql://postgres:12345@unioncoin-db.render.com:5432/unioncoin

#### SQLite Fallback:
DATABASE_URL=sqlite:///unioncoin.db

### Step 5: Verify Database Connection
1. 🧪 Test: https://unioncoin.onrender.com/health
2. 📊 Check logs for database connection
3. ✅ Success: "Database connected successfully"

## 🔍 TROUBLESHOOTING:

### Error: "could not translate host name"
- ✅ Solution: Create PostgreSQL service first
- ✅ Solution: Use internal database URL
- ✅ Solution: Check service name spelling

### Error: "connection refused"
- ✅ Solution: Wait for database to be ready
- ✅ Solution: Check database credentials
- ✅ Solution: Verify port number (5432)

### Error: "authentication failed"
- ✅ Solution: Check database password
- ✅ Solution: Verify database user
- ✅ Solution: Update environment variables

## 📋 CRITICAL ENVIRONMENT VARIABLES:
DATABASE_URL=postgresql://postgres:12345@unioncoin-db:5432/unioncoin
DB_HOST=unioncoin-db
DB_PORT=5432
DB_NAME=unioncoin
DB_USER=postgres
DB_PASSWORD=12345

## 🎯 EXPECTED RESULT:
- ✅ Database service created
- ✅ Database connection successful
- ✅ Application starts without errors
- ✅ Health check passes
- ✅ Users can register and login
"""
        
        try:
            with open('DATABASE_SERVICE_GUIDE.md', 'w') as f:
                f.write(guide_content)
            print("✅ DATABASE_SERVICE_GUIDE.md created successfully!")
            return True
        except Exception as e:
            print(f"❌ Error creating database service guide: {e}")
            return False
    
    def show_render_database_solution(self):
        """Show Render.com database solution"""
        print("\n🌐 RENDER.COM DATABASE SOLUTION")
        print("=" * 80)
        
        print("📋 STEP-BY-STEP DATABASE FIX:")
        print("1. 🌐 Open: https://render.com")
        print("2. ➕ Click: 'New +' button")
        print("3. 🗄️ Select: 'PostgreSQL'")
        print("4. 📝 Service Name: unioncoin-db")
        print("5. 🗄️ Database Name: unioncoin")
        print("6. 👤 User: postgres")
        print("7. 🔐 Password: 12345")
        print("8. 🌐 Region: Oregon")
        print("9. 💰 Plan: Free")
        print("10. ✅ Click: 'Create PostgreSQL Database'")
        print("11. ⏳ Wait 2-3 minutes for database to be ready")
        print("12. 🔍 Go to: unioncoin-db service")
        print("13. 🔗 Copy: Internal Database URL")
        print("14. 🔍 Go to: unioncoin-web service")
        print("15. ⚙️ Go to: Environment tab")
        print("16. 📤 Add: DATABASE_URL=postgresql://postgres:12345@unioncoin-db:5432/unioncoin")
        print("17. 💾 Save Changes")
        print("18. 🔄 Wait for redeploy")
        print("19. 🧪 Test: https://unioncoin.onrender.com/health")
        
        return True
    
    def show_quick_database_fix(self):
        """Show quick database fix"""
        print("\n⚡ QUICK DATABASE FIX")
        print("=" * 80)
        
        print("🎯 ONE-LINE SOLUTIONS:")
        print("")
        print("1. 🗄️ Create PostgreSQL service on Render.com")
        print("2. 🔧 Update DATABASE_URL environment variable:")
        print("   DATABASE_URL=postgresql://postgres:12345@unioncoin-db:5432/unioncoin")
        print("3. 🔄 Wait for redeploy")
        print("4. 🧪 Test: https://unioncoin.onrender.com/health")
        print("")
        print("🚨 ALTERNATIVE - SQLite Fallback:")
        print("DATABASE_URL=sqlite:///unioncoin.db")
        print("(Works immediately but not recommended for production)")
        
        return True

def main():
    """Main function"""
    print("🔧 UnionCoin Database Connection Fix")
    print("=" * 80)
    print(f"📅 Fix Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    fixer = DatabaseFixer()
    
    while True:
        print("\n📋 DATABASE FIX OPTIONS:")
        print("1. 🔍 Database Error Analysis")
        print("2. 🗄️ Create Database Configuration")
        print("3. 🔧 Create Enhanced Database.py")
        print("4. 📋 Create Database Service Guide")
        print("5. 🌐 Render.com Database Solution")
        print("6. ⚡ Quick Database Fix")
        print("7. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-7): ").strip()
        
        if choice == "1":
            fixer.show_database_error_analysis()
        elif choice == "2":
            fixer.create_database_config()
        elif choice == "3":
            fixer.create_enhanced_database_py()
        elif choice == "4":
            fixer.create_database_service_guide()
        elif choice == "5":
            fixer.show_render_database_solution()
        elif choice == "6":
            fixer.show_quick_database_fix()
        elif choice == "7":
            print("👋 Good luck with database fix!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
