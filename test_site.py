#!/usr/bin/env python3
"""
UnionCoin Site Tester
Test all UnionCoin endpoints and services
"""

import requests
import json
import time
from datetime import datetime

class UnionCoinSiteTester:
    def __init__(self):
        self.base_url = "https://unioncoin.onrender.com"
        self.admin_password = "unioncoin_admin_2026"
        
    def test_endpoint(self, url, description, timeout=10):
        """Test single endpoint"""
        try:
            response = requests.get(url, timeout=timeout)
            return {
                'url': url,
                'description': description,
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'content_length': len(response.content),
                'success': response.status_code == 200
            }
        except requests.exceptions.Timeout:
            return {
                'url': url,
                'description': description,
                'status_code': None,
                'response_time': None,
                'content_length': None,
                'success': False,
                'error': 'Timeout'
            }
        except requests.exceptions.RequestException as e:
            return {
                'url': url,
                'description': description,
                'status_code': None,
                'response_time': None,
                'content_length': None,
                'success': False,
                'error': str(e)
            }
    
    def test_all_endpoints(self):
        """Test all UnionCoin endpoints"""
        print("🚀 UnionCoin Site Testing")
        print("=" * 60)
        print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Base URL: {self.base_url}")
        print("=" * 60)
        
        endpoints = [
            {
                'url': self.base_url,
                'description': 'Main Page'
            },
            {
                'url': f"{self.base_url}/health",
                'description': 'Health Check'
            },
            {
                'url': f"{self.base_url}/verify",
                'description': 'Blockchain Verify'
            },
            {
                'url': f"{self.base_url}/api/data?admin={self.admin_password}",
                'description': 'Admin Panel'
            },
            {
                'url': f"{self.base_url}/api/stats",
                'description': 'API Stats'
            },
            {
                'url': f"{self.base_url}/api/user-accounts",
                'description': 'API User Accounts'
            }
        ]
        
        results = []
        
        for endpoint in endpoints:
            print(f"\n🧪 Testing: {endpoint['description']}")
            print(f"🌐 URL: {endpoint['url']}")
            
            result = self.test_endpoint(endpoint['url'], endpoint['description'])
            results.append(result)
            
            if result['success']:
                print(f"✅ Status: {result['status_code']}")
                print(f"⏱️ Response Time: {result['response_time']:.2f}s")
                print(f"📏 Content Length: {result['content_length']} bytes")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
            
            time.sleep(1)  # Small delay between requests
        
        return results
    
    def show_summary(self, results):
        """Show test summary"""
        print("\n📊 TEST SUMMARY")
        print("=" * 60)
        
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        print(f"✅ Successful: {len(successful)}/{len(results)}")
        print(f"❌ Failed: {len(failed)}/{len(results)}")
        
        if successful:
            print("\n✅ WORKING ENDPOINTS:")
            for result in successful:
                print(f"   • {result['description']}: {result['status_code']} ({result['response_time']:.2f}s)")
        
        if failed:
            print("\n❌ FAILED ENDPOINTS:")
            for result in failed:
                error = result.get('error', 'Unknown error')
                print(f"   • {result['description']}: {error}")
        
        # Overall status
        if len(successful) == len(results):
            print("\n🎉 ALL ENDPOINTS WORKING!")
            print("🚀 UnionCoin is fully operational!")
        elif len(successful) > 0:
            print("\n⚠️ PARTIAL SUCCESS")
            print("🔧 Some endpoints need attention")
        else:
            print("\n❌ ALL ENDPOINTS FAILED")
            print("🚨 UnionCoin needs immediate attention!")
        
        return len(successful) == len(results)
    
    def test_bot_status(self):
        """Test Telegram bot status"""
        print("\n🤖 TESTING TELEGRAM BOT")
        print("=" * 40)
        
        bot_username = "@tokenuchunku12bot"
        print(f"📱 Bot Username: {bot_username}")
        print("🧪 To test bot:")
        print("   1. Open Telegram")
        print("   2. Search for: @tokenuchunku12bot")
        print("   3. Send /start command")
        print("   4. Check if bot responds")
        print("   5. Try /admin command")
        print("   6. Check if admin panel works")
        
        return True
    
    def show_next_steps(self, all_working):
        """Show next steps based on test results"""
        print("\n🎯 NEXT STEPS")
        print("=" * 40)
        
        if all_working:
            print("🎉 CONGRATULATIONS!")
            print("✅ UnionCoin is fully operational!")
            print("🌐 All endpoints are working")
            print("🤖 Bot should be working")
            print("📊 Admin panel is accessible")
            print("\n📋 What you can do:")
            print("   • Use the web interface")
            print("   • Manage users via admin panel")
            print("   • Monitor transactions")
            print("   • Use Telegram bot")
            print("   • Deploy to production")
        else:
            print("🔧 TROUBLESHOOTING NEEDED")
            print("❌ Some endpoints are not working")
            print("\n📋 What to check:")
            print("   • Environment variables")
            print("   • Database connection")
            print("   • Service logs on Render.com")
            print("   • Build logs")
            print("   • Service status")
            print("\n🔧 Quick fixes:")
            print("   • Restart services on Render.com")
            print("   • Check environment variables")
            print("   • Verify database connection")
            print("   • Check build logs")
        
        return True

def main():
    """Main function"""
    tester = UnionCoinSiteTester()
    
    # Test all endpoints
    results = tester.test_all_endpoints()
    
    # Show summary
    all_working = tester.show_summary(results)
    
    # Test bot status
    tester.test_bot_status()
    
    # Show next steps
    tester.show_next_steps(all_working)
    
    # Save results
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Test results saved to: test_results.json")
    return all_working

if __name__ == "__main__":
    main()
