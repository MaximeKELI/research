#!/bin/bash

echo "🗄️  Configuration de PostgreSQL pour JobApp"
echo "=========================================="
echo ""

# Vérifier si PostgreSQL est installé
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL n'est pas installé."
    echo "Installez-le avec: sudo apt-get install postgresql postgresql-contrib"
    exit 1
fi

# Vérifier si PostgreSQL est démarré
if ! sudo systemctl is-active --quiet postgresql; then
    echo "⚠️  PostgreSQL n'est pas démarré. Démarrage..."
    sudo systemctl start postgresql
fi

echo "✅ PostgreSQL est actif"
echo ""

# Demander les informations
read -p "Nom d'utilisateur PostgreSQL (défaut: postgres): " DB_USER
DB_USER=${DB_USER:-postgres}

read -sp "Mot de passe pour $DB_USER: " DB_PASSWORD
echo ""

read -p "Nom de la base de données (défaut: jobapp_db): " DB_NAME
DB_NAME=${DB_NAME:-jobapp_db}

# Créer la base de données
echo ""
echo "📦 Création de la base de données..."
sudo -u postgres psql <<EOF
-- Créer la base de données si elle n'existe pas
SELECT 'CREATE DATABASE $DB_NAME'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec

-- Afficher les bases de données
\l
EOF

if [ $? -eq 0 ]; then
    echo "✅ Base de données '$DB_NAME' créée ou existe déjà"
else
    echo "❌ Erreur lors de la création de la base de données"
    exit 1
fi

# Mettre à jour le fichier .env
echo ""
echo "📝 Mise à jour du fichier .env..."

# Générer une clé secrète aléatoire
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

cat > .env <<EOF
# Configuration PostgreSQL
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@localhost:5432/${DB_NAME}
SECRET_KEY=${SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=uploads
EOF

echo "✅ Fichier .env mis à jour"
echo ""
echo "🔐 Configuration terminée !"
echo ""
echo "Vous pouvez maintenant lancer l'application avec:"
echo "  source venv/bin/activate"
echo "  python run.py"

