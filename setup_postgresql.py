#!/usr/bin/env python3
"""
PostgreSQL Setup Script for UnionCoin
Install and configure PostgreSQL database
"""

import subprocess
import sys
import os

def run_command(command, description=""):
    """Run shell command and handle errors"""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"   {e.stderr}")
        return False

def install_postgresql():
    """Install PostgreSQL on Ubuntu/Debian"""
    print("🐘 Installing PostgreSQL...")
    
    commands = [
        ("sudo apt update", "Update package list"),
        ("sudo apt install -y postgresql postgresql-contrib", "Install PostgreSQL"),
        ("sudo systemctl start postgresql", "Start PostgreSQL service"),
        ("sudo systemctl enable postgresql", "Enable PostgreSQL on boot")
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            print(f"❌ Failed to {desc.lower()}")
            return False
    
    return True

def setup_database():
    """Setup UnionCoin database and user"""
    print("🗄️ Setting up UnionCoin database...")
    
    commands = [
        ('sudo -u postgres psql -c "DROP DATABASE IF EXISTS unioncoin;"', 'Drop existing database'),
        ('sudo -u postgres psql -c "CREATE DATABASE unioncoin;"', 'Create unioncoin database'),
        ('sudo -u postgres psql -c "DROP USER IF EXISTS postgres;"', 'Drop existing postgres user'),
        ('sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD \\"12345\\";"', 'Create postgres user with password'),
        ('sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE unioncoin TO postgres;"', 'Grant privileges to postgres user'),
        ('sudo -u postgres psql -c "ALTER USER postgres CREATEDB;"', 'Allow database creation'),
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            print(f"❌ Failed to {desc.lower()}")
            return False
    
    return True

def update_database_config():
    """Update database configuration to use PostgreSQL"""
    print("⚙️ Updating database configuration...")
    
    config_content = '''# Database configuration for UnionCoin
# Production PostgreSQL configuration

# Database connection
DATABASE_URL = "postgresql://postgres:12345@localhost/unioncoin"

# Database settings
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "unioncoin"
DB_USER = "postgres"
DB_PASSWORD = "12345"

# Pool settings
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20
DB_POOL_TIMEOUT = 30

# Connection settings
DB_ECHO = False
DB_CLIENT_ENCODING = "utf8"
'''
    
    with open('.env.production', 'w') as f:
        f.write(config_content)
    
    print("✅ Database configuration updated in .env.production")
    return True

def create_database_init_script():
    """Create database initialization script"""
    print("📜 Creating database initialization script...")
    
    script_content = '''#!/bin/bash
# UnionCoin Database Initialization Script

echo "🚀 Initializing UnionCoin PostgreSQL database..."

# Set environment variables
export PGPASSWORD="12345"

# Create database and user
echo "📊 Creating database and user..."
sudo -u postgres psql -c "CREATE DATABASE unioncoin;" || echo "Database already exists"
sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD '12345';" || echo "User already exists"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE unioncoin TO postgres;" || echo "Privileges already granted"

# Run database migrations
echo "🔄 Running database migrations..."
cd /var/www/unioncoin
python database.py

echo "✅ Database initialization completed!"
echo "📊 Database: unioncoin"
echo "👤 User: postgres"
echo "🔐 Password: 12345"
echo "🌐 Host: localhost:5432"
'''
    
    with open('init_database.sh', 'w') as f:
        f.write(script_content)
    
    os.chmod('init_database.sh', 0o755)
    print("✅ Database initialization script created: init_database.sh")
    return True

def test_database_connection():
    """Test PostgreSQL connection"""
    print("🧪 Testing database connection...")
    
    test_script = '''
import psycopg2
import os

try:
    # Test connection
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="unioncoin",
        user="postgres",
        password="12345"
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    
    print(f"✅ Database connection successful!")
    print(f"📊 PostgreSQL version: {version}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    exit(1)
'''
    
    with open('test_db_connection.py', 'w') as f:
        f.write(test_script)
    
    result = run_command([sys.executable, 'test_db_connection.py'], "Test database connection")
    return result

def create_systemd_services():
    """Create systemd services for PostgreSQL"""
    print("⚙️ Creating PostgreSQL systemd services...")
    
    postgres_service = '''[Unit]
Description=PostgreSQL Database Server
After=network.target

[Service]
Type=forking
User=postgres
Group=postgres
ExecStart=/usr/lib/postgresql/*/bin/postgres -D /etc/postgresql/*/postgresql.conf
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
KillSignal=SIGINT
TimeoutSec=300
LimitNOFILE=65536
LimitNPROC=4096
PrivateTmp=yes
ProtectSystem=full
ProtectHome=true
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
'''
    
    with open('postgresql.service', 'w') as f:
        f.write(postgres_service)
    
    print("✅ PostgreSQL service file created")
    return True

def setup_pg_hba():
    """Setup PostgreSQL host-based authentication"""
    print("🔐 Setting up PostgreSQL authentication...")
    
    pg_hba_content = '''# PostgreSQL Client Authentication Configuration File
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# IPv4 local connections:
host    all             all             127.0.0.1/32            md5

# IPv6 local connections:
host    all             all             ::1/128                   md5

# Allow replication connections from localhost, by a user with the replication privilege
host    replication     replicator        127.0.0.1/32            md5

# Allow remote connections (for production - adjust as needed)
# host    all             all             0.0.0.0/0               md5
'''
    
    with open('pg_hba.conf', 'w') as f:
        f.write(pg_hba_content)
    
    # Copy to PostgreSQL config directory
    run_command("sudo cp pg_hba.conf /etc/postgresql/*/pg_hba.conf", "Copy pg_hba.conf")
    run_command("sudo chown postgres:postgres /etc/postgresql/*/pg_hba.conf", "Set ownership")
    
    print("✅ PostgreSQL authentication configured")
    return True

def main():
    """Main PostgreSQL setup menu"""
    print("🐘 UnionCoin PostgreSQL Setup")
    print("=" * 50)
    
    while True:
        print("\n📋 PostgreSQL Setup Options:")
        print("1. 📦 Install PostgreSQL")
        print("2. 🗄️ Setup Database")
        print("3. ⚙️ Update Configuration")
        print("4. 🧪 Test Connection")
        print("5. 🔐 Setup Authentication")
        print("6. 📜 Create Init Script")
        print("7. ⚙️ Create Systemd Services")
        print("8. 🔄 Complete Setup")
        print("9. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-9): ").strip()
        
        if choice == "1":
            install_postgresql()
        elif choice == "2":
            setup_database()
        elif choice == "3":
            update_database_config()
        elif choice == "4":
            test_database_connection()
        elif choice == "5":
            setup_pg_hba()
        elif choice == "6":
            create_database_init_script()
        elif choice == "7":
            create_systemd_services()
        elif choice == "8":
            print("🚀 Running complete PostgreSQL setup...")
            install_postgresql()
            setup_database()
            update_database_config()
            setup_pg_hba()
            create_database_init_script()
            create_systemd_services()
            test_database_connection()
            print("\n✅ PostgreSQL setup completed!")
            print("📊 Database: unioncoin")
            print("👤 User: postgres")
            print("🔐 Password: 12345")
            print("🌐 Host: localhost:5432")
            print("\n📋 Next steps:")
            print("1. Restart PostgreSQL: sudo systemctl restart postgresql")
            print("2. Run UnionCoin with PostgreSQL")
            print("3. Update .env file to use PostgreSQL")
        elif choice == "9":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
