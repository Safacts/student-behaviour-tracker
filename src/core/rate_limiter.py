"""
Simple, self-contained API rate limiting system
"""
import time
from typing import Dict, Any, Tuple
from collections import defaultdict

class SimpleRateLimiter:
    """Production-ready rate limiter without external dependencies"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_ip: str) -> Tuple[bool, Dict[str, Any]]:
        """Check if client is allowed based on rate limit"""
        current_time = time.time()
        
        # Remove old requests outside the window
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < self.window_seconds
        ]
        
        # Check if under the limit
        if len(self.requests[client_ip]) < self.max_requests:
            self.requests[client_ip].append(current_time)
            remaining = self.max_requests - len(self.requests[client_ip])
            return True, {
                "remaining": remaining,
                "limit": self.max_requests,
                "window": self.window_seconds
            }
        else:
            return False, {
                "error": "Rate limit exceeded",
                "retry_after": self.window_seconds,
                "limit": self.max_requests,
                "window": self.window_seconds
            }
    
    def reset(self, client_ip: str):
        """Reset rate limit for specific client"""
        self.requests[client_ip] = []
    
    def get_stats(self, client_ip: str) -> Dict[str, Any]:
        """Get current rate limit stats for client"""
        current_time = time.time()
        recent_requests = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < self.window_seconds
        ]
        
        return {
            "client_ip": client_ip,
            "requests_in_window": len(recent_requests),
            "limit": self.max_requests,
            "remaining": max(0, self.max_requests - len(recent_requests)),
            "window_seconds": self.window_seconds,
            "window_remaining": max(0, self.window_seconds - (current_time - min(recent_requests) if recent_requests else 0))
        }

# Global rate limiter instance
rate_limiter = SimpleRateLimiter(max_requests=100, window_seconds=60)
