#!/usr/bin/env python3
"""
UnionCoin Windows Service Manager
Create Windows service to run UnionCoin 24/7
"""

import os
import sys
import subprocess
import time
import json
from datetime import datetime

class WindowsServiceManager:
    def __init__(self):
        self.service_name = "UnionCoin"
        self.service_display_name = "UnionCoin Crypto Platform"
        self.service_description = "UnionCoin - Production-Grade Token Ecosystem with Telegram Bot"
        self.executable_path = os.path.abspath("bot.py")
        self.web_executable_path = os.path.abspath("api.py")
        self.log_path = os.path.abspath("unioncoin_service.log")
        
    def create_service_script(self):
        """Create Windows service installation script"""
        print("🔧 Creating Windows service installation script...")
        
        script_content = f'''@echo off
echo 🚀 UnionCoin Windows Service Installation
echo =====================================
echo.
echo Service Name: {self.service_name}
echo Display Name: {self.service_display_name}
echo Description: {self.service_description}
echo.
echo Installing Windows service...
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Please run this script as Administrator!
    echo.
    echo Right-click the script and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo ✅ Running as Administrator
echo.

REM Create service directory
if not exist "C:\\UnionCoin" mkdir "C:\\UnionCoin"
cd /d C:\\UnionCoin

REM Copy UnionCoin files
echo 📁 Copying UnionCoin files...
xcopy "{os.path.dirname(os.path.abspath(__file__))}\\*" "C:\\UnionCoin\\" /E /Y

REM Install bot service
echo 🤖 Installing bot service...
sc create "{self.service_name}Bot" binPath= "C:\\Python311\\python.exe" start= auto DisplayName="{self.service_name} Bot" depend= Tcpip
sc config "{self.service_name}Bot" start= auto depend= Tcpip obj= "C:\\UnionCoin\\bot.py"

REM Install web service
echo 🌐 Installing web service...
sc create "{self.service_name}Web" binPath= "C:\\Python311\\python.exe" start= auto DisplayName="{self.service_name} Web" depend= Tcpip
sc config "{self.service_name}Web" start= auto depend= Tcpip obj= "C:\\UnionCoin\\api.py"

REM Start services
echo 🚀 Starting services...
sc start "{self.service_name}Bot"
sc start "{self.service_name}Web"

REM Configure services to auto-start
echo ⚙️ Configuring auto-start...
sc config "{self.service_name}Bot" start= auto
sc config "{self.service_name}Web" start= auto

echo.
echo ✅ UnionCoin services installed and started!
echo.
echo 🌐 Web Interface: http://localhost:8000
echo 📊 Admin Panel: http://localhost:8000/api/data?admin=unioncoin_admin_2026
echo 🤖 Telegram Bot: @tokenuchunku12bot
echo.
echo 📋 Service Management:
echo   Start:   sc start {self.service_name}Bot
echo   Start:   sc start {self.service_name}Web
echo   Stop:    sc stop {self.service_name}Bot
echo   Stop:    sc stop {self.service_name}Web
echo   Status:  sc query {self.service_name}Bot
echo   Status:  sc query {self.service_name}Web
echo.
echo 📁 Log files:
echo   Bot: C:\\UnionCoin\\bot_service.log
echo   Web: C:\\UnionCoin\\web_service.log
echo.
echo 🔄 To restart services:
echo   1. Stop both services
echo   2. Update files in C:\\UnionCoin
echo   3. Start both services
echo.
echo 🎉 UnionCoin is now running as Windows services!
echo.
pause
'''
        
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'install_unioncoin_service.bat')
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        print(f"✅ Installation script created: {script_path}")
        return script_path
    
    def create_service_uninstaller(self):
        """Create service uninstallation script"""
        print("🗑️ Creating Windows service uninstallation script...")
        
        uninstall_script = f'''@echo off
echo 🗑️ UnionCoin Windows Service Uninstallation
echo =====================================
echo.

REM Stop services
echo 🛑 Stopping UnionCoin services...
sc stop "{self.service_name}Bot"
sc stop "{self.service_name}Web"

REM Delete services
echo 🗑️ Deleting UnionCoin services...
sc delete "{self.service_name}Bot"
sc delete "{self.service_name}Web"

REM Remove service directory
echo 📁 Removing UnionCoin directory...
if exist "C:\\UnionCoin" rmdir /s /q "C:\\UnionCoin"

echo.
echo ✅ UnionCoin services uninstalled successfully!
echo.
pause
'''
        
        uninstall_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uninstall_unioncoin_service.bat')
        
        with open(uninstall_path, 'w') as f:
            f.write(uninstall_script)
        
        print(f"✅ Uninstallation script created: {uninstall_path}")
        return uninstall_path
    
    def create_service_monitor(self):
        """Create service monitoring script"""
        print("📊 Creating service monitoring script...")
        
        monitor_script = f'''@echo off
echo 📊 UnionCoin Service Monitor
echo ========================
echo.

:check_services
cls
echo 📊 UnionCoin Service Status - %date% %time%
echo =====================================
echo.

REM Check bot service
echo 🤖 Checking bot service...
sc query "{self.service_name}Bot" | find "RUNNING" > nul
if %errorlevel% equ 0 (
    echo ✅ Bot Service: RUNNING
) else (
    echo ❌ Bot Service: STOPPED
)

REM Check web service
echo 🌐 Checking web service...
sc query "{self.service_name}Web" | find "RUNNING" > nul
if %errorlevel% equ 0 (
    echo ✅ Web Service: RUNNING
) else (
    echo ❌ Web Service: STOPPED
)

REM Check if ports are accessible
echo 🔍 Checking port 8000...
netstat -an | find ":8000" > nul
if %errorlevel% equ 0 (
    echo ✅ Port 8000: IN USE
) else (
    echo ❌ Port 8000: NOT IN USE
)

echo.
echo 📋 Service Commands:
echo   Start Bot:   sc start {self.service_name}Bot
echo   Start Web:   sc start {self.service_name}Web
echo   Stop Bot:    sc stop {self.service_name}Bot
echo   Stop Web:    sc stop {self.service_name}Web
echo   Restart Bot: sc stop {self.service_name}Bot && sc start {self.service_name}Bot
echo   Restart Web: sc stop {self.service_name}Web && sc start {self.service_name}Web
echo.
echo 🌐 URLs:
echo   Web Interface: http://localhost:8000
echo   Admin Panel: http://localhost:8000/api/data?admin=unioncoin_admin_2026
echo.
echo 🔄 Auto-refresh in 30 seconds...
timeout /t 30 > nul
goto check_services
'''
        
        monitor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'monitor_unioncoin_service.bat')
        
        with open(monitor_path, 'w') as f:
            f.write(monitor_script)
        
        print(f"✅ Monitor script created: {monitor_path}")
        return monitor_path
    
    def create_startup_shortcut(self):
        """Create startup shortcut"""
        print("🔗 Creating startup shortcut...")
        
        shortcut_script = f'''@echo off
echo 🔗 Creating UnionCoin startup shortcut...
echo.

REM Create shortcut in startup folder
echo 📁 Creating shortcut in startup folder...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('{os.path.abspath('api.py')}'); $Shortcut.TargetPath = 'C:\\Python311\\python.exe'; $Shortcut.Arguments = '{os.path.abspath('api.py')}'; $Shortcut.WorkingDirectory = '{os.path.dirname(os.path.abspath('api.py'))}'; $Shortcut.Save()"
'''
        
        shortcut_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'create_startup_shortcut.bat')
        
        with open(shortcut_path, 'w') as f:
            f.write(shortcut_script)
        
        print(f"✅ Shortcut script created: {shortcut_path}")
        return shortcut_path
    
    def show_service_status(self):
        """Show current service status"""
        print("📊 Checking UnionCoin service status...")
        
        try:
            # Check bot service
            result = subprocess.run(['sc', 'query', f'{self.service_name}Bot'], 
                                  capture_output=True, text=True)
            
            if 'RUNNING' in result.stdout:
                print("✅ Bot Service: RUNNING")
            else:
                print("❌ Bot Service: STOPPED")
            
            # Check web service
            result = subprocess.run(['sc', 'query', f'{self.service_name}Web'], 
                                  capture_output=True, text=True)
            
            if 'RUNNING' in result.stdout:
                print("✅ Web Service: RUNNING")
            else:
                print("❌ Web Service: STOPPED")
                
        except Exception as e:
            print(f"❌ Error checking services: {e}")
    
    def start_services(self):
        """Start UnionCoin services"""
        print("🚀 Starting UnionCoin services...")
        
        try:
            # Start bot service
            subprocess.run(['sc', 'start', f'{self.service_name}Bot'], check=True)
            print("✅ Bot service started")
            
            # Start web service
            subprocess.run(['sc', 'start', f'{self.service_name}Web'], check=True)
            print("✅ Web service started")
            
            print("🌐 Web Interface: http://localhost:8000")
            print("📊 Admin Panel: http://localhost:8000/api/data?admin=unioncoin_admin_2026")
            
        except Exception as e:
            print(f"❌ Error starting services: {e}")
    
    def stop_services(self):
        """Stop UnionCoin services"""
        print("🛑️ Stopping UnionCoin services...")
        
        try:
            # Stop bot service
            subprocess.run(['sc', 'stop', f'{self.service_name}Bot'], check=True)
            print("✅ Bot service stopped")
            
            # Stop web service
            subprocess.run(['sc', 'stop', f'{self.service_name}Web'], check=True)
            print("✅ Web service stopped")
            
        except Exception as e:
            print(f"❌ Error stopping services: {e}")
    
    def restart_services(self):
        """Restart UnionCoin services"""
        print("🔄 Restarting UnionCoin services...")
        
        try:
            self.stop_services()
            time.sleep(3)
            self.start_services()
        except Exception as e:
            print(f"❌ Error restarting services: {e}")
    
    def open_web_interface(self):
        """Open web interface"""
        print("🌐 Opening UnionCoin web interface...")
        
        try:
            import webbrowser
            webbrowser.open("http://localhost:8000")
            print("✅ Web interface opened")
        except Exception as e:
            print(f"❌ Error opening web interface: {e}")
    
    def open_admin_panel(self):
        """Open admin panel"""
        print("📊 Opening UnionCoin admin panel...")
        
        try:
            import webbrowser
            webbrowser.open("http://localhost:8000/api/data?admin=unioncoin_admin_2026")
            print("✅ Admin panel opened")
        except Exception as e:
            print(f"❌ Error opening admin panel: {e}")
    
    def show_service_info(self):
        """Show service information"""
        print("📋 UnionCoin Windows Service Information")
        print("=" * 60)
        
        print(f"\n🏷️ Service Name: {self.service_name}")
        print(f"📝 Display Name: {self.service_display_name}")
        print(f"📄 Description: {self.service_description}")
        print(f"🤖 Bot Executable: {self.executable_path}")
        print(f"🌐 Web Executable: {self.web_executable_path}")
        print(f"📁 Log Path: {self.log_path}")
        
        print("\n🌐 URLs:")
        print("• Web Interface: http://localhost:8000")
        print("• Admin Panel: http://localhost:8000/api/data?admin=unioncoin_admin_2026")
        print("• Health Check: http://localhost:8000/verify")
        
        print("\n📋 Service Commands:")
        print("• Start Bot: sc start UnionCoinBot")
        print("• Start Web: sc start UnionCoinWeb")
        print("• Stop Bot: sc stop UnionCoinBot")
        print("• Stop Web: sc stop UnionCoinWeb")
        print("• Restart Bot: sc stop UnionCoinBot && sc start UnionCoinBot")
        print("• Restart Web: sc stop UnionCoinWeb && sc start UnionCoinWeb")
        
        return True

def main():
    """Main Windows service manager menu"""
    print("🖥️ UnionCoin Windows Service Manager")
    print("=" * 60)
    
    manager = WindowsServiceManager()
    
    while True:
        print("\n📋 Windows Service Options:")
        print("1. 🔧 Create Installation Script")
        print("2. 🔧 Create Uninstallation Script")
        print("3. 📊 Create Monitor Script")
        print("4. 🔗 Create Startup Shortcut")
        print("5. 📊 Show Service Status")
        print("6. 🚀 Start Services")
        print("7. 🛑️ Stop Services")
        print("8. 🔄 Restart Services")
        print("9. 🌐 Open Web Interface")
        print("10. 📊 Open Admin Panel")
        print("11. 📋 Show Service Info")
        print("12. ❌ Exit")
        
        choice = input("\n👉 Enter your choice (1-12): ").strip()
        
        if choice == "1":
            manager.create_service_script()
        elif choice == "2":
            manager.create_service_uninstaller()
        elif choice == "3":
            manager.create_service_monitor()
        elif choice == "4":
            manager.create_startup_shortcut()
        elif choice == "5":
            manager.show_service_status()
        elif choice == "6":
            manager.start_services()
        elif choice == "7":
            manager.stop_services()
        elif choice == "8":
            manager.restart_services()
        elif choice == "9":
            manager.open_web_interface()
        elif choice == "10":
            manager.open_admin_panel()
        elif choice == "11":
            manager.show_service_info()
        elif choice == "12":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
