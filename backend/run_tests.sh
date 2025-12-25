#!/bin/bash

# Script pour lancer tous les tests

echo "🧪 Lancement des tests backend..."

# Activer l'environnement virtuel si présent
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Lancer les tests avec coverage
pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html

echo ""
echo "✅ Tests terminés !"
echo "📊 Rapport de couverture généré dans htmlcov/index.html"



