# 🚀 Commandes Exactes à Exécuter

## Étape 1 : Créer la Base de Données

Ouvrez un terminal et exécutez ces commandes **UNE PAR UNE** :

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql
```

Dans le prompt psql, tapez :
```sql
CREATE DATABASE jobapp_db;
\l
\q
```

## OU Utiliser le Script Automatique

```bash
cd ~/Research_App/backend
./quick_setup.sh
```

## Étape 2 : Vérifier que .env est Configuré

Le fichier `.env` a déjà été créé avec cette configuration :

```env
DATABASE_URL=postgresql://postgres@localhost:5432/jobapp_db
SECRET_KEY=k7t-9IK_iM_xoR_M9mFS7Md3ndHsxZPthbWi3IxfpPA
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=uploads
```

**Si PostgreSQL demande un mot de passe**, modifiez `.env` :

```bash
cd ~/Research_App/backend
nano .env
```

Et changez la ligne DATABASE_URL :
```env
DATABASE_URL=postgresql://postgres:VOTRE_MOT_DE_PASSE@localhost:5432/jobapp_db
```

## Étape 3 : Lancer l'Application

```bash
cd ~/Research_App/backend
source venv/bin/activate
python run.py
```

## Si PostgreSQL Demande un Mot de Passe

### Option A : Définir un mot de passe pour postgres

```bash
sudo -u postgres psql
ALTER USER postgres PASSWORD 'votre_mot_de_passe';
\q
```

Puis dans `.env` :
```env
DATABASE_URL=postgresql://postgres:votre_mot_de_passe@localhost:5432/jobapp_db
```

### Option B : Configurer PostgreSQL pour accepter les connexions sans mot de passe (développement)

```bash
sudo nano /etc/postgresql/*/main/pg_hba.conf
```

Trouvez cette ligne :
```
local   all             all                                     peer
```

Changez-la en :
```
local   all             all                                     trust
```

Puis redémarrez :
```bash
sudo systemctl restart postgresql
```

---

**Une fois la base créée, l'application devrait démarrer !** 🎉

