"""
Simple, self-contained caching system
"""
import time
import hashlib
import json
from typing import Any, Optional, Dict
from datetime import datetime, timedelta

class SimpleCache:
    """Production-ready cache without external dependencies"""
    
    def __init__(self, default_ttl: int = 300):
        self.cache = {}
        self.default_ttl = default_ttl
        self.stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0
        }
    
    def _generate_key(self, key: str) -> str:
        """Generate a cache key"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set a value in cache with optional TTL"""
        cache_key = self._generate_key(key)
        ttl = ttl if ttl is not None else self.default_ttl
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        self.cache[cache_key] = {
            "key": key,
            "value": value,
            "expires_at": expires_at.isoformat(),
            "created_at": datetime.now().isoformat()
        }
        self.stats["sets"] += 1
        return True
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache"""
        cache_key = self._generate_key(key)
        
        if cache_key not in self.cache:
            self.stats["misses"] += 1
            return None
        
        cache_entry = self.cache[cache_key]
        expires_at = datetime.fromisoformat(cache_entry["expires_at"])
        
        # Check if expired
        if datetime.now() > expires_at:
            del self.cache[cache_key]
            self.stats["misses"] += 1
            return None
        
        self.stats["hits"] += 1
        return cache_entry["value"]
    
    def delete(self, key: str) -> bool:
        """Delete a value from cache"""
        cache_key = self._generate_key(key)
        if cache_key in self.cache:
            del self.cache[cache_key]
            self.stats["deletes"] += 1
            return True
        return False
    
    def clear(self) -> bool:
        """Clear all cache entries"""
        self.cache.clear()
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "sets": self.stats["sets"],
            "deletes": self.stats["deletes"],
            "hit_rate_percent": round(hit_rate, 2),
            "total_entries": len(self.cache),
            "timestamp": datetime.now().isoformat()
        }
    
    def cleanup_expired(self) -> int:
        """Remove expired entries from cache"""
        current_time = datetime.now()
        expired_keys = []
        
        for cache_key, cache_entry in self.cache.items():
            expires_at = datetime.fromisoformat(cache_entry["expires_at"])
            if current_time > expires_at:
                expired_keys.append(cache_key)
        
        for key in expired_keys:
            del self.cache[key]
        
        return len(expired_keys)

# Global cache instance
cache = SimpleCache(default_ttl=300)
