"""
Database Models and Blockchain Hash-Chain Logic (UnionCoin Ultimate V4 + 2FA)
"""

import os
import hashlib
import random
import sqlalchemy
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import Optional, List

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./unioncoin.db")

# Render/SQLAlchemy compatibility fix: Replace postgres:// with postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash password (input MUST be lowercased before calling)"""
    return pwd_context.hash(password.lower())

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password (input MUST be lowercased before calling)"""
    return pwd_context.verify(plain_password.lower(), hashed_password)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, unique=True, index=True, nullable=False) # PRIMARY AUTH ID
    username = Column(String, unique=True, index=True, nullable=False) # Lowercase
    wallet_address = Column(String(12), unique=True, index=True)
    balance = Column(Float, default=1000.0)
    password_hash = Column(String, nullable=False) # Hashed lowercase password
    seed_phrase = Column(String, unique=True, nullable=True)
    
    # Customization & Meta
    profile_color = Column(String, default="#6366f1")
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_daily_claim = Column(DateTime, nullable=True)
    
    # Telegram Login Confirmation (2FA)
    login_token = Column(String(32), nullable=True)
    login_confirmed = Column(Boolean, default=False)
    
    # Referral system
    referral_code = Column(String(20), unique=True, index=True)
    referred_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.sender_id", back_populates="sender")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.receiver_id", back_populates="receiver")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Nullable for BURNS
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    prev_hash = Column(String(64))
    current_hash = Column(String(64))
    transaction_type = Column(String(20)) # "p2p", "bonus", "reward"
    status = Column(String(20), default="SUCCESS") # "SUCCESS", "BURNED", "PENDING"
    tx_hash = Column(String(64), unique=True) # SHA-256 Public Hash
    
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_transactions")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_transactions")

def create_transaction(db, sender_id: int, receiver_id: Optional[int], amount: float, tx_type: str = "p2p", status: str = "SUCCESS") -> Transaction:
    """Create transaction with SHA-256 hashing and chain link"""
    last_tx = db.query(Transaction).order_by(Transaction.id.desc()).first()
    prev_hash = last_tx.current_hash if last_tx else "0" * 64
    
    tx = Transaction(
        sender_id=sender_id,
        receiver_id=receiver_id,
        amount=amount,
        transaction_type=tx_type,
        status=status,
        prev_hash=prev_hash
    )
    db.add(tx)
    db.flush() # Get ID
    
    # SHA-256 Internal Chain Hash
    chain_data = f"{tx.sender_id}{tx.receiver_id}{tx.amount}{tx.timestamp}{prev_hash}"
    tx.current_hash = hashlib.sha256(chain_data.encode()).hexdigest()
    
    # SHA-256 Public Transaction ID
    public_data = f"{tx.id}{tx.sender_id}{amount}{random.random()}{tx.timestamp}"
    tx.tx_hash = hashlib.sha256(public_data.encode()).hexdigest()
    
    return tx

def generate_mnemonic():
    """Simple 12-word mnemonic generator"""
    words = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "theta", "iota", "kappa", "lambda", "sigma", "omega",
             "crypto", "chain", "safe", "fast", "gold", "moon", "star", "node", "seed", "key", "vault", "user"]
    return " ".join(random.sample(words, 12))

def get_user_by_any(db: Session, identifier: str) -> Optional[User]:
    """
    Universal Finder Logic:
    1. Input.lower()
    2. If numeric -> query by tg_id
    3. Else -> query by username or wallet_address
    """
    if not identifier:
        return None
        
    target = identifier.strip().lower()
    
    # Try TG ID
    if target.isdigit():
        user = db.query(User).filter(User.tg_id == int(target)).first()
        if user: return user
        
    # Try Username or Wallet
    user = db.query(User).filter(
        (User.username == target) | 
        (User.wallet_address == target.replace('0x', ''))
    ).first()
    
    return user

def init_db(force_reset=False):
    """Initialize database. If force_reset=True, wipe all data for Ultimate Spec."""
    if force_reset:
        print("⚠️ Resetting database for UnionCoin Ultimate...")
        Base.metadata.drop_all(bind=engine)
    
    Base.metadata.create_all(bind=engine)
    
    # Ensure Burn Wallet exists
    with SessionLocal() as db:
        burn_exists = db.query(User).filter(User.wallet_address == "000000000000").first()
        if not burn_exists:
            burn = User(
                tg_id=0,
                username="burn_wallet",
                wallet_address="000000000000",
                password_hash="system_locked",
                balance=0.0,
                is_admin=False
            )
            db.add(burn)
            db.commit()

if __name__ == "__main__":
    init_db(force_reset=True)
