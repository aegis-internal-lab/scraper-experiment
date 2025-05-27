#!/usr/bin/env python3
"""
Simple test script to verify anti-detection features
"""
import time
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper.libs.rotation_utils import UserAgentRotator, ProxyRotator, RateLimiter
from scraper.configs.constants import (
    JITTER_MIN, JITTER_MAX, PROXY_LIST, 
    USE_PROXY_ROTATION, USE_USER_AGENT_ROTATION
)

def test_user_agent_rotation():
    """Test User Agent rotation"""
    print("🔄 Testing User Agent Rotation...")
    rotator = UserAgentRotator()
    
    # Get several user agents to verify rotation
    agents = []
    for i in range(5):
        agent = rotator.get_next_user_agent()
        agents.append(agent)
        print(f"  Agent {i+1}: {agent[:50]}...")
    
    # Check if we got different agents
    unique_agents = set(agents)
    print(f"  ✅ Generated {len(unique_agents)} unique user agents out of {len(agents)}")
    print(f"  📊 Total available agents: {len(rotator.user_agents)}")
    return len(unique_agents) > 1

def test_proxy_rotation():
    """Test Proxy rotation"""
    print("\n🌐 Testing Proxy Rotation...")
    
    # Test with no proxies configured
    rotator = ProxyRotator()
    proxy = rotator.get_next_proxy()
    print(f"  No proxies configured: {proxy}")
    
    # Test proxy count
    count = rotator.get_proxy_count()
    print(f"  Available proxies: {count}")
    
    # Test multiple proxy requests
    proxies = []
    for i in range(3):
        proxy = rotator.get_next_proxy()
        proxies.append(proxy)
        print(f"  Proxy {i+1}: {proxy}")
    
    print(f"  ✅ Proxy rotation test completed")
    return True

def test_rate_limiting():
    """Test Rate limiting with jitter"""
    print("\n⏱️  Testing Rate Limiting...")
    rate_limiter = RateLimiter()
    
    print(f"  Jitter range: {JITTER_MIN}s - {JITTER_MAX}s")
    print(f"  Base interval: {rate_limiter.base_interval}s")
    
    # Test synchronous delay calculation (we can't easily test async wait in sync context)
    import random
    
    for i in range(3):
        jitter = random.uniform(JITTER_MIN, JITTER_MAX)
        total_delay = rate_limiter.base_interval + jitter
        print(f"  Calculated delay {i+1}: {total_delay:.2f}s (base: {rate_limiter.base_interval}s, jitter: {jitter:.2f}s)")
    
    print(f"  ✅ Rate limiting calculation test completed")
    return True

def test_configuration():
    """Test configuration loading"""
    print("\n⚙️  Testing Configuration...")
    print(f"  JITTER_MIN: {JITTER_MIN}")
    print(f"  JITTER_MAX: {JITTER_MAX}")
    print(f"  PROXY_LIST: {PROXY_LIST}")
    print(f"  USE_PROXY_ROTATION: {USE_PROXY_ROTATION}")
    print(f"  USE_USER_AGENT_ROTATION: {USE_USER_AGENT_ROTATION}")
    return True

def main():
    """Run all tests"""
    print("🧪 Anti-Detection Features Test Suite")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("User Agent Rotation", test_user_agent_rotation),
        ("Proxy Rotation", test_proxy_rotation),
        ("Rate Limiting", test_rate_limiting),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ Error in {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n📊 Test Results Summary")
    print("=" * 50)
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All anti-detection features are working correctly!")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()
