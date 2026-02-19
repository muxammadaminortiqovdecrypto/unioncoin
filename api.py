"""
FastAPI Web Server for P2P Token Transfers
"""

from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from database import get_db, User, Transaction, create_transaction, verify_chain_integrity, verify_password, get_password_hash
from typing import Optional, List
import os
import random
import string
import time
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

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request, username: str = Form(...), email: str = Form(""), db: Session = Depends(get_db)):
    """Handle user registration"""
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "error": "Username already exists"
        })
    
    # Generate unique wallet address
    def generate_wallet_address():
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    
    wallet_address = generate_wallet_address()
    while db.query(User).filter(User.wallet_address == wallet_address).first():
        wallet_address = generate_wallet_address()
    
    # Create new user
    new_user = User(
        username=username,
        wallet_address=wallet_address,
        balance=1000.0,  # Welcome bonus
        tg_id=None  # None for web users
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
        "wallet_address": wallet_address
    })

@app.post("/login")
async def login(request: Request, wallet_address: str = Form(...), db: Session = Depends(get_db)):
    """Handle login and set session"""
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Invalid wallet address"
        })
    
    # Set session
    request.session["user_id"] = user.id
    
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, db: Session = Depends(get_db)):
    """User dashboard centered on the logged-in user"""
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login")
    
    # Get user transactions (Isolation)
    transactions = db.query(Transaction).filter(
        (Transaction.sender_id == user.id) | (Transaction.receiver_id == user.id)
    ).order_by(Transaction.id.desc()).all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "transactions": transactions
    })

@app.get("/logout")
async def logout(request: Request):
    """Clear session and logout"""
    request.session.clear()
    return RedirectResponse(url="/login")

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
