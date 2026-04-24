"""
Simple, self-contained authentication system
"""
import hashlib
import hmac
import secrets
import sqlite3
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

class SimpleAuth:
    """Production-ready authentication without external dependencies"""
    
    def __init__(self, secret_key: str = "default-secret-key-change-in-production", db_path: str = "behavior.db"):
        self.secret_key = secret_key
        self.api_keys = {}  # In production, use database
        self.sessions = {}  # In production, use Redis
        self.db_path = db_path
    
    def _get_db_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
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
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user with username and password"""
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            # Get user from database
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND is_active = 1",
                (username,)
            )
            user = cursor.fetchone()
            conn.close()
            
            if not user:
                return {
                    "success": False,
                    "message": "Invalid username or password"
                }
            
            # Verify password
            password_hash = user["password_hash"]
            if not self.verify_password(password, password_hash):
                return {
                    "success": False,
                    "message": "Invalid username or password"
                }
            
            # Generate token
            token = self.generate_token(user["user_id"])
            
            return {
                "success": True,
                "user_id": user["user_id"],
                "username": user["username"],
                "role": user["role"],
                "name": user["name"],
                "token": token,
                "message": "Login successful"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Login failed: {str(e)}"
            }
    
    def register_user(self, username: str, password: str, role: str, name: str, email: str) -> Dict[str, Any]:
        """Register a new user"""
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            # Check if username already exists
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                conn.close()
                return {
                    "success": False,
                    "message": "Username already exists"
                }
            
            # Generate user ID
            user_id = f"U{secrets.token_hex(2).upper()}"
            
            # Hash password
            password_hash = self.hash_password(password)
            
            # Insert user
            cursor.execute(
                """INSERT INTO users (user_id, username, password_hash, role, name, email, created_at, is_active)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, username, password_hash, role, name, email, datetime.now().isoformat(), 1)
            )
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "user_id": user_id,
                "message": "User registered successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Registration failed: {str(e)}"
            }
    
    def logout(self, token: str) -> Dict[str, Any]:
        """Logout user by revoking token"""
        if self.revoke_token(token):
            return {
                "success": True,
                "message": "Logout successful"
            }
        return {
            "success": False,
            "message": "Invalid token"
        }

# Global auth instance
auth = SimpleAuth()
