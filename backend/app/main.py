from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routers import auth, candidats, entreprises, offres, candidatures, admin
from app.security.middleware import (
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
    InputSanitizationMiddleware,
    BruteForceProtectionMiddleware,
    RequestLoggingMiddleware
)
import os
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security.log'),
        logging.StreamHandler()
    ]
)

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JobApp API",
    description="API pour la plateforme de stages et emplois",
    version="1.0.0"
)

# Middlewares de sécurité (ordre important!)
# Désactiver en mode test (détecté via variable d'environnement)
if not os.getenv("TESTING", "").lower() == "true":
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(InputSanitizationMiddleware)
    app.add_middleware(BruteForceProtectionMiddleware)
    app.add_middleware(RateLimitMiddleware, requests_per_minute=60)
else:
    # En mode test, seulement les headers de sécurité
    app.add_middleware(SecurityHeadersMiddleware)

# CORS avec restrictions de sécurité
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-CSRF-Token"],
    expose_headers=["X-CSRF-Token"],
    max_age=3600,
)

# Inclure les routeurs
app.include_router(auth.router, prefix="/api/auth", tags=["Authentification"])
app.include_router(candidats.router, prefix="/api/candidats", tags=["Candidats"])
app.include_router(entreprises.router, prefix="/api/entreprises", tags=["Entreprises"])
app.include_router(offres.router, prefix="/api/offres", tags=["Offres"])
app.include_router(candidatures.router, prefix="/api/candidatures", tags=["Candidatures"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

# Servir les fichiers statiques (CV)
uploads_dir = "uploads"
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

@app.get("/")
async def root():
    return {"message": "JobApp API - Bienvenue"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

