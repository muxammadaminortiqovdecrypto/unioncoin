"""
UnionCoin Data Viewer
View all users, transactions, and blockchain data
"""

from database import get_db, User, Transaction
from datetime import datetime

def view_all_users():
    """View all users in the system"""
    print("\n" + "="*60)
    print("👥 ALL USERS")
    print("="*60)
    
    with next(get_db()) as db:
        users = db.query(User).all()
        
        if not users:
            print("No users found in the database.")
            return
            
        for user in users:
            print(f"\n📱 User ID: {user.id}")
            print(f"👤 Username: @{user.username}")
            print(f"💳 Wallet: {user.wallet_address}")
            print(f"💰 Balance: {user.balance:.2f} UC")
            print(f"🤖 Telegram ID: {user.tg_id if user.tg_id else 'Web User'}")
            print(f"📅 Created: {user.created_at}")
            print(f"✅ Active: {user.is_active}")
            print("-" * 40)

def view_all_transactions():
    """View all transactions with blockchain details"""
    print("\n" + "="*60)
    print("🔗 ALL TRANSACTIONS (BLOCKCHAIN)")
    print("="*60)
    
    with next(get_db()) as db:
        transactions = db.query(Transaction).order_by(Transaction.id).all()
        
        if not transactions:
            print("No transactions found in the database.")
            return
            
        for tx in transactions:
            # Get sender and receiver info
            sender = db.query(User).filter(User.id == tx.sender_id).first() if tx.sender_id != 0 else None
            receiver = db.query(User).filter(User.id == tx.receiver_id).first()
            
            print(f"\n🆔 Transaction ID: {tx.id}")
            print(f"📅 Timestamp: {tx.timestamp}")
            print(f"💸 Amount: {tx.amount:.2f} UC")
            print(f"📝 Type: {tx.transaction_type}")
            print(f"✅ Approved: {tx.is_approved}")
            
            if sender:
                print(f"👤 Sender: @{sender.username} ({sender.wallet_address})")
            else:
                print(f"👤 Sender: SYSTEM (Bonus/Admin)")
                
            if receiver:
                print(f"👤 Receiver: @{receiver.username} ({receiver.wallet_address})")
                
            print(f"🔗 Previous Hash: {tx.prev_hash[:16]}...")
            print(f"🔗 Current Hash: {tx.current_hash[:16]}...")
            print("-" * 60)

def view_blockchain_verification():
    """Show blockchain integrity details"""
    print("\n" + "="*60)
    print("🛡️ BLOCKCHAIN INTEGRITY VERIFICATION")
    print("="*60)
    
    with next(get_db()) as db:
        from database import verify_chain_integrity
        
        is_valid = verify_chain_integrity(db)
        print(f"✅ Blockchain Valid: {is_valid}")
        
        transactions = db.query(Transaction).order_by(Transaction.id).all()
        print(f"📊 Total Transactions: {len(transactions)}")
        
        if transactions:
            print(f"🔗 Chain Links: {len(transactions)} blocks")
            print(f"📅 First Transaction: {transactions[0].timestamp}")
            print(f"📅 Last Transaction: {transactions[-1].timestamp}")

def view_system_statistics():
    """Show system-wide statistics"""
    print("\n" + "="*60)
    print("📊 SYSTEM STATISTICS")
    print("="*60)
    
    with next(get_db()) as db:
        # User statistics
        total_users = db.query(User).count()
        web_users = db.query(User).filter(User.tg_id.is_(None)).count()
        telegram_users = db.query(User).filter(User.tg_id.isnot(None)).count()
        
        # Transaction statistics
        total_transactions = db.query(Transaction).count()
        bonus_transactions = db.query(Transaction).filter(Transaction.transaction_type == "bonus").count()
        p2p_transactions = db.query(Transaction).filter(Transaction.transaction_type == "p2p").count()
        admin_transactions = db.query(Transaction).filter(Transaction.transaction_type == "admin_approval").count()
        
        # Balance statistics
        total_supply = db.query(User).with_entities(db.func.sum(User.balance)).scalar() or 0
        
        print(f"👥 Total Users: {total_users}")
        print(f"   🌐 Web Users: {web_users}")
        print(f"   🤖 Telegram Users: {telegram_users}")
        print(f"\n🔗 Total Transactions: {total_transactions}")
        print(f"   🎁 Bonus Transactions: {bonus_transactions}")
        print(f"   🔄 P2P Transactions: {p2p_transactions}")
        print(f"   👑 Admin Transactions: {admin_transactions}")
        print(f"\n💰 Total Token Supply: {total_supply:.2f} UC")

def search_user_by_wallet(wallet_address):
    """Find user by wallet address"""
    print(f"\n🔍 Searching for wallet: {wallet_address}")
    
    with next(get_db()) as db:
        user = db.query(User).filter(User.wallet_address == wallet_address).first()
        
        if not user:
            print("❌ Wallet not found!")
            return
            
        print(f"✅ Found User:")
        print(f"👤 Username: @{user.username}")
        print(f"💳 Wallet: {user.wallet_address}")
        print(f"💰 Balance: {user.balance:.2f} UC")
        print(f"🤖 Telegram ID: {user.tg_id if user.tg_id else 'Web User'}")
        
        # Show user's transactions
        sent_tx = db.query(Transaction).filter(Transaction.sender_id == user.id).all()
        received_tx = db.query(Transaction).filter(Transaction.receiver_id == user.id).all()
        
        print(f"\n📤 Sent Transactions: {len(sent_tx)}")
        print(f"📥 Received Transactions: {len(received_tx)}")

def main():
    """Main menu for data viewer"""
    while True:
        print("\n" + "="*60)
        print("🔍 UNIONCOIN DATA VIEWER")
        print("="*60)
        print("1. 👥 View All Users")
        print("2. 🔗 View All Transactions (Blockchain)")
        print("3. 🛡️ Blockchain Verification")
        print("4. 📊 System Statistics")
        print("5. 🔍 Search by Wallet Address")
        print("6. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-6): ").strip()
        
        if choice == "1":
            view_all_users()
        elif choice == "2":
            view_all_transactions()
        elif choice == "3":
            view_blockchain_verification()
        elif choice == "4":
            view_system_statistics()
        elif choice == "5":
            wallet = input("👉 Enter wallet address: ").strip()
            search_user_by_wallet(wallet)
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")
        
        input("\n👉 Press Enter to continue...")

if __name__ == "__main__":
    main()
