from fastapi import Request, HTTPException, status
from itsdangerous import URLSafeTimedSerializer
import secrets
from app.database import settings

class CSRFProtection:
    """Protection CSRF"""
    
    def __init__(self):
        self.secret_key = settings.secret_key
        self.serializer = URLSafeTimedSerializer(self.secret_key)
    
    def generate_token(self) -> str:
        """Générer un token CSRF"""
        return self.serializer.dumps(secrets.token_urlsafe(32))
    
    def validate_token(self, token: str, max_age: int = 3600) -> bool:
        """Valider un token CSRF"""
        try:
            self.serializer.loads(token, max_age=max_age)
            return True
        except Exception:
            return False
    
    def get_token_from_request(self, request: Request) -> str:
        """Récupérer le token CSRF depuis la requête"""
        # Vérifier dans le header
        token = request.headers.get("X-CSRF-Token")
        if token:
            return token
        
        # Vérifier dans le body pour les requêtes POST
        if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            try:
                if hasattr(request, "_json"):
                    return request._json.get("csrf_token", "")
            except Exception:
                pass
        
        return ""


async def verify_csrf_token(request: Request):
    """Vérifier le token CSRF pour les requêtes modifiantes"""
    if request.method in ["GET", "HEAD", "OPTIONS"]:
        return True
    
    csrf_protection = CSRFProtection()
    token = csrf_protection.get_token_from_request(request)
    
    if not token or not csrf_protection.validate_token(token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing CSRF token"
        )
    
    return True

