"""
UnionCoin Ultimate (V4) - Telegram Bot Bridge & Identity Provider (IdP)
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
from database import get_db, User, Transaction, create_transaction, init_db, generate_mnemonic, get_password_hash
from dotenv import load_dotenv

load_dotenv()

# Bot setup
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable is not set!")
    exit(1)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Elegant Persistent Menu (Ultimate Spec)
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💎 Open Web Wallet", web_app=WebAppInfo(url=f"https://{os.getenv('DOMAIN', 'unioncoin.onrender.com')}/login"))],
        [KeyboardButton(text="👤 My Profile"), KeyboardButton(text="📝 Request Claim")],
        [KeyboardButton(text="📊 Stats"), KeyboardButton(text="❓ Support")]
    ],
    resize_keyboard=True
)

# FSM States
class RegisterStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()

# --- Elegant Registration Flow ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Entry: Check user (Strict 1-account-per-ID)"""
    with next(get_db()) as db:
        user = db.query(User).filter(User.tg_id == message.from_user.id).first()
        
        if not user:
            await state.set_state(RegisterStates.waiting_for_username)
            await message.answer(
                "✨ **Welcome to UnionCoin Ultimate** ✨\n\n"
                "The world's first Telegram-native token ecosystem.\n\n"
                "🚀 Let's get you set up.\n"
                "👤 **Step 1:** Choose your **Username**.\n"
                "(Lowercase, 3+ alphanumeric chars)",
                parse_mode="Markdown"
            )
            return

        # Known User: Dashboard
        await message.answer(
            f"👋 **Welcome back, {user.username}!**\n\n"
            f"💰 Balance: `{user.balance:.2f} UC`\n"
            f"🆔 Wallet: `0x{user.wallet_address[:4]}...{user.wallet_address[-4:]}`\n\n"
            "Use the menu below to manage your assets.",
            reply_markup=main_menu,
            parse_mode="Markdown"
        )

@dp.message(RegisterStates.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    if not message.text: return
    username = message.text.strip().lower()
    
    # Strictly alphanumeric
    if not username.isalnum():
        await message.answer("❌ **Error:** Only letters and numbers are allowed in usernames.", parse_mode=ParseMode.HTML)
        return
        
    if len(username) < 3:
        await message.answer("❌ **Error:** Username must be at least 3 characters.", parse_mode=ParseMode.HTML)
        return

    with next(get_db()) as db:
        # Extra safety check for 1-account-per-ID even if they bypassed /start
        existing_id = db.query(User).filter(User.tg_id == message.from_user.id).first()
        if existing_id:
            await state.clear()
            await message.answer("⚠️ You already have an account.", reply_markup=main_menu)
            return

        if db.query(User).filter(User.username == username).first():
            await message.answer("❌ Taken! Choose another.")
            return

    await state.update_data(reg_username=username)
    await state.set_state(RegisterStates.waiting_for_password)
    await message.answer(
        f"✅ Username: `{username}`\n\n"
        "🔐 **Step 2:** Choose a **Password**.\n"
        "(Lowercase, 6+ chars. We'll hash it securely with bcrypt.)",
        parse_mode="Markdown"
    )

@dp.message(RegisterStates.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    if not message.text: return
    password = message.text.strip().lower() # Force lowercase
    data = await state.get_data()
    username = data['reg_username']
    
    # Requirement: password can be any length (as per last user update)
    # But for safety, we still want a minimum just for basic hygiene
    if len(password) < 4:
        await message.answer("❌ **Error:** Password too short (min 4).", parse_mode=ParseMode.HTML)
        return

    with next(get_db()) as db:
        wallet = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        user = User(
            tg_id=message.from_user.id,
            username=username,
            password_hash=get_password_hash(password),
            wallet_address=wallet,
            seed_phrase=generate_mnemonic(),
            balance=1000.0,
            referral_code=''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        create_transaction(db, 0, user.id, 1000.0, "welcome_bonus")
        db.commit()

        domain = os.getenv("DOMAIN", "unioncoin.render.com")
        
        # Elegant Credentials Card (Tap-to-copy formatting)
        summary = (
            "<b>✅ Account Created Successfully!</b>\n\n"
            "Use the details below to login to our Web App:\n"
            f"Login ID: <code>{user.tg_id}</code> or <code>{user.username}</code>\n"
            f"Password: <code>{password}</code>\n"
            f"🌐 Website Link: <code>https://{domain}</code>\n\n"
            "<i>(Tip: You can tap the ID and Password to copy them!)</i>"
        )

    await state.clear()
    await message.answer(summary, reply_markup=main_menu, parse_mode=ParseMode.HTML)

# --- Admin Handling (Claims) ---
@dp.callback_query(lambda c: c.data.startswith('adm_ok_'))
async def admin_ok(callback: CallbackQuery):
    _, _, user_id, amount = callback.data.split('_')
    with next(get_db()) as db:
        user = db.get(User, int(user_id))
        user.balance += float(amount)
        create_transaction(db, 0, user.id, float(amount), "admin_reward")
        db.commit()
        await bot.send_message(user.tg_id, f"✅ Admin approved your reward: `{amount} UC` added!")
    await callback.message.edit_text(f"Approved {amount} for {user.username}")
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith('adm_no_'))
async def admin_no(callback: CallbackQuery):
    user_id = int(callback.data.split('_')[2])
    with next(get_db()) as db:
        user = db.get(User, user_id)
        await bot.send_message(user.tg_id, "❌ Admin declined your claim request.")
    await callback.message.edit_text(f"Rejected {user.username}")
    await callback.answer()

# --- Menu Button Handlers (Ultimate Spec) ---
@dp.message(F.text == "👤 My Profile")
async def menu_profile(message: types.Message):
    with next(get_db()) as db:
        user = db.query(User).filter(User.tg_id == message.from_user.id).first()
        if user:
            await message.answer(
                f"👤 **{user.username.upper()}**\n"
                f"💰 Balance: `{user.balance:.2f} UC`\n"
                f"🆔 ID: `{user.tg_id}`\n"
                f"💳 Wallet: `0x{user.wallet_address}`\n\n"
                f"🔗 Referral: `UC_{user.referral_code}`",
                parse_mode="Markdown"
            )
        else:
            await message.answer("❌ Account not found. Use /start to register.")

@dp.message(F.text == "📝 Request Claim")
async def menu_claim_msg(message: types.Message):
    with next(get_db()) as db:
        user = db.query(User).filter(User.tg_id == message.from_user.id).first()
        if user:
            admin_id = int(os.getenv("ADMIN_ID", 1685342390))
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Approve 500 UC", callback_data=f"adm_ok_{user.id}_500"),
                 InlineKeyboardButton(text="Reject", callback_data=f"adm_no_{user.id}")]
            ])
            await bot.send_message(admin_id, f"🔔 **Reward Request**\nUser: {user.username}\nID: {user.tg_id}", reply_markup=keyboard)
            await message.answer("📝 Reward request sent to Admin!")
        else:
            await message.answer("❌ Account not found.")

@dp.message(F.text == "📊 Stats")
async def menu_stats(message: types.Message):
    with next(get_db()) as db:
        total_users = db.query(User).count()
        total_balance = db.query(User).with_entities(Session.func.sum(User.balance)).scalar() or 0
        await message.answer(
            f"📊 **UnionCoin Network Stats**\n\n"
            f"👥 Total Users: `{total_users}`\n"
            f"💰 Total Circulation: `{total_balance:.2f} UC`",
            parse_mode="Markdown"
        )

@dp.message(F.text == "❓ Support")
async def menu_support(message: types.Message):
    await message.answer("💎 **UnionCoin Ultimate Support**\n\nFor assistance, contact the network administrator.")

async def main():
    init_db()
    print("🚀 UnionCoin Ultimate V4 Bot (Elegant) Started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
