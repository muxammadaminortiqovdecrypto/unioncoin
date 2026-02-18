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

🔧 **Admin Commands** (ID: {ADMIN_ID}):
/admindata - 📊 Get full database as CSV files
/adminstats - 📈 Quick statistics
"""
        await message.answer(welcome_text, parse_mode="Markdown")

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

@dp.message(Command("adminstats"))
async def admin_stats_command(message: types.Message):
    """Quick admin stats command"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Admin only!")
        return
    
    with next(get_db()) as db:
        users = db.query(User).all()
        transactions = db.query(Transaction).all()
        
        total_balance = sum(user.balance for user in users)
        
        stats_text = f"""
📊 **QUICK STATS**

👥 Users: {len(users)}
💰 Total Supply: {total_balance:.2f} UC
🔗 Transactions: {len(transactions)}

🌐 Web: {len([u for u in users if u.tg_id is None])}
🤖 Telegram: {len([u for u in users if u.tg_id is not None])}
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
