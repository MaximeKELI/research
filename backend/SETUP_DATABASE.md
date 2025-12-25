# 🗄️ Configuration de la Base de Données PostgreSQL

## Problème de Connexion

Si vous voyez l'erreur :
```
FATAL: password authentication failed for user "user"
```

Cela signifie que les identifiants PostgreSQL dans `.env` ne sont pas corrects.

## Solution Rapide

### Option 1 : Utiliser l'utilisateur postgres par défaut

1. **Modifier le fichier `.env`** :
```bash
cd backend
nano .env
```

2. **Mettre à jour la ligne DATABASE_URL** :
```env
DATABASE_URL=postgresql://postgres:VOTRE_MOT_DE_PASSE@localhost:5432/jobapp_db
```

Remplacez `VOTRE_MOT_DE_PASSE` par le mot de passe de l'utilisateur `postgres`.

### Option 2 : Créer un utilisateur dédié

1. **Se connecter à PostgreSQL** :
```bash
sudo -u postgres psql
```

2. **Créer un utilisateur et la base de données** :
```sql
-- Créer l'utilisateur
CREATE USER jobapp_user WITH PASSWORD 'votre_mot_de_passe_securise';

-- Créer la base de données
CREATE DATABASE jobapp_db OWNER jobapp_user;

-- Donner les permissions
GRANT ALL PRIVILEGES ON DATABASE jobapp_db TO jobapp_user;

-- Quitter
\q
```

3. **Mettre à jour `.env`** :
```env
DATABASE_URL=postgresql://jobapp_user:votre_mot_de_passe_securise@localhost:5432/jobapp_db
```

### Option 3 : Utiliser PostgreSQL sans mot de passe (développement local)

Si PostgreSQL est configuré pour accepter les connexions locales sans mot de passe :

1. **Vérifier la configuration** :
```bash
sudo cat /etc/postgresql/*/main/pg_hba.conf | grep local
```

2. **Si nécessaire, modifier pg_hba.conf** :
```bash
sudo nano /etc/postgresql/*/main/pg_hba.conf
```

Changer cette ligne :
```
local   all             all                                     peer
```

En :
```
local   all             all                                     trust
```

3. **Redémarrer PostgreSQL** :
```bash
sudo systemctl restart postgresql
```

4. **Mettre à jour `.env`** :
```env
DATABASE_URL=postgresql://postgres@localhost:5432/jobapp_db
```

## Vérifier la Connexion

### Tester la connexion manuellement
```bash
psql -U postgres -d jobapp_db
# ou
psql -U jobapp_user -d jobapp_db
```

### Vérifier que PostgreSQL est démarré
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql  # Si arrêté
```

## Créer la Base de Données

Si la base de données n'existe pas encore :

```bash
sudo -u postgres psql
```

Puis dans psql :
```sql
CREATE DATABASE jobapp_db;
\q
```

## Après Configuration

Une fois `.env` configuré correctement, relancer l'application :

```bash
source venv/bin/activate
python run.py
```

L'application créera automatiquement les tables au démarrage.

## Format de DATABASE_URL

Le format est :
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

Exemples :
- `postgresql://postgres:mypassword@localhost:5432/jobapp_db`
- `postgresql://user:pass@localhost:5432/jobapp_db`
- `postgresql://postgres@localhost:5432/jobapp_db` (sans mot de passe)

