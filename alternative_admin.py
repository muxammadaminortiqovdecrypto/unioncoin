#!/usr/bin/env python3
"""
UnionCoin Alternative Admin Panel Solutions
Multiple admin panel options if main one fails
"""

import os
import webbrowser
import requests
import json
from datetime import datetime

class AlternativeAdminPanel:
    def __init__(self):
        self.web_url = "http://localhost:8000"
        self.render_url = "https://unioncoin.onrender.com"
        self.admin_password = "unioncoin_admin_2026"
        
    def create_alternative_admin_endpoints(self):
        """Create alternative admin endpoints"""
        print("🔧 Creating alternative admin endpoints...")
        
        # Alternative admin endpoint 1: Simple admin
        alt_admin_1 = '''
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db, User, Transaction
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/admin-simple")
async def admin_simple():
    """Simple admin panel without password"""
    try:
        db = next(get_db())
        users = db.query(User).all()
        transactions = db.query(Transaction).all()
        
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>UnionCoin Admin Panel (Simple)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
        .stat { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f4f4f4; font-weight: bold; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 UnionCoin Admin Panel (Simple)</h1>
            <p>Alternative admin panel - No password required</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <h3>👥 Total Users</h3>
                <h2>{}</h2>
            </div>
            <div class="stat">
                <h3>🔗 Total Transactions</h3>
                <h2>{}</h2>
            </div>
            <div class="stat">
                <h3>💰 Total Balance</h3>
                <h2>{:.2f} UC</h2>
            </div>
            <div class="stat">
                <h3>📊 Active Users</h3>
                <h2>{}</h2>
            </div>
        </div>
        
        <div class="card">
            <h2>👥 Recent Users</h2>
            <table>
                <tr><th>Username</th><th>Wallet</th><th>Balance</th><th>Created</th></tr>
                {}
            </table>
        </div>
        
        <div class="card">
            <h2>🔗 Recent Transactions</h2>
            <table>
                <tr><th>Time</th><th>Sender</th><th>Receiver</th><th>Amount</th><th>Type</th></tr>
                {}
            </table>
        </div>
    </div>
</body>
</html>
        """.format(
            len(users),
            len(transactions),
            sum(user.balance for user in users),
            len([u for u in users if u.balance > 0]),
            "".join([f"<tr><td>{user.username}</td><td>{user.wallet_address}</td><td>{user.balance:.2f}</td><td>{user.created_at}</td></tr>" for user in users[-10:]]),
            "".join([f"<tr><td>{tx.timestamp}</td><td>{tx.sender_id}</td><td>{tx.receiver_id}</td><td>{tx.amount:.2f}</td><td>{tx.transaction_type}</td></tr>" for tx in transactions[-10:]])
        )
        
        return HTMLResponse(content=html)
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
'''
        
        with open('alternative_admin_1.py', 'w') as f:
            f.write(alt_admin_1)
        
        print("✅ Alternative admin 1 created: alternative_admin_1.py")
        
        # Alternative admin endpoint 2: JSON API
        alt_admin_2 = '''
from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db, User, Transaction

app = FastAPI()

@app.get("/admin-json")
async def admin_json():
    """JSON admin API without password"""
    try:
        db = next(get_db())
        users = db.query(User).all()
        transactions = db.query(Transaction).all()
        
        return {
            "users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "wallet_address": user.wallet_address,
                    "balance": user.balance,
                    "created_at": user.created_at.isoformat() if user.created_at else None
                }
                for user in users
            ],
            "transactions": [
                {
                    "id": tx.id,
                    "sender_id": tx.sender_id,
                    "receiver_id": tx.receiver_id,
                    "amount": tx.amount,
                    "timestamp": tx.timestamp.isoformat() if tx.timestamp else None,
                    "transaction_type": tx.transaction_type
                }
                for tx in transactions
            ],
            "stats": {
                "total_users": len(users),
                "total_transactions": len(transactions),
                "total_balance": sum(user.balance for user in users),
                "active_users": len([u for u in users if u.balance > 0])
            }
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/admin-stats")
async def admin_stats():
    """Simple stats endpoint"""
    try:
        db = next(get_db())
        users = db.query(User).all()
        transactions = db.query(Transaction).all()
        
        return {
            "total_users": len(users),
            "total_transactions": len(transactions),
            "total_balance": sum(user.balance for user in users),
            "active_users": len([u for u in users if u.balance > 0]),
            "new_users_today": len([u for u in users if u.created_at.date() == datetime.now().date()]),
            "transactions_today": len([t for t in transactions if t.timestamp.date() == datetime.now().date()])
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
'''
        
        with open('alternative_admin_2.py', 'w') as f:
            f.write(alt_admin_2)
        
        print("✅ Alternative admin 2 created: alternative_admin_2.py")
        
        return True
    
    def create_standalone_admin_dashboard(self):
        """Create standalone admin dashboard"""
        print("📊 Creating standalone admin dashboard...")
        
        dashboard_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UnionCoin Admin Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 20px; border-radius: 15px; margin-bottom: 30px; text-align: center; color: white; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,0.1); transition: transform 0.3s; }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-number { font-size: 2.5em; font-weight: bold; color: #667eea; margin-bottom: 10px; }
        .stat-label { color: #666; font-size: 1.1em; }
        .chart-container { background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); padding: 25px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }
        .data-table { background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); padding: 25px; border-radius: 15px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; font-weight: 600; color: #333; }
        .refresh-btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 12px 24px; border-radius: 25px; cursor: pointer; font-size: 1em; margin: 10px; transition: transform 0.3s; }
        .refresh-btn:hover { transform: scale(1.05); }
        .url-display { background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; margin: 20px 0; text-align: center; }
        .url-display a { color: white; text-decoration: none; font-weight: bold; }
        .loading { text-align: center; padding: 50px; color: white; font-size: 1.2em; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 UnionCoin Admin Dashboard</h1>
            <p>Alternative Admin Panel - Direct Database Access</p>
            <div class="url-display">
                <p>🌐 Main Admin: <a href="http://localhost:8000/api/data?admin=unioncoin_admin_2026" target="_blank">http://localhost:8000/api/data?admin=unioncoin_admin_2026</a></p>
                <p>🔧 Alternative 1: <a href="http://localhost:8001/admin-simple" target="_blank">http://localhost:8001/admin-simple</a></p>
                <p>📊 Alternative 2: <a href="http://localhost:8002/admin-json" target="_blank">http://localhost:8002/admin-json</a></p>
                <p>🌐 Render Admin: <a href="https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026" target="_blank">https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026</a></p>
            </div>
            <button class="refresh-btn" onclick="loadData()">🔄 Refresh Data</button>
        </div>
        
        <div id="loading" class="loading">
            <p>🔄 Loading admin data...</p>
        </div>
        
        <div id="dashboard" style="display: none;">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number" id="totalUsers">0</div>
                    <div class="stat-label">👥 Total Users</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="totalTransactions">0</div>
                    <div class="stat-label">🔗 Total Transactions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="totalBalance">0</div>
                    <div class="stat-label">💰 Total Balance</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="activeUsers">0</div>
                    <div class="stat-label">📊 Active Users</div>
                </div>
            </div>
            
            <div class="chart-container">
                <h2>📈 Transaction Activity</h2>
                <canvas id="transactionChart" width="400" height="200"></canvas>
            </div>
            
            <div class="data-table">
                <h2>👥 Recent Users</h2>
                <table id="usersTable">
                    <thead>
                        <tr>
                            <th>Username</th>
                            <th>Wallet Address</th>
                            <th>Balance</th>
                            <th>Created</th>
                        </tr>
                    </thead>
                    <tbody id="usersTableBody">
                        <tr><td colspan="4" style="text-align: center;">Loading...</td></tr>
                    </tbody>
                </table>
            </div>
            
            <div class="data-table">
                <h2>🔗 Recent Transactions</h2>
                <table id="transactionsTable">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Sender</th>
                            <th>Receiver</th>
                            <th>Amount</th>
                            <th>Type</th>
                        </tr>
                    </thead>
                    <tbody id="transactionsTableBody">
                        <tr><td colspan="5" style="text-align: center;">Loading...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <script>
        let chart = null;
        
        async function loadData() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('dashboard').style.display = 'none';
            
            try {
                // Try multiple endpoints
                const endpoints = [
                    'http://localhost:8000/api/data?admin=unioncoin_admin_2026',
                    'http://localhost:8001/admin-simple',
                    'http://localhost:8002/admin-json',
                    'https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026'
                ];
                
                let data = null;
                for (let endpoint of endpoints) {
                    try {
                        const response = await fetch(endpoint);
                        if (response.ok) {
                            data = await response.json();
                            break;
                        }
                    } catch (e) {
                        continue;
                    }
                }
                
                if (data) {
                    updateDashboard(data);
                } else {
                    showError('Unable to load admin data. Please check if the server is running.');
                }
            } catch (error) {
                showError('Error loading admin data: ' + error.message);
            }
        }
        
        function updateDashboard(data) {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
            
            // Update stats
            document.getElementById('totalUsers').textContent = data.total_users || 0;
            document.getElementById('totalTransactions').textContent = data.total_transactions || 0;
            document.getElementById('totalBalance').textContent = (data.total_balance || 0).toFixed(2);
            document.getElementById('activeUsers').textContent = data.active_users || 0;
            
            // Update users table
            const usersTableBody = document.getElementById('usersTableBody');
            if (data.users && data.users.length > 0) {
                usersTableBody.innerHTML = data.users.slice(0, 10).map(user => `
                    <tr>
                        <td>${user.username}</td>
                        <td>${user.wallet_address}</td>
                        <td>${user.balance.toFixed(2)}</td>
                        <td>${new Date(user.created_at).toLocaleString()}</td>
                    </tr>
                `).join('');
            } else {
                usersTableBody.innerHTML = '<tr><td colspan="4" style="text-align: center;">No users found</td></tr>';
            }
            
            // Update transactions table
            const transactionsTableBody = document.getElementById('transactionsTableBody');
            if (data.transactions && data.transactions.length > 0) {
                transactionsTableBody.innerHTML = data.transactions.slice(0, 10).map(tx => `
                    <tr>
                        <td>${new Date(tx.timestamp).toLocaleString()}</td>
                        <td>${tx.sender_id}</td>
                        <td>${tx.receiver_id}</td>
                        <td>${tx.amount.toFixed(2)}</td>
                        <td>${tx.transaction_type}</td>
                    </tr>
                `).join('');
            } else {
                transactionsTableBody.innerHTML = '<tr><td colspan="5" style="text-align: center;">No transactions found</td></tr>';
            }
            
            // Update chart
            updateChart(data.transactions || []);
        }
        
        function updateChart(transactions) {
            const ctx = document.getElementById('transactionChart').getContext('2d');
            
            // Group transactions by date
            const dailyData = {};
            transactions.forEach(tx => {
                const date = new Date(tx.timestamp).toLocaleDateString();
                dailyData[date] = (dailyData[date] || 0) + tx.amount;
            });
            
            const labels = Object.keys(dailyData).slice(-7);
            const data = labels.map(date => dailyData[date] || 0);
            
            if (chart) {
                chart.destroy();
            }
            
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Daily Transaction Volume',
                        data: data,
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Amount (UC)'
                            }
                        }
                    }
                }
            });
        }
        
        function showError(message) {
            document.getElementById('loading').innerHTML = `<p style="color: #ff6b6b;">❌ ${message}</p>`;
        }
        
        // Load data on page load
        loadData();
        
        // Auto-refresh every 30 seconds
        setInterval(loadData, 30000);
    </script>
</body>
</html>
        '''
        
        with open('admin_dashboard.html', 'w') as f:
            f.write(dashboard_html)
        
        print("✅ Standalone admin dashboard created: admin_dashboard.html")
        return True
    
    def start_alternative_servers(self):
        """Start alternative admin servers"""
        print("🚀 Starting alternative admin servers...")
        
        try:
            # Start alternative admin 1
            import subprocess
            import threading
            
            def start_admin_1():
                subprocess.Popen(['python', 'alternative_admin_1.py'], 
                             creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            
            def start_admin_2():
                subprocess.Popen(['python', 'alternative_admin_2.py'], 
                             creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            
            # Start in separate threads
            threading.Thread(target=start_admin_1, daemon=True).start()
            threading.Thread(target=start_admin_2, daemon=True).start()
            
            print("✅ Alternative admin servers started!")
            print("🌐 Alternative 1: http://localhost:8001/admin-simple")
            print("📊 Alternative 2: http://localhost:8002/admin-json")
            print("📁 Dashboard: admin_dashboard.html")
            
            return True
            
        except Exception as e:
            print(f"❌ Error starting alternative servers: {e}")
            return False
    
    def open_alternative_panels(self):
        """Open all alternative admin panels"""
        print("🌐 Opening alternative admin panels...")
        
        urls = [
            ("Main Admin", "http://localhost:8000/api/data?admin=unioncoin_admin_2026"),
            ("Alternative 1", "http://localhost:8001/admin-simple"),
            ("Alternative 2", "http://localhost:8002/admin-json"),
            ("Standalone Dashboard", "file://" + os.path.abspath("admin_dashboard.html")),
            ("Render Admin", "https://unioncoin.onrender.com/api/data?admin=unioncoin_admin_2026")
        ]
        
        for name, url in urls:
            try:
                webbrowser.open(url)
                print(f"✅ Opened {name}: {url}")
            except Exception as e:
                print(f"❌ Failed to open {name}: {e}")
        
        return True
    
    def show_alternative_solutions(self):
        """Show all alternative solutions"""
        print("🔧 ALTERNATIVE ADMIN PANEL SOLUTIONS")
        print("=" * 60)
        
        print("\n1️⃣ ALTERNATIVE ENDPOINTS:")
        print("-" * 40)
        print("• Simple Admin: http://localhost:8001/admin-simple")
        print("• JSON API: http://localhost:8002/admin-json")
        print("• Stats API: http://localhost:8002/admin-stats")
        print("• Standalone Dashboard: admin_dashboard.html")
        
        print("\n2️⃣ DIFFERENT APPROACHES:")
        print("-" * 40)
        print("• Direct Database Access: Connect directly to PostgreSQL")
        print("• Local API Server: Run separate admin server")
        print("• Static HTML Dashboard: No server required")
        print("• Mobile App: Admin panel on mobile")
        
        print("\n3️⃣ BACKUP SOLUTIONS:")
        print("-" * 40)
        print("• Excel Export: Manual data analysis")
        print("• CSV Export: Data backup and analysis")
        print("• Database Backup: Direct database access")
        print("• Log Analysis: Server log monitoring")
        
        print("\n4️⃣ QUICK FIXES:")
        print("-" * 40)
        print("• Change Admin Password: Use different password")
        print("• Remove Password: No password required")
        print("• IP Whitelist: Allow only your IP")
        print("• Basic Auth: Simple username/password")
        
        return True
    
    def create_database_direct_access(self):
        """Create direct database access script"""
        print("🗄️ Creating direct database access script...")
        
        db_script = '''
import sqlite3
import psycopg2
import pandas as pd
from datetime import datetime

class DirectDatabaseAccess:
    def __init__(self):
        self.sqlite_path = "unioncoin.db"
        self.postgres_url = "postgresql://postgres:12345@localhost/unioncoin"
    
    def connect_sqlite(self):
        try:
            conn = sqlite3.connect(self.sqlite_path)
            return conn
        except Exception as e:
            print(f"SQLite error: {e}")
            return None
    
    def connect_postgres(self):
        try:
            conn = psycopg2.connect(self.postgres_url)
            return conn
        except Exception as e:
            print(f"PostgreSQL error: {e}")
            return None
    
    def get_all_data(self):
        # Try PostgreSQL first, then SQLite
        conn = self.connect_postgres() or self.connect_sqlite()
        if not conn:
            return None
        
        try:
            # Get users
            users_df = pd.read_sql("SELECT * FROM users", conn)
            
            # Get transactions
            transactions_df = pd.read_sql("SELECT * FROM transactions", conn)
            
            conn.close()
            
            return {
                'users': users_df,
                'transactions': transactions_df,
                'stats': {
                    'total_users': len(users_df),
                    'total_transactions': len(transactions_df),
                    'total_balance': users_df['balance'].sum(),
                    'active_users': len(users_df[users_df['balance'] > 0])
                }
            }
        except Exception as e:
            print(f"Error getting data: {e}")
            conn.close()
            return None
    
    def export_to_excel(self):
        data = self.get_all_data()
        if not data:
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"unioncoin_direct_access_{timestamp}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            data['users'].to_excel(writer, sheet_name='Users', index=False)
            data['transactions'].to_excel(writer, sheet_name='Transactions', index=False)
            
            # Summary
            summary_df = pd.DataFrame([
                ['Total Users', data['stats']['total_users']],
                ['Total Transactions', data['stats']['total_transactions']],
                ['Total Balance', data['stats']['total_balance']],
                ['Active Users', data['stats']['active_users']]
            ], columns=['Metric', 'Value'])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        print(f"✅ Data exported to {filename}")
        return filename
    
    def show_data(self):
        data = self.get_all_data()
        if not data:
            return
        
        print("\\n📊 UNIONCOIN DATABASE DIRECT ACCESS")
        print("=" * 50)
        print(f"👥 Total Users: {data['stats']['total_users']}")
        print(f"🔗 Total Transactions: {data['stats']['total_transactions']}")
        print(f"💰 Total Balance: {data['stats']['total_balance']:.2f}")
        print(f"📊 Active Users: {data['stats']['active_users']}")
        
        print("\\n👥 Recent Users:")
        print(data['users'].tail(5)[['username', 'wallet_address', 'balance', 'created_at']].to_string(index=False))
        
        print("\\n🔗 Recent Transactions:")
        print(data['transactions'].tail(5)[['timestamp', 'sender_id', 'receiver_id', 'amount']].to_string(index=False))

if __name__ == "__main__":
    access = DirectDatabaseAccess()
    access.show_data()
    access.export_to_excel()
'''
        
        with open('direct_database_access.py', 'w') as f:
            f.write(db_script)
        
        print("✅ Direct database access script created: direct_database_access.py")
        return True

def main():
    """Main alternative admin menu"""
    print("🔧 UnionCoin Alternative Admin Panel Solutions")
    print("=" * 60)
    
    admin = AlternativeAdminPanel()
    
    while True:
        print("\\n📋 Alternative Admin Options:")
        print("1. 🔧 Create Alternative Endpoints")
        print("2. 📊 Create Standalone Dashboard")
        print("3. 🚀 Start Alternative Servers")
        print("4. 🌐 Open All Admin Panels")
        print("5. 🗄️ Create Direct Database Access")
        print("6. 📋 Show All Solutions")
        print("7. ❌ Exit")
        
        choice = input("\\n👉 Enter your choice (1-7): ").strip()
        
        if choice == "1":
            admin.create_alternative_admin_endpoints()
        elif choice == "2":
            admin.create_standalone_admin_dashboard()
        elif choice == "3":
            admin.start_alternative_servers()
        elif choice == "4":
            admin.open_alternative_panels()
        elif choice == "5":
            admin.create_database_direct_access()
        elif choice == "6":
            admin.show_alternative_solutions()
        elif choice == "7":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
