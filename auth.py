"""
Simple, self-contained authentication system
"""
import hashlib
import hmac
import secrets
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

class SimpleAuth:
    """Production-ready authentication without external dependencies"""
    
    def __init__(self, secret_key: str = "default-secret-key-change-in-production"):
        self.secret_key = secret_key
        self.api_keys = {}  # In production, use database
        self.sessions = {}  # In production, use Redis
    
    def generate_api_key(self, user_id: str) -> str:
        """Generate a secure API key for a user"""
        api_key = secrets.token_urlsafe(32)
        self.api_keys[api_key] = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "last_used": None
        }
        return api_key
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate an API key and return user info"""
        if api_key in self.api_keys:
            key_info = self.api_keys[api_key]
            key_info["last_used"] = datetime.now().isoformat()
            return {
                "user_id": key_info["user_id"],
                "valid": True
            }
        return None
    
    def revoke_api_key(self, api_key: str) -> bool:
        """Revoke an API key"""
        if api_key in self.api_keys:
            del self.api_keys[api_key]
            return True
        return False
    
    def generate_token(self, user_id: str, expires_in_hours: int = 24) -> str:
        """Generate a simple token"""
        expires_at = datetime.now() + timedelta(hours=expires_in_hours)
        token_data = f"{user_id}:{expires_at.timestamp()}:{secrets.token_hex(16)}"
        signature = hmac.new(
            self.secret_key.encode(),
            token_data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        token = f"{token_data}:{signature}"
        self.sessions[token] = {
            "user_id": user_id,
            "expires_at": expires_at.isoformat(),
            "created_at": datetime.now().isoformat()
        }
        return token
    
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate a token and return user info"""
        if token not in self.sessions:
            return None
        
        session = self.sessions[token]
        expires_at = datetime.fromisoformat(session["expires_at"])
        
        if datetime.now() > expires_at:
            del self.sessions[token]
            return None
        
        return {
            "user_id": session["user_id"],
            "valid": True,
            "expires_at": session["expires_at"]
        }
    
    def revoke_token(self, token: str) -> bool:
        """Revoke a token"""
        if token in self.sessions:
            del self.sessions[token]
            return True
        return False
    
    def hash_password(self, password: str) -> str:
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against a hash"""
        return hmac.compare_digest(
            hashlib.sha256(password.encode()).hexdigest(),
            hashed_password
        )
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get authentication system stats"""
        return {
            "total_api_keys": len(self.api_keys),
            "active_sessions": len(self.sessions),
            "timestamp": datetime.now().isoformat()
        }

# Global auth instance
auth = SimpleAuth()
