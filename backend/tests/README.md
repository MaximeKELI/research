# Tests Backend

## Structure des Tests

```
tests/
├── __init__.py
├── conftest.py              # Configuration et fixtures
├── test_auth.py             # Tests d'authentification
├── test_candidats.py        # Tests candidats
├── test_offres.py           # Tests offres
├── test_candidatures.py     # Tests candidatures
├── test_database.py         # Tests base de données
└── test_integration.py      # Tests d'intégration
```

## Installation

```bash
cd backend
pip install -r requirements.txt
```

Les dépendances de test sont incluses dans `requirements.txt`.

## Lancer les Tests

### Tous les tests
```bash
pytest
```

### Avec verbose
```bash
pytest -v
```

### Un fichier spécifique
```bash
pytest tests/test_auth.py
```

### Une fonction spécifique
```bash
pytest tests/test_auth.py::TestAuth::test_login_success
```

### Avec coverage
```bash
pytest --cov=app --cov-report=html
```

Le rapport HTML sera généré dans `htmlcov/index.html`.

### Script de lancement
```bash
./run_tests.sh
```

## Configuration

Les tests utilisent SQLite en mémoire pour la rapidité. La configuration est dans `conftest.py`.

## Fixtures Disponibles

- `db`: Session de base de données de test
- `client`: Client FastAPI de test
- `test_user_candidat`: Utilisateur candidat de test
- `test_user_entreprise`: Utilisateur entreprise de test
- `test_user_admin`: Utilisateur admin de test
- `auth_token_candidat`: Token JWT pour candidat
- `auth_token_entreprise`: Token JWT pour entreprise
- `auth_token_admin`: Token JWT pour admin

## Types de Tests

### Tests Unitaires
- **Auth**: Inscription, connexion, validation
- **Candidats**: CRUD profil, upload CV
- **Offres**: CRUD offres, filtres, recherche
- **Candidatures**: Postulation, gestion statut

### Tests Base de Données
- Contraintes d'unicité
- Relations et clés étrangères
- Suppression en cascade

### Tests d'Intégration
- Workflows complets utilisateur
- Communication entre modules
- Scénarios réels d'utilisation

## Exemple de Test

```python
def test_example(client, auth_token_candidat):
    response = client.get(
        "/api/candidats/profil",
        headers={"Authorization": f"Bearer {auth_token_candidat}"}
    )
    assert response.status_code == 200
```

## Coverage

Le coverage est configuré pour afficher:
- Rapport terminal avec lignes manquantes
- Rapport HTML interactif

Objectif: >80% de couverture de code.



