#!/usr/bin/env python3
"""
UnionCoin PostgreSQL Dashboard
Real-time monitoring of all transactions and user activities
"""

import sqlite3
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
import json
import os
import subprocess
import webbrowser
from tabulate import tabulate

class PostgreSQLDashboard:
    def __init__(self):
        self.db_url = "postgresql://postgres:12345@localhost/unioncoin"
        self.web_url = "http://localhost:8000"
        self.admin_url = "http://localhost:8000/api/data?admin=unioncoin_admin_2026"
        self.refresh_interval = 30  # seconds
        
    def connect_postgresql(self):
        """Connect to PostgreSQL database"""
        try:
            import psycopg2
            conn = psycopg2.connect(self.db_url)
            return conn
        except Exception as e:
            print(f"❌ PostgreSQL connection failed: {e}")
            return None
    
    def connect_sqlite(self):
        """Connect to SQLite database (fallback)"""
        try:
            conn = sqlite3.connect('unioncoin.db')
            return conn
        except Exception as e:
            print(f"❌ SQLite connection failed: {e}")
            return None
    
    def get_database_stats(self):
        """Get comprehensive database statistics"""
        print("📊 Getting database statistics...")
        
        # Try PostgreSQL first, then fallback to SQLite
        conn = self.connect_postgresql()
        if not conn:
            conn = self.connect_sqlite()
        
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            # Get user statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_users,
                    COUNT(CASE WHEN balance > 0 THEN 1 END) as active_users,
                    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 1 DAY) THEN 1 END) as new_today,
                    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 END) as new_week,
                    SUM(balance) as total_balance,
                    AVG(balance) as avg_balance,
                    MAX(balance) as max_balance,
                    MIN(balance) as min_balance
                FROM users
            """)
            
            user_stats = cursor.fetchone()
            
            # Get transaction statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_transactions,
                    COUNT(CASE WHEN timestamp >= DATE_SUB(NOW(), INTERVAL 1 DAY) THEN 1 END) as transactions_today,
                    COUNT(CASE WHEN timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 END) as transactions_week,
                    SUM(amount) as total_volume,
                    AVG(amount) as avg_transaction,
                    MAX(amount) as max_transaction,
                    MIN(amount) as min_transaction,
                    COUNT(CASE WHEN transaction_type = 'p2p' THEN 1 END) as p2p_transactions,
                    COUNT(CASE WHEN transaction_type = 'welcome_bonus' THEN 1 END) as bonus_transactions
                FROM transactions
            """)
            
            transaction_stats = cursor.fetchone()
            
            # Get top users by balance
            cursor.execute("""
                SELECT username, wallet_address, balance, created_at
                FROM users 
                ORDER BY balance DESC 
                LIMIT 10
            """)
            
            top_users = cursor.fetchall()
            
            # Get recent transactions
            cursor.execute("""
                SELECT t.timestamp, s.username as sender, r.username as receiver, 
                       t.amount, t.transaction_type
                FROM transactions t
                LEFT JOIN users s ON t.sender_id = s.id
                LEFT JOIN users r ON t.receiver_id = r.id
                ORDER BY t.timestamp DESC
                LIMIT 20
            """)
            
            recent_transactions = cursor.fetchall()
            
            # Get daily statistics for last 7 days
            cursor.execute("""
                SELECT 
                    DATE(timestamp) as date,
                    COUNT(*) as transactions,
                    SUM(amount) as volume,
                    COUNT(DISTINCT sender_id) as active_senders
                FROM transactions
                WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)
                GROUP BY DATE(timestamp)
                ORDER BY date DESC
            """)
            
            daily_stats = cursor.fetchall()
            
            conn.close()
            
            return {
                'user_stats': user_stats,
                'transaction_stats': transaction_stats,
                'top_users': top_users,
                'recent_transactions': recent_transactions,
                'daily_stats': daily_stats
            }
            
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            conn.close()
            return None
    
    def display_dashboard(self):
        """Display comprehensive dashboard"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("🚀 UnionCoin PostgreSQL Dashboard")
            print("=" * 80)
            print(f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"🔄 Auto-refresh: Every {self.refresh_interval} seconds")
            print("=" * 80)
            
            stats = self.get_database_stats()
            
            if not stats:
                print("❌ Failed to get database statistics")
                break
            
            # User Statistics
            print("\n👥 USER STATISTICS")
            print("-" * 40)
            user_stats = stats['user_stats']
            print(f"📊 Total Users: {user_stats[0]:,}")
            print(f"✅ Active Users: {user_stats[1]:,}")
            print(f"🆕 New Today: {user_stats[2]:,}")
            print(f"📈 New This Week: {user_stats[3]:,}")
            print(f"💰 Total Balance: {user_stats[4]:,.2f} UC")
            print(f"📊 Average Balance: {user_stats[5]:,.2f} UC")
            print(f"🏆 Highest Balance: {user_stats[6]:,.2f} UC")
            print(f"📉 Lowest Balance: {user_stats[7]:,.2f} UC")
            
            # Transaction Statistics
            print("\n🔗 TRANSACTION STATISTICS")
            print("-" * 40)
            tx_stats = stats['transaction_stats']
            print(f"📊 Total Transactions: {tx_stats[0]:,}")
            print(f"🆕 Today: {tx_stats[1]:,}")
            print(f"📈 This Week: {tx_stats[2]:,}")
            print(f"💰 Total Volume: {tx_stats[3]:,.2f} UC")
            print(f"📊 Average Transaction: {tx_stats[4]:,.2f} UC")
            print(f"🏆 Largest Transaction: {tx_stats[5]:,.2f} UC")
            print(f"📉 Smallest Transaction: {tx_stats[6]:,.2f} UC")
            print(f"🤝 P2P Transactions: {tx_stats[7]:,}")
            print(f"🎁 Bonus Transactions: {tx_stats[8]:,}")
            
            # Top Users
            print("\n🏆 TOP 10 USERS BY BALANCE")
            print("-" * 40)
            top_users_data = []
            for user in stats['top_users']:
                top_users_data.append([
                    user[0][:15],  # username
                    user[1][:12],  # wallet_address
                    f"{user[2]:,.2f}",  # balance
                    user[3].strftime('%Y-%m-%d') if user[3] else 'N/A'  # created_at
                ])
            
            headers = ['Username', 'Wallet', 'Balance (UC)', 'Created']
            print(tabulate(top_users_data, headers=headers, tablefmt='grid'))
            
            # Recent Transactions
            print("\n📈 RECENT TRANSACTIONS (Last 20)")
            print("-" * 40)
            recent_tx_data = []
            for tx in stats['recent_transactions']:
                recent_tx_data.append([
                    tx[0].strftime('%H:%M:%S') if tx[0] else 'N/A',  # timestamp
                    tx[1][:12] if tx[1] else 'System',  # sender
                    tx[2][:12] if tx[2] else 'System',  # receiver
                    f"{tx[3]:,.2f}",  # amount
                    tx[4][:10]  # transaction_type
                ])
            
            headers = ['Time', 'Sender', 'Receiver', 'Amount (UC)', 'Type']
            print(tabulate(recent_tx_data, headers=headers, tablefmt='grid'))
            
            # Daily Statistics
            print("\n📅 DAILY STATISTICS (Last 7 Days)")
            print("-" * 40)
            daily_data = []
            for day in stats['daily_stats']:
                daily_data.append([
                    day[0].strftime('%Y-%m-%d'),  # date
                    day[1],  # transactions
                    f"{day[2]:,.2f}",  # volume
                    day[3]  # active_senders
                ])
            
            headers = ['Date', 'Transactions', 'Volume (UC)', 'Active Senders']
            print(tabulate(daily_data, headers=headers, tablefmt='grid'))
            
            print("\n" + "=" * 80)
            print("🔄 Refreshing in 30 seconds... (Press Ctrl+C to exit)")
            
            try:
                time.sleep(self.refresh_interval)
            except KeyboardInterrupt:
                print("\n👋 Dashboard stopped by user")
                break
    
    def export_to_excel(self):
        """Export data to Excel file"""
        print("📊 Exporting data to Excel...")
        
        stats = self.get_database_stats()
        
        if not stats:
            print("❌ Failed to get data for export")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        try:
            # Create Excel file
            with pd.ExcelWriter(f'unioncoin_report_{timestamp}.xlsx', engine='openpyxl') as writer:
                
                # Users data
                users_data = []
                for user in stats['top_users']:
                    users_data.append({
                        'Username': user[0],
                        'Wallet Address': user[1],
                        'Balance': user[2],
                        'Created At': user[3]
                    })
                
                users_df = pd.DataFrame(users_data)
                users_df.to_excel(writer, sheet_name='Top Users', index=False)
                
                # Transactions data
                tx_data = []
                for tx in stats['recent_transactions']:
                    tx_data.append({
                        'Timestamp': tx[0],
                        'Sender': tx[1],
                        'Receiver': tx[2],
                        'Amount': tx[3],
                        'Type': tx[4]
                    })
                
                tx_df = pd.DataFrame(tx_data)
                tx_df.to_excel(writer, sheet_name='Recent Transactions', index=False)
                
                # Daily statistics
                daily_data = []
                for day in stats['daily_stats']:
                    daily_data.append({
                        'Date': day[0],
                        'Transactions': day[1],
                        'Volume': day[2],
                        'Active Senders': day[3]
                    })
                
                daily_df = pd.DataFrame(daily_data)
                daily_df.to_excel(writer, sheet_name='Daily Statistics', index=False)
                
                # Summary statistics
                summary_data = {
                    'Metric': ['Total Users', 'Active Users', 'New Today', 'Total Balance', 
                              'Total Transactions', 'Total Volume', 'Average Transaction'],
                    'Value': [
                        stats['user_stats'][0],
                        stats['user_stats'][1],
                        stats['user_stats'][2],
                        f"{stats['user_stats'][4]:,.2f}",
                        stats['transaction_stats'][0],
                        f"{stats['transaction_stats'][3]:,.2f}",
                        f"{stats['transaction_stats'][4]:,.2f}"
                    ]
                }
                
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            print(f"✅ Data exported to: unioncoin_report_{timestamp}.xlsx")
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
    
    def search_transactions(self, username=None, wallet_address=None):
        """Search transactions by username or wallet address"""
        print(f"🔍 Searching transactions...")
        
        conn = self.connect_postgresql()
        if not conn:
            conn = self.connect_sqlite()
        
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            if username:
                cursor.execute("""
                    SELECT t.timestamp, s.username as sender, r.username as receiver, 
                           t.amount, t.transaction_type
                    FROM transactions t
                    LEFT JOIN users s ON t.sender_id = s.id
                    LEFT JOIN users r ON t.receiver_id = r.id
                    WHERE s.username LIKE ? OR r.username LIKE ?
                    ORDER BY t.timestamp DESC
                    LIMIT 50
                """, (f'%{username}%', f'%{username}%'))
            
            elif wallet_address:
                cursor.execute("""
                    SELECT t.timestamp, s.username as sender, r.username as receiver, 
                           t.amount, t.transaction_type
                    FROM transactions t
                    LEFT JOIN users s ON t.sender_id = s.id
                    LEFT JOIN users r ON t.receiver_id = r.id
                    WHERE s.wallet_address LIKE ? OR r.wallet_address LIKE ?
                    ORDER BY t.timestamp DESC
                    LIMIT 50
                """, (f'%{wallet_address}%', f'%{wallet_address}%'))
            
            results = cursor.fetchall()
            conn.close()
            
            return results
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            conn.close()
            return None
    
    def get_user_details(self, username=None, wallet_address=None):
        """Get detailed user information"""
        print(f"👤 Getting user details...")
        
        conn = self.connect_postgresql()
        if not conn:
            conn = self.connect_sqlite()
        
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            if username:
                cursor.execute("""
                    SELECT id, username, wallet_address, balance, created_at, tg_id, is_primary, profile_color
                    FROM users
                    WHERE username = ?
                """, (username,))
            
            elif wallet_address:
                cursor.execute("""
                    SELECT id, username, wallet_address, balance, created_at, tg_id, is_primary, profile_color
                    FROM users
                    WHERE wallet_address = ?
                """, (wallet_address,))
            
            user = cursor.fetchone()
            
            if user:
                # Get user's transactions
                cursor.execute("""
                    SELECT t.timestamp, s.username as sender, r.username as receiver, 
                           t.amount, t.transaction_type
                    FROM transactions t
                    LEFT JOIN users s ON t.sender_id = s.id
                    LEFT JOIN users r ON t.receiver_id = r.id
                    WHERE t.sender_id = ? OR t.receiver_id = ?
                    ORDER BY t.timestamp DESC
                    LIMIT 20
                """, (user[0], user[0]))
                
                transactions = cursor.fetchall()
                
                conn.close()
                
                return {
                    'user': user,
                    'transactions': transactions
                }
            
            conn.close()
            return None
            
        except Exception as e:
            print(f"❌ Error getting user details: {e}")
            conn.close()
            return None
    
    def show_menu(self):
        """Show interactive menu"""
        while True:
            print("\n🚀 UnionCoin PostgreSQL Dashboard")
            print("=" * 50)
            print("1. 📊 Live Dashboard")
            print("2. 🔍 Search Transactions")
            print("3. 👤 Get User Details")
            print("4. 📊 Export to Excel")
            print("5. 🌐 Open Web Interface")
            print("6. 📊 Open Admin Panel")
            print("7. ❌ Exit")
            
            choice = input("\n👉 Enter your choice (1-7): ").strip()
            
            if choice == "1":
                self.display_dashboard()
            elif choice == "2":
                search_type = input("🔍 Search by (username/wallet): ").strip().lower()
                if search_type == 'username':
                    username = input("👤 Enter username: ").strip()
                    results = self.search_transactions(username=username)
                elif search_type == 'wallet':
                    wallet = input("💳 Enter wallet address: ").strip()
                    results = self.search_transactions(wallet_address=wallet)
                else:
                    print("❌ Invalid search type")
                    continue
                
                if results:
                    print(f"\n🔍 Found {len(results)} transactions:")
                    for tx in results:
                        print(f"  {tx[0]} - {tx[1]} → {tx[2]}: {tx[3]} UC ({tx[4]})")
                else:
                    print("❌ No transactions found")
            
            elif choice == "3":
                search_type = input("🔍 Search by (username/wallet): ").strip().lower()
                if search_type == 'username':
                    username = input("👤 Enter username: ").strip()
                    details = self.get_user_details(username=username)
                elif search_type == 'wallet':
                    wallet = input("💳 Enter wallet address: ").strip()
                    details = self.get_user_details(wallet_address=wallet)
                else:
                    print("❌ Invalid search type")
                    continue
                
                if details:
                    user = details['user']
                    transactions = details['transactions']
                    
                    print(f"\n👤 User Details:")
                    print(f"  Username: {user[1]}")
                    print(f"  Wallet: {user[2]}")
                    print(f"  Balance: {user[3]:,.2f} UC")
                    print(f"  Created: {user[4]}")
                    print(f"  Telegram ID: {user[5]}")
                    print(f"  Is Primary: {user[6]}")
                    print(f"  Profile Color: {user[7]}")
                    
                    print(f"\n📈 Recent Transactions ({len(transactions)}):")
                    for tx in transactions:
                        print(f"  {tx[0]} - {tx[1]} → {tx[2]}: {tx[3]} UC ({tx[4]})")
                else:
                    print("❌ User not found")
            
            elif choice == "4":
                self.export_to_excel()
            
            elif choice == "5":
                webbrowser.open(self.web_url)
                print("🌐 Web interface opened")
            
            elif choice == "6":
                webbrowser.open(self.admin_url)
                print("📊 Admin panel opened")
            
            elif choice == "7":
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice! Please try again.")

def main():
    """Main dashboard application"""
    print("🚀 UnionCoin PostgreSQL Dashboard")
    print("=" * 50)
    
    dashboard = PostgreSQLDashboard()
    dashboard.show_menu()

if __name__ == "__main__":
    main()
