# Backend API - JobApp

API REST construite avec FastAPI pour la plateforme de stages et emplois.

## Installation

1. Créer un environnement virtuel:
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

2. Installer les dépendances:
```bash
pip install -r requirements.txt
```

3. Configurer la base de données PostgreSQL:
- Créer une base de données: `CREATE DATABASE jobapp_db;`
- Copier `.env.example` vers `.env` et modifier les variables

4. Lancer l'application:
```bash
python run.py
```

L'API sera accessible sur `http://localhost:8000`

## Documentation API

Une fois l'application lancée, accédez à:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Structure

- `app/main.py`: Point d'entrée de l'application
- `app/models.py`: Modèles SQLAlchemy
- `app/schemas.py`: Schémas Pydantic pour validation
- `app/auth.py`: Logique d'authentification JWT
- `app/routers/`: Routeurs pour chaque ressource
- `app/database.py`: Configuration de la base de données

## Endpoints principaux

- `/api/auth/register` - Inscription
- `/api/auth/login` - Connexion
- `/api/candidats/` - Gestion des profils candidats
- `/api/entreprises/` - Gestion des profils entreprises
- `/api/offres/` - Gestion des offres
- `/api/candidatures/` - Gestion des candidatures
- `/api/admin/` - Administration (réservé aux admins)

