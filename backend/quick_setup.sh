#!/bin/bash

echo "🗄️  Configuration Rapide de PostgreSQL"
echo "======================================"
echo ""

# Créer la base de données
echo "📦 Création de la base de données jobapp_db..."
sudo -u postgres psql -c "CREATE DATABASE jobapp_db;" 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Base de données créée avec succès!"
else
    echo "⚠️  La base de données existe peut-être déjà ou erreur de création"
fi

# Vérifier qu'elle existe
echo ""
echo "🔍 Vérification..."
sudo -u postgres psql -c "\l" | grep jobapp_db

# Générer une clé secrète
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || echo "change-this-secret-key-$(date +%s)")

# Mettre à jour .env
echo ""
echo "📝 Configuration du fichier .env..."
cat > .env <<EOF
# Configuration PostgreSQL
DATABASE_URL=postgresql://postgres@localhost:5432/jobapp_db
SECRET_KEY=${SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=uploads
EOF

echo "✅ Fichier .env configuré"
echo ""
echo "📋 Configuration:"
echo "  DATABASE_URL=postgresql://postgres@localhost:5432/jobapp_db"
echo "  SECRET_KEY=${SECRET_KEY}"
echo ""
echo "🚀 Vous pouvez maintenant lancer: python run.py"
echo ""

