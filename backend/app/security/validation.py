from pydantic import BaseModel, validator, EmailStr
from typing import Optional
import re
import bleach
from html import escape

class SecureEmailStr(EmailStr):
    """Email avec validation renforcée"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise ValueError('must be a string')
        
        # Longueur maximale
        if len(v) > 254:
            raise ValueError('email too long')
        
        # Pattern strict
        email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        if not email_pattern.match(v):
            raise ValueError('invalid email format')
        
        # Vérifier les caractères dangereux
        dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
        if any(char in v for char in dangerous_chars):
            raise ValueError('email contains invalid characters')
        
        return v.lower().strip()


class SecurePassword(str):
    """Mot de passe avec validation de sécurité"""
    
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise ValueError('must be a string')
        
        # Longueur minimale
        if len(v) < 8:
            raise ValueError('password must be at least 8 characters')
        
        # Longueur maximale (prévenir DoS)
        if len(v) > 128:
            raise ValueError('password too long')
        
        # Vérifier la complexité
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v)
        
        if not (has_upper and has_lower and has_digit):
            raise ValueError(
                'password must contain uppercase, lowercase, and digits'
            )
        
        # Vérifier les patterns communs (dictionnaire)
        common_passwords = [
            'password', '12345678', 'qwerty', 'admin', 'letmein'
        ]
        if v.lower() in common_passwords:
            raise ValueError('password is too common')
        
        return v


def sanitize_string(value: str, max_length: int = 1000, allow_html: bool = False) -> str:
    """Sanitizer une chaîne de caractères"""
    if not isinstance(value, str):
        return ""
    
    # Limiter la longueur
    if len(value) > max_length:
        value = value[:max_length]
    
    # Si on permet HTML, ne pas échapper
    if not allow_html:
        # Échapper les caractères HTML
        value = escape(value)
        
    # Nettoyer avec bleach
    value = bleach.clean(
        value,
        tags=[],
        attributes=[],
        strip=True
    )
    
    # Supprimer les caractères de contrôle (mais garder les caractères normaux)
    value = ''.join(char for char in value if ord(char) >= 32 or char in '\n\r\t')
    
    return value.strip()


def sanitize_text(value: str, max_length: int = 10000) -> str:
    """Sanitizer un texte long (description, etc.)"""
    if not isinstance(value, str):
        return ""
    
    if len(value) > max_length:
        value = value[:max_length]
    
    # Nettoyer mais garder les retours à la ligne
    value = bleach.clean(
        value,
        tags=['p', 'br'],
        attributes={},
        strip=True
    )
    
    return value.strip()


def validate_file_upload(filename: str, content: bytes, max_size: int = 5 * 1024 * 1024, file_type: str = "pdf") -> tuple[bool, str]:
    """Valider un upload de fichier
    
    Args:
        filename: Nom du fichier
        content: Contenu du fichier en bytes
        max_size: Taille maximale en bytes (défaut: 5MB)
        file_type: Type de fichier attendu ("pdf" ou "image")
    """
    # Vérifier la taille
    if len(content) > max_size:
        return False, f"File too large (max {max_size // (1024*1024)}MB)"

    if len(content) == 0:
        return False, "Empty file"

    # Vérifier le nom du fichier
    if len(filename) > 255:
        return False, "Filename too long"

    # Vérifier les caractères dangereux dans le nom
    dangerous_chars = ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*']
    if any(char in filename for char in dangerous_chars):
        return False, "Invalid filename"

    if file_type == "pdf":
        # Vérifier l'extension pour PDF
        allowed_extensions = ['.pdf']
        if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
            return False, "Invalid file type. Only PDF files are allowed"
        
        # Vérifier le magic number pour PDF
        if not content.startswith(b'%PDF'):
            return False, "Invalid PDF file content"
    
    elif file_type == "image":
        # Vérifier l'extension pour images
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
            return False, "Invalid file type. Only JPG, PNG, GIF, and WEBP images are allowed"
        
        # Vérifier le magic number pour images
        # JPEG: FF D8 FF
        # PNG: 89 50 4E 47
        # GIF: 47 49 46 38
        # WEBP: 52 49 46 46 (RIFF) suivi de WEBP
        is_valid_image = (
            content.startswith(b'\xFF\xD8\xFF') or  # JPEG
            content.startswith(b'\x89PNG\r\n\x1a\n') or  # PNG
            content.startswith(b'GIF89a') or  # GIF89a
            content.startswith(b'GIF87a') or  # GIF87a
            (content.startswith(b'RIFF') and b'WEBP' in content[:20])  # WEBP
        )
        if not is_valid_image:
            return False, "Invalid image file content"

    return True, "OK"

