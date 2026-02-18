#!/usr/bin/env python3
"""
UnionCoin Server Mode - Turn your computer into a production server
"""

import subprocess
import time
import os
import sys
import signal
import requests
from datetime import datetime
import sqlite3
import pandas as pd

class UnionCoinServer:
    def __init__(self):
        self.web_process = None
        self.bot_process = None
        self.running = True
        
    def start_services(self):
        """Start web and bot services"""
        print("🚀 Starting UnionCoin services...")
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Start web server
            self.web_process = subprocess.Popen(
                [sys.executable, 'api.py'], 
                cwd=os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Start bot
            self.bot_process = subprocess.Popen(
                [sys.executable, 'bot.py'], 
                cwd=os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            print("✅ Services started successfully!")
            print("🌐 Web Interface: http://localhost:8000")
            print("📊 Admin Panel: http://localhost:8000/api/data?admin=unioncoin_admin_2026")
            print("🤖 Telegram Bot: @tokenuchunku12bot")
            print("=" * 50)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start services: {e}")
            return False
    
    def monitor_services(self):
        """Monitor and restart services if needed"""
        print("👀 Starting service monitoring...")
        print("🔄 Auto-restart enabled (checks every 30 seconds)")
        
        while self.running:
            try:
                # Check web server
                if self.web_process and self.web_process.poll() is not None:
                    print("🔄 Web server stopped, restarting...")
                    self.web_process = subprocess.Popen(
                        [sys.executable, 'api.py'], 
                        cwd=os.getcwd(),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    print("✅ Web server restarted")
                
                # Check bot
                if self.bot_process and self.bot_process.poll() is not None:
                    print("🔄 Bot stopped, restarting...")
                    self.bot_process = subprocess.Popen(
                        [sys.executable, 'bot.py'], 
                        cwd=os.getcwd(),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    print("✅ Bot restarted")
                
                # Check if services are responsive
                try:
                    response = requests.get('http://localhost:8000', timeout=5)
                    if response.status_code == 200:
                        print("✅ Services responsive")
                    else:
                        print("⚠️ Services not responding properly")
                except:
                    print("⚠️ Cannot reach web service")
                
                time.sleep(30)  # Check every 30 seconds
                
            except KeyboardInterrupt:
                print("\n🛑 Shutdown requested by user")
                self.stop_services()
                break
            except Exception as e:
                print(f"⚠️ Monitor error: {e}")
                time.sleep(30)
    
    def stop_services(self):
        """Stop all services"""
        print("🛑 Stopping UnionCoin services...")
        self.running = False
        
        if self.web_process:
            try:
                self.web_process.terminate()
                self.web_process.wait(timeout=10)
                print("✅ Web server stopped")
            except:
                try:
                    self.web_process.kill()
                    print("🔨 Web server force killed")
                except:
                    pass
        
        if self.bot_process:
            try:
                self.bot_process.terminate()
                self.bot_process.wait(timeout=10)
                print("✅ Bot stopped")
            except:
                try:
                    self.bot_process.kill()
                    print("🔨 Bot force killed")
                except:
                    pass
    
    def create_backup(self):
        """Create automatic backup"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Create backup directory
            os.makedirs('server_backups', exist_ok=True)
            
            # Connect to database
            conn = sqlite3.connect('unioncoin.db')
            
            # Export data
            users_df = pd.read_sql_query("SELECT * FROM users", conn)
            transactions_df = pd.read_sql_query("""
                SELECT t.*, s.username as sender_name, r.username as receiver_name
                FROM transactions t
                LEFT JOIN users s ON t.sender_id = s.id
                LEFT JOIN users r ON t.receiver_id = r.id
                ORDER BY t.id DESC
            """, conn)
            
            # Save to Excel
            users_file = f"server_backups/users_{timestamp}.xlsx"
            transactions_file = f"server_backups/transactions_{timestamp}.xlsx"
            
            users_df.to_excel(users_file, index=False, engine='openpyxl')
            transactions_df.to_excel(transactions_file, index=False, engine='openpyxl')
            
            conn.close()
            
            print(f"📊 Auto-backup created: {timestamp}")
            return True
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            print(f"\n📡 Received signal {signum}")
            self.stop_services()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def show_status(self):
        """Show current server status"""
        print("\n📊 Server Status:")
        print("=" * 30)
        
        try:
            # Check web server
            if self.web_process:
                if self.web_process.poll() is None:
                    print("🌐 Web Server: ✅ Running")
                    print(f"   PID: {self.web_process.pid}")
                else:
                    print("🌐 Web Server: ❌ Stopped")
                    print(f"   Exit Code: {self.web_process.poll()}")
            
            # Check bot
            if self.bot_process:
                if self.bot_process.poll() is None:
                    print("🤖 Telegram Bot: ✅ Running")
                    print(f"   PID: {self.bot_process.pid}")
                else:
                    print("🤖 Telegram Bot: ❌ Stopped")
                    print(f"   Exit Code: {self.bot_process.poll()}")
            
            # Check service availability
            try:
                response = requests.get('http://localhost:8000/verify', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    print("🔗 Blockchain: ✅ Valid")
                    print(f"   Valid: {data.get('blockchain_valid', 'Unknown')}")
                else:
                    print("🔗 Service: ⚠️ Not responding")
            except:
                print("🔗 Service: ❌ Unreachable")
            
        except Exception as e:
            print(f"❌ Status check failed: {e}")
        
        print("=" * 30)
    
    def run_interactive_mode(self):
        """Run in interactive mode with commands"""
        print("\n🎮 Interactive Server Mode")
        print("Type 'help' for commands, 'quit' to exit")
        
        while self.running:
            try:
                command = input("\n👉 server> ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    self.stop_services()
                    break
                elif command == 'help':
                    self.show_help()
                elif command == 'status':
                    self.show_status()
                elif command == 'restart':
                    print("🔄 Restarting services...")
                    self.stop_services()
                    time.sleep(2)
                    self.start_services()
                elif command == 'backup':
                    self.create_backup()
                elif command == 'logs':
                    self.show_logs()
                else:
                    print(f"❓ Unknown command: {command}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n🛑 Exiting...")
                self.stop_services()
                break
            except Exception as e:
                print(f"❌ Command error: {e}")
    
    def show_help(self):
        """Show available commands"""
        print("\n📖 Available Commands:")
        print("  help     - Show this help message")
        print("  status   - Show service status")
        print("  restart  - Restart all services")
        print("  backup   - Create database backup")
        print("  logs     - Show recent logs")
        print("  quit     - Stop server and exit")
        print("\n🌐 Access URLs:")
        print("  Web: http://localhost:8000")
        print("  Admin: http://localhost:8000/api/data?admin=unioncoin_admin_2026")
    
    def show_logs(self):
        """Show recent service logs"""
        print("\n📋 Recent Service Activity:")
        print("=" * 30)
        
        try:
            # Read log files if they exist
            if os.path.exists('logs/unioncoin.log'):
                with open('logs/unioncoin.log', 'r') as f:
                    lines = f.readlines()
                    for line in lines[-10:]:  # Last 10 lines
                        print(f"   {line.strip()}")
            else:
                print("   No log files found")
                
        except Exception as e:
            print(f"   Error reading logs: {e}")
        
        print("=" * 30)
    
    def run(self):
        """Main server run method"""
        print("🖥️ UnionCoin Server Mode")
        print("=" * 50)
        print("🎯 Turning your computer into a production server")
        print("📅 Started:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("=" * 50)
        
        # Setup signal handlers
        self.setup_signal_handlers()
        
        # Start services
        if self.start_services():
                # Start monitoring
                self.monitor_services()
        
        print("\n👋 Server stopped")

def main():
    """Main entry point"""
    server = UnionCoinServer()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        # Interactive mode
        server.run_interactive_mode()
    else:
        # Normal mode with monitoring
        server.run()

if __name__ == "__main__":
    main()
