#!/bin/bash

echo "🗄️  Création de la Base de Données PostgreSQL pour JobApp"
echo "=========================================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Vérifier si PostgreSQL est installé
if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ PostgreSQL n'est pas installé.${NC}"
    echo ""
    echo "Installez PostgreSQL avec:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install postgresql postgresql-contrib"
    exit 1
fi

echo -e "${GREEN}✅ PostgreSQL est installé${NC}"
echo ""

# Vérifier si PostgreSQL est démarré
if ! systemctl is-active --quiet postgresql 2>/dev/null; then
    echo -e "${YELLOW}⚠️  PostgreSQL n'est pas démarré.${NC}"
    echo "Démarrage de PostgreSQL..."
    sudo systemctl start postgresql
    sleep 2
fi

if systemctl is-active --quiet postgresql 2>/dev/null; then
    echo -e "${GREEN}✅ PostgreSQL est actif${NC}"
else
    echo -e "${RED}❌ Impossible de démarrer PostgreSQL${NC}"
    echo "Essayez manuellement: sudo systemctl start postgresql"
    exit 1
fi

echo ""
echo "📝 Configuration de la base de données..."
echo ""

# Demander les informations
read -p "Nom d'utilisateur PostgreSQL (défaut: postgres): " DB_USER
DB_USER=${DB_USER:-postgres}

read -sp "Mot de passe pour $DB_USER (laisser vide si pas de mot de passe): " DB_PASSWORD
echo ""

read -p "Nom de la base de données (défaut: jobapp_db): " DB_NAME
DB_NAME=${DB_NAME:-jobapp_db}

echo ""
echo "🔨 Création de la base de données..."

# Créer un script SQL temporaire
SQL_FILE=$(mktemp)
cat > "$SQL_FILE" <<EOF
-- Vérifier si la base existe déjà
SELECT 'CREATE DATABASE $DB_NAME'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec

-- Afficher un message de confirmation
\echo ''
\echo 'Base de données créée avec succès!'
\echo ''
EOF

# Exécuter le script SQL
if [ -z "$DB_PASSWORD" ]; then
    # Sans mot de passe
    sudo -u postgres psql -f "$SQL_FILE"
else
    # Avec mot de passe (utiliser PGPASSWORD)
    export PGPASSWORD="$DB_PASSWORD"
    psql -U "$DB_USER" -h localhost -f "$SQL_FILE"
    unset PGPASSWORD
fi

RESULT=$?
rm "$SQL_FILE"

if [ $RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ Base de données '$DB_NAME' créée ou existe déjà${NC}"
else
    echo -e "${RED}❌ Erreur lors de la création de la base de données${NC}"
    echo ""
    echo "Essayez manuellement:"
    echo "  sudo -u postgres psql"
    echo "  CREATE DATABASE $DB_NAME;"
    exit 1
fi

# Vérifier que la base existe
echo ""
echo "🔍 Vérification de la base de données..."
if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo -e "${GREEN}✅ Base de données '$DB_NAME' trouvée${NC}"
else
    echo -e "${YELLOW}⚠️  La base de données n'a pas été trouvée dans la liste${NC}"
fi

# Générer une clé secrète
echo ""
echo "🔐 Génération de la clé secrète..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -base64 32)

# Mettre à jour le fichier .env
echo ""
echo "📝 Mise à jour du fichier .env..."

if [ -z "$DB_PASSWORD" ]; then
    DATABASE_URL="postgresql://${DB_USER}@localhost:5432/${DB_NAME}"
else
    DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@localhost:5432/${DB_NAME}"
fi

cat > .env <<EOF
# Configuration PostgreSQL
DATABASE_URL=${DATABASE_URL}
SECRET_KEY=${SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=uploads
EOF

echo -e "${GREEN}✅ Fichier .env mis à jour${NC}"
echo ""
echo "=========================================="
echo -e "${GREEN}🎉 Configuration terminée !${NC}"
echo "=========================================="
echo ""
echo "📋 Résumé:"
echo "  - Base de données: $DB_NAME"
echo "  - Utilisateur: $DB_USER"
echo "  - Fichier .env: configuré"
echo ""
echo "🚀 Vous pouvez maintenant lancer l'application:"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""

