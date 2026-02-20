"""
UnionCoin Telegram Authentication API
Users must register via Telegram bot only - no web registration
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from database import get_db, User, Transaction, create_transaction
from pydantic import BaseModel
from typing import Optional, List
import os
import hashlib
import random
import string
from datetime import datetime
import requests

app = FastAPI(title="UnionCoin - Telegram Auth Only", version="3.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://unioncoin.onrender.com",
        "http://localhost:8000",
        "https://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class TelegramAuthRequest(BaseModel):
    telegram_id: int
    username: str
    auth_token: str

class UserResponse(BaseModel):
    id: int
    username: str
    wallet_address: str
    balance: float
    created_at: Optional[datetime]
    telegram_id: Optional[int]

class TransactionRequest(BaseModel):
    receiver_wallet: str
    amount: float

# Telegram Bot Integration
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_BOT_URL = "https://t.me/tokenuchunku12bot"

def verify_telegram_auth(telegram_id: int, username: str, auth_token: str) -> bool:
    """Verify Telegram authentication"""
    # In a real implementation, you'd verify with Telegram API
    # For now, we'll check if user exists in database
    return True  # Simplified for demo

def get_user_by_telegram_id(db: Session, telegram_id: int) -> Optional[User]:
    """Get user by Telegram ID"""
    return db.query(User).filter(User.tg_id == telegram_id).first()

def check_telegram_user_exists(db: Session, telegram_id: int) -> bool:
    """Check if Telegram user already exists"""
    user = db.query(User).filter(User.tg_id == telegram_id).first()
    return user is not None

# --- Routes ---
@app.get("/")
async def root():
    """Main page - Telegram auth only"""
    return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
    <title>UnionCoin - Telegram Authentication Required</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container { 
            max-width: 500px; 
            background: white; 
            padding: 40px; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
        }
        h1 { color: #333; margin-bottom: 30px; font-size: 28px; }
        .telegram-req { 
            background: #e8f4fd; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0; 
            border-left: 4px solid #2196f3;
        }
        .step { 
            background: #f8f9fa; 
            padding: 15px; 
            margin: 15px 0; 
            border-radius: 8px; 
            text-align: left;
        }
        .btn { 
            background: #0088cc; 
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 16px;
            text-decoration: none; 
            display: inline-block; 
            margin: 20px 10px;
            transition: all 0.3s ease;
        }
        .btn:hover { 
            background: #0066cc; 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .warning { 
            background: #fff3cd; 
            border: 1px solid #ffeaa7; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 20px 0; 
            color: #856404;
        }
        .feature { 
            background: #d1ecf1; 
            border: 1px solid #bee5eb; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 10px 0; 
            color: #0c5460;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 UnionCoin</h1>
        <h2>Telegram Authentication Required</h2>
        
        <div class="telegram-req">
            <h3>📱 IMPORTANT: Telegram Registration Only</h3>
            <p><strong>You must register via Telegram bot first!</strong></p>
            <p>Web registration is disabled for security.</p>
        </div>
        
        <div class="step">
            <h3>📋 Step 1: Register via Telegram</h3>
            <p>1. Open Telegram bot: <strong>@tokenuchunku12bot</strong></p>
            <p>2. Send <strong>/start</strong> command</p>
            <p>3. Create your account with username and password</p>
            <p>4. Get your unique wallet address</p>
        </div>
        
        <div class="step">
            <h3>🔑 Step 2: Get Auth Token</h3>
            <p>After registration, you'll receive an authentication token.</p>
            <p>Use this token to access web interface.</p>
        </div>
        
        <div class="warning">
            <h3>⚠️ Security Notice</h3>
            <p>• Each Telegram account can only have ONE UnionCoin account</p>
            <p>• Your data is private and secure</p>
            <p>• No web registration available</p>
            <p>• Admin access via Telegram only</p>
        </div>
        
        <div class="step">
            <h3>🚀 Get Started</h3>
            <p>Click the button below to open Telegram bot:</p>
            <a href="https://t.me/tokenuchunku12bot" class="btn">📱 Open Telegram Bot</a>
        </div>
        
        <div class="feature">
            <h3>✅ Features</h3>
            <p>• 🔐 Secure Telegram authentication</p>
            <p>• 👤 Private user data</p>
            <p>• 🔗 Blockchain transactions</p>
            <p>• 📊 Personal statistics</p>
        </div>
    </div>
</body>
</html>
    """)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "auth_method": "telegram_only", "timestamp": datetime.now().isoformat()}

@app.get("/verify")
async def verify_blockchain():
    """Blockchain verification"""
    return {"status": "verified", "blockchain": "unioncoin", "auth_required": "telegram"}

@app.post("/auth/telegram")
async def telegram_auth(auth_data: TelegramAuthRequest, db: Session = Depends(get_db)):
    """Authenticate via Telegram"""
    # Verify user exists in database
    user = get_user_by_telegram_id(db, auth_data.telegram_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please register via Telegram bot first."
        )
    
    if user.username != auth_data.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username mismatch"
        )
    
    # Generate session token
    session_token = hashlib.sha256(f"{user.id}{auth_data.telegram_id}{datetime.now()}".encode()).hexdigest()
    
    return {
        "message": "Authentication successful",
        "access_token": session_token,
        "token_type": "telegram",
        "user_id": user.id,
        "username": user.username,
        "wallet_address": user.wallet_address,
        "balance": user.balance,
        "telegram_id": user.telegram_id
    }

@app.get("/auth/telegram/check/{telegram_id}")
async def check_telegram_user(telegram_id: int, db: Session = Depends(get_db)):
    """Check if Telegram user exists"""
    exists = check_telegram_user_exists(db, telegram_id)
    
    return {
        "telegram_id": telegram_id,
        "exists": exists,
        "message": "User exists" if exists else "User not found. Please register via Telegram bot.",
        "register_url": "https://t.me/tokenuchunku12bot"
    }

@app.get("/user/profile")
async def get_user_profile(telegram_id: int, db: Session = Depends(get_db)):
    """Get user profile via Telegram ID"""
    user = get_user_by_telegram_id(db, telegram_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please register via Telegram bot first."
        )
    
    # Get user's transactions
    transactions = db.query(Transaction).filter(
        or_(Transaction.sender_id == user.id, Transaction.receiver_id == user.id)
    ).order_by(Transaction.timestamp.desc()).limit(20).all()
    
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "wallet_address": user.wallet_address,
            "balance": user.balance,
            "telegram_id": user.telegram_id,
            "created_at": user.created_at.isoformat() if user.created_at else None
        },
        "transactions": [
            {
                "id": tx.id,
                "sender_id": tx.sender_id,
                "receiver_id": tx.receiver_id,
                "amount": tx.amount,
                "timestamp": tx.timestamp.isoformat() if tx.timestamp else None,
                "transaction_type": tx.transaction_type,
                "tx_hash": tx.tx_hash
            }
            for tx in transactions
        ],
        "stats": {
            "total_transactions": len(transactions),
            "sent": len([tx for tx in transactions if tx.sender_id == user.id]),
            "received": len([tx for tx in transactions if tx.receiver_id == user.id])
        }
    }

@app.post("/user/transaction")
async def create_transaction_telegram(
    tx_data: TransactionRequest,
    telegram_id: int,
    db: Session = Depends(get_db)
):
    """Create transaction via Telegram authentication"""
    user = get_user_by_telegram_id(db, telegram_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found. Please register via Telegram bot first."
        )
    
    # Check balance
    if user.balance < tx_data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )
    
    # Get receiver
    receiver = db.query(User).filter(User.wallet_address == tx_data.receiver_wallet).first()
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )
    
    # Create transaction
    transaction = create_transaction(
        db=db,
        sender_id=user.id,
        receiver_id=receiver.id,
        amount=tx_data.amount,
        tx_type="p2p"
    )
    
    # Update balances
    user.balance -= tx_data.amount
    receiver.balance += tx_data.amount
    
    db.commit()
    
    return {
        "message": "Transaction created successfully",
        "transaction_id": transaction.id,
        "tx_hash": transaction.tx_hash,
        "sender_balance": user.balance,
        "receiver_balance": receiver.balance
    }

@app.get("/register")
async def register_redirect():
    """Redirect to Telegram bot for registration"""
    return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head>
    <title>Redirect to Telegram</title>
    <meta http-equiv="refresh" content="3; url=https://t.me/tokenuchunku12bot">
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 20px;
            text-align: center;
            color: white;
        }}
        .container {{ 
            background: rgba(255,255,255,0.1); 
            padding: 40px; 
            border-radius: 15px; 
            backdrop-filter: blur(10px);
        }}
        h1 {{ font-size: 24px; margin-bottom: 20px; }}
        p {{ font-size: 18px; margin: 10px 0; }}
        .spinner {{ 
            border: 4px solid rgba(255,255,255,0.3); 
            border-top: 4px solid white; 
            border-radius: 50%; 
            width: 40px; 
            height: 40px; 
            animation: spin 1s linear infinite; 
            margin: 20px auto;
        }}
        @keyframes spin {{ 
            0% {{ transform: rotate(0deg); }} 
            100% {{ transform: rotate(360deg); }} 
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="spinner"></div>
        <h1>📱 Redirecting to Telegram Bot...</h1>
        <p>You will be automatically redirected to the Telegram bot for registration.</p>
        <p>If not redirected, <a href="https://t.me/tokenuchunku12bot" style="color: white;">click here</a>.</p>
    </div>
</body>
</html>
    """)

# --- Removed Web Registration ---
# All web registration endpoints are removed
# Users MUST register via Telegram bot only

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
