# UnionCoin - Production-Grade Token Ecosystem

**Modern blockchain-based token system with Telegram bot and web interface**

## Features

### Web Interface
- **Modern Design** - Responsive, animated UI with gradient effects
- **User Registration** - Instant wallet creation with 1000 UC bonus
- **P2P Transfers** - Direct user-to-user token transfers
- **Dashboard** - Real-time balance and transaction history
- **Data Viewer** - Admin panel with statistics and CSV export

### Telegram Bot
- **Complete Interface** - Full wallet management via Telegram
- **Admin Controls** - Token approval system with CSV export
- **Instant Notifications** - Real-time transaction alerts
- **Secure Authentication** - Telegram ID-based user verification

### Blockchain Security
- **SHA-256 Hashing** - Tamper-proof transaction records
- **Chain Verification** - Complete blockchain integrity checks
- **ACID Compliance** - Database transaction safety
- **Immutable Ledger** - Permanent transaction history

## Technology Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Font Awesome
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Bot**: aiogram 3.x
- **Deployment**: Docker, Docker Compose

## 🚀 Production Deployment

### Option 1: Computer as Server (Recommended for testing)

Turn your current computer into a production server:

```bash
# Start server mode
python server_mode.py

# Interactive mode
python server_mode.py --interactive
```

**Features:**
- 🖥️ Auto-restart services if they crash
- 📊 Automatic backup every 6 hours
- 🔍 Service monitoring and status
- 🎮 Interactive command interface
- 📋 Real-time log viewing

### Option 2: Online Server Deployment

```bash
# Run deployment script
python deploy.py

# Manual deployment to cloud server
```

**Server Requirements:**
- Ubuntu 20.04+ / CentOS 8+
- 2GB+ RAM
- 20GB+ Storage
- Python 3.8+
- PostgreSQL 13+
- Nginx
- SSL Certificate

### Option 3: Docker Deployment

```bash
# Build and deploy
docker-compose up -d

# Production Dockerfile
docker build -t unioncoin-prod .
docker run -d -p 8000:8000 unioncoin-prod
```

## 🔧 Configuration

### Environment Variables
```bash
# Production (.env.production)
DATABASE_URL=postgresql://user:password@localhost/unioncoin
BOT_TOKEN=your_bot_token
ADMIN_ID=your_telegram_id
DOMAIN=yourdomain.com
```

### Security Setup
```bash
# SSL with Let's Encrypt
sudo certbot --nginx -d yourdomain.com

# Firewall setup
sudo ufw allow 22,80,443
sudo ufw enable
```

## 📊 Monitoring & Backup

### Automatic Backup
- **Frequency:** Every 6 hours
- **Format:** Excel files
- **Location:** `server_backups/` directory
- **Includes:** Users and transactions data

### Service Monitoring
- **Web Server:** HTTP/HTTPS checks
- **Bot Status:** Process monitoring
- **Database:** Connection health
- **Auto-restart:** Failed services

### Admin Notifications
- **Email alerts** for service failures
- **Telegram notifications** for critical errors
- **Daily reports** with statistics

## Project Structure

```
unioncoin/
├── static/                 # CSS, JS, images
│   ├── css/
│   │   ├── style.css          # Main styles
│   │   └── dashboard.css     # Dashboard styles
│   ├── js/
│   │   └── main.js           # Interactive features
│   └── images/               # Assets
├── templates/             # HTML templates
│   ├── base.html             # Base template
│   ├── index.html            # Landing page
│   ├── login.html            # User login
│   ├── register.html          # User registration
│   └── dashboard.html        # User dashboard
├── api.py                 # FastAPI web server
├── bot.py                 # Telegram bot
├── database.py            # Database models & logic
├── verify.py              # Blockchain verification
├── view_data.py           # Data viewer CLI
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Multi-service deployment
├── .env.example          # Environment template
└── .gitignore            # Git ignore rules
```

## Security Features

- **Admin Protection** - Password-protected data access
- **Input Validation** - Form sanitization and validation
- **CSRF Protection** - Cross-site request forgery prevention
- **SQL Injection Safe** - Parameterized queries
- **Environment Variables** - Secure configuration management

## API Endpoints

### Public Endpoints
- `GET /` - Landing page
- `GET /login` - User login page
- `GET /register` - User registration page
- `POST /register` - Create new wallet
- `POST /login` - User authentication
- `POST /send` - P2P token transfer

### Admin Endpoints
- `GET /api/data?admin=PASSWORD` - Data viewer with export
- `GET /verify` - Blockchain integrity check

## Telegram Bot Commands

### User Commands
- `/start` - Register and get wallet
- `/balance` - Check wallet balance
- `/send <wallet> <amount>` - Send tokens
- `/request` - Request admin approval

### Admin Commands
- `/admindata` - Export database as CSV
- `/adminstats` - Quick statistics

## Deployment Options

### 1. **VPS/Cloud Server**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip postgresql nginx
git clone https://github.com/yourusername/unioncoin.git
cd unioncoin
pip3 install -r requirements.txt
docker-compose up -d
```

### 2. **Heroku**
```bash
# Install Heroku CLI
heroku create your-app-name
git push heroku main
```

### 3. **AWS/Azure/GCP**
- Use provided Dockerfile
- Deploy container registry
- Configure load balancer
- Set up SSL certificate

### 4. **Shared Hosting**
- Upload files via FTP
- Install Python requirements
- Configure .htaccess for routing
- Set up cron jobs for bot

## Monitoring & Analytics

### Built-in Analytics
- **User Statistics** - Registration and activity metrics
- **Transaction Analytics** - Volume and frequency data
- **System Health** - Database and service monitoring
- **Export Features** - CSV data for external analysis

### Log Management
```bash
# View application logs
tail -f logs/unioncoin.log

# Error monitoring
grep ERROR logs/unioncoin.log
```

## Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=sqlite:///./unioncoin.db

# Telegram Bot
BOT_TOKEN=your_bot_token
ADMIN_ID=your_telegram_id

# Security
SECRET_KEY=your_secret_key
ADMIN_PASSWORD=unioncoin_admin_2026

# Server
HOST=0.0.0.0
PORT=8000
```

## Important Notes

### Security
- **Never commit** `.env` file or sensitive data
- **Change default** admin password in production
- **Use HTTPS** in production environment
- **Regular backups** of database and configurations

### Legal
- **Compliance** with local cryptocurrency regulations
- **Privacy policy** for user data handling
- **Terms of service** for platform usage
- **AML/KYC** requirements if applicable

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/unioncoin/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/unioncoin/discussions)
- **Email**: support@unioncoin.com

---
 
**Built with passion for decentralized finance**  
**Security-first approach**  
**Production-ready code**:
```bash
python verify.py
