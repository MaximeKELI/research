from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, candidats, entreprises, offres, candidatures, admin

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JobApp API",
    description="API pour la plateforme de stages et emplois",
    version="1.0.0"
)

# CORS pour permettre les requêtes depuis Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routeurs
app.include_router(auth.router, prefix="/api/auth", tags=["Authentification"])
app.include_router(candidats.router, prefix="/api/candidats", tags=["Candidats"])
app.include_router(entreprises.router, prefix="/api/entreprises", tags=["Entreprises"])
app.include_router(offres.router, prefix="/api/offres", tags=["Offres"])
app.include_router(candidatures.router, prefix="/api/candidatures", tags=["Candidatures"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "JobApp API - Bienvenue"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

