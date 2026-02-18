"""
Telegram Bot for Token Ecosystem
"""

import asyncio
import random
import string
import csv
import io
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
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

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
            balance=1000.0,  # Welcome bonus
            is_primary=True,
            profile_color=random.choice(["#667eea", "#f093fb", "#4facfe", "#fa709a", "#fee140", "#00d4ff"])
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create welcome bonus transaction
        bonus_tx = create_transaction(db, 0, user.id, 1000.0, "welcome_bonus", True)
        db.add(bonus_tx)
        db.commit()
    
    return user

@dp.message(Command("start"))
async def start_command(message: types.Message):
    """Handle /start command with enhanced user experience"""
    with next(get_db()) as db:
        # Check if user already exists
        user = db.query(User).filter(User.tg_id == message.from_user.id).first()
        
        if user:
            # Welcome back message with account switcher
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💼 My Accounts", callback_data=f"accounts_{message.from_user.id}")],
                [InlineKeyboardButton(text="📊 Balance", callback_data=f"balance_{user.id}")],
                [InlineKeyboardButton(text="📤 Send Tokens", callback_data=f"send_{user.id}")]
            ])
            
            welcome_text = f"""
🎉 **Welcome back to UnionCoin!** 🎉

👤 **Your Profile:**
🆔 **Username:** @{user.username}
💳 **Wallet:** `{user.wallet_address}`
💰 **Balance:** {user.balance:.2f} UC
🎨 **Profile Color:** {user.profile_color}

📅 **Member Since:** {user.created_at.strftime('%Y-%m-%d')}

Choose an action below or manage multiple accounts!
            """
            await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")
        else:
            # New user registration with enhanced experience
            # Generate unique wallet address
            wallet_address = generate_wallet_address()
            while db.query(User).filter(User.wallet_address == wallet_address).first():
                wallet_address = generate_wallet_address()
            
            # Generate random profile color
            profile_color = random.choice(["#667eea", "#f093fb", "#4facfe", "#fa709a", "#fee140", "#00d4ff"])
            
            # Create new user
            new_user = User(
                tg_id=message.from_user.id,
                username=message.from_user.username or f"user_{message.from_user.id}",
                wallet_address=wallet_address,
                balance=1000.0,  # Welcome bonus
                is_primary=True,
                profile_color=profile_color
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            # Create welcome bonus transaction
            bonus_tx = create_transaction(db, 0, new_user.id, 1000.0, "welcome_bonus", True)
            db.add(bonus_tx)
            db.commit()
            
            # Enhanced welcome message
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🎉 View Profile", callback_data=f"profile_{new_user.id}")],
                [InlineKeyboardButton(text="💰 Check Balance", callback_data=f"balance_{new_user.id}")],
                [InlineKeyboardButton(text="📤 Send First Transfer", callback_data=f"send_{new_user.id}")],
                [InlineKeyboardButton(text="➕ Add Another Account", callback_data=f"add_account_{message.from_user.id}")]
            ])
            
            welcome_text = f"""
🚀 **Welcome to UnionCoin Ecosystem!** 🚀

🎊 **CONGRATULATIONS!** You've received:
💰 **1000 UC Welcome Bonus!**

👤 **Your New Profile:**
🆔 **Username:** @{new_user.username}
💳 **Wallet:** `{new_user.wallet_address}`
💰 **Balance:** {new_user.balance:.2f} UC
🎨 **Profile Theme:** {profile_color}

📅 **Created:** {new_user.created_at.strftime('%Y-%m-%d %H:%M')}

🔥 **Ready to start trading!** Choose an action below:

✨ **Features Available:**
• 💸 Instant P2P transfers
• 🤖 Telegram bot control
• 🌐 Modern web interface
• 🔒 Blockchain security
• 👥 Multi-account support (up to 3)
            """
            await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data.startswith('accounts_'))
async def handle_accounts(callback: CallbackQuery):
    """Handle account management"""
    tg_id = int(callback.data.split('_')[1])
    
    with next(get_db()) as db:
        users = db.query(User).filter(User.tg_id == tg_id).all()
        
        if not users:
            await callback.answer("No accounts found!", show_alert=True)
            return
        
        # Create account selection keyboard
        keyboard = []
        for user in users:
            is_primary = "⭐" if user.is_primary else ""
            keyboard.append([InlineKeyboardButton(
                text=f"{is_primary} @{user.username} ({user.balance:.2f} UC)", 
                callback_data=f"switch_{user.id}"
            )])
        
        if len(users) < 3:
            keyboard.append([InlineKeyboardButton(
                text="➕ Add New Account", 
                callback_data=f"add_account_{tg_id}"
            )])
        
        keyboard.append([InlineKeyboardButton(text="❌ Close", callback_data="close")])
        
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        
        text = f"""
👥 **Your UnionCoin Accounts** ({len(users)}/3)

💡 **Tip:** You can have up to 3 accounts per device!
⭐ = Primary account
        """
        
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data.startswith('add_account_'))
async def handle_add_account(callback: CallbackQuery):
    """Handle adding new account"""
    tg_id = int(callback.data.split('_')[2])
    
    with next(get_db()) as db:
        # Check account limit
        existing_accounts = db.query(User).filter(User.tg_id == tg_id).count()
        
        if existing_accounts >= 3:
            await callback.answer("Account limit reached! (3 accounts max)", show_alert=True)
            return
        
        # Generate new account
        wallet_address = generate_wallet_address()
        while db.query(User).filter(User.wallet_address == wallet_address).first():
            wallet_address = generate_wallet_address()
        
        # Generate random profile color
        profile_color = random.choice(["#667eea", "#f093fb", "#4facfe", "#fa709a", "#fee140", "#00d4ff"])
        
        # Create new user
        account_num = existing_accounts + 1
        new_user = User(
            tg_id=tg_id,
            username=f"{callback.from_user.username or 'user'}_acc{account_num}",
            wallet_address=wallet_address,
            balance=1000.0,  # Welcome bonus for each account
            is_primary=False,
            profile_color=profile_color
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Create welcome bonus transaction
        bonus_tx = create_transaction(db, 0, new_user.id, 1000.0, "welcome_bonus", True)
        db.add(bonus_tx)
        db.commit()
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎉 View New Account", callback_data=f"profile_{new_user.id}")],
            [InlineKeyboardButton(text="👥 View All Accounts", callback_data=f"accounts_{tg_id}")],
            [InlineKeyboardButton(text="❌ Close", callback_data="close")]
        ])
        
        text = f"""
🎊 **NEW ACCOUNT CREATED!** 🎊

💰 **Another 1000 UC Bonus Added!**

👤 **New Account Details:**
🆔 **Username:** @{new_user.username}
💳 **Wallet:** `{new_user.wallet_address}`
💰 **Balance:** {new_user.balance:.2f} UC
🎨 **Profile Theme:** {profile_color}

📅 **Created:** {new_user.created_at.strftime('%Y-%m-%d %H:%M')}

👥 **Total Accounts:** {existing_accounts + 1}/3
        """
        
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data.startswith('switch_'))
async def handle_switch_account(callback: CallbackQuery):
    """Handle switching between accounts"""
    user_id = int(callback.data.split('_')[1])
    
    with next(get_db()) as db:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            await callback.answer("Account not found!", show_alert=True)
            return
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 Balance", callback_data=f"balance_{user.id}")],
            [InlineKeyboardButton(text="📤 Send Tokens", callback_data=f"send_{user.id}")],
            [InlineKeyboardButton(text="👥 All Accounts", callback_data=f"accounts_{user.tg_id}")],
            [InlineKeyboardButton(text="❌ Close", callback_data="close")]
        ])
        
        text = f"""
✅ **Switched to Account:** @{user.username}

💳 **Wallet:** `{user.wallet_address}`
💰 **Balance:** {user.balance:.2f} UC
🎨 **Profile Theme:** {user.profile_color}
{'⭐ Primary Account' if user.is_primary else ''}
        """
        
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data.startswith('profile_'))
async def handle_profile(callback: CallbackQuery):
    """Handle profile view"""
    user_id = int(callback.data.split('_')[1])
    
    with next(get_db()) as db:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            await callback.answer("Profile not found!", show_alert=True)
            return
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 Balance", callback_data=f"balance_{user.id}")],
            [InlineKeyboardButton(text="📤 Send Tokens", callback_data=f"send_{user.id}")],
            [InlineKeyboardButton(text="👥 Switch Account", callback_data=f"accounts_{user.tg_id}")],
            [InlineKeyboardButton(text="❌ Close", callback_data="close")]
        ])
        
        text = f"""
👤 **UnionCoin Profile**

🆔 **Username:** @{user.username}
💳 **Wallet:** `{user.wallet_address}`
💰 **Balance:** {user.balance:.2f} UC
🎨 **Profile Theme:** {user.profile_color}
{'⭐ Primary Account' if user.is_primary else ''}

📅 **Member Since:** {user.created_at.strftime('%Y-%m-%d %H:%M')}
🔗 **Transactions:** {len(user.sent_transactions) + len(user.received_transactions)}

🚀 **Account Status:** ✅ Active
        """
        
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data == 'close')
async def handle_close(callback: CallbackQuery):
    """Handle close action"""
    await callback.message.delete()
    await callback.answer()

@dp.message(Command("balance"))
async def balance_command(message: types.Message):
    """Handle /balance command"""
    with next(get_db()) as db:
        user = db.query(User).filter(User.tg_id == message.from_user.id).first()
        if user:
            await message.answer(f"Your balance: {user.balance:.2f} UC\nWallet: `{user.wallet_address}`", parse_mode="Markdown")
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
        admin_text = f"Token Request:\nUser: @{user.username}\nWallet: {user.wallet_address}\nAmount: 1000 UC"
        await bot.send_message(ADMIN_ID, admin_text, reply_markup=keyboard)
        
        await message.answer("Your request has been sent to admin for approval.")

@dp.message(Command("admindata"))
async def admin_data_command(message: types.Message):
    """Admin command to get database data as CSV file"""
    # Check if user is admin
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ This command is only for admin!")
        return
    
    await message.answer("📊 Preparing database data...")
    
    try:
        with next(get_db()) as db:
            # Get all users
            users = db.query(User).all()
            
            # Create CSV for users
            output_users = io.StringIO()
            writer_users = csv.writer(output_users)
            
            # Write headers for users
            writer_users.writerow(['ID', 'Username', 'Wallet_Address', 'Balance', 'Telegram_ID', 'Created_At', 'Is_Active'])
            
            # Write user data
            for user in users:
                writer_users.writerow([
                    user.id,
                    user.username,
                    user.wallet_address,
                    user.balance,
                    user.tg_id if user.tg_id else 'Web User',
                    user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    user.is_active
                ])
            
            # Get all transactions
            transactions = db.query(Transaction).order_by(Transaction.id.desc()).all()
            
            # Create CSV for transactions
            output_tx = io.StringIO()
            writer_tx = csv.writer(output_tx)
            
            # Write headers for transactions
            writer_tx.writerow(['ID', 'Sender_ID', 'Receiver_ID', 'Amount', 'Transaction_Type', 'Is_Approved', 'Timestamp', 'Prev_Hash', 'Current_Hash'])
            
            # Write transaction data
            for tx in transactions:
                writer_tx.writerow([
                    tx.id,
                    tx.sender_id,
                    tx.receiver_id,
                    tx.amount,
                    tx.transaction_type,
                    tx.is_approved,
                    tx.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    tx.prev_hash,
                    tx.current_hash
                ])
            
            # Send users CSV file
            users_csv = output_users.getvalue().encode('utf-8')
            await bot.send_document(
                ADMIN_ID,
                document=types.BufferedInputFile(users_csv, filename="users_data.csv"),
                caption=f"👥 Users Data ({len(users)} users)"
            )
            
            # Send transactions CSV file
            tx_csv = output_tx.getvalue().encode('utf-8')
            await bot.send_document(
                ADMIN_ID,
                document=types.BufferedInputFile(tx_csv, filename="transactions_data.csv"),
                caption=f"🔗 Transactions Data ({len(transactions)} transactions)"
            )
            
            # Send summary
            total_balance = sum(user.balance for user in users)
            summary_text = f"""
📊 **DATABASE SUMMARY**

👥 **Users:** {len(users)} total
   🌐 Web Users: {len([u for u in users if u.tg_id is None])}
   🤖 Telegram Users: {len([u for u in users if u.tg_id is not None])}

🔗 **Transactions:** {len(transactions)} total
   🎁 Bonus: {len([t for t in transactions if t.transaction_type == 'bonus'])}
   🔄 P2P: {len([t for t in transactions if t.transaction_type == 'p2p'])}
   👑 Admin: {len([t for t in transactions if t.transaction_type == 'admin_approval'])}

💰 **Total Supply:** {total_balance:.2f} UC

📅 **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            await message.answer(summary_text, parse_mode="Markdown")
            
    except Exception as e:
        await message.answer(f"❌ Error generating data: {str(e)}")

@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    """Admin panel with advanced features"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ This command is only for admin!")
        return
    
    with next(get_db()) as db:
        users = db.query(User).all()
        transactions = db.query(Transaction).all()
        total_balance = sum(user.balance for user in users)
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 Full Statistics", callback_data="admin_stats_full")],
            [InlineKeyboardButton(text="👥 User Management", callback_data="admin_users")],
            [InlineKeyboardButton(text="🔗 Transaction Control", callback_data="admin_transactions")],
            [InlineKeyboardButton(text="📤 Broadcast Message", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="🔧 System Control", callback_data="admin_system")],
            [InlineKeyboardButton(text="❌ Close", callback_data="close")]
        ])
        
        admin_text = f"""
🔥 **ADMIN PANEL** 🔥

📊 **System Overview:**
👥 Total Users: {len(users)}
💰 Total Supply: {total_balance:.2f} UC
🔗 Total Transactions: {len(transactions)}

🤖 **Telegram Users:** {len([u for u in users if u.tg_id is not None])}
🌐 **Web Users:** {len([u for u in users if u.tg_id is None])}

👑 **Admin ID:** {ADMIN_ID}
🤖 **Bot Username:** @tokenuchunku12bot

Choose an action below:
        """
        await message.answer(admin_text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data == 'admin_stats_full')
async def admin_stats_full(callback: CallbackQuery):
    """Show detailed statistics"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Access denied!", show_alert=True)
        return
    
    with next(get_db()) as db:
        users = db.query(User).all()
        transactions = db.query(Transaction).all()
        
        # Today's transactions
        from datetime import datetime, timedelta
        today = datetime.now().date()
        today_tx = [tx for tx in transactions if tx.timestamp.date() == today]
        
        # Active users (with transactions)
        active_users = len(set([tx.sender_id for tx in transactions if tx.sender_id != 0] + 
                           [tx.receiver_id for tx in transactions]))
        
        text = f"""
📊 **DETAILED STATISTICS**

👥 **Users:**
• Total: {len(users)}
• Active: {active_users}
• New Today: {len([u for u in users if u.created_at.date() == today])}

💰 **Economy:**
• Total Supply: {sum(u.balance for u in users):.2f} UC
• Average Balance: {(sum(u.balance for u in users) / len(users)):.2f} UC
• Total Distributed: {sum(tx.amount for tx in transactions if tx.transaction_type == 'welcome_bonus'):.2f} UC

🔗 **Transactions:**
• Total: {len(transactions)}
• Today: {len(today_tx)}
• P2P: {len([tx for tx in transactions if tx.transaction_type == 'p2p'])}
• Bonuses: {len([tx for tx in transactions if tx.transaction_type == 'welcome_bonus'])}

📈 **Growth:**
• Daily New Users: {len([u for u in users if u.created_at.date() == today])}
• Daily Transactions: {len(today_tx)}
        """
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back to Panel", callback_data="admin_panel")],
            [InlineKeyboardButton(text="❌ Close", callback_data="close")]
        ])
        
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data == 'admin_users')
async def admin_users(callback: CallbackQuery):
    """User management panel"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Access denied!", show_alert=True)
        return
    
    with next(get_db()) as db:
        users = db.query(User).order_by(User.created_at.desc()).limit(10).all()
        
        text = "� **RECENT USERS**\n\n"
        for user in users:
            user_type = "🤖" if user.tg_id else "🌐"
            text += f"{user_type} @{user.username} - {user.balance:.2f} UC\n"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 Load More", callback_data="admin_users_more")],
            [InlineKeyboardButton(text="🔙 Back to Panel", callback_data="admin_panel")],
            [InlineKeyboardButton(text="❌ Close", callback_data="close")]
        ])
        
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data == 'admin_broadcast')
async def admin_broadcast(callback: CallbackQuery):
    """Broadcast message to all users"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Access denied!", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 Send to All Users", callback_data="broadcast_all")],
        [InlineKeyboardButton(text="🤖 Telegram Users Only", callback_data="broadcast_telegram")],
        [InlineKeyboardButton(text="🌐 Web Users Only", callback_data="broadcast_web")],
        [InlineKeyboardButton(text="🔙 Back to Panel", callback_data="admin_panel")],
        [InlineKeyboardButton(text="❌ Close", callback_data="close")]
        ])
    
    text = """
📤 **BROADCAST MESSAGE**

Choose recipient group:
• 📤 All Users
• 🤖 Telegram Users Only  
• 🌐 Web Users Only

Type your message after selecting group.
        """
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data.startswith('broadcast_'))
async def handle_broadcast(callback: CallbackQuery):
    """Handle broadcast message sending"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Access denied!", show_alert=True)
        return
    
    broadcast_type = callback.data.split('_')[1]
    
    # Here you would implement the actual message sending
    await callback.answer(f"Broadcast to {broadcast_type} users - Feature coming soon!", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith(('admin_panel', 'admin_transactions', 'admin_system')))
async def handle_admin_callbacks(callback: CallbackQuery):
    """Handle other admin callbacks"""
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Access denied!", show_alert=True)
        return
    
    action = callback.data
    
    if action == 'admin_panel':
        await admin_panel(callback.message)
    elif action == 'admin_transactions':
        await callback.answer("Transaction control - Coming soon!", show_alert=True)
    elif action == 'admin_system':
        await callback.answer("System control - Coming soon!", show_alert=True)

@dp.message(Command("admin_broadcast"))
async def admin_broadcast_command(message: types.Message):
    """Direct broadcast command"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Admin only!")
        return
    
    # Extract message after command
    broadcast_text = message.text.replace('/admin_broadcast', '').strip()
    
    if not broadcast_text:
        await message.answer("Please provide message to broadcast: /admin_broadcast Your message here")
        return
    
    with next(get_db()) as db:
        users = db.query(User).filter(User.tg_id.isnot(None)).all()
        
        success_count = 0
        for user in users:
            try:
                await bot.send_message(user.tg_id, f"📢 **ADMIN BROADCAST**\n\n{broadcast_text}")
                success_count += 1
            except Exception as e:
                print(f"Failed to send to {user.username}: {e}")
        
        await message.answer(f"✅ Broadcast sent to {success_count}/{len(users)} Telegram users")

@dp.message(Command("admin_stats"))
async def admin_stats_command(message: types.Message):
    """Enhanced admin stats command"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Admin only!")
        return
    
    with next(get_db()) as db:
        users = db.query(User).all()
        transactions = db.query(Transaction).all()
        
        total_balance = sum(user.balance for user in users)
        telegram_users = len([u for u in users if u.tg_id is not None])
        web_users = len([u for u in users if u.tg_id is None])
        
        stats_text = f"""
🔥 **ADMIN STATISTICS** 🔥

📊 **USERS:**
• Total: {len(users)}
• Telegram: {telegram_users} 🤖
• Web: {web_users} 🌐
• New Today: {len([u for u in users if u.created_at.date() == datetime.now().date()])}

💰 **ECONOMY:**
• Total Supply: {total_balance:.2f} UC
• Average Balance: {(total_balance / len(users)):.2f} UC
• Total Distributed: {sum(tx.amount for tx in transactions if tx.transaction_type == 'welcome_bonus'):.2f} UC

🔗 **TRANSACTIONS:**
• Total: {len(transactions)}
• P2P: {len([tx for tx in transactions if tx.transaction_type == 'p2p'])}
• Bonuses: {len([tx for tx in transactions if tx.transaction_type == 'welcome_bonus'])}
• Admin: {len([tx for tx in transactions if tx.transaction_type == 'admin_approval'])}

👑 **ADMIN INFO:**
• Your ID: {ADMIN_ID}
• Bot: @tokenuchunku12bot
• Status: ✅ Active
        """
        
        await message.answer(stats_text, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data.startswith(('approve_', 'decline_')))
async def handle_admin_callback(callback: CallbackQuery):
    """Handle admin approval/decline"""
    try:
        action, user_id, amount = callback.data.split('_')
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
                await bot.send_message(user.tg_id, f"Your request for {amount} UC has been approved!\nNew balance: {user.balance:.2f} UC")
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
