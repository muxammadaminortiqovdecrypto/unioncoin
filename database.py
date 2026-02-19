"""
Database Models and Blockchain Hash-Chain Logic
"""

import os
import hashlib
import sqlalchemy
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import Optional, List

# Database configuration
# For development with SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./unioncoin.db")

# For production with PostgreSQL (uncomment below)
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:12345@localhost/unioncoin")

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calculate_hash(sender: str, receiver: str, amount: float, timestamp: datetime, prev_hash: str) -> str:
    """Calculate SHA-256 hash for transaction"""
    data = f"{sender}{receiver}{amount}{timestamp.isoformat()}{prev_hash}"
    return hashlib.sha256(data.encode()).hexdigest()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, unique=True, index=True, nullable=True)
    username = Column(String, unique=True, index=True)
    wallet_address = Column(String(12), unique=True, index=True)
    balance = Column(Float, default=1000.0)  # Welcome bonus
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    is_primary = Column(Boolean, default=False)  # Primary account for multi-account users
    profile_color = Column(String, default="#667eea")  # Profile theme color
    
    # New features fields
    last_daily_claim = Column(DateTime, nullable=True)
    referral_code = Column(String(20), unique=True, index=True)
    referred_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    seed_phrase = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=True) # For V3 auth
    
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.sender_id", back_populates="sender")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.receiver_id", back_populates="receiver")
    referred_users = relationship("User", backref=sqlalchemy.orm.backref("referrer", remote_side=[id]))

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    prev_hash = Column(String(64))
    current_hash = Column(String(64))
    transaction_type = Column(String(20))  # "p2p", "bonus", "admin_request"
    status = Column(String(20), default="Approved") # "Pending", "Approved", "Rejected"
    tx_hash = Column(String(64), unique=True, nullable=True) # Unique Tx ID
    is_approved = Column(Boolean, default=False)
    
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_transactions")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_transactions")

def create_transaction(db, sender_id: int, receiver_id: int, amount: float, transaction_type: str = "p2p", is_approved: bool = True) -> Transaction:
    """Create new transaction with hash chain"""
    # Get last transaction hash
    last_tx = db.query(Transaction).order_by(Transaction.id.desc()).first()
    prev_hash = last_tx.current_hash if last_tx else "0" * 64
    
    # Create transaction
    transaction = Transaction(
        sender_id=sender_id,
        receiver_id=receiver_id,
        amount=amount,
        transaction_type=transaction_type,
        is_approved=is_approved,
        prev_hash=prev_hash
    )
    
    # Calculate current hash
    transaction.current_hash = calculate_hash(
        str(sender_id), str(receiver_id), amount, 
        transaction.timestamp, prev_hash
    )
    
    return transaction

def verify_chain_integrity(db) -> bool:
    """Verify entire blockchain integrity"""
    transactions = db.query(Transaction).order_by(Transaction.id).all()
    
    for i, tx in enumerate(transactions):
        expected_hash = calculate_hash(
            str(tx.sender_id), str(tx.receiver_id), 
            tx.amount, tx.timestamp, tx.prev_hash
        )
        
        if tx.current_hash != expected_hash:
            return False
            
        # Check hash chain linkage
        if i > 0 and tx.prev_hash != transactions[i-1].current_hash:
            return False
    
    return True

def generate_mnemonic():
    """Simple 12-word mnemonic generator for V2 recovery"""
    words = [
        "apple", "beach", "cloud", "dance", "eagle", "flame", "grape", "house", "image", "juice",
        "koala", "lemon", "melon", "night", "ocean", "piano", "queen", "river", "solar", "tiger",
        "urban", "voice", "whale", "xenon", "yacht", "zebra", "alarm", "brick", "candy", "dream",
        "earth", "frost", "ghost", "honey", "index", "joker", "knife", "light", "magic", "noise",
        "olive", "paper", "quiet", "rocks", "smile", "table", "uncle", "video", "water", "young"
    ]
    import random
    return " ".join(random.choices(words, k=12))

def init_db():
    """Initialize database tables and handle auto-migrations"""
    Base.metadata.create_all(bind=engine)
    
    # Auto-migration for missing columns
    try:
        with engine.connect() as conn:
            # Check users table
            columns_users = []
            if "sqlite" in str(engine.url):
                columns_users = [row[1] for row in conn.execute(text("PRAGMA table_info(users)"))]
            else:
                result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users'"))
                columns_users = [row[0] for row in result]

            if "seed_phrase" not in columns_users:
                conn.execute(text("ALTER TABLE users ADD COLUMN seed_phrase VARCHAR"))
            if "password_hash" not in columns_users:
                conn.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR"))
            
            # Check transactions table
            columns_tx = []
            if "sqlite" in str(engine.url):
                columns_tx = [row[1] for row in conn.execute(text("PRAGMA table_info(transactions)"))]
            else:
                result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='transactions'"))
                columns_tx = [row[0] for row in result]

            if "status" not in columns_tx:
                conn.execute(text("ALTER TABLE transactions ADD COLUMN status VARCHAR DEFAULT 'Approved'"))
            if "tx_hash" not in columns_tx:
                conn.execute(text("ALTER TABLE transactions ADD COLUMN tx_hash VARCHAR"))
            
            conn.commit()
    except Exception as e:
        print(f"Migration warning: {e} (This is normal if tables are fresh)")

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
