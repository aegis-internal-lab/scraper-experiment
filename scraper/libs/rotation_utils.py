"""
Enhanced rotation utilities for proxy and user agent management
"""
import asyncio
import random
import threading
from typing import Dict, List, Optional, Tuple, Any

from scraper.configs.constants import (
    HTTP_PROXY,
    HTTPS_PROXY,
    INTERVAL_TIME,
    JITTER_MAX,
    JITTER_MIN,
    PROXY_LIST,
    USE_PROXY_ROTATION,
    USE_USER_AGENT_ROTATION,
)
from scraper.libs.logger import logger


class UserAgentRotator:
    """Manages rotation of user agents to avoid detection"""
    
    def __init__(self):
        self.user_agents = [
            # Chrome on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            
            # Chrome on macOS
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            
            # Firefox on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            
            # Firefox on macOS
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
            
            # Safari on macOS
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            
            # Edge on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            
            # Chrome on Linux
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            
            # Firefox on Linux
            "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        ]
        self._lock = threading.Lock()
        self.current_index = 0
        
    def get_random_user_agent(self) -> str:
        """Get a random user agent"""
        if not USE_USER_AGENT_ROTATION:
            return self.user_agents[0]  # Use first one as default
            
        return random.choice(self.user_agents)
    
    def get_next_user_agent(self) -> str:
        """Get next user agent in rotation"""
        if not USE_USER_AGENT_ROTATION:
            return self.user_agents[0]  # Use first one as default
            
        with self._lock:
            user_agent = self.user_agents[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.user_agents)
            return user_agent
    
    def get_user_agent_headers(self) -> Dict[str, str]:
        """Get headers with rotated user agent"""
        user_agent = self.get_next_user_agent()
        return {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }


class ProxyRotator:
    """Manages rotation of proxy servers to avoid detection"""
    
    def __init__(self):
        self.proxies = self._parse_proxy_list()
        self._lock = threading.Lock()
        self.current_index = 0
        
        if self.proxies:
            logger.info(f"Initialized ProxyRotator with {len(self.proxies)} proxies")
        else:
            logger.info("No proxies configured for rotation")
    
    def _parse_proxy_list(self) -> List[Dict[str, str]]:
        """Parse proxy list from environment variables"""
        proxies = []
        
        # Add single proxy configuration if available
        if HTTP_PROXY or HTTPS_PROXY:
            proxy_config = {}
            if HTTP_PROXY:
                proxy_config["http"] = HTTP_PROXY
            if HTTPS_PROXY:
                proxy_config["https"] = HTTPS_PROXY
            proxies.append(proxy_config)
        
        # Add proxy list if configured
        if PROXY_LIST:
            proxy_urls = [p.strip() for p in PROXY_LIST.split(",") if p.strip()]
            for proxy_url in proxy_urls:
                # Assume HTTP and HTTPS use the same proxy
                proxy_config = {
                    "http": f"http://{proxy_url}",
                    "https": f"http://{proxy_url}"
                }
                proxies.append(proxy_config)
        
        return proxies
    
    def get_next_proxy(self) -> Optional[Dict[str, str]]:
        """Get next proxy in rotation"""
        if not USE_PROXY_ROTATION or not self.proxies:
            # Return single proxy config if rotation is disabled
            if HTTP_PROXY or HTTPS_PROXY:
                config = {}
                if HTTP_PROXY:
                    config["http"] = HTTP_PROXY
                if HTTPS_PROXY:
                    config["https"] = HTTPS_PROXY
                return config
            return None
        
        with self._lock:
            proxy = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)
            return proxy
    
    def get_random_proxy(self) -> Optional[Dict[str, str]]:
        """Get a random proxy"""
        if not USE_PROXY_ROTATION or not self.proxies:
            if HTTP_PROXY or HTTPS_PROXY:
                config = {}
                if HTTP_PROXY:
                    config["http"] = HTTP_PROXY
                if HTTPS_PROXY:
                    config["https"] = HTTPS_PROXY
                return config
            return None
            
        return random.choice(self.proxies)
    
    def get_proxy_count(self) -> int:
        """Get number of available proxies"""
        return len(self.proxies)
    
    def is_rotation_enabled(self) -> bool:
        """Check if proxy rotation is enabled and available"""
        return USE_PROXY_ROTATION and len(self.proxies) > 1


class RateLimiter:
    """Enhanced rate limiter with jitter and adaptive delays"""
    
    def __init__(self, base_interval: float = 5.0):
        self.base_interval = base_interval
        self.last_request_time = 0
        self._lock = threading.Lock()
    
    async def wait_with_jitter(self) -> None:
        """Wait with base interval plus random jitter"""
        jitter = random.uniform(JITTER_MIN, JITTER_MAX)
        total_delay = self.base_interval + jitter
        
        logger.debug(f"Rate limiting: waiting {total_delay:.2f}s (base: {self.base_interval}s, jitter: {jitter:.2f}s)")
        await asyncio.sleep(total_delay)
    
    async def adaptive_wait(self, request_count: int = 0) -> None:
        """Adaptive waiting based on request count and other factors"""
        # Base jitter
        jitter = random.uniform(JITTER_MIN, JITTER_MAX)
        
        # Adaptive component based on request count
        adaptive_delay = 0
        if request_count > 10:
            adaptive_delay = random.uniform(2, 5)
        elif request_count > 5:
            adaptive_delay = random.uniform(1, 3)
        
        total_delay = self.base_interval + jitter + adaptive_delay
        
        logger.debug(f"Adaptive rate limiting: waiting {total_delay:.2f}s (base: {self.base_interval}s, jitter: {jitter:.2f}s, adaptive: {adaptive_delay:.2f}s)")
        await asyncio.sleep(total_delay)


# Global instances  
user_agent_rotator = UserAgentRotator()
proxy_rotator = ProxyRotator()
rate_limiter = RateLimiter(base_interval=INTERVAL_TIME)


def get_rotation_status() -> Dict[str, Any]:
    """Get status of all rotation utilities"""
    return {
        "user_agent_rotation": {
            "enabled": USE_USER_AGENT_ROTATION,
            "available_agents": len(user_agent_rotator.user_agents),
        },
        "proxy_rotation": {
            "enabled": USE_PROXY_ROTATION,
            "available_proxies": proxy_rotator.get_proxy_count(),
            "rotation_capable": proxy_rotator.is_rotation_enabled(),
        },
        "rate_limiting": {
            "base_interval": rate_limiter.base_interval,
            "jitter_range": f"{JITTER_MIN}-{JITTER_MAX}s",
        }
    }
