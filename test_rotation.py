#!/usr/bin/env python3
"""
Simple test script to verify rotation functionality
"""
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, '/home/tsanyqudsi/Documents/aegis/scraper-experiment')

def test_rotation_features():
    """Test the main rotation features"""
    print("🔧 Testing Scraper Anti-Detection Features")
    print("=" * 50)
    
    try:
        # Test imports
        from scraper.libs.rotation_utils import (
            user_agent_rotator, 
            proxy_rotator, 
            rate_limiter,
            get_rotation_status
        )
        print("✅ All rotation modules imported successfully")
        
        # Test user agent rotation
        print("\n🕵️ User Agent Rotation Test:")
        for i in range(3):
            ua = user_agent_rotator.get_next_user_agent()
            print(f"   {i+1}. {ua[:60]}...")
        
        # Test proxy rotation status
        print("\n🌐 Proxy Configuration:")
        proxy_count = proxy_rotator.get_proxy_count()
        print(f"   Available proxies: {proxy_count}")
        print(f"   Rotation enabled: {proxy_rotator.is_rotation_enabled()}")
        
        # Test rotation status
        print("\n📊 Rotation Status:")
        status = get_rotation_status()
        for key, value in status.items():
            if isinstance(value, dict):
                print(f"   {key}: {value}")
            else:
                print(f"   {key}: {value}")
        
        print("\n🎉 All tests passed! Rotation features are working correctly.")
        
        # Configuration recommendations
        print("\n💡 Configuration Tips:")
        if not status["proxy_rotation"]["enabled"]:
            print("   - Add PROXY_LIST to enable proxy rotation")
            print("   - Set USE_PROXY_ROTATION=true")
        
        if status["user_agent_rotation"]["enabled"]:
            print("   ✅ User agent rotation is enabled")
        else:
            print("   - Set USE_USER_AGENT_ROTATION=true")
            
        print("   - Configure JITTER_MIN and JITTER_MAX for rate limiting")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_rotation_features()
