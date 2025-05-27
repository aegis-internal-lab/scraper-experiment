"""
Enhanced proxy validation utility for the scraper application with rotation support
"""
import urllib.request
from typing import Dict, Optional, Tuple

from scraper.configs.constants import HTTP_PROXY, HTTPS_PROXY
from scraper.libs.logger import setup_logger
from scraper.libs.rotation_utils import get_rotation_status, proxy_rotator, user_agent_rotator

logger = setup_logger(__name__)


def validate_proxy_configuration() -> Tuple[bool, Dict[str, str]]:
    """
    Validate proxy configuration by testing connectivity with rotation support
    
    Returns:
        Tuple of (is_valid, status_dict)
    """
    status = {
        "http_proxy": "Not configured",
        "https_proxy": "Not configured",
        "proxy_rotation": "Disabled",
        "user_agent_rotation": "Disabled",
        "connectivity": "Unknown"
    }
    
    # Get rotation status
    rotation_status = get_rotation_status()
    
    # Update status with rotation info
    if rotation_status["proxy_rotation"]["enabled"]:
        status["proxy_rotation"] = f"Enabled ({rotation_status['proxy_rotation']['available_proxies']} proxies)"
    
    if rotation_status["user_agent_rotation"]["enabled"]:
        status["user_agent_rotation"] = f"Enabled ({rotation_status['user_agent_rotation']['available_agents']} agents)"
    
    # Check basic proxy configuration
    if HTTP_PROXY:
        status["http_proxy"] = f"Configured: {HTTP_PROXY}"
        logger.info(f"HTTP proxy configured: {HTTP_PROXY}")
    
    if HTTPS_PROXY:
        status["https_proxy"] = f"Configured: {HTTPS_PROXY}"
        logger.info(f"HTTPS proxy configured: {HTTPS_PROXY}")
    
    # Test connectivity through proxy with rotation
    proxy_config = proxy_rotator.get_next_proxy()
    if proxy_config:
        try:
            # Get rotated user agent headers
            headers = user_agent_rotator.get_user_agent_headers()
            
            proxy_handler = urllib.request.ProxyHandler(proxy_config)
            opener = urllib.request.build_opener(proxy_handler)
            
            # Create request with rotated user agent
            request = urllib.request.Request('http://httpbin.org/ip')
            for key, value in headers.items():
                request.add_header(key, value)
            
            # Test with enhanced request
            response = opener.open(request, timeout=10)
            if response.getcode() == 200:
                status["connectivity"] = "✅ Proxy connection successful with rotation"
                logger.info("Enhanced proxy connectivity test passed with rotation")
                return True, status
            else:
                status["connectivity"] = f"❌ Proxy returned status: {response.getcode()}"
                logger.warning(f"Proxy test failed with status: {response.getcode()}")
                return False, status
                
        except Exception as e:
            status["connectivity"] = f"❌ Proxy connection failed: {str(e)}"
            logger.error(f"Enhanced proxy connectivity test failed: {e}")
            return False, status
    else:
        status["connectivity"] = "⚠️ No proxy configured - direct connection"
        logger.info("No proxy configured, using direct connection")
        return True, status


def get_proxy_info() -> Dict[str, Optional[str]]:
    """
    Get current proxy configuration information
    
    Returns:
        Dictionary with proxy configuration details
    """
    return {
        "http_proxy": HTTP_PROXY,
        "https_proxy": HTTPS_PROXY,
        "status": "configured" if (HTTP_PROXY or HTTPS_PROXY) else "not_configured"
    }


if __name__ == "__main__":
    print("🔧 Validating Proxy Configuration")
    print("=" * 40)
    
    is_valid, status = validate_proxy_configuration()
    
    for key, value in status.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    if is_valid:
        print("\n✅ Proxy configuration is valid!")
    else:
        print("\n❌ Proxy configuration issues detected!")
