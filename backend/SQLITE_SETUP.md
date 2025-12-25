# 🗄️ Configuration SQLite

## ✅ Configuration Terminée !

L'application est maintenant configurée pour utiliser **SQLite** au lieu de PostgreSQL.

### Avantages de SQLite pour le développement :
- ✅ Pas besoin d'installer/configurer PostgreSQL
- ✅ Pas de mot de passe à gérer
- ✅ Base de données dans un fichier simple (`jobapp.db`)
- ✅ Parfait pour le développement et les tests

## 📁 Fichier de Base de Données

La base de données sera créée automatiquement dans :
```
backend/jobapp.db
```

## 🚀 Lancer l'Application

```bash
cd ~/Research_App/backend
source venv/bin/activate
python run.py
```

La base de données et toutes les tables seront créées automatiquement au premier lancement !

## 🔄 Passer à PostgreSQL Plus Tard

Si vous voulez utiliser PostgreSQL plus tard, modifiez simplement le fichier `.env` :

```env
# Décommentez et configurez PostgreSQL
DATABASE_URL=postgresql://postgres:password@localhost:5432/jobapp_db
```

L'application détectera automatiquement le type de base de données.

## 📊 Vérifier la Base de Données

Pour voir le contenu de la base SQLite :

```bash
sqlite3 backend/jobapp.db
.tables
.schema
.quit
```

Ou avec un outil graphique comme DB Browser for SQLite.

## ✅ Prêt !

Vous pouvez maintenant lancer l'application sans configuration supplémentaire !

