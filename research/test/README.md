# Tests Flutter

## Structure des Tests

```
test/
├── models_test.dart              # Tests des modèles de données
├── services/                     # Tests des services
│   └── auth_service_test.dart
├── providers/                    # Tests des providers
│   └── auth_provider_test.dart
├── widgets_test.dart             # Tests des widgets
├── integration_test.dart         # Tests d'intégration
└── helpers/                      # Helpers pour les tests
    └── test_helpers.dart
```

## Lancer les Tests

### Tous les tests
```bash
flutter test
```

### Un fichier spécifique
```bash
flutter test test/models_test.dart
```

### Avec coverage
```bash
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
```

## Types de Tests

### Tests Unitaires
- **Models**: Vérification de la sérialisation/désérialisation
- **Services**: Logique métier et appels API
- **Providers**: Gestion d'état

### Tests Widgets
- Interface utilisateur
- Interactions utilisateur
- Navigation

### Tests d'Intégration
- Communication complète avec le backend
- Workflows utilisateur complets

## Configuration

Pour les tests d'intégration avec le backend réel, configurez l'URL dans `lib/core/config.dart`:
```dart
static const String baseUrl = 'http://localhost:8000'; // ou votre URL de test
```

## Mocking

Utilisez `mocktail` pour créer des mocks:
```dart
class MockAuthService extends Mock implements AuthService {}
```

## Notes

- Les tests d'intégration nécessitent que le backend soit en cours d'exécution
- Utilisez `SharedPreferences.setMockInitialValues()` pour les tests de stockage
- Les tests asynchrones utilisent `await tester.pumpAndSettle()`

