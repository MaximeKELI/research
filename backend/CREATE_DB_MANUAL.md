# 🗄️ Guide Manuel - Création de la Base de Données PostgreSQL

## Méthode 1 : Script Automatique (Recommandé)

```bash
cd ~/Research_App/backend
./create_database.sh
```

Le script vous guidera étape par étape.

## Méthode 2 : Manuellement avec psql

### Étape 1 : Se connecter à PostgreSQL

```bash
sudo -u postgres psql
```

### Étape 2 : Créer la base de données

Dans le prompt psql, exécutez :

```sql
-- Créer la base de données
CREATE DATABASE jobapp_db;

-- Vérifier qu'elle a été créée
\l

-- Quitter psql
\q
```

### Étape 3 : (Optionnel) Créer un utilisateur dédié

Si vous voulez créer un utilisateur spécifique pour l'application :

```bash
sudo -u postgres psql
```

```sql
-- Créer l'utilisateur
CREATE USER jobapp_user WITH PASSWORD 'votre_mot_de_passe_securise';

-- Créer la base de données avec cet utilisateur comme propriétaire
CREATE DATABASE jobapp_db OWNER jobapp_user;

-- Donner tous les privilèges
GRANT ALL PRIVILEGES ON DATABASE jobapp_db TO jobapp_user;

-- Vérifier
\l

-- Quitter
\q
```

### Étape 4 : Configurer le fichier .env

Modifiez le fichier `.env` dans `backend/` :

```bash
cd ~/Research_App/backend
nano .env
```

**Si vous utilisez l'utilisateur postgres** :
```env
DATABASE_URL=postgresql://postgres:VOTRE_MOT_DE_PASSE@localhost:5432/jobapp_db
```

**Si vous utilisez un utilisateur dédié** :
```env
DATABASE_URL=postgresql://jobapp_user:votre_mot_de_passe_securise@localhost:5432/jobapp_db
```

**Si PostgreSQL n'a pas de mot de passe (développement local)** :
```env
DATABASE_URL=postgresql://postgres@localhost:5432/jobapp_db
```

### Étape 5 : Générer une clé secrète

Ajoutez aussi dans `.env` :

```env
SECRET_KEY=votre_cle_secrete_aleatoire_tres_longue
```

Pour générer une clé secrète :
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Vérification

### Vérifier que PostgreSQL est démarré

```bash
sudo systemctl status postgresql
```

Si arrêté :
```bash
sudo systemctl start postgresql
```

### Vérifier que la base existe

```bash
sudo -u postgres psql -l
```

Vous devriez voir `jobapp_db` dans la liste.

### Tester la connexion

```bash
psql -U postgres -d jobapp_db
# ou
psql -U jobapp_user -d jobapp_db
```

## Problèmes Courants

### Erreur : "password authentication failed"

**Solution 1** : Vérifier le mot de passe dans `.env`

**Solution 2** : Réinitialiser le mot de passe de postgres
```bash
sudo -u postgres psql
ALTER USER postgres PASSWORD 'nouveau_mot_de_passe';
\q
```

**Solution 3** : Configurer PostgreSQL pour accepter les connexions locales sans mot de passe (développement uniquement)
```bash
sudo nano /etc/postgresql/*/main/pg_hba.conf
```

Changer :
```
local   all             all                                     peer
```

En :
```
local   all             all                                     trust
```

Puis redémarrer :
```bash
sudo systemctl restart postgresql
```

### Erreur : "database does not exist"

La base de données n'a pas été créée. Suivez l'Étape 2 ci-dessus.

### Erreur : "could not connect to server"

PostgreSQL n'est pas démarré :
```bash
sudo systemctl start postgresql
```

## Après la Configuration

Une fois tout configuré, lancez l'application :

```bash
cd ~/Research_App/backend
source venv/bin/activate
python run.py
```

L'application créera automatiquement toutes les tables au démarrage !

