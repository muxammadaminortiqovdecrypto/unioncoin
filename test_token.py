import asyncio
from aiogram import Bot

async def test_token():
    token = "8362335664:AAHzVL2gFmgu8X3QoxYTiLtZNFTbZom9_7A"
    bot = Bot(token=token)
    try:
        me = await bot.get_me()
        print(f"✅ Token is valid! Bot: @{me.username}")
    except Exception as e:
        print(f"❌ Token is invalid: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(test_token())
