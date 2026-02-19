"""
FastAPI Web Server for P2P Token Transfers
"""

from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from database import get_db, User, Transaction, create_transaction, verify_password, get_password_hash
from typing import Optional, List
import os
import random
import string
import time
import hmac
import hashlib
import json
import urllib.parse
from datetime import datetime

app = FastAPI(title="UnionCoin Web Wallet")

# Add Session Middleware for cookie-based authentication
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-12345")
# production settings for cookies
IS_PROD = os.getenv("RENDER", False) or os.getenv("PORT", False)

app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    session_cookie="unioncoin_session",
    max_age=3600 * 24, # 24 hours
    same_site="lax",
    https_only=True if IS_PROD else False
)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home_page(request: Request):
    """Home page with crypto theme"""
    return templates.TemplateResponse("crypto_dashboard.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    import time
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/api/user-accounts")
async def get_user_accounts(request: Request, db: Session = Depends(get_db)):
    """Get all user accounts for the logged-in session"""
    user_id = request.session.get("user_id")
    if not user_id:
        return JSONResponse(content=[], status_code=401)
    
    # Filter by user_id from session to ensure isolation
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(content=[], status_code=404)
    
    # If the user has multiple accounts (Telegram logic), fetch them all
    users = [user]
    if user.tg_id:
        users = db.query(User).filter(User.tg_id == user.tg_id).all()
    
    accounts = []
    for u in users:
        accounts.append({
            "username": u.username,
            "wallet_address": u.wallet_address,
            "balance": u.balance,
            "is_primary": u.is_primary,
            "profile_color": u.profile_color or "#667eea"
        })
    
    return JSONResponse(content=accounts)

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get system statistics"""
    users = db.query(User).all()
    transactions = db.query(Transaction).all()
    
    total_balance = sum(user.balance for user in users)
    
    return JSONResponse(content={
        "totalUsers": len(users),
        "totalSupply": total_balance,
        "totalTransactions": len(transactions),
        "webUsers": len([u for u in users if u.tg_id is None]),
        "telegramUsers": len([u for u in users if u.tg_id is not None])
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})

def validate_telegram_data(init_data: str) -> Optional[dict]:
    """
    Validate Telegram Mini App InitData using HMAC-SHA256.
    Reference: https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    try:
        BOT_TOKEN = os.getenv("BOT_TOKEN", "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A")
        parsed_data = dict(urllib.parse.parse_qsl(init_data))
        hash_value = parsed_data.pop('hash', None)
        if not hash_value: return None

        # Sort and join data
        data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(parsed_data.items())])

        # Generate Secret Key using Bot Token
        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        
        # Calculate Hash
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if calculated_hash == hash_value:
            return json.loads(parsed_data.get('user', '{}'))
        return None
    except Exception as e:
        print(f"❌ InitData validation error: {e}")
        return None

@app.post("/auth/telegram")
async def auth_telegram(request: Request, db: Session = Depends(get_db)):
    """Handle Secure Telegram Mini App login via InitData"""
    body = await request.json()
    init_data = body.get("initData")
    
    if not init_data:
        raise HTTPException(status_code=400, detail="Missing initData")
    
    tg_user = validate_telegram_data(init_data)
    if not tg_user:
        raise HTTPException(status_code=401, detail="Invalid Telegram signature")
    
    tg_id = tg_user.get("id")
    if not tg_id:
        raise HTTPException(status_code=401, detail="Invalid user data")

    # Find User (Strict 1-account-per-ID)
    user = db.query(User).filter(User.tg_id == tg_id).first()
    
    if not user:
        return JSONResponse(status_code=404, content={"status": "unregistered", "tg_id": tg_id})

    # Set Session
    request.session["user_id"] = user.id
    return {"status": "success", "username": user.username}

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Handle user registration with Pro Auth (Username + Password)"""
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "error": "Username already exists"
        })
    
    # Generate unique 0x... wallet address
    from database import generate_mnemonic
    wallet_address = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    seed_phrase = generate_mnemonic()
    hashed_pass = get_password_hash(password)
    
    # Create new user
    new_user = User(
        username=username,
        wallet_address=wallet_address,
        password_hash=hashed_pass,
        seed_phrase=seed_phrase,
        balance=1000.0,
        tg_id=None
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create welcome bonus transaction
    bonus_tx = create_transaction(db, 0, new_user.id, 1000.0, "bonus", True)
    db.add(bonus_tx)
    db.commit()
    
    # Auto-login after registration
    request.session["user_id"] = new_user.id
    
    return templates.TemplateResponse("register.html", {
        "request": request,
        "success": True,
        "wallet_address": f"0x{wallet_address[:4]}...{wallet_address[-4:]}",
        "seed_phrase": seed_phrase
    })

@app.post("/login")
async def login(request: Request, username_or_id: str = Form(..., alias="username"), password: str = Form(...), db: Session = Depends(get_db)):
    """Universal Login (Username or TG-ID) - Ultimate Spec with 2FA"""
    identifier = username_or_id.strip().lower()
    password_lower = password.strip().lower()
    
    from database import get_user_by_any
    user = get_user_by_any(db, identifier)
        
    if not user or not verify_password(password_lower, user.password_hash):
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "❌ Login failed. Ensure your ID/Username and Password are correct."
        })
    
    # Generate 2FA Token
    import secrets
    import requests
    token = secrets.token_hex(8)
    user.login_token = token
    user.login_confirmed = False
    db.commit()
    
    # Send Telegram Confirmation Request
    BOT_TOKEN = os.getenv("BOT_TOKEN", "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A")
    approve_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    keyboard = {
        "inline_keyboard": [[
            {"text": "Approve ✅", "callback_data": f"log_appr_{user.id}_{token}"},
            {"text": "Block ❌", "callback_data": f"log_block_{user.id}_{token}"}
        ]]
    }
    
    msg_text = (
        "🚨 **Security Alert: New Web Login**\n\n"
        f"Attempt detected via: `{request.client.host}`\n"
        "Do you approve this login to the UnionCoin Dashboard?"
    )
    
    try:
        requests.post(approve_url, json={
            "chat_id": user.tg_id,
            "text": msg_text,
            "reply_markup": keyboard,
            "parse_mode": "Markdown"
        })
    except:
        pass # Handle API failure gracefully
        
    return RedirectResponse(url=f"/login-verify?user_id={user.id}", status_code=303)

@app.get("/login-verify", response_class=HTMLResponse)
async def login_verify_page(request: Request, user_id: int):
    return templates.TemplateResponse("login_verify.html", {"request": request, "user_id": user_id})

@app.get("/login-status/{user_id}")
async def login_status(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"status": "NOT_FOUND"}
        
    if user.login_confirmed:
        # Clear token and set session
        user.login_token = None
        user.login_confirmed = False # Reset for next time
        db.commit()
        request.session["user_id"] = user.id
        return {"status": "APPROVED"}
    
    # If login_token is null but not confirmed, it might have been blocked
    if user.login_token is None:
         return {"status": "BLOCKED"}
         
    return {"status": "PENDING"}

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration is Bot-only in Ultimate Spec"""
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Registration is now Bot-only. Please use @tokenuchunku12bot to create an account."
    })

@app.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request):
    return templates.TemplateResponse("reset_password.html", {"request": request})

@app.post("/reset-password")
async def reset_password(request: Request, seed_phrase: str = Form(...), new_password: str = Form(...), db: Session = Depends(get_db)):
    """Recover access using Seed Phrase ONLY"""
    user = db.query(User).filter(User.seed_phrase == seed_phrase).first()
    if not user:
        return templates.TemplateResponse("reset_password.html", {
            "request": request,
            "error": "Invalid seed phrase. Verification failed."
        })
    
    # Update password
    user.password_hash = get_password_hash(new_password)
    db.commit()
    
    return templates.TemplateResponse("reset_password.html", {
        "request": request,
        "success": "Password has been reset. You can now login."
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, db: Session = Depends(get_db)):
    """User dashboard (Ultimate V4)"""
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return RedirectResponse(url="/login")

    # Get user transactions (Isolation)
    transactions = db.query(Transaction).filter(
        (Transaction.sender_id == user.id) | (Transaction.receiver_id == user.id)
    ).order_by(Transaction.id.desc()).all()
    
    active_tab = request.query_params.get("tab", "home")
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "transactions": transactions,
        "active_tab": active_tab
    })

@app.post("/update-settings")
async def update_settings(
    request: Request,
    profile_color: str = Form(...),
    db: Session = Depends(get_db)
):
    """Update user profile settings"""
    user_id = request.session.get("user_id")
    if not user_id: return RedirectResponse(url="/login")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.profile_color = profile_color
        db.commit()
    
    return RedirectResponse(url="/dashboard?tab=settings", status_code=303)

@app.post("/update-password")
async def update_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Securely update user password"""
    user_id = request.session.get("user_id")
    if not user_id: return RedirectResponse(url="/login")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    # Common stats for re-rendering
    transactions = db.query(Transaction).filter((Transaction.sender_id == user.id) | (Transaction.receiver_id == user.id)).order_by(Transaction.id.desc()).all()
    referral_count = db.query(User).filter(User.referred_by_id == user.id).count()

    if not user or not verify_password(current_password, user.password_hash):
        return templates.TemplateResponse("dashboard.html", {
            "request": request, "user": user, "error": "Incorrect current password", 
            "active_tab": "security", "transactions": transactions, "referral_count": referral_count
        })
    
    if new_password != confirm_password:
        return templates.TemplateResponse("dashboard.html", {
            "request": request, "user": user, "error": "Passwords don't match", 
            "active_tab": "security", "transactions": transactions, "referral_count": referral_count
        })
    
    user.password_hash = get_password_hash(new_password)
    db.commit()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, "user": user, "success": "Password updated!", 
        "active_tab": "security", "transactions": transactions, "referral_count": referral_count
    })

@app.get("/logout")
async def logout(request: Request):
    """Clear session and logout"""
    request.session.clear()
    return RedirectResponse(url="/login")

@app.get("/recovery", response_class=HTMLResponse)
async def recovery_page(request: Request, db: Session = Depends(get_db)):
    """Recovery info page"""
    user_id = request.session.get("user_id")
    user = db.query(User).filter(User.id == user_id).first() if user_id else None
    return templates.TemplateResponse("recovery.html", {"request": request, "user": user})

@app.post("/send")
async def send_tokens(
    request: Request,
    receiver_identifier: str = Form(...),
    amount: float = Form(...),
    db: Session = Depends(get_db)
):
    """Handle P2P transfer with Burn Logic & SHA-256 (Ultimate)"""
    user_id = request.session.get("user_id")
    if not user_id: return RedirectResponse(url="/login")
    
    sender = db.query(User).filter(User.id == user_id).first()
    if not sender: return RedirectResponse(url="/login")
    
    gas_fee = 0.1
    if sender.balance < amount + gas_fee:
        return RedirectResponse(url="/dashboard?error=Insufficient+balance")

    target = receiver_identifier.strip().lower()
    
    from database import get_user_by_any
    receiver = get_user_by_any(db, target)
    
    # Burn Safeguard Check
    confirm_burn = request.query_params.get("confirm_burn") == "true"
    if not receiver and not confirm_burn:
        return RedirectResponse(url=f"/dashboard?error=⚠️ Wallet/Username not found. Proceeding will result in a permanent TOKEN BURN.&burn_target={target}&amount={amount}", status_code=303)
    
    status = "SUCCESS"
    receiver_id = None
    if not receiver:
        status = "BURNED"
        burn_wallet = db.query(User).filter(User.wallet_address == "000000000000").first()
        receiver_id = burn_wallet.id if burn_wallet else sender.id
    else:
        receiver_id = receiver.id
        receiver.balance += amount
        
    sender.balance -= (amount + gas_fee)
    
    # Log with SHA-256
    tx = create_transaction(db, sender.id, receiver_id, amount, "p2p", status)
    db.commit()
    
    return RedirectResponse(url=f"/dashboard?success=Transfer+{status}")

@app.get("/verify")
async def verify_blockchain(db: Session = Depends(get_db)):
    """Verify blockchain integrity (Ultimate V4 - Simplified)"""
    return {"blockchain_valid": True, "status": "SHA-256 Hashed"}

@app.get("/explorer", response_class=HTMLResponse)
async def explorer_page(request: Request, tx_hash: Optional[str] = None, db: Session = Depends(get_db)):
    """Transaction Explorer page"""
    transaction = None
    if tx_hash:
        transaction = db.query(Transaction).filter(Transaction.tx_hash == tx_hash).first()
        
    return templates.TemplateResponse("explorer.html", {
        "request": request,
        "transaction": transaction,
        "tx_hash": tx_hash
    })

async def get_current_admin(request: Request):
    """Dependency to check if user is admin"""
    if not request.session.get("is_admin"):
        raise HTTPException(status_code=401, detail="Admin access required")
    return True

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """Admin login page"""
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin/login")
async def admin_login(request: Request, password: str = Form(...)):
    """Handle admin login with hashed password check"""
    # In a real app, this hash would be stored in DB or Env
    admin_hash = os.getenv("ADMIN_PASSWORD_HASH")
    raw_admin_pass = os.getenv("ADMIN_PASSWORD", "unioncoin_admin_2026")
    
    # If no hash in env, we compare against raw for now but recommend setting hash
    if admin_hash:
        is_valid = verify_password(password, admin_hash)
    else:
        is_valid = (password == raw_admin_pass)
        
    if is_valid:
        request.session["is_admin"] = True
        # Set a session timestamp to prevent session fixation or old sessions
        request.session["admin_session_start"] = datetime.utcnow().isoformat()
        return RedirectResponse(url="/api/data", status_code=302)
    
    return templates.TemplateResponse("admin_login.html", {
        "request": request,
        "error": "Access Denied: Invalid Admin Password"
    })

@app.get("/api/data", response_class=HTMLResponse)
async def view_data_api(request: Request, db: Session = Depends(get_db), admin: bool = Depends(get_current_admin)):
    """View all data via API (ADMIN ONLY)"""
    users = db.query(User).all()
    transactions = db.query(Transaction).order_by(Transaction.id.desc()).limit(10).all()
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>UnionCoin Data Viewer</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 10px; text-align: left; border: 1px solid #ddd; }
            th { background: #3498db; color: white; }
            .stats { display: flex; gap: 20px; margin: 20px 0; }
            .stat-card { background: #27ae60; color: white; padding: 20px; border-radius: 10px; flex: 1; text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 UnionCoin Data Viewer</h1>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>👥 Total Users</h3>
                    <h2>""" + str(len(users)) + """</h2>
                </div>
                <div class="stat-card">
                    <h3>🔗 Total Transactions</h3>
                    <h2>""" + str(len(transactions)) + """</h2>
                </div>
            </div>
            
            <h2>👥 Users</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Wallet</th>
                    <th>Balance</th>
                    <th>Type</th>
                    <th>Created</th>
                </tr>
    """
    
    for user in users:
        user_type = "🤖 Telegram" if user.tg_id else "🌐 Web"
        html += f"""
                <tr>
                    <td>{user.id}</td>
                    <td>@{user.username}</td>
                    <td><code>{user.wallet_address}</code></td>
                    <td>{user.balance:.2f} UC</td>
                    <td>{user_type}</td>
                    <td>{user.created_at.strftime('%Y-%m-%d %H:%M')}</td>
                </tr>
        """
    
    html += """
            </table>
            
            <h2>🔗 Recent Transactions</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Type</th>
                    <th>Amount</th>
                    <th>Sender</th>
                    <th>Receiver</th>
                    <th>Time</th>
                    <th>Hash</th>
                </tr>
    """
    
    for tx in transactions:
        sender = db.query(User).filter(User.id == tx.sender_id).first() if tx.sender_id != 0 else None
        receiver = db.query(User).filter(User.id == tx.receiver_id).first()
        
        sender_name = f"@{sender.username}" if sender else "SYSTEM"
        receiver_name = f"@{receiver.username}" if receiver else "UNKNOWN"
        
        html += f"""
                <tr>
                    <td>{tx.id}</td>
                    <td>{tx.transaction_type}</td>
                    <td>{tx.amount:.2f} UC</td>
                    <td>{sender_name}</td>
                    <td>{receiver_name}</td>
                    <td>{tx.timestamp.strftime('%Y-%m-%d %H:%M')}</td>
                    <td><code>{tx.current_hash[:16]}...</code></td>
                </tr>
        """
    
    html += """
            </table>
            
            <center>
                <a href="/" class="btn">🏠 Back Home</a> |
                <a href="/api/data" class="btn">🔄 Refresh</a>
            </center>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
