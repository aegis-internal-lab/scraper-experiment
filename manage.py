#!/usr/bin/env python3
"""
Management script for testing scraper rotation and anti-detection features
"""
import asyncio
import sys
from typing import Dict, Any

from scraper.libs.logger import setup_logger
from scraper.libs.proxy_utils import validate_proxy_configuration
from scraper.libs.rotation_utils import get_rotation_status, proxy_rotator, user_agent_rotator
from scraper.libs.get_news import get_news_list

logger = setup_logger(__name__)


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_status_item(key: str, value: Any):
    """Print a status item with formatting"""
    if isinstance(value, dict):
        print(f"📊 {key}:")
        for sub_key, sub_value in value.items():
            print(f"   - {sub_key}: {sub_value}")
    else:
        print(f"📊 {key}: {value}")


def test_rotation_status():
    """Test and display rotation status"""
    print_section("ROTATION & ANTI-DETECTION STATUS")
    
    try:
        status = get_rotation_status()
        
        for category, details in status.items():
            print_status_item(category.replace("_", " ").title(), details)
            
        print("\n✅ Rotation status retrieved successfully")
        return True
    except Exception as e:
        print(f"❌ Error getting rotation status: {e}")
        return False


def test_proxy_configuration():
    """Test proxy configuration and connectivity"""
    print_section("PROXY CONFIGURATION TEST")
    
    try:
        is_valid, status = validate_proxy_configuration()
        
        for key, value in status.items():
            print_status_item(key.replace("_", " ").title(), value)
        
        if is_valid:
            print("\n✅ Proxy configuration is valid and working")
        else:
            print("\n⚠️ Proxy configuration has issues")
            
        return is_valid
    except Exception as e:
        print(f"❌ Error testing proxy configuration: {e}")
        return False


def test_user_agent_rotation():
    """Test user agent rotation"""
    print_section("USER AGENT ROTATION TEST")
    
    try:
        print("🔄 Testing user agent rotation (5 samples):")
        for i in range(5):
            user_agent = user_agent_rotator.get_next_user_agent()
            print(f"   {i+1}. {user_agent[:80]}...")
        
        print("\n🔄 Testing random user agent selection (3 samples):")
        for i in range(3):
            user_agent = user_agent_rotator.get_random_user_agent()
            print(f"   {i+1}. {user_agent[:80]}...")
            
        print("\n✅ User agent rotation working correctly")
        return True
    except Exception as e:
        print(f"❌ Error testing user agent rotation: {e}")
        return False


def test_proxy_rotation():
    """Test proxy rotation"""
    print_section("PROXY ROTATION TEST")
    
    try:
        proxy_count = proxy_rotator.get_proxy_count()
        rotation_enabled = proxy_rotator.is_rotation_enabled()
        
        print(f"📊 Available proxies: {proxy_count}")
        print(f"📊 Rotation enabled: {rotation_enabled}")
        
        if proxy_count > 0:
            print("\n🔄 Testing proxy rotation (up to 5 samples):")
            for i in range(min(5, proxy_count + 2)):  # Test a few rotations
                proxy = proxy_rotator.get_next_proxy()
                if proxy:
                    proxy_info = ", ".join([f"{k}: {v}" for k, v in proxy.items()])
                    print(f"   {i+1}. {proxy_info}")
                else:
                    print(f"   {i+1}. No proxy returned")
        else:
            print("⚠️ No proxies configured for rotation testing")
            
        print("\n✅ Proxy rotation test completed")
        return True
    except Exception as e:
        print(f"❌ Error testing proxy rotation: {e}")
        return False


async def test_news_fetching():
    """Test news fetching with rotation features"""
    print_section("NEWS FETCHING WITH ROTATION")
    
    try:
        print("🔍 Testing news fetching with rotation features...")
        print("   Keyword: 'technology'")
        print("   Use RCA: False")
        
        result = await get_news_list("technology", use_rca=False)
        
        print(f"📊 Status: {result.status.value}")
        print(f"📊 Message: {result.message}")
        
        if result.status.value == "success":
            print("\n✅ News fetching with rotation working correctly")
            return True
        else:
            print("\n⚠️ News fetching completed with issues")
            return False
    except Exception as e:
        print(f"❌ Error testing news fetching: {e}")
        return False


def print_recommendations():
    """Print recommendations for improvement"""
    print_section("RECOMMENDATIONS")
    
    status = get_rotation_status()
    
    recommendations = []
    
    # Check proxy rotation
    if not status["proxy_rotation"]["enabled"]:
        recommendations.append("🔧 Enable proxy rotation by setting USE_PROXY_ROTATION=true and configuring PROXY_LIST")
    elif status["proxy_rotation"]["available_proxies"] < 3:
        recommendations.append("🔧 Add more proxies to PROXY_LIST for better rotation (recommended: 3+ proxies)")
    
    # Check user agent rotation
    if not status["user_agent_rotation"]["enabled"]:
        recommendations.append("🔧 Enable user agent rotation by setting USE_USER_AGENT_ROTATION=true")
    
    # Rate limiting recommendations
    recommendations.append("🔧 Adjust JITTER_MIN and JITTER_MAX for optimal rate limiting")
    recommendations.append("🔧 Consider increasing INTERVAL_TIME if getting rate limited")
    
    if recommendations:
        for rec in recommendations:
            print(rec)
    else:
        print("✅ Configuration looks good! No specific recommendations.")


async def run_comprehensive_test():
    """Run all tests"""
    print_section("COMPREHENSIVE ROTATION & ANTI-DETECTION TEST")
    print("Testing all rotation and anti-detection features...\n")
    
    results = {}
    
    # Run all tests
    results["rotation_status"] = test_rotation_status()
    results["proxy_config"] = test_proxy_configuration()
    results["user_agent_rotation"] = test_user_agent_rotation()
    results["proxy_rotation"] = test_proxy_rotation()
    results["news_fetching"] = await test_news_fetching()
    
    # Print summary
    print_section("TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    print(f"\n📊 Overall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Your rotation system is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    # Print recommendations
    print_recommendations()


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "status":
            test_rotation_status()
        elif command == "proxy":
            test_proxy_configuration()
        elif command == "user-agent":
            test_user_agent_rotation()
        elif command == "proxy-rotation":
            test_proxy_rotation()
        elif command == "news":
            asyncio.run(test_news_fetching())
        elif command == "all":
            asyncio.run(run_comprehensive_test())
        else:
            print("❌ Unknown command. Available commands:")
            print("   status - Test rotation status")
            print("   proxy - Test proxy configuration")
            print("   user-agent - Test user agent rotation")
            print("   proxy-rotation - Test proxy rotation")
            print("   news - Test news fetching")
            print("   all - Run comprehensive test")
    else:
        # Run comprehensive test by default
        asyncio.run(run_comprehensive_test())


if __name__ == "__main__":
    main()
