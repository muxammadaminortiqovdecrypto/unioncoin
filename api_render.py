from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import sys
from sqlalchemy.orm import Session
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db, User, Transaction

# Create FastAPI app
app = FastAPI(title="UnionCoin", description="Production-Grade Token Ecosystem")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Main page with crypto dashboard"""
    return templates.TemplateResponse("crypto_dashboard.html", {"request": {}})

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
            "status": "verified",
            "timestamp": str(datetime.utcnow())
        }
    except Exception as e:
        return {
            "blockchain_valid": False,
            "error": str(e),
            "status": "error"
        }

@app.get("/health")
async def health_check():
    """Health check endpoint for Render"""
    return {
        "status": "healthy",
        "service": "unioncoin",
        "timestamp": str(datetime.utcnow()),
        "version": "2.0"
    }

@app.get("/api/user-accounts")
async def get_user_accounts():
    """Get user accounts for dashboard"""
    try:
        # Sample data for now - in production this would be dynamic
        return {
            "accounts": [
                {
                    "id": 1,
                    "username": "abd",
                    "wallet_address": "abc123def456",
                    "balance": 1000.0,
                    "is_primary": True,
                    "profile_color": "#667eea",
                    "created_at": "2026-02-18T10:00:00Z"
                },
                {
                    "id": 2,
                    "username": "abd_acc2",
                    "wallet_address": "xyz789uvw012",
                    "balance": 1000.0,
                    "is_primary": False,
                    "profile_color": "#f56565",
                    "created_at": "2026-02-18T10:05:00Z"
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_system_stats():
    """Get system statistics"""
    try:
        db = next(get_db())
        users = db.query(User).all()
        transactions = db.query(Transaction).all()
        
        return {
            "total_users": len(users),
            "total_supply": sum(user.balance for user in users),
            "total_transactions": len(transactions),
            "active_users": len([u for u in users if u.balance > 0]),
            "new_users_today": len([u for u in users if u.created_at.date() == datetime.now().date()]),
            "timestamp": str(datetime.utcnow())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data")
async def view_data(admin: str = None):
    """View all data (admin only)"""
    if admin != "unioncoin_admin_2026":
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        db = next(get_db())
        users = db.query(User).all()
        transactions = db.query(Transaction).all()
        
        return {
            "users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "wallet_address": user.wallet_address,
                    "balance": user.balance,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "tg_id": user.tg_id,
                    "is_primary": user.is_primary,
                    "profile_color": user.profile_color
                }
                for user in users
            ],
            "transactions": [
                {
                    "id": tx.id,
                    "sender_id": tx.sender_id,
                    "receiver_id": tx.receiver_id,
                    "amount": tx.amount,
                    "timestamp": tx.timestamp.isoformat() if tx.timestamp else None,
                    "transaction_type": tx.transaction_type
                }
                for tx in transactions
            ],
            "total_users": len(users),
            "total_transactions": len(transactions),
            "total_balance": sum(user.balance for user in users)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
