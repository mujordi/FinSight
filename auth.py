"""
Authentication module for FinSight
Handles user authentication and session management
"""
from datetime import datetime, timedelta
from typing import Optional
import secrets
import hashlib

class AuthManager:
    """Manages user authentication and sessions"""
    
    def __init__(self):
        # In production, store these in a secure database
        # For now, using a simple in-memory store
        self.users = {
            "admin": self._hash_password("finsight2026"),
            "demo": self._hash_password("demo123")
        }
        
        # Session storage: {token: {username, expires}}
        self.sessions = {}
        
        # Session duration (24 hours)
        self.session_duration = timedelta(hours=24)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """
        Authenticate user and return session token
        Returns None if authentication fails
        """
        if username not in self.users:
            return None
        
        password_hash = self._hash_password(password)
        if self.users[username] != password_hash:
            return None
        
        # Create session token
        token = secrets.token_urlsafe(32)
        expires = datetime.now() + self.session_duration
        
        self.sessions[token] = {
            "username": username,
            "expires": expires
        }
        
        return token
    
    def validate_session(self, token: Optional[str]) -> bool:
        """Validate if session token is valid and not expired"""
        if not token or token not in self.sessions:
            return False
        
        session = self.sessions[token]
        if datetime.now() > session["expires"]:
            # Session expired, remove it
            del self.sessions[token]
            return False
        
        return True
    
    def logout(self, token: str):
        """Logout user by removing session"""
        if token in self.sessions:
            del self.sessions[token]
    
    def get_username(self, token: str) -> Optional[str]:
        """Get username from session token"""
        if token in self.sessions:
            return self.sessions[token]["username"]
        return None
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions (call periodically)"""
        now = datetime.now()
        expired = [
            token for token, session in self.sessions.items()
            if now > session["expires"]
        ]
        for token in expired:
            del self.sessions[token]

