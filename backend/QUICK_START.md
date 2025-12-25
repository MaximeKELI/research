# 🚀 Guide de Démarrage Rapide

## Installation Complète

### 1. Créer l'environnement virtuel (déjà fait ✅)
```bash
cd backend
python3 -m venv venv
```

### 2. Activer l'environnement virtuel
```bash
source venv/bin/activate
# Vous devriez voir (venv) dans votre prompt
```

### 3. Installer les dépendances (déjà fait ✅)
```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données

Créer un fichier `.env` dans le dossier `backend/`:
```bash
cp .env.example .env
```

Modifier `.env` avec vos paramètres:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/jobapp_db
SECRET_KEY=votre-cle-secrete-tres-longue-et-aleatoire
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=uploads
```

### 5. Créer la base de données PostgreSQL
```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Créer la base de données
CREATE DATABASE jobapp_db;

# Quitter
\q
```

### 6. Lancer l'application
```bash
# S'assurer que l'environnement virtuel est activé
source venv/bin/activate

# Lancer le serveur
python run.py
```

L'API sera accessible sur `http://localhost:8000`

## Commandes Utiles

### Activer l'environnement virtuel
```bash
source venv/bin/activate
```

### Désactiver l'environnement virtuel
```bash
deactivate
```

### Vérifier les dépendances installées
```bash
pip list
```

### Lancer les tests
```bash
pytest tests/ -v
```

### Lancer l'audit de sécurité
```bash
python security_audit.py
```

## Dépannage

### Erreur: ModuleNotFoundError
**Solution**: Activer l'environnement virtuel
```bash
source venv/bin/activate
```

### Erreur: Database connection
**Solution**: Vérifier que PostgreSQL est démarré
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

### Erreur: Port déjà utilisé
**Solution**: Changer le port dans `run.py` ou tuer le processus
```bash
# Trouver le processus
lsof -i :8000
# Tuer le processus
kill -9 <PID>
```

## Prochaines Étapes

1. ✅ Environnement virtuel créé
2. ✅ Dépendances installées
3. ⏭️ Configurer `.env`
4. ⏭️ Créer la base de données
5. ⏭️ Lancer l'application

