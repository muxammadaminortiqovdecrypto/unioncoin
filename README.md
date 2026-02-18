# UnionCoin Token Ecosystem

Production-grade token system with Telegram bot, web interface, and PostgreSQL backend.

## Features
- Blockchain hash-chain verification
- Telegram bot with admin approval
- Web wallet for P2P transfers
- Tamper-proof transaction records

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up PostgreSQL database and update DATABASE_URL

3. Initialize database:
   ```bash
   python database.py
   ```

4. Run Telegram bot:
   ```bash
   python bot.py
   ```

5. Run web server:
   ```bash
   python api.py
   ```

6. Verify blockchain integrity:
   ```bash
   python verify.py
   ```
