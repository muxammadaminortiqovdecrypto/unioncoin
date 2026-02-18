#!/usr/bin/env python3
"""
Token Ecosystem Initialization Script
Creates complete production-grade token system with Telegram bot, web interface, and PostgreSQL backend
"""

import os
import sys
from pathlib import Path

def create_directory_structure():
    """Create the project directory structure"""
    base_dir = Path("D:/unioncoin")
    base_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    (base_dir / "static").mkdir(exist_ok=True)
    (base_dir / "templates").mkdir(exist_ok=True)
    (base_dir / "logs").mkdir(exist_ok=True)
    
    return base_dir

def create_requirements_txt(base_dir):
    """Create requirements.txt file"""
    requirements = """fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
aiogram==3.4.1
python-multipart==0.0.6
jinja2==3.1.2
pydantic==2.5.0
python-dotenv==1.0.0
"""
    (base_dir / "requirements.txt").write_text(requirements)

def create_database_py(base_dir):
    """Create database.py with SQLAlchemy models and blockchain logic"""
    database_code = '''"""
Database Models and Blockchain Hash-Chain Logic
"""

import os
import hashlib
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import Optional, List

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/unioncoin")

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

def calculate_hash(sender: str, receiver: str, amount: float, timestamp: datetime, prev_hash: str) -> str:
    """Calculate SHA-256 hash for transaction"""
    data = f"{sender}{receiver}{amount}{timestamp.isoformat()}{prev_hash}"
    return hashlib.sha256(data.encode()).hexdigest()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    wallet_address = Column(String(12), unique=True, index=True)
    balance = Column(Float, default=1000.0)  # Welcome bonus
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.sender_id", back_populates="sender")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.receiver_id", back_populates="receiver")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    prev_hash = Column(String(64))
    current_hash = Column(String(64))
    transaction_type = Column(String(20))  # "p2p", "bonus", "admin_approval"
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

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
'''
    (base_dir / "database.py").write_text(database_code)

def create_bot_py(base_dir):
    """Create bot.py with Telegram bot functionality"""
    bot_code = '''"""
Telegram Bot for Token Ecosystem
"""

import asyncio
import random
import string
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from sqlalchemy.orm import Session
from database import get_db, User, Transaction, create_transaction, init_db
import os

# Bot configuration
BOT_TOKEN = "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A"
ADMIN_ID = 1685342390

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def generate_wallet_address():
    """Generate 12-character unique wallet address"""
    return \'\'.join(random.choices(string.ascii_lowercase + string.digits, k=12))

def get_or_create_user(db: Session, tg_id: int, username: str) -> User:
    """Get existing user or create new one"""
    user = db.query(User).filter(User.tg_id == tg_id).first()
    if not user:
        # Generate unique wallet address
        wallet_address = generate_wallet_address()
        while db.query(User).filter(User.wallet_address == wallet_address).first():
            wallet_address = generate_wallet_address()
        
        user = User(
            tg_id=tg_id,
            username=username,
            wallet_address=wallet_address,
            balance=1000.0  # Welcome bonus
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create welcome bonus transaction
        bonus_tx = create_transaction(db, 0, user.id, 1000.0, "bonus", True)
        db.add(bonus_tx)
        db.commit()
    
    return user

@dp.message(Command("start"))
async def start_command(message: types.Message):
    """Handle /start command"""
    with next(get_db()) as db:
        user = get_or_create_user(db, message.from_user.id, message.from_user.username)
        
        welcome_text = f"""
Welcome to UnionCoin Ecosystem!

Your Profile:
Username: @{user.username}
Wallet: `{user.wallet_address}`
Balance: {user.balance:.2f} UC

Commands:
/start - Show this message
/balance - Check balance
/request - Request tokens (requires admin approval)
/send <wallet> <amount> - Send tokens to another wallet
/help - Show help
"""
        await message.answer(welcome_text, parse_mode="Markdown")

@dp.message(Command("balance"))
async def balance_command(message: types.Message):
    """Handle /balance command"""
    with next(get_db()) as db:
        user = db.query(User).filter(User.tg_id == message.from_user.id).first()
        if user:
            await message.answer(f"Your balance: {user.balance:.2f} UC\\nWallet: `{user.wallet_address}`", parse_mode="Markdown")
        else:
            await message.answer("Please use /start to register first.")

@dp.message(Command("request"))
async def request_command(message: types.Message):
    """Handle token request with admin approval"""
    with next(get_db()) as db:
        user = db.query(User).filter(User.tg_id == message.from_user.id).first()
        if not user:
            await message.answer("Please use /start to register first.")
            return
        
        # Create admin approval request
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Approve", callback_data=f"approve_{user.id}_1000"),
             InlineKeyboardButton(text="Decline", callback_data=f"decline_{user.id}")]
        ])
        
        # Send to admin
        admin_text = f"Token Request:\\nUser: @{user.username}\\nWallet: {user.wallet_address}\\nAmount: 1000 UC"
        await bot.send_message(ADMIN_ID, admin_text, reply_markup=keyboard)
        
        await message.answer("Your request has been sent to admin for approval.")

@dp.callback_query(lambda c: c.data.startswith((\'approve_\', \'decline_\')))
async def handle_admin_callback(callback: CallbackQuery):
    """Handle admin approval/decline"""
    try:
        action, user_id, amount = callback.data.split(\'_\')
        user_id = int(user_id)
        amount = float(amount)
        
        with next(get_db()) as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                await callback.answer("User not found!")
                return
            
            if action == "approve":
                # Create approved transaction
                tx = create_transaction(db, 0, user.id, amount, "admin_approval", True)
                db.add(tx)
                
                # Update user balance
                user.balance += amount
                db.commit()
                
                # Notify user
                await bot.send_message(user.tg_id, f"Your request for {amount} UC has been approved!\\nNew balance: {user.balance:.2f} UC")
                await callback.answer(f"Approved {amount} UC for @{user.username}")
            else:
                await bot.send_message(user.tg_id, f"Your request for {amount} UC has been declined.")
                await callback.answer(f"Declined request for @{user.username}")
                
    except Exception as e:
        await callback.answer(f"Error: {str(e)}")

async def main():
    """Start the bot"""
    init_db()
    print("Bot started successfully!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
'''
    (base_dir / "bot.py").write_text(bot_code)

def create_api_py(base_dir):
    """Create api.py with FastAPI web server"""
    api_code = '''"""
FastAPI Web Server for P2P Token Transfers
"""

from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db, User, Transaction, create_transaction, verify_chain_integrity
from typing import Optional
import os

app = FastAPI(title="UnionCoin Web Wallet")

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, wallet_address: str = Form(...), db: Session = Depends(get_db)):
    """Handle login"""
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Invalid wallet address"
        })
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user
    })

@app.post("/send")
async def send_tokens(
    request: Request,
    sender_wallet: str = Form(...),
    receiver_wallet: str = Form(...),
    amount: float = Form(...),
    db: Session = Depends(get_db)
):
    """Handle P2P token transfer"""
    # Get users
    sender = db.query(User).filter(User.wallet_address == sender_wallet).first()
    receiver = db.query(User).filter(User.wallet_address == receiver_wallet).first()
    
    if not sender or not receiver:
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "user": sender,
            "error": "Invalid wallet addresses"
        })
    
    if sender.balance < amount:
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "user": sender,
            "error": "Insufficient balance"
        })
    
    # Create transaction
    tx = create_transaction(db, sender.id, receiver.id, amount, "p2p", True)
    db.add(tx)
    
    # Update balances
    sender.balance -= amount
    receiver.balance += amount
    db.commit()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": sender,
        "success": f"Successfully sent {amount} UC to {receiver_wallet}"
    })

@app.get("/verify")
async def verify_blockchain(db: Session = Depends(get_db)):
    """Verify blockchain integrity"""
    is_valid = verify_chain_integrity(db)
    return {"blockchain_valid": is_valid}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    (base_dir / "api.py").write_text(api_code)

def create_verify_py(base_dir):
    """Create verify.py for blockchain verification"""
    verify_code = '''"""
Blockchain Verification Script
Audits database for tampered records
"""

from database import get_db, Transaction, verify_chain_integrity
import sys

def audit_database():
    """Perform complete database audit"""
    print("Starting blockchain audit...")
    
    with next(get_db()) as db:
        # Verify chain integrity
        is_valid = verify_chain_integrity(db)
        
        if is_valid:
            print("Blockchain integrity verified - No tampering detected")
        else:
            print("BLOCKCHAIN TAMPERING DETECTED!")
            print("Analyzing transactions...")
            
            transactions = db.query(Transaction).order_by(Transaction.id).all()
            for i, tx in enumerate(transactions):
                print(f"Transaction {i+1}: ID={tx.id}, Hash={tx.current_hash[:16]}...")
        
        # Get statistics
        total_tx = db.query(Transaction).count()
        total_users = db.query(Transaction).distinct(Transaction.sender_id).count()
        
        print(f"\\nDatabase Statistics:")
        print(f"Total Transactions: {total_tx}")
        print(f"Active Users: {total_users}")
        print(f"Chain Valid: {\'Yes\' if is_valid else \'No\'}")

if __name__ == "__main__":
    audit_database()
'''
    (base_dir / "verify.py").write_text(verify_code)

def create_templates(base_dir):
    """Create HTML templates"""
    # Create index.html
    index_html = '''<!DOCTYPE html>
<html>
<head>
    <title>UnionCoin - Digital Token Ecosystem</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #2c3e50; text-align: center; }
        .btn { background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>UnionCoin Ecosystem</h1>
        <p>Welcome to the production-grade token system with blockchain verification.</p>
        <center>
            <a href="/login" class="btn">Enter Web Wallet</a>
        </center>
    </div>
</body>
</html>'''
    
    # Create login.html
    login_html = '''<!DOCTYPE html>
<html>
<head>
    <title>Login - UnionCoin</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        .btn { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; width: 100%; cursor: pointer; }
        .error { color: red; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Login to Wallet</h2>
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
        <form method="post">
            <input type="text" name="wallet_address" placeholder="Enter your 12-char wallet address" required>
            <button type="submit" class="btn">Login</button>
        </form>
    </div>
</body>
</html>'''
    
    # Create dashboard.html
    dashboard_html = '''<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - UnionCoin</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        .balance { font-size: 24px; color: #27ae60; text-align: center; margin: 20px 0; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        .btn { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .success { color: green; text-align: center; }
        .error { color: red; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Wallet Dashboard</h2>
        <p><strong>Wallet:</strong> {{ user.wallet_address }}</p>
        <div class="balance">Balance: {{ "%.2f"|format(user.balance) }} UC</div>
        
        {% if success %}
            <p class="success">{{ success }}</p>
        {% endif %}
        
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
        
        <h3>Send Tokens</h3>
        <form method="post" action="/send">
            <input type="hidden" name="sender_wallet" value="{{ user.wallet_address }}">
            <input type="text" name="receiver_wallet" placeholder="Receiver wallet address" required>
            <input type="number" name="amount" placeholder="Amount" step="0.01" required>
            <button type="submit" class="btn">Send Tokens</button>
        </form>
    </div>
</body>
</html>'''
    
    (base_dir / "templates" / "index.html").write_text(index_html)
    (base_dir / "templates" / "login.html").write_text(login_html)
    (base_dir / "templates" / "dashboard.html").write_text(dashboard_html)

def main():
    """Main initialization function"""
    print("Initializing Token Ecosystem...")
    
    # Create directory structure
    base_dir = create_directory_structure()
    print(f"Created directory structure at {base_dir}")
    
    # Create all files
    create_requirements_txt(base_dir)
    create_database_py(base_dir)
    create_bot_py(base_dir)
    create_api_py(base_dir)
    create_verify_py(base_dir)
    create_templates(base_dir)
    
    print("Created all project files")
    
    # Create README
    readme = '''# UnionCoin Token Ecosystem

Production-grade token system with Telegram bot, web interface, and PostgreSQL backend.

## Features
- Blockchain hash-chain verification
- Telegram bot with admin approval
- Web wallet for P2P transfers
- Tamper-proof transaction records

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up PostgreSQL database and update DATABASE_URL

3. Initialize database:
   ```bash
   python database.py
   ```

4. Run Telegram bot:
   ```bash
   python bot.py
   ```

5. Run web server:
   ```bash
   python api.py
   ```

6. Verify blockchain integrity:
   ```bash
   python verify.py
   ```
'''
    (base_dir / "README.md").write_text(readme)
    
    print(f"\\nToken Ecosystem initialized successfully at {base_dir}")
    print("\\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set up PostgreSQL database")
    print("3. Run: python database.py")
    print("4. Run: python bot.py")
    print("5. Run: python api.py")

if __name__ == "__main__":
    main()
