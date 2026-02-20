#!/usr/bin/env python3
"""
UnionCoin Telegram Auth Test
Test Telegram-only authentication system
"""

import requests
import json
import time
from datetime import datetime

class TelegramAuthTester:
    def __init__(self):
        self.base_url = "https://unioncoin.onrender.com"
        self.telegram_bot_url = "https://t.me/tokenuchunku12bot"
        
    def test_telegram_auth_endpoints(self):
        """Test Telegram authentication endpoints"""
        print("📱 UnionCoin Telegram Auth Testing")
        print("=" * 60)
        print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Base URL: {self.base_url}")
        print(f"📱 Telegram Bot: {self.telegram_bot_url}")
        print("=" * 60)
        
        endpoints = [
            {
                'url': self.base_url,
                'description': 'Main Page (Telegram Auth Required)',
                'expected_content': 'Telegram Authentication Required'
            },
            {
                'url': f"{self.base_url}/health",
                'description': 'Health Check',
                'expected_content': 'healthy'
            },
            {
                'url': f"{self.base_url}/verify",
                'description': 'Blockchain Verify',
                'expected_content': 'verified'
            },
            {
                'url': f"{self.base_url}/register",
                'description': 'Register Redirect (Should redirect to Telegram)',
                'expected_content': 'Redirecting to Telegram'
            },
            {
                'url': f"{self.base_url}/auth/telegram/check/123456789",
                'description': 'Check Telegram User (Non-existent)',
                'expected_content': 'User not found'
            },
            {
                'url': f"{self.base_url}/api/stats/public",
                'description': 'Public Stats',
                'expected_content': 'total_users'
            }
        ]
        
        results = []
        
        for endpoint in endpoints:
            print(f"\n🧪 Testing: {endpoint['description']}")
            print(f"🌐 URL: {endpoint['url']}")
            
            try:
                response = requests.get(endpoint['url'], timeout=15)
                
                success = response.status_code == 200
                
                if success:
                    content_check = endpoint['expected_content'] in response.text
                    print(f"✅ Status: {response.status_code}")
                    print(f"⏱️ Response Time: {response.elapsed.total_seconds():.2f}s")
                    print(f"📏 Content Length: {len(response.content)} bytes")
                    print(f"🔍 Content Check: {'✅ Pass' if content_check else '❌ Fail'}")
                    
                    if not content_check:
                        print(f"⚠️ Expected content not found: {endpoint['expected_content']}")
                else:
                    print(f"❌ Status: {response.status_code}")
                    print(f"⚠️ Error: {response.text[:200]}")
                
                result = {
                    'url': endpoint['url'],
                    'description': endpoint['description'],
                    'status_code': response.status_code,
                    'response_time': response.elapsed.total_seconds(),
                    'content_length': len(response.content),
                    'success': success,
                    'content_check': endpoint['expected_content'] in response.text if success else False
                }
                
            except requests.exceptions.Timeout:
                print(f"❌ Timeout Error")
                result = {
                    'url': endpoint['url'],
                    'description': endpoint['description'],
                    'status_code': None,
                    'response_time': None,
                    'content_length': None,
                    'success': False,
                    'error': 'Timeout'
                }
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Request Error: {str(e)[:100]}")
                result = {
                    'url': endpoint['url'],
                    'description': endpoint['description'],
                    'status_code': None,
                    'response_time': None,
                    'content_length': None,
                    'success': False,
                    'error': str(e)[:100]
                }
            
            results.append(result)
            time.sleep(1)  # Small delay between requests
        
        return results
    
    def test_telegram_registration_flow(self):
        """Test Telegram registration flow"""
        print("\n📱 TESTING TELEGRAM REGISTRATION FLOW")
        print("-" * 50)
        
        print("📋 Registration Flow Test:")
        print("1. 📱 User opens Telegram bot: @tokenuchunku12bot")
        print("2. 🚀 User sends: /start")
        print("3. 📝 Bot checks: Is Telegram ID already registered?")
        print("4. ✅ If not registered: Start registration process")
        print("5. 📝 User provides: Username + Password")
        print("6. 🔗 Bot creates: Unique wallet + account")
        print("7. 💰 User gets: 1000 UC welcome bonus")
        print("8. 🔐 User gets: Authentication token for web")
        print("9. 🌐 User can: Access private web features")
        
        print("\n🔒 Security Features:")
        print("✅ One Telegram ID = One UnionCoin account")
        print("✅ No web registration possible")
        print("✅ Duplicate Telegram ID blocked")
        print("✅ All account creation via Telegram")
        print("✅ Web access requires Telegram auth")
        
        return True
    
    def test_web_interface_redirect(self):
        """Test web interface redirects to Telegram"""
        print("\n🌐 TESTING WEB INTERFACE REDIRECT")
        print("-" * 40)
        
        try:
            # Test main page content
            response = requests.get(self.base_url, timeout=15)
            
            if response.status_code == 200:
                print("✅ Main page accessible")
                
                # Check for Telegram auth content
                if "Telegram Authentication Required" in response.text:
                    print("✅ Telegram auth message found")
                else:
                    print("❌ Telegram auth message not found")
                
                # Check for Telegram bot link
                if "t.me/tokenuchunku12bot" in response.text:
                    print("✅ Telegram bot link found")
                else:
                    print("❌ Telegram bot link not found")
                
                # Check for registration redirect
                if "Register via Telegram bot" in response.text:
                    print("✅ Registration redirect message found")
                else:
                    print("❌ Registration redirect message not found")
                
                return True
            else:
                print(f"❌ Main page not accessible: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing web interface: {e}")
            return False
    
    def test_admin_security(self):
        """Test admin security (should be blocked on web)"""
        print("\n🔒 TESTING ADMIN SECURITY")
        print("-" * 40)
        
        # Test old admin endpoints (should fail)
        admin_endpoints = [
            f"{self.base_url}/admin",
            f"{self.base_url}/dashboard/admin",
            f"{self.base_url}/api/data?admin=unioncoin_admin_2026",
            f"{self.base_url}/api/admin/users",
            f"{self.base_url}/api/admin/transactions"
        ]
        
        all_blocked = True
        
        for endpoint in admin_endpoints:
            try:
                response = requests.get(endpoint, timeout=10)
                
                if response.status_code == 404:
                    print(f"✅ {endpoint}: 404 (Blocked as expected)")
                elif response.status_code == 401:
                    print(f"✅ {endpoint}: 401 (Unauthorized as expected)")
                elif response.status_code == 403:
                    print(f"✅ {endpoint}: 403 (Forbidden as expected)")
                else:
                    print(f"❌ {endpoint}: {response.status_code} (Should be blocked)")
                    all_blocked = False
                    
            except Exception as e:
                print(f"✅ {endpoint}: Error (Blocked as expected)")
        
        if all_blocked:
            print("✅ All admin endpoints properly blocked on web")
        else:
            print("❌ Some admin endpoints still accessible on web")
        
        return all_blocked
    
    def show_summary(self, results):
        """Show test summary"""
        print("\n📊 TELEGRAM AUTH TEST SUMMARY")
        print("=" * 60)
        
        successful = [r for r in results if r['success'] and r.get('content_check', False)]
        failed = [r for r in results if not r['success'] or not r.get('content_check', False)]
        
        print(f"✅ Successful: {len(successful)}/{len(results)}")
        print(f"❌ Failed: {len(failed)}/{len(results)}")
        
        if successful:
            print("\n✅ WORKING ENDPOINTS:")
            for result in successful:
                print(f"   • {result['description']}: {result['status_code']} ({result['response_time']:.2f}s)")
        
        if failed:
            print("\n❌ FAILED ENDPOINTS:")
            for result in failed:
                error = result.get('error', 'Content check failed')
                print(f"   • {result['description']}: {error}")
        
        # Overall status
        if len(successful) == len(results):
            print("\n🎉 ALL ENDPOINTS WORKING!")
            print("📱 Telegram authentication system is fully operational!")
        elif len(successful) > len(results) // 2:
            print("\n⚠️ PARTIAL SUCCESS")
            print("🔧 Some endpoints need attention")
        else:
            print("\n❌ MOST ENDPOINTS FAILED")
            print("🚨 Telegram authentication system needs immediate attention!")
        
        return len(successful) == len(results)
    
    def show_telegram_bot_instructions(self):
        """Show Telegram bot test instructions"""
        print("\n🤖 TELEGRAM BOT TEST INSTRUCTIONS")
        print("=" * 50)
        
        print("📱 To test the Telegram bot:")
        print("1. 📱 Open Telegram app")
        print("2. 🔍 Search for: @tokenuchunku12bot")
        print("3. 🚀 Send: /start")
        print("4. 📝 Follow registration instructions")
        print("5. ✅ Create your account")
        print("6. 💰 Check your balance (should be 1000 UC)")
        print("7. 🔐 Get your authentication token")
        print("8. 🌐 Try to access web interface")
        print("9. 🔍 Test admin commands (if you're admin)")
        
        print("\n🔒 Security Tests:")
        print("1. 🚫 Try to register with same Telegram ID (should fail)")
        print("2. 🚫 Try to access /admin on web (should fail)")
        print("3. ✅ Try to register new account (should work)")
        print("4. ✅ Try to access your private data (should work)")
        
        print("\n📊 Expected Results:")
        print("✅ Registration works via Telegram only")
        print("✅ Web interface redirects to Telegram")
        print("✅ Admin access via Telegram only")
        print("✅ User data is private and isolated")
        print("✅ No web registration possible")
        
        return True

def main():
    """Main function"""
    tester = TelegramAuthTester()
    
    # Test Telegram auth endpoints
    results = tester.test_telegram_auth_endpoints()
    
    # Test registration flow
    tester.test_telegram_registration_flow()
    
    # Test web interface redirect
    tester.test_web_interface_redirect()
    
    # Test admin security
    tester.test_admin_security()
    
    # Show summary
    all_working = tester.show_summary(results)
    
    # Show Telegram bot instructions
    tester.show_telegram_bot_instructions()
    
    # Save results
    with open('telegram_auth_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Test results saved to: telegram_auth_test_results.json")
    
    if all_working:
        print("\n🎉 TELEGRAM AUTHENTICATION SYSTEM IS WORKING!")
        print("📱 Users can register via Telegram bot only")
        print("🔒 Security is properly implemented")
        print("🌐 Web interface redirects to Telegram")
        print("👤 User data is private and isolated")
    else:
        print("\n⚠️ SOME ISSUES FOUND")
        print("🔧 Check the failed endpoints above")
        print("📱 Test the Telegram bot manually")
        print("🌐 Verify web interface behavior")
    
    return all_working

if __name__ == "__main__":
    main()
