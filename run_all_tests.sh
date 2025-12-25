#!/bin/bash

# Script pour lancer tous les tests (backend + frontend)

echo "🧪 =========================================="
echo "🧪 Lancement de TOUS les tests"
echo "🧪 =========================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend Tests
echo -e "${YELLOW}📦 Tests Backend (FastAPI)${NC}"
echo "----------------------------------------"
cd backend

if [ -d "venv" ]; then
    source venv/bin/activate
fi

if pytest tests/ -v --tb=short; then
    echo -e "${GREEN}✅ Tests backend réussis${NC}"
    BACKEND_SUCCESS=true
else
    echo -e "${RED}❌ Tests backend échoués${NC}"
    BACKEND_SUCCESS=false
fi

echo ""
cd ..

# Frontend Tests
echo -e "${YELLOW}📱 Tests Frontend (Flutter)${NC}"
echo "----------------------------------------"
cd research

if flutter test; then
    echo -e "${GREEN}✅ Tests frontend réussis${NC}"
    FRONTEND_SUCCESS=true
else
    echo -e "${RED}❌ Tests frontend échoués${NC}"
    FRONTEND_SUCCESS=false
fi

echo ""
cd ..

# Résumé
echo "🧪 =========================================="
echo "🧪 RÉSUMÉ"
echo "🧪 =========================================="

if [ "$BACKEND_SUCCESS" = true ] && [ "$FRONTEND_SUCCESS" = true ]; then
    echo -e "${GREEN}✅ Tous les tests sont passés !${NC}"
    exit 0
else
    echo -e "${RED}❌ Certains tests ont échoué${NC}"
    if [ "$BACKEND_SUCCESS" = false ]; then
        echo -e "${RED}  - Backend: ÉCHEC${NC}"
    fi
    if [ "$FRONTEND_SUCCESS" = false ]; then
        echo -e "${RED}  - Frontend: ÉCHEC${NC}"
    fi
    exit 1
fi

