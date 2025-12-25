from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
import logging
from collections import defaultdict
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)

# Rate limiting storage (en production, utiliser Redis)
rate_limit_store = defaultdict(list)
failed_login_attempts = defaultdict(list)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware pour ajouter des headers de sécurité"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Headers de sécurité OWASP recommandés
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # Supprimer le header Server
        response.headers.pop("server", None)
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware pour limiter le taux de requêtes"""
    
    def __init__(self, app: ASGIApp, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Nettoyer les anciennes entrées
        rate_limit_store[client_ip] = [
            timestamp for timestamp in rate_limit_store[client_ip]
            if current_time - timestamp < 60
        ]
        
        # Vérifier le rate limit
        if len(rate_limit_store[client_ip]) >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "Too many requests. Please try again later.",
                    "retry_after": 60
                },
                headers={"Retry-After": "60"}
            )
        
        # Ajouter la requête actuelle
        rate_limit_store[client_ip].append(current_time)
        
        response = await call_next(request)
        return response


class InputSanitizationMiddleware(BaseHTTPMiddleware):
    """Middleware pour sanitizer les inputs et prévenir les injections"""
    
    # Patterns dangereux
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)",
        r"(--|#|/\*|\*/)",
        r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
        r"('|(\\')|(;)|(\|)|(\*))",
    ]
    
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe[^>]*>",
        r"<object[^>]*>",
        r"<embed[^>]*>",
    ]
    
    COMMAND_INJECTION_PATTERNS = [
        r"[;&|`$(){}]",
        r"\b(cat|ls|pwd|whoami|id|uname|ps|netstat)\b",
    ]
    
    # Patterns à ignorer (formulaires normaux)
    SAFE_PATTERNS = [
        r"username=[^&]*&password=",  # Formulaire de login
        r"email=[^&]*",  # Email dans les formulaires
    ]
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.sql_pattern = re.compile("|".join(self.SQL_INJECTION_PATTERNS), re.IGNORECASE)
        self.xss_pattern = re.compile("|".join(self.XSS_PATTERNS), re.IGNORECASE)
        self.cmd_pattern = re.compile("|".join(self.COMMAND_INJECTION_PATTERNS), re.IGNORECASE)
    
    def detect_attack(self, value: str) -> tuple[bool, str]:
        """Détecter les tentatives d'attaque"""
        if not isinstance(value, str):
            return False, ""
        
        # Ignorer les patterns sûrs (formulaires normaux)
        for safe_pattern in self.SAFE_PATTERNS:
            if re.search(safe_pattern, value, re.IGNORECASE):
                # C'est un formulaire normal, vérifier seulement les patterns vraiment dangereux
                # mais pas les caractères @ qui sont normaux dans les emails
                dangerous_sql = re.search(r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b|--|#|/\*|\*/)", value, re.IGNORECASE)
                if dangerous_sql:
                    return True, "SQL_INJECTION"
                dangerous_xss = re.search(r"<script[^>]*>|javascript:|on\w+\s*=", value, re.IGNORECASE)
                if dangerous_xss:
                    return True, "XSS"
                # Pour les commandes, ignorer @ et & qui sont normaux dans les formulaires
                dangerous_cmd = re.search(r"[;|`$(){}]|\b(cat|ls|pwd|whoami|id|uname|ps|netstat)\b", value, re.IGNORECASE)
                if dangerous_cmd:
                    return True, "COMMAND_INJECTION"
                return False, ""
        
        # Pour les autres cas, vérifier tous les patterns
        if self.sql_pattern.search(value):
            return True, "SQL_INJECTION"
        if self.xss_pattern.search(value):
            return True, "XSS"
        if self.cmd_pattern.search(value):
            return True, "COMMAND_INJECTION"
        return False, ""
    
    async def dispatch(self, request: Request, call_next):
        # Vérifier les query parameters
        for key, value in request.query_params.items():
            is_attack, attack_type = self.detect_attack(str(value))
            if is_attack:
                logger.critical(
                    f"SECURITY ALERT: {attack_type} attempt from {request.client.host} "
                    f"in parameter {key}: {value[:100]}"
                )
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": "Invalid input detected"}
                )
        
        # Vérifier le body si c'est du JSON (pas les formulaires)
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            # Ignorer les formulaires (form-urlencoded) qui sont normaux
            if "application/json" in content_type:
                try:
                    body = await request.body()
                    if body:
                        body_str = body.decode('utf-8')
                        is_attack, attack_type = self.detect_attack(body_str)
                        if is_attack:
                            logger.critical(
                                f"SECURITY ALERT: {attack_type} attempt from {request.client.host} "
                                f"in body: {body_str[:200]}"
                            )
                            return JSONResponse(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                content={"detail": "Invalid input detected"}
                            )
                except Exception:
                    pass
        
        response = await call_next(request)
        return response


class BruteForceProtectionMiddleware(BaseHTTPMiddleware):
    """Protection contre les attaques par force brute"""
    
    MAX_ATTEMPTS = 5
    LOCKOUT_DURATION = timedelta(minutes=15)
    
    async def dispatch(self, request: Request, call_next):
        # Vérifier uniquement pour les endpoints de login
        if "/api/auth/login" in str(request.url):
            client_ip = request.client.host if request.client else "unknown"
            current_time = datetime.now()
            
            # Nettoyer les anciennes tentatives
            failed_login_attempts[client_ip] = [
                attempt_time for attempt_time in failed_login_attempts[client_ip]
                if current_time - attempt_time < self.LOCKOUT_DURATION
            ]
            
            # Vérifier si l'IP est bloquée
            if len(failed_login_attempts[client_ip]) >= self.MAX_ATTEMPTS:
                logger.warning(f"Brute force protection: IP {client_ip} is locked out")
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": "Too many failed login attempts. "
                                 f"Account locked for {self.LOCKOUT_DURATION.seconds // 60} minutes.",
                        "retry_after": self.LOCKOUT_DURATION.seconds
                    },
                    headers={"Retry-After": str(self.LOCKOUT_DURATION.seconds)}
                )
        
        response = await call_next(request)
        
        # Si c'est un échec de login, enregistrer la tentative
        if "/api/auth/login" in str(request.url) and response.status_code == 401:
            client_ip = request.client.host if request.client else "unknown"
            failed_login_attempts[client_ip].append(datetime.now())
            logger.warning(f"Failed login attempt from IP: {client_ip}")
        
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware pour logger les requêtes suspectes"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        # Logger les requêtes suspectes
        if response.status_code >= 400:
            logger.warning(
                f"HTTP {response.status_code} | "
                f"IP: {client_ip} | "
                f"Method: {request.method} | "
                f"Path: {request.url.path} | "
                f"User-Agent: {user_agent} | "
                f"Time: {process_time:.3f}s"
            )
        
        # Logger les accès aux endpoints sensibles
        sensitive_paths = ["/api/auth", "/api/admin", "/api/candidats/upload-cv"]
        if any(path in request.url.path for path in sensitive_paths):
            logger.info(
                f"SECURITY LOG | "
                f"IP: {client_ip} | "
                f"Method: {request.method} | "
                f"Path: {request.url.path} | "
                f"Status: {response.status_code}"
            )
        
        return response

