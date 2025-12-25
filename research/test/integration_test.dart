import 'package:flutter_test/flutter_test.dart';
import 'package:research/core/api_client.dart';
import 'package:research/services/auth_service.dart';
import 'package:research/services/offre_service.dart';
import 'package:research/services/candidat_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  group('Integration Tests', () {
    // Note: Ces tests nécessitent que le backend soit en cours d'exécution
    // Pour les tests d'intégration complets, utilisez un serveur de test

    test('API Client should be initialized', () {
      final apiClient = ApiClient();
      expect(apiClient, isNotNull);
      expect(apiClient.dio, isNotNull);
    });

    test('AuthService should be initialized', () {
      final authService = AuthService();
      expect(authService, isNotNull);
    });

    test('OffreService should be initialized', () {
      final offreService = OffreService();
      expect(offreService, isNotNull);
    });

    test('CandidatService should be initialized', () {
      final candidatService = CandidatService();
      expect(candidatService, isNotNull);
    });

    // Test d'intégration avec le backend (nécessite le serveur en cours d'exécution)
    // Décommentez et configurez l'URL de test pour activer
    /*
    test('Full integration test - Register and Login', () async {
      SharedPreferences.setMockInitialValues({});
      
      final authService = AuthService();
      
      // Inscription
      final registerResult = await authService.register(
        'integration_test@test.com',
        'password123',
        'candidat',
      );
      
      expect(registerResult['success'], true);
      
      // Connexion
      final loginResult = await authService.login(
        'integration_test@test.com',
        'password123',
      );
      
      expect(loginResult['success'], true);
      expect(loginResult['token'], isNotNull);
    });
    */
  });
}

