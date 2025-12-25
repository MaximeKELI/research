# Guide Complet des Tests

Ce guide explique comment lancer et interpréter les tests pour l'application JobApp.

## 📋 Vue d'Ensemble

L'application dispose de tests pour:
- ✅ **Backend** (FastAPI): Tests unitaires, intégration, base de données
- ✅ **Frontend** (Flutter): Tests unitaires, widgets, intégration
- ✅ **Communication**: Tests d'intégration API

## 🚀 Backend - Tests FastAPI

### Prérequis
```bash
cd backend
pip install -r requirements.txt
```

### Lancer les Tests

#### Tous les tests
```bash
pytest
```

#### Avec rapport de couverture
```bash
pytest --cov=app --cov-report=html
# Ouvrir htmlcov/index.html dans le navigateur
```

#### Script automatique
```bash
./run_tests.sh
```

### Structure des Tests Backend

```
tests/
├── conftest.py              # Fixtures partagées
├── test_auth.py             # Authentification (8 tests)
├── test_candidats.py        # Gestion candidats (7 tests)
├── test_offres.py           # Gestion offres (8 tests)
├── test_candidatures.py     # Candidatures (4 tests)
├── test_database.py         # Base de données (10 tests)
└── test_integration.py      # Intégration (3 tests)
```

**Total: ~40 tests backend**

### Exemples de Tests

#### Test d'authentification
```bash
pytest tests/test_auth.py -v
```

#### Test de base de données
```bash
pytest tests/test_database.py -v
```

#### Test d'intégration complet
```bash
pytest tests/test_integration.py -v
```

## 📱 Frontend - Tests Flutter

### Prérequis
```bash
cd research
flutter pub get
```

### Lancer les Tests

#### Tous les tests
```bash
flutter test
```

#### Avec coverage
```bash
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

#### Un fichier spécifique
```bash
flutter test test/models_test.dart
```

### Structure des Tests Flutter

```
test/
├── models_test.dart              # Tests modèles (5 groupes)
├── services/
│   └── auth_service_test.dart    # Tests services
├── providers/
│   └── auth_provider_test.dart   # Tests providers
├── widgets_test.dart             # Tests widgets
├── integration_test.dart         # Tests d'intégration
└── helpers/
    └── test_helpers.dart         # Helpers
```

## 🔗 Tests d'Intégration API

### Prérequis
1. Backend en cours d'exécution sur `http://localhost:8000`
2. Base de données PostgreSQL configurée

### Lancer les Tests d'Intégration

#### Backend
```bash
cd backend
pytest tests/test_integration.py -v
```

#### Frontend (nécessite backend actif)
```bash
cd research
flutter test test/integration_test.dart
```

### Scénarios Testés

1. **Workflow Candidat Complet**
   - Inscription → Connexion → Création profil → Postulation

2. **Workflow Entreprise Complet**
   - Inscription → Connexion → Création profil → Validation → Publication offre

3. **Workflow Candidat Postule**
   - Candidat postule → Entreprise voit → Entreprise accepte → Candidat voit statut

## 📊 Interprétation des Résultats

### Backend

#### Succès
```
tests/test_auth.py::TestAuth::test_login_success PASSED
```

#### Échec
```
tests/test_auth.py::TestAuth::test_login_success FAILED
AssertionError: assert 401 == 200
```

#### Coverage
```
Name                      Stmts   Miss  Cover
----------------------------------------------
app/auth.py                  45      5    89%
app/routers/auth.py         30      2    93%
----------------------------------------------
TOTAL                       200     20    90%
```

### Frontend

#### Succès
```
✓ Models Test - User Model - should create User from JSON
```

#### Échec
```
✗ Models Test - User Model - should create User from JSON
Expected: 1
  Actual: 2
```

## 🐛 Dépannage

### Backend

#### Erreur: Module not found
```bash
pip install -r requirements.txt
```

#### Erreur: Database locked
Les tests utilisent SQLite en mémoire, pas de problème de verrouillage.

#### Erreur: Import error
Vérifier que vous êtes dans le dossier `backend/` et que l'environnement virtuel est activé.

### Frontend

#### Erreur: Package not found
```bash
flutter pub get
```

#### Erreur: Test timeout
Augmenter le timeout dans `test/integration_test.dart`:
```dart
setUpAll(() {
  // Configuration
});
```

## 📈 Améliorer la Couverture

### Backend
1. Ajouter des tests pour les cas limites
2. Tester les erreurs (400, 401, 403, 404)
3. Tester les validations de données

### Frontend
1. Tester tous les écrans
2. Tester les interactions utilisateur
3. Tester les cas d'erreur réseau

## ✅ Checklist de Tests

### Avant chaque commit
- [ ] Tous les tests backend passent
- [ ] Tous les tests frontend passent
- [ ] Coverage > 80%
- [ ] Aucun test en échec

### Avant chaque release
- [ ] Tests d'intégration complets
- [ ] Tests de performance
- [ ] Tests de sécurité
- [ ] Documentation des tests à jour

## 🔧 Configuration CI/CD

### GitHub Actions (exemple)

```yaml
name: Tests
on: [push, pull_request]
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: cd backend && pip install -r requirements.txt
      - run: cd backend && pytest --cov=app
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: subosito/flutter-action@v2
      - run: cd research && flutter test
```

## 📚 Ressources

- [Pytest Documentation](https://docs.pytest.org/)
- [Flutter Testing](https://docs.flutter.dev/testing)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

**Bon test ! 🧪**

