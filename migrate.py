import os
import sqlalchemy
from sqlalchemy import create_engine, text

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./unioncoin.db")

def migrate():
    print(f"🔍 Checking database at: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Check users table
        print("Checking 'users' table...")
        columns_users = [row[1] for row in conn.execute(text("PRAGMA table_info(users)"))] if "sqlite" in DATABASE_URL else []
        
        # For PostgreSQL
        if "postgresql" in DATABASE_URL:
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users'"))
            columns_users = [row[0] for row in result]

        if "seed_phrase" not in columns_users:
            print("Adding 'seed_phrase' column to 'users'...")
            conn.execute(text("ALTER TABLE users ADD COLUMN seed_phrase VARCHAR"))
            conn.commit()
            
        if "password_hash" not in columns_users:
            print("Adding 'password_hash' column to 'users'...")
            conn.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR"))
            conn.commit()

        # Check transactions table
        print("Checking 'transactions' table...")
        columns_tx = [row[1] for row in conn.execute(text("PRAGMA table_info(transactions)"))] if "sqlite" in DATABASE_URL else []
        
        if "postgresql" in DATABASE_URL:
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='transactions'"))
            columns_tx = [row[0] for row in result]

        if "status" not in columns_tx:
            print("Adding 'status' column to 'transactions'...")
            conn.execute(text("ALTER TABLE transactions ADD COLUMN status VARCHAR DEFAULT 'Approved'"))
            conn.commit()
            
        if "tx_hash" not in columns_tx:
            print("Adding 'tx_hash' column to 'transactions'...")
            conn.execute(text("ALTER TABLE transactions ADD COLUMN tx_hash VARCHAR"))
            conn.commit()

    print("✅ Migration completed successfully!")

if __name__ == "__main__":
    migrate()
