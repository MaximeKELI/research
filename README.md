# JobApp - Plateforme de Stages et Emplois

Application mobile complète (Android & iOS) permettant de connecter entreprises et candidats pour la publication et la recherche de stages et emplois.

## Architecture

- **Frontend Mobile**: Flutter (Android & iOS)
- **Backend API**: FastAPI (Python)
- **Base de données**: PostgreSQL
- **Authentification**: JWT
- **Stockage fichiers**: CV en PDF

## Structure du Projet

```
Research_App/
├── backend/          # API FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   ├── database.py
│   │   └── routers/
│   ├── requirements.txt
│   ├── schema.sql
│   └── README.md
│
└── research/         # Application Flutter
    ├── lib/
    │   ├── main.dart
    │   ├── core/
    │   ├── models/
    │   ├── services/
    │   ├── providers/
    │   └── screens/
    └── pubspec.yaml
```

## Installation et Lancement

### Prérequis

- Python 3.8+
- PostgreSQL 12+
- Flutter 3.7+
- Node.js (optionnel, pour certains outils)

### Backend

1. **Créer un environnement virtuel Python**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

2. **Installer les dépendances**:
```bash
pip install -r requirements.txt
```

3. **Configurer PostgreSQL**:
```bash
# Créer la base de données
createdb jobapp_db

# Ou via psql:
psql -U postgres
CREATE DATABASE jobapp_db;
```

4. **Configurer les variables d'environnement**:
```bash
cp .env.example .env
# Modifier .env avec vos paramètres
```

5. **Créer les tables**:
```bash
# Option 1: Via SQLAlchemy (automatique au démarrage)
python run.py

# Option 2: Via le script SQL
psql -U postgres -d jobapp_db -f schema.sql
```

6. **Lancer le serveur**:
```bash
python run.py
```

L'API sera accessible sur `http://localhost:8000`
- Documentation Swagger: `http://localhost:8000/docs`
- Documentation ReDoc: `http://localhost:8000/redoc`

### Frontend Flutter

1. **Installer les dépendances**:
```bash
cd research
flutter pub get
```

2. **Configurer l'URL de l'API**:
Modifier `lib/core/config.dart` avec l'URL de votre backend:
- Android Emulator: `http://10.0.2.2:8000`
- iOS Simulator: `http://localhost:8000`
- Device physique: `http://VOTRE_IP:8000`

3. **Lancer l'application**:
```bash
flutter run
```

## Fonctionnalités

### Candidat
- ✅ Inscription / Connexion
- ✅ Création et modification de profil
- ✅ Upload de CV (PDF)
- ✅ Recherche d'offres (filtres: type, lieu, mot-clé)
- ✅ Postuler à une offre
- ✅ Suivi des candidatures

### Entreprise
- ✅ Inscription / Connexion
- ✅ Création de profil entreprise
- ✅ Publication d'offres (stage / emploi)
- ✅ Consultation des candidatures reçues
- ✅ Gestion du statut des candidatures (accepter/refuser)

### Admin
- ✅ Validation des entreprises
- ✅ Gestion des offres
- ✅ Statistiques globales

## Sécurité

### Bonnes pratiques implémentées

1. **Authentification JWT**
   - Tokens avec expiration
   - Stockage sécurisé côté client

2. **Hachage des mots de passe**
   - Utilisation de bcrypt
   - Salt automatique

3. **Validation des données**
   - Pydantic pour le backend
   - Validation des formulaires Flutter

4. **Permissions par rôle**
   - Vérification des rôles pour chaque endpoint
   - Middleware d'authentification

### À améliorer en production

- [ ] HTTPS obligatoire
- [ ] Rate limiting
- [ ] Validation email
- [ ] Récupération de mot de passe
- [ ] Logs d'audit
- [ ] Backup automatique de la base de données

## Configuration Production

### Backend

1. Modifier `SECRET_KEY` dans `.env` avec une clé forte
2. Configurer CORS avec les domaines autorisés
3. Utiliser un serveur WSGI (Gunicorn + Nginx)
4. Configurer SSL/TLS

### Frontend

1. Configurer les URLs de production dans `config.dart`
2. Optimiser les images et assets
3. Activer le code obfuscation pour la release
4. Configurer les permissions Android/iOS

## Tests

### Backend
```bash
# Tests unitaires (à créer)
pytest tests/
```

### Frontend
```bash
# Tests Flutter
flutter test
```

## Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT.

## Support

Pour toute question ou problème, ouvrir une issue sur le dépôt GitHub.

## Auteur

Développé pour le contexte africain avec simplicité et efficacité.
