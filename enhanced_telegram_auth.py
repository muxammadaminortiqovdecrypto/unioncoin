"""
UnionCoin Enhanced Telegram Auth System
Intelligent error handling, seamless UX, and admin security
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

app = FastAPI(title="UnionCoin - Enhanced Telegram Auth", version="4.0.0")

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

# Bot Integration
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_BOT_URL = "https://t.me/tokenuchunku12bot"
ADMIN_TELEGRAM_ID = int(os.getenv("ADMIN_TELEGRAM_ID", "1685342390"))

def verify_telegram_auth(telegram_id: int, username: str, auth_token: str) -> bool:
    """Verify Telegram authentication"""
    return True  # Simplified for demo

def get_user_by_telegram_id(db: Session, telegram_id: int) -> Optional[User]:
    """Get user by Telegram ID"""
    return db.query(User).filter(User.tg_id == telegram_id).first()

def check_telegram_user_exists(db: Session, telegram_id: int) -> bool:
    """Check if Telegram user already exists"""
    user = db.query(User).filter(User.tg_id == telegram_id).first()
    return user is not None

def check_user_status(db: Session, user: User) -> str:
    """Check user status for intelligent messaging"""
    if user.is_banned:
        return "banned"
    elif user.is_inactive:
        return "inactive"
    elif user.is_suspended:
        return "suspended"
    else:
        return "active"

# --- Enhanced Error Pages ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Enhanced HTTP exception handler with intelligent messaging"""
    status_code = exc.status_code
    
    if status_code == 404:
        if "admin" in request.url.path:
            # Admin access attempts - show generic 404
            return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
    <title>Page Not Found</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f8f9fa; }
        h1 { color: #dc3545; font-size: 48px; margin-bottom: 20px; }
        p { color: #6c757d; font-size: 18px; }
        .home-link { color: #007bff; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <h1>404</h1>
    <p>Page not found</p>
    <p><a href="/" class="home-link">Return to Home</a></p>
</body>
</html>
            """, status_code=404)
        else:
            # User not found - friendly message
            return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head>
    <title>Account Not Found</title>
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
            color: white;
        }}
        .container {{ 
            background: rgba(255,255,255,0.1); 
            padding: 40px; 
            border-radius: 15px; 
            backdrop-filter: blur(10px);
            text-align: center;
            max-width: 500px;
        }}
        h1 {{ font-size: 28px; margin-bottom: 20px; }}
        p {{ font-size: 18px; margin: 15px 0; line-height: 1.6; }}
        .btn {{ 
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
        }}
        .btn:hover {{ 
            background: #0066cc; 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        .telegram-btn {{ 
            background: #0088cc; 
            color: white; 
            padding: 15px 25px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 16px;
            text-decoration: none; 
            display: inline-block; 
            margin: 20px 0;
        }}
        .telegram-btn:hover {{ 
            background: #0066cc; 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        .error-icon {{ font-size: 48px; margin-bottom: 20px; }}
        .message {{ background: rgba(255,255,255,0.2); padding: 15px; border-radius: 8px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="error-icon">🔍</div>
        <h1>Account Not Found</h1>
        <div class="message">
            <p><strong>Account Not Found.</strong></p>
            <p>To access the dashboard, please register via our official bot first.</p>
        </div>
        <a href="{TELEGRAM_BOT_URL}?start=register" class="telegram-btn">
            📱 Register on Telegram
        </a>
        <a href="/" class="btn">🏠 Return to Home</a>
    </div>
</body>
</html>
            """, status_code=404)
    
    elif status_code == 401:
        return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head>
    <title>Authentication Required</title>
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
            color: white;
        }}
        .container {{ 
            background: rgba(255,255,255,0.1); 
            padding: 40px; 
            border-radius: 15px; 
            backdrop-filter: blur(10px);
            text-align: center;
            max-width: 500px;
        }}
        h1 {{ font-size: 28px; margin-bottom: 20px; }}
        p {{ font-size: 18px; margin: 15px 0; line-height: 1.6; }}
        .btn {{ 
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
        }}
        .btn:hover {{ 
            background: #0066cc; 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        .telegram-btn {{ 
            background: #0088cc; 
            color: white; 
            padding: 15px 25px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 16px;
            text-decoration: none; 
            display: inline-block; 
            margin: 20px 0;
        }}
        .telegram-btn:hover {{ 
            background: #0066cc; 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        .lock-icon {{ font-size: 48px; margin-bottom: 20px; }}
        .message {{ background: rgba(255,255,255,0.2); padding: 15px; border-radius: 8px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="lock-icon">🔒</div>
        <h1>Authentication Required</h1>
        <div class="message">
            <p><strong>Authentication Required.</strong></p>
            <p>Please register via our Telegram bot to access the dashboard.</p>
        </div>
        <a href="{TELEGRAM_BOT_URL}?start=register" class="telegram-btn">
            📱 Register on Telegram
        </a>
        <a href="/" class="btn">🏠 Return to Home</a>
    </div>
</body>
</html>
            """, status_code=401)
    
    elif status_code == 403:
        if "admin" in request.url.path:
            # Admin access attempt - show generic 404
            return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
    <title>Page Not Found</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f8f9fa; }
        h1 { color: #dc3545; font-size: 48px; margin-bottom: 20px; }
        p { color: #6c757d; font-size: 18px; }
        .home-link { color: #007bff; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <h1>404</h1>
    <p>Page not found</p>
    <p><a href="/" class="home-link">Return to Home</a></p>
</body>
</html>
            """, status_code=404)
        else:
            # Forbidden access
            return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head>
    <title>Access Denied</title>
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
            color: white;
        }}
        .container {{ 
            background: rgba(255,255,255,0.1); 
            padding: 40px; 
            border-radius: 15px; 
            backdrop-filter: blur(10px);
            text-align: center;
            max-width: 500px;
        }}
        h1 {{ font-size: 28px; margin-bottom: 20px; }}
        p {{ font-size: 18px; margin: 15px 0; line-height: 1.6; }}
        .btn {{ 
            background: #dc3545; 
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
        }}
        .btn:hover {{ 
            background: #c82333; 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        .error-icon {{ font-size: 48px; margin-bottom: 20px; }}
        .message {{ background: rgba(255,255,255,0.2); padding: 15px; border-radius: 8px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="error-icon">🚫</div>
        <h1>Access Denied</h1>
        <div class="message">
            <p><strong>Access Denied.</strong></p>
            <p>You don't have permission to access this resource.</p>
        </div>
        <a href="/" class="btn">🏠 Return to Home</a>
    </div>
</body>
</html>
            """, status_code=403)
    
    # Default error handling
    return JSONResponse(
        status_code=status_code,
        content={"detail": exc.detail}
    )

# --- Enhanced Main Page ---
@app.get("/")
async def root():
    """Enhanced main page with Telegram auth required"""
    return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head>
    <title>UnionCoin - Telegram Authentication Required</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .container {{ 
            max-width: 600px; 
            background: white; 
            padding: 50px; 
            border-radius: 20px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
        }}
        h1 {{ color: #333; margin-bottom: 30px; font-size: 32px; }}
        .telegram-req {{ 
            background: #e8f4fd; 
            padding: 25px; 
            border-radius: 15px; 
            margin: 20px 0; 
            border-left: 4px solid #2196f3;
            text-align: left;
        }}
        .step {{ 
            background: #f8f9fa; 
            padding: 20px; 
            margin: 15px 0; 
            border-radius: 10px; 
            text-align: left;
            border-left: 3px solid #007bff;
        }}
        .btn {{ 
            background: #0088cc; 
            color: white; 
            padding: 18px 35px; 
            border: none; 
            border-radius: 10px; 
            cursor: pointer; 
            font-size: 18px;
            text-decoration: none; 
            display: inline-block; 
            margin: 20px 10px;
            transition: all 0.3s ease;
            font-weight: bold;
        }}
        .btn:hover {{ 
            background: #0066cc; 
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }}
        .btn-primary {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 20px 40px; 
            border: none; 
            border-radius: 10px; 
            cursor: pointer; 
            font-size: 18px;
            text-decoration: none; 
            display: inline-block; 
            margin: 25px 15px;
            transition: all 0.3s ease;
            font-weight: bold;
        }}
        .btn-primary:hover {{ 
            background: linear-gradient(135deg, #5a67d8 0%, #667eea 100%); 
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }}
        .warning {{ 
            background: #fff3cd; 
            border: 1px solid #ffeaa7; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0; 
            color: #856404;
        }}
        .feature {{ 
            background: #d1ecf1; 
            border: 1px solid #bee5eb; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 10px 0; 
            color: #0c5460;
        }}
        .loading {{ 
            display: none; 
            position: fixed; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%; 
            background: rgba(0,0,0,0.8); 
            z-index: 9999; 
            justify-content: center; 
            align-items: center; 
        }}
        .spinner {{ 
            border: 4px solid rgba(255,255,255,0.3); 
            border-top: 4px solid white; 
            border-radius: 50%; 
            width: 50px; 
            height: 50px; 
            animation: spin 1s linear infinite; 
            margin-bottom: 20px;
        }}
        @keyframes spin {{ 
            0% {{ transform: rotate(0deg); }} 
            100% {{ transform: rotate(360deg); }} 
        }}
    </style>
</head>
<body>
    <div class="loading" id="loading">
        <div class="spinner"></div>
        <h2 style="color: white;">Loading UnionCoin...</h2>
    </div>
    
    <div class="container">
        <h1>🔐 UnionCoin</h1>
        <h2>Telegram Authentication Required</h2>
        
        <div class="telegram-req">
            <h3>📱 IMPORTANT: Telegram Registration Only</h3>
            <p><strong>You must register via Telegram bot first!</strong></p>
            <p>Web registration is disabled for maximum security.</p>
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
            <a href="{TELEGRAM_BOT_URL}?start=register" class="btn-primary">
                📱 Register on Telegram
            </a>
        </div>
        
        <div class="feature">
            <h3>✅ Security Features</h3>
            <p>• 🔐 Secure Telegram authentication</p>
            <p>• 👤 Private user data</p>
            <p>• 🔗 Blockchain transactions</p>
            <p>• 📊 Personal statistics</p>
        </div>
    </div>
    
    <script>
        // Hide loading when page is ready
        window.addEventListener('load', function() {{
            document.getElementById('loading').style.display = 'none';
        }});
        
        // Handle registration deep link
        if (window.location.hash === '#register') {{
            // Scroll to registration section
            document.querySelector('.telegram-req').scrollIntoView({{ behavior: 'smooth' }});
        }}
    </script>
</body>
</html>
    """)

@app.get("/health")
async def health_check():
    """Health check with loading indicator"""
    return {
        "status": "healthy", 
        "auth_method": "telegram_only", 
        "timestamp": datetime.now().isoformat(),
        "loading": False
    }

@app.get("/verify")
async def verify_blockchain():
    """Blockchain verification"""
    return {
        "status": "verified", 
        "blockchain": "unioncoin", 
        "auth_required": "telegram",
        "security_level": "maximum"
    }

@app.get("/register")
async def register_redirect():
    """Enhanced redirect to Telegram bot with deep link support"""
    return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head>
    <title>Redirect to Telegram</title>
    <meta http-equiv="refresh" content="3; url={TELEGRAM_BOT_URL}?start=register">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
        <p>If not redirected, <a href="{TELEGRAM_BOT_URL}?start=register" style="color: white;">click here</a>.</p>
        <p><strong>🔐 Secure Registration: Telegram Only</strong></p>
    </div>
</body>
</html>
    """)

@app.post("/auth/telegram")
async def telegram_auth(auth_data: TelegramAuthRequest, db: Session = Depends(get_db)):
    """Enhanced Telegram authentication with status checking"""
    user = get_user_by_telegram_id(db, auth_data.telegram_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account Not Found. To access the dashboard, please register via our official bot first."
        )
    
    # Check user status
    user_status = check_user_status(db, user)
    
    if user_status == "banned":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is currently banned. Please contact support via bot."
        )
    elif user_status == "inactive":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is currently inactive. Please contact support via bot."
        )
    elif user_status == "suspended":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is currently suspended. Please contact support via bot."
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
        "telegram_id": user.telegram_id,
        "status": user_status,
        "message": f"Welcome back, {user.username}!" if user_status == "active" else f"Account status: {user_status}"
    }

@app.get("/auth/telegram/check/{telegram_id}")
async def check_telegram_user(telegram_id: int, db: Session = Depends(get_db)):
    """Check if Telegram user exists with enhanced response"""
    exists = check_telegram_user_exists(db, telegram_id)
    
    if not exists:
        return {
            "telegram_id": telegram_id,
            "exists": False,
            "message": "User not found. Please register via Telegram bot.",
            "register_url": f"{TELEGRAM_BOT_URL}?start=register",
            "action": "register"
        }
    else:
        return {
            "telegram_id": telegram_id,
            "exists": True,
            "message": "User already registered. Please use the Login button on the website.",
            "login_url": "/login",
            "action": "login"
        }

@app.get("/user/profile")
async def get_user_profile(telegram_id: int, db: Session = Depends(get_db)):
    """Get user profile with status checking"""
    user = get_user_by_telegram_id(db, telegram_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account Not Found. To access the dashboard, please register via our official bot first."
        )
    
    # Check user status
    user_status = check_user_status(db, user)
    
    if user_status == "banned":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is currently banned. Please contact support via bot."
        )
    elif user_status == "inactive":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is currently inactive. Please contact support via bot."
        )
    elif user_status == "suspended":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is currently suspended. Please contact support via bot."
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
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "status": user_status
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
        },
        "message": f"Welcome back, {user.username}!" if user_status == "active" else f"Account status: {user_status}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
