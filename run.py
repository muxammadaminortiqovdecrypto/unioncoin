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
    """Main entry point with robust restart logic for both services"""
    # Initialize database
    init_db()
    
    while True:
        try:
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
            logger.info(f"🚀 Starting UnionCoin Ecosystem on port {port}...")
            
            # Create tasks
            web_task = asyncio.create_task(server.serve())
            bot_task = asyncio.create_task(dp.start_polling(bot))
            
            logger.info("✅ Services initiated. Web and Bot are starting...")
            
            # Wait for any task to fail or complete
            done, pending = await asyncio.wait(
                [web_task, bot_task],
                return_when=asyncio.FIRST_EXCEPTION
            )
            
            for task in done:
                if task.exception():
                    logger.error(f"❌ Task failed with exception: {task.exception()}")
            
            # Cancel pending tasks before restart
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            
            logger.info("🔄 Restarting services in 5 seconds...")
            await asyncio.sleep(5)
            
        except Exception as e:
            logger.error(f"⚠️ Global crash detected: {e}")
            logger.info("🔄 Retrying in 10 seconds...")
            await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Service stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {e}")
