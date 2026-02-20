"""
UnionCoin Enhanced Secure Bot
Intelligent registration flow, duplicate prevention, and admin security
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
ADMIN_TELEGRAM_ID = int(os.getenv("ADMIN_TELEGRAM_ID", "1685342390"))
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Enhanced Main Menu
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
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'status': 'active' if not user.is_banned else 'banned'
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

# --- Enhanced Registration Flow ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Enhanced entry with registration trigger support"""
    with next(get_db()) as db:
        user = db.query(User).filter(User.tg_id == message.from_user.id).first()
        
        if user:
            # User already exists - check status
            user_status = check_user_status(db, user)
            
            if user_status == "banned":
                await message.answer(
                    "🚫 **Account Banned**\n\n"
                    "Your account has been banned due to policy violations.\n"
                    "Please contact support via the bot for more information.",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            elif user_status == "inactive":
                await message.answer(
                    "⏸️ **Account Inactive**\n\n"
                    "Your account is currently inactive.\n"
                    "Please contact support via the bot to reactivate your account.",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            elif user_status == "suspended":
                await message.answer(
                    "⚠️ **Account Suspended**\n\n"
                    "Your account is temporarily suspended.\n"
                    "Please contact support via the bot for assistance.",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            # Active user - show their private data
            await message.answer(
                f"👋 Welcome back, {user.username}!\n\n"
                f"💰 Your balance: {user.balance:.2f} UC\n"
                f"🔗 Your wallet: {user.wallet_address}\n"
                f"✅ **Account Status: Active**\n\n"
                f"💎 Use the button below to access your private wallet:",
                reply_markup=main_menu
            )
            return
        
        # New user - check for registration trigger
        if message.text and "register" in message.text.lower():
            await message.answer(
                "🔐 **Welcome to UnionCoin Secure Registration!**\n\n"
                "You've been redirected here for secure registration.\n"
                "📝 Please create your account:\n\n"
                "1. Choose a unique username\n"
                "2. Set a secure password\n"
                "3. Your wallet will be created automatically\n\n"
                "🔒 Your data will be private and secure!",
                reply_markup=types.ReplyKeyboardRemove()
            )
        else:
            await message.answer(
                "🔐 **Welcome to UnionCoin!**\n\n"
                "📝 Please create your account:\n\n"
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
    """Process username with enhanced validation"""
    username = message.text.strip().lower()
    
    if len(username) < 3:
        await message.answer("❌ Username must be at least 3 characters!")
        return
    
    if len(username) > 20:
        await message.answer("❌ Username must be less than 20 characters!")
        return
    
    # Check for inappropriate content
    inappropriate_words = ['admin', 'system', 'root', 'null', 'test']
    if any(word in username for word in inappropriate_words):
        await message.answer("❌ This username is not allowed. Please choose another.")
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
    """Process password with enhanced validation"""
    password = message.text.strip()
    
    if len(password) < 6:
        await message.answer("❌ Password must be at least 6 characters!")
        return
    
    # Check for weak passwords
    weak_passwords = ['123456', 'password', 'qwerty', 'abc123']
    if password.lower() in weak_passwords:
        await message.answer("❌ This password is too weak. Please choose a stronger password.")
        return
    
    with next(get_db()) as db:
        # Get username from state
        data = await state.get_data()
        username = data['username']
        
        # Final check - ensure Telegram ID is still unique
        if not check_unique_telegram_account(db, message.from_user.id):
            await message.answer(
                "🚫 **Already Registered!**\n\n"
                "You are already registered with this Telegram account!\n"
                "Each Telegram account can only have ONE UnionCoin account.\n\n"
                "💎 Use the 'Open Web Wallet' button to access your dashboard.",
                reply_markup=main_menu
            )
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
        
        # Enhanced success message
        await message.answer(
            f"🎉 **Registration Successful!**\n\n"
            f"👤 **Username:** {username}\n"
            f"🔗 **Wallet:** {wallet_address}\n"
            f"💰 **Balance:** 1000.00 UC\n"
            f"🎁 **Welcome Bonus:** 1000 UC\n"
            f"✅ **Account Status:** Active\n\n"
            f"🔐 **Security Note:** Your account is now secure and private.\n"
            f"💎 Use the button below to access your private wallet:",
            reply_markup=main_menu,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Send welcome bonus notification
        await message.answer(
            f"💰 **Welcome Bonus Received!**\n\n"
            f"You've received 1000 UC as a welcome bonus!\n"
            f"Your current balance: 1000.00 UC\n\n"
            f"Start using UnionCoin now! 🚀",
            parse_mode=ParseMode.MARKDOWN
        )

# --- Enhanced Admin Commands ---
@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    """Enhanced admin access with security"""
    if not is_admin(message.from_user.id):
        # Don't reveal that admin panel exists
        await message.answer("❌ Command not recognized. Use /help for available commands.")
        return
    
    await message.answer(
        "🔐 **Admin Panel - Telegram Only**\n\n"
        "👥 View all users and their data\n"
        "🔗 View all transactions\n"
        "📊 System statistics\n"
        "🔍 Get specific user hash\n"
        "🔄 System reset options\n\n"
        "Choose an option:",
        reply_markup=admin_menu,
        parse_mode=ParseMode.MARKDOWN
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Enhanced help command"""
    help_text = """
🔐 **UnionCoin Help**

**User Commands:**
• `/start` - Register or access your account
• `/profile` - View your profile
• `/balance` - Check your balance
• `/help` - Show this help message

**Security Features:**
• 🔒 Telegram-only registration
• 👤 One account per Telegram ID
• 🛡️ Private data protection
• 🚫 No web registration

**Need Help?**
• 📱 Contact support via bot
• 🌐 Visit: https://unioncoin.onrender.com
• 📧 Support: Available via bot

**Admin Access:**
• 🔐 Admin functions via Telegram only
• 📱 Contact admin via bot for assistance
    """
    
    await message.answer(help_text, parse_mode=ParseMode.MARKDOWN)

@dp.message(Command("profile"))
async def cmd_profile(message: types.Message):
    """Enhanced profile command"""
    with next(get_db()) as db:
        user = db.query(User).filter(User.tg_id == message.from_user.id).first()
        
        if not user:
            await message.answer(
                "❌ **Account Not Found**\n\n"
                "Please register first with /start",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        user_status = check_user_status(db, user)
        
        if user_status != "active":
            status_messages = {
                "banned": "🚫 **Account Banned**",
                "inactive": "⏸️ **Account Inactive**",
                "suspended": "⚠️ **Account Suspended**"
            }
            
            await message.answer(
                f"{status_messages.get(user_status, '❓ **Unknown Status**')}\n\n"
                f"Please contact support via bot for assistance.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Get user's transactions
        transactions = db.query(Transaction).filter(
            or_(Transaction.sender_id == user.id, Transaction.receiver_id == user.id)
        ).order_by(Transaction.timestamp.desc()).limit(5).all()
        
        profile_text = f"""
👤 **Your Profile**

🆔 **User ID:** {user.id}
👤 **Username:** {user.username}
🔗 **Wallet:** {user.wallet_address}
💰 **Balance:** {user.balance:.2f} UC
📅 **Member Since:** {user.created_at.strftime('%Y-%m-%d %H:%M') if user.created_at else 'Unknown'}
✅ **Status:** Active

📊 **Recent Activity:**
"""
        
        for tx in transactions:
            if tx.sender_id == user.id:
                profile_text += f"📤 Sent: {tx.amount:.2f} UC to {tx.receiver_id}\n"
            else:
                profile_text += f"📥 Received: {tx.amount:.2f} UC from {tx.sender_id}\n"
        
        await message.answer(profile_text, parse_mode=ParseMode.MARKDOWN)

@dp.message(Command("balance"))
async def cmd_balance(message: types.Message):
    """Enhanced balance command"""
    with next(get_db()) as db:
        user = db.query(User).filter(User.tg_id == message.from_user.id).first()
        
        if not user:
            await message.answer(
                "❌ **Account Not Found**\n\n"
                "Please register first with /start",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        user_status = check_user_status(db, user)
        
        if user_status != "active":
            await message.answer(
                f"❌ **Account {user_status.title()}**\n\n"
                f"Please contact support via bot for assistance.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Get recent transactions
        transactions = db.query(Transaction).filter(
            or_(Transaction.sender_id == user.id, Transaction.receiver_id == user.id)
        ).order_by(Transaction.timestamp.desc()).limit(10).all()
        
        sent_total = sum(tx.amount for tx in transactions if tx.sender_id == user.id)
        received_total = sum(tx.amount for tx in transactions if tx.receiver_id == user.id)
        
        balance_text = f"""
💰 **Your Balance**

🔗 **Wallet:** {user.wallet_address}
💳 **Current Balance:** {user.balance:.2f} UC

📊 **Transaction Summary:**
📤 **Total Sent:** {sent_total:.2f} UC
📥 **Total Received:** {received_total:.2f} UC
🔗 **Total Transactions:** {len(transactions)}

✅ **Account Status:** Active
"""
        
        await message.answer(balance_text, parse_mode=ParseMode.MARKDOWN)

# --- Enhanced User Commands ---
@dp.message(F.text == "👤 My Profile")
async def cmd_my_profile(message: types.Message):
    """Show user's private profile"""
    await cmd_profile(message)

@dp.message(F.text == "📊 My Stats")
async def cmd_my_stats(message: types.Message):
    """Show user's private stats"""
    await cmd_balance(message)

@dp.message(F.text == "🚫 Back to Main Menu")
async def back_to_main(message: types.Message):
    """Return to main menu"""
    await message.answer("🏠 Returning to main menu...", reply_markup=main_menu)

# --- Enhanced Admin Commands ---
@dp.message(F.text == "👥 View All Users")
async def admin_view_all_users(message: types.Message):
    """View all users - admin only"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Command not recognized.")
        return
    
    with next(get_db()) as db:
        users = db.query(User).order_by(User.created_at.desc()).all()
        
        if not users:
            await message.answer("📭 No users found in database.")
            return
        
        response = "👥 **All Users**\n\n"
        
        for i, user in enumerate(users[:20], 1):  # Limit to first 20
            user_status = check_user_status(db, user)
            status_emoji = {"active": "✅", "banned": "🚫", "inactive": "⏸️", "suspended": "⚠️"}
            
            response += f"{i}. **{user.username}** {status_emoji.get(user_status, '❓')}\n"
            response += f"   🆔 ID: {user.id}\n"
            response += f"   📱 Telegram ID: {user.tg_id}\n"
            response += f"   🔗 Wallet: {user.wallet_address}\n"
            response += f"   💰 Balance: {user.balance:.2f} UC\n"
            response += f"   📅 Created: {user.created_at.strftime('%Y-%m-%d %H:%M') if user.created_at else 'Unknown'}\n"
            response += f"   📊 Status: {user_status.title()}\n\n"
        
        if len(users) > 20:
            response += f"... and {len(users) - 20} more users\n"
        
        response += f"📊 **Total Users: {len(users)}**"
        
        await message.answer(response, parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "🔗 View All Transactions")
async def admin_view_all_transactions(message: types.Message):
    """View all transactions - admin only"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Command not recognized.")
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

# --- Enhanced Error Handling ---
@dp.message()
async def handle_unknown_message(message: types.Message):
    """Handle unknown messages gracefully"""
    if message.text and message.text.startswith('/'):
        await message.answer(
            "❌ **Unknown Command**\n\n"
            "Use /help to see available commands.",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        # Regular text message - provide help
        await message.answer(
            "💬 **Message Received**\n\n"
            "I'm UnionCoin bot! Use /help to see available commands.\n"
            "🔐 For registration, use /start",
            parse_mode=ParseMode.MARKDOWN
        )

async def main():
    """Initialize enhanced bot"""
    await init_db()
    print("🔐 UnionCoin Enhanced Secure Bot Started!")
    print(f"👤 Admin ID: {ADMIN_TELEGRAM_ID}")
    print("🔒 Security: Enhanced Telegram-only admin")
    print("👥 Registration: Enhanced flow with duplicate prevention")
    print("🛡️ Error Handling: Intelligent messaging")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
