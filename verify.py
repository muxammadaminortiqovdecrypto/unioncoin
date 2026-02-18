"""
Blockchain Verification Script
Audits database for tampered records
"""

from database import get_db, Transaction, verify_chain_integrity
import sys

def audit_database():
    """Perform complete database audit"""
    print("Starting blockchain audit...")
    
    with next(get_db()) as db:
        # Verify chain integrity
        is_valid = verify_chain_integrity(db)
        
        if is_valid:
            print("Blockchain integrity verified - No tampering detected")
        else:
            print("BLOCKCHAIN TAMPERING DETECTED!")
            print("Analyzing transactions...")
            
            transactions = db.query(Transaction).order_by(Transaction.id).all()
            for i, tx in enumerate(transactions):
                print(f"Transaction {i+1}: ID={tx.id}, Hash={tx.current_hash[:16]}...")
        
        # Get statistics
        total_tx = db.query(Transaction).count()
        total_users = db.query(Transaction).distinct(Transaction.sender_id).count()
        
        print(f"\nDatabase Statistics:")
        print(f"Total Transactions: {total_tx}")
        print(f"Active Users: {total_users}")
        print(f"Chain Valid: {'Yes' if is_valid else 'No'}")

if __name__ == "__main__":
    audit_database()
