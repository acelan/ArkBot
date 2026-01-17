from datetime import datetime, timedelta
from typing import Any, Optional


class StockDataCache:
    """
    Simple TTL cache for stock data to minimize API calls
    """
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}  # {cache_key: (data, timestamp)}
        self.ttl = timedelta(seconds=ttl_seconds)

    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                return data
            else:
                # Expired, remove from cache
                del self.cache[key]
        return None

    def set(self, key: str, data: Any):
        """Store value with current timestamp"""
        self.cache[key] = (data, datetime.now())

    def clear(self):
        """Clear all cached data"""
        self.cache.clear()
