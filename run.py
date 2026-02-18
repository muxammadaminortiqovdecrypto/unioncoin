import asyncio
import logging
import uvicorn
from api import app as web_app
from bot import dp, bot, init_db
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main entry point to run both Web Server and Telegram Bot"""
    # Initialize database
    init_db()
    
    # Get port from environment (for Render/Railway)
    port = int(os.getenv("PORT", 8000))
    
    # Configure Uvicorn server
    config = uvicorn.Config(
        app=web_app, 
        host="0.0.0.0", 
        port=port, 
        loop="asyncio"
    )
    server = uvicorn.Server(config)
    
    # Start both tasks
    logger.info(f"Starting UnionCoin Ecosystem on port {port}...")
    
    # Run both the bot and the web server concurrently
    await asyncio.gather(
        server.serve(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Service stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {e}")
