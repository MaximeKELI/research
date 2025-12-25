from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
from app.database import settings

class DataEncryption:
    """Chiffrement des données sensibles"""
    
    def __init__(self):
        # En production, utiliser une clé depuis les variables d'environnement
        key = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())
        if isinstance(key, str):
            key = key.encode()
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Chiffrer une donnée"""
        if not data:
            return ""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Déchiffrer une donnée"""
        if not encrypted_data:
            return ""
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return ""


class TokenBlacklist:
    """Gestion de la blacklist des tokens"""
    
    def __init__(self):
        # En production, utiliser Redis
        self.blacklisted_tokens = set()
    
    def add(self, token: str):
        """Ajouter un token à la blacklist"""
        self.blacklisted_tokens.add(token)
    
    def is_blacklisted(self, token: str) -> bool:
        """Vérifier si un token est blacklisté"""
        return token in self.blacklisted_tokens
    
    def clear_expired(self):
        """Nettoyer les tokens expirés (à implémenter avec TTL)"""
        pass

