# Instructions de Démarrage - Backend

## Installation Rapide

### 1. Prérequis
- Python 3.8 ou supérieur
- PostgreSQL 12 ou supérieur
- pip (gestionnaire de paquets Python)

### 2. Configuration de la Base de Données

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Créer la base de données
CREATE DATABASE jobapp_db;

# Créer un utilisateur (optionnel)
CREATE USER jobapp_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE jobapp_db TO jobapp_user;

# Quitter psql
\q
```

### 3. Configuration de l'Environnement

```bash
cd backend

# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac:
source venv/bin/activate
# Sur Windows:
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 4. Configuration des Variables d'Environnement

Créer un fichier `.env` dans le dossier `backend/`:

```env
DATABASE_URL=postgresql://jobapp_user:votre_mot_de_passe@localhost:5432/jobapp_db
SECRET_KEY=votre-cle-secrete-tres-longue-et-aleatoire
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=uploads
```

**Important**: Remplacez `votre-cle-secrete-tres-longue-et-aleatoire` par une clé aléatoire forte. Vous pouvez en générer une avec:

```python
import secrets
print(secrets.token_urlsafe(32))
```

### 5. Initialisation de la Base de Données

Les tables seront créées automatiquement au premier démarrage grâce à `Base.metadata.create_all(bind=engine)` dans `main.py`.

Alternativement, vous pouvez exécuter le script SQL:

```bash
psql -U jobapp_user -d jobapp_db -f schema.sql
```

### 6. Lancement du Serveur

```bash
python run.py
```

Le serveur démarrera sur `http://localhost:8000`

### 7. Vérification

- API: http://localhost:8000/api/health
- Documentation Swagger: http://localhost:8000/docs
- Documentation ReDoc: http://localhost:8000/redoc

## Création d'un Utilisateur Admin

Pour créer un utilisateur admin, vous pouvez:

1. **Via l'API** (après avoir créé un compte admin manuellement dans la base):
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@jobapp.com", "mot_de_passe": "admin123", "role": "admin"}'
```

2. **Directement dans PostgreSQL**:
```sql
-- Le mot de passe doit être hashé avec bcrypt
-- Utiliser Python pour générer le hash:
-- python -c "from passlib.context import CryptContext; pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto'); print(pwd_context.hash('admin123'))"
```

## Dépannage

### Erreur de connexion à la base de données
- Vérifiez que PostgreSQL est démarré: `sudo systemctl status postgresql`
- Vérifiez les credentials dans `.env`
- Vérifiez que la base de données existe

### Erreur d'import
- Vérifiez que l'environnement virtuel est activé
- Réinstallez les dépendances: `pip install -r requirements.txt`

### Port déjà utilisé
- Changez le port dans `run.py`: `uvicorn.run(..., port=8001)`

## Production

Pour la production, utilisez Gunicorn avec Uvicorn workers:

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Configurez Nginx comme reverse proxy et activez HTTPS.



