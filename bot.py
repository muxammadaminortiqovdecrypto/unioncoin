"""
UnionCoin Secure Bot - Admin Only via Telegram
Secure implementation with hardcoded admin ID and privacy features
"""

import asyncio
import random
import string
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from database import get_db, User, Transaction, create_transaction, init_db, generate_mnemonic, get_password_hash
from dotenv import load_dotenv

load_dotenv()

# Bot setup
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable is not set!")
    exit(1)

# Hardcoded admin security
ADMIN_TELEGRAM_ID = int(os.getenv("ADMIN_TELEGRAM_ID", "1685342390"))  # Hardcoded admin ID
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Secure Main Menu
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💎 Open Web Wallet", web_app=WebAppInfo(url=f"https://{os.getenv('DOMAIN', 'unioncoin.onrender.com')}/login"))],
        [KeyboardButton(text="👤 My Profile"), KeyboardButton(text="📝 Request Claim")],
        [KeyboardButton(text="📊 My Stats"), KeyboardButton(text="❓ Support")]
    ],
    resize_keyboard=True
)

# Admin Menu (only for admin)
admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👥 View All Users"), KeyboardButton(text="🔗 View All Transactions")],
        [KeyboardButton(text="📊 System Stats"), KeyboardButton(text="🔍 Get User Hash")],
        [KeyboardButton(text="🔄 Reset System"), KeyboardButton(text="🚫 Back to Main Menu")]
    ],
    resize_keyboard=True
)

# FSM States
class RegisterStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()

class AdminStates(StatesGroup):
    waiting_for_user_id = State()

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id == ADMIN_TELEGRAM_ID

def check_unique_telegram_account(db: Session, tg_id: int) -> bool:
    """Ensure One Telegram Account = One User rule"""
    existing_user = db.query(User).filter(User.tg_id == tg_id).first()
    return existing_user is None

def get_user_private_data(db: Session, user_id: int) -> dict:
    """Get only user's private data"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {}
    
    # Get only user's transactions
    transactions = db.query(Transaction).filter(
        or_(Transaction.sender_id == user_id, Transaction.receiver_id == user_id)
    ).order_by(Transaction.timestamp.desc()).limit(20).all()
    
    return {
        'user': {
            'id': user.id,
            'username': user.username,
            'wallet_address': user.wallet_address,
            'balance': user.balance,
            'created_at': user.created_at.isoformat() if user.created_at else None
        },
        'transactions': [
            {
                'id': tx.id,
                'sender_id': tx.sender_id,
                'receiver_id': tx.receiver_id,
                'amount': tx.amount,
                'timestamp': tx.timestamp.isoformat() if tx.timestamp else None,
                'transaction_type': tx.transaction_type,
                'tx_hash': tx.tx_hash,
                'current_hash': tx.current_hash
            }
            for tx in transactions
        ]
    }

# --- Secure Registration Flow ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Secure entry with unique account check"""
    with next(get_db()) as db:
        # Check if Telegram ID already exists
        existing_user = db.query(User).filter(User.tg_id == message.from_user.id).first()
        
        if existing_user:
            # User already exists, show their private data
            await message.answer(
                f"👋 Welcome back, {existing_user.username}!\n\n"
                f"💰 Your balance: {existing_user.balance:.2f} UC\n"
                f"🔗 Your wallet: {existing_user.wallet_address}\n\n"
                f"💎 Use the button below to access your private wallet:",
                reply_markup=main_menu
            )
            return
        
        # New user - start registration
        await message.answer(
            "🔐 Welcome to UnionCoin Secure!\n\n"
            "📝 Please create your account:\n"
            "1. Choose a unique username\n"
            "2. Set a secure password\n"
            "3. Your wallet will be created automatically\n\n"
            "🔒 Your data will be private and secure!",
            reply_markup=types.ReplyKeyboardRemove()
        )
        
        await state.set_state(RegisterStates.waiting_for_username)
        await message.answer("👤 Enter your username:")

@dp.message(RegisterStates.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    """Process username with uniqueness check"""
    username = message.text.strip().lower()
    
    if len(username) < 3:
        await message.answer("❌ Username must be at least 3 characters!")
        return
    
    if len(username) > 20:
        await message.answer("❌ Username must be less than 20 characters!")
        return
    
    with next(get_db()) as db:
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            await message.answer("❌ This username is already taken! Please choose another.")
            return
        
        # Store username in state
        await state.update_data(username=username)
        await state.set_state(RegisterStates.waiting_for_password)
        await message.answer("🔐 Enter your password (min 6 characters):")

@dp.message(RegisterStates.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    """Process password and create account"""
    password = message.text.strip()
    
    if len(password) < 6:
        await message.answer("❌ Password must be at least 6 characters!")
        return
    
    with next(get_db()) as db:
        # Get username from state
        data = await state.get_data()
        username = data['username']
        
        # Final check - ensure Telegram ID is still unique
        if not check_unique_telegram_account(db, message.from_user.id):
            await message.answer("❌ This Telegram account is already registered! Each Telegram account can only have one UnionCoin account.")
            await state.clear()
            return
        
        # Generate unique wallet address
        while True:
            wallet_address = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            if not db.query(User).filter(User.wallet_address == wallet_address).first():
                break
        
        # Create new user
        new_user = User(
            tg_id=message.from_user.id,
            username=username,
            wallet_address=wallet_address,
            balance=1000.0,  # Welcome bonus
            password_hash=get_password_hash(password)
        )
        
        db.add(new_user)
        db.commit()
        
        # Create welcome transaction
        create_transaction(
            db=db,
            sender_id=None,  # System
            receiver_id=new_user.id,
            amount=1000.0,
            tx_type="bonus"
        )
        db.commit()
        
        await state.clear()
        
        await message.answer(
            f"🎉 Account created successfully!\n\n"
            f"👤 Username: {username}\n"
            f"🔗 Wallet: {wallet_address}\n"
            f"💰 Balance: 1000.00 UC\n"
            f"🎁 Welcome bonus: 1000 UC\n\n"
            f"💎 Use the button below to access your private wallet:",
            reply_markup=main_menu
        )

# --- Admin Commands (Telegram Only) ---
@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    """Admin access - Telegram only"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied! Admin functions are restricted.")
        return
    
    await message.answer(
        "🔐 Admin Panel - Telegram Only\n\n"
        "👥 View all users and their data\n"
        "🔗 View all transactions\n"
        "📊 System statistics\n"
        "🔍 Get specific user hash\n"
        "🔄 System reset options\n\n"
        "Choose an option:",
        reply_markup=admin_menu
    )

@dp.message(F.text == "👥 View All Users")
async def admin_view_all_users(message: types.Message):
    """View all users - admin only"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied!")
        return
    
    with next(get_db()) as db:
        users = db.query(User).order_by(User.created_at.desc()).all()
        
        if not users:
            await message.answer("📭 No users found in database.")
            return
        
        response = "👥 **All Users**\n\n"
        
        for i, user in enumerate(users[:20], 1):  # Limit to first 20
            response += f"{i}. **{user.username}**\n"
            response += f"   🆔 ID: {user.id}\n"
            response += f"   📱 Telegram ID: {user.tg_id}\n"
            response += f"   🔗 Wallet: {user.wallet_address}\n"
            response += f"   💰 Balance: {user.balance:.2f} UC\n"
            response += f"   📅 Created: {user.created_at.strftime('%Y-%m-%d %H:%M') if user.created_at else 'Unknown'}\n\n"
        
        if len(users) > 20:
            response += f"... and {len(users) - 20} more users\n"
        
        response += f"📊 **Total Users: {len(users)}**"
        
        await message.answer(response, parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "🔗 View All Transactions")
async def admin_view_all_transactions(message: types.Message):
    """View all transactions - admin only"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied!")
        return
    
    with next(get_db()) as db:
        transactions = db.query(Transaction).order_by(Transaction.timestamp.desc()).all()
        
        if not transactions:
            await message.answer("📭 No transactions found in database.")
            return
        
        response = "🔗 **All Transactions**\n\n"
        
        for i, tx in enumerate(transactions[:20], 1):  # Limit to first 20
            sender = db.query(User).filter(User.id == tx.sender_id).first() if tx.sender_id else None
            receiver = db.query(User).filter(User.id == tx.receiver_id).first() if tx.receiver_id else None
            
            response += f"{i}. **{tx.transaction_type.upper()}**\n"
            response += f"   📅 Time: {tx.timestamp.strftime('%Y-%m-%d %H:%M') if tx.timestamp else 'Unknown'}\n"
            response += f"   💰 Amount: {tx.amount:.2f} UC\n"
            response += f"   👤 From: {sender.username if sender else 'SYSTEM'}\n"
            response += f"   👤 To: {receiver.username if receiver else 'SYSTEM'}\n"
            response += f"   🔗 Hash: `{tx.tx_hash}`\n\n"
        
        if len(transactions) > 20:
            response += f"... and {len(transactions) - 20} more transactions\n"
        
        response += f"📊 **Total Transactions: {len(transactions)}**"
        
        await message.answer(response, parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "📊 System Stats")
async def admin_system_stats(message: types.Message):
    """View system statistics - admin only"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied!")
        return
    
    with next(get_db()) as db:
        users = db.query(User).all()
        transactions = db.query(Transaction).all()
        
        total_balance = sum(user.balance for user in users)
        active_users = len([u for u in users if u.balance > 0])
        
        response = "📊 **System Statistics**\n\n"
        response += f"👥 **Total Users:** {len(users)}\n"
        response += f"📊 **Total Transactions:** {len(transactions)}\n"
        response += f"💰 **Total Balance:** {total_balance:.2f} UC\n"
        response += f"📈 **Active Users:** {active_users}\n"
        response += f"📉 **Inactive Users:** {len(users) - active_users}\n"
        
        # Recent transactions
        today_tx = [tx for tx in transactions if tx.timestamp and tx.timestamp.date() == datetime.now().date()]
        response += f"📅 **Today's Transactions:** {len(today_tx)}\n"
        
        await message.answer(response, parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "🔍 Get User Hash")
async def admin_get_user_hash(message: types.Message):
    """Get specific user hash - admin only"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied!")
        return
    
    await message.answer("🔍 Enter User ID to get hash:")
    # In a real implementation, you'd set a state here

@dp.message(Command("get_user_hash"))
async def cmd_get_user_hash(message: types.Message):
    """Get user hash by ID - admin only"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied!")
        return
    
    try:
        user_id = int(message.text.split()[1]) if len(message.text.split()) > 1 else None
        if not user_id:
            await message.answer("❌ Please provide User ID: /get_user_hash <user_id>")
            return
        
        with next(get_db()) as db:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                await message.answer(f"❌ User with ID {user_id} not found!")
                return
            
            # Get user's transactions
            transactions = db.query(Transaction).filter(
                or_(Transaction.sender_id == user_id, Transaction.receiver_id == user_id)
            ).order_by(Transaction.timestamp.desc()).limit(10).all()
            
            response = f"🔍 **User Hash Information**\n\n"
            response += f"👤 **User:** {user.username}\n"
            response += f"🆔 **ID:** {user.id}\n"
            response += f"📱 **Telegram ID:** {user.tg_id}\n"
            response += f"🔗 **Wallet:** {user.wallet_address}\n"
            response += f"💰 **Balance:** {user.balance:.2f} UC\n"
            response += f"📅 **Created:** {user.created_at.strftime('%Y-%m-%d %H:%M') if user.created_at else 'Unknown'}\n\n"
            
            response += "🔗 **Recent Transaction Hashes:**\n"
            for tx in transactions:
                response += f"   • `{tx.tx_hash}`\n"
            
            await message.answer(response, parse_mode=ParseMode.MARKDOWN)
            
    except (ValueError, IndexError):
        await message.answer("❌ Invalid format! Use: /get_user_hash <user_id>")

@dp.message(Command("view_all_transactions"))
async def cmd_view_all_transactions(message: types.Message):
    """View all transactions - admin only"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied!")
        return
    
    with next(get_db()) as db:
        transactions = db.query(Transaction).order_by(Transaction.timestamp.desc()).limit(50).all()
        
        if not transactions:
            await message.answer("📭 No transactions found!")
            return
        
        response = "🔗 **All Transaction Hashes**\n\n"
        
        for tx in transactions:
            sender = db.query(User).filter(User.id == tx.sender_id).first() if tx.sender_id else None
            receiver = db.query(User).filter(User.id == tx.receiver_id).first() if tx.receiver_id else None
            
            response += f"🔗 **Hash:** `{tx.tx_hash}`\n"
            response += f"📅 **Time:** {tx.timestamp.strftime('%Y-%m-%d %H:%M') if tx.timestamp else 'Unknown'}\n"
            response += f"💰 **Amount:** {tx.amount:.2f} UC\n"
            response += f"👤 **From:** {sender.username if sender else 'SYSTEM'}\n"
            response += f"👤 **To:** {receiver.username if receiver else 'SYSTEM'}\n"
            response += f"🏷️ **Type:** {tx.transaction_type}\n\n"
        
        await message.answer(response, parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "🔄 Reset System")
async def admin_reset_system(message: types.Message):
    """System reset options - admin only"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied!")
        return
    
    await message.answer(
        "🔄 **System Reset Options**\n\n"
        "⚠️ **WARNING:** These actions are irreversible!\n\n"
        "1. /reset_users - Delete all users\n"
        "2. /reset_transactions - Delete all transactions\n"
        "3. /reset_all - Complete system reset\n\n"
        "🔒 Use with extreme caution!"
    )

@dp.message(Command("reset_users"))
async def cmd_reset_users(message: types.Message):
    """Reset all users - admin only"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied!")
        return
    
    with next(get_db()) as db:
        user_count = db.query(User).count()
        db.query(User).delete()
        db.commit()
        
        await message.answer(f"🔄 **Users Reset Complete!**\n\nDeleted {user_count} users from database.")

@dp.message(Command("reset_transactions"))
async def cmd_reset_transactions(message: types.Message):
    """Reset all transactions - admin only"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied!")
        return
    
    with next(get_db()) as db:
        tx_count = db.query(Transaction).count()
        db.query(Transaction).delete()
        db.commit()
        
        await message.answer(f"🔄 **Transactions Reset Complete!**\n\nDeleted {tx_count} transactions from database.")

@dp.message(Command("reset_all"))
async def cmd_reset_all(message: types.Message):
    """Complete system reset - admin only"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied!")
        return
    
    with next(get_db()) as db:
        user_count = db.query(User).count()
        tx_count = db.query(Transaction).count()
        
        db.query(User).delete()
        db.query(Transaction).delete()
        db.commit()
        
        await message.answer(
            f"🔄 **Complete System Reset!**\n\n"
            f"👥 Deleted {user_count} users\n"
            f"🔗 Deleted {tx_count} transactions\n"
            f"🔒 System is now fresh!"
        )

@dp.message(F.text == "🚫 Back to Main Menu")
async def back_to_main(message: types.Message):
    """Return to main menu"""
    await message.answer("🏠 Returning to main menu...", reply_markup=main_menu)

# --- User Private Commands ---
@dp.message(F.text == "👤 My Profile")
async def cmd_my_profile(message: types.Message):
    """Show user's private profile"""
    with next(get_db()) as db:
        user = db.query(User).filter(User.tg_id == message.from_user.id).first()
        
        if not user:
            await message.answer("❌ Please register first with /start")
            return
        
        response = f"👤 **Your Private Profile**\n\n"
        response += f"👤 **Username:** {user.username}\n"
        response += f"🔗 **Wallet:** {user.wallet_address}\n"
        response += f"💰 **Balance:** {user.balance:.2f} UC\n"
        response += f"📅 **Member Since:** {user.created_at.strftime('%Y-%m-%d %H:%M') if user.created_at else 'Unknown'}\n"
        response += f"🔐 **Your data is private and secure!**"
        
        await message.answer(response, parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "📊 My Stats")
async def cmd_my_stats(message: types.Message):
    """Show user's private stats"""
    with next(get_db()) as db:
        user = db.query(User).filter(User.tg_id == message.from_user.id).first()
        
        if not user:
            await message.answer("❌ Please register first with /start")
            return
        
        # Get user's transactions
        transactions = db.query(Transaction).filter(
            or_(Transaction.sender_id == user.id, Transaction.receiver_id == user.id)
        ).all()
        
        sent_tx = [tx for tx in transactions if tx.sender_id == user.id]
        received_tx = [tx for tx in transactions if tx.receiver_id == user.id]
        
        total_sent = sum(tx.amount for tx in sent_tx)
        total_received = sum(tx.amount for tx in received_tx)
        
        response = f"📊 **Your Private Statistics**\n\n"
        response += f"💰 **Current Balance:** {user.balance:.2f} UC\n"
        response += f"📤 **Total Sent:** {total_sent:.2f} UC ({len(sent_tx)} transactions)\n"
        response += f"📥 **Total Received:** {total_received:.2f} UC ({len(received_tx)} transactions)\n"
        response += f"📊 **Total Transactions:** {len(transactions)}\n"
        response += f"🔐 **Your data is private and secure!**"
        
        await message.answer(response, parse_mode=ParseMode.MARKDOWN)

async def main():
    """Initialize bot"""
    await init_db()
    print("🔐 UnionCoin Secure Bot Started!")
    print(f"👤 Admin ID: {ADMIN_TELEGRAM_ID}")
    print("🔒 Security: Admin functions via Telegram only")
    print("🔒 Privacy: User data isolation enabled")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
