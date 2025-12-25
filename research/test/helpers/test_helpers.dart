import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../lib/providers/auth_provider.dart';
import '../../lib/providers/offre_provider.dart';

/// Helper pour créer un widget de test avec tous les providers
Widget createTestWidget(Widget child) {
  return MultiProvider(
    providers: [
      ChangeNotifierProvider(create: (_) => AuthProvider()),
      ChangeNotifierProvider(create: (_) => OffreProvider()),
    ],
    child: MaterialApp(
      home: child,
    ),
  );
}

/// Helper pour créer des données de test
class TestData {
  static Map<String, dynamic> get testUser => {
        'id': 1,
        'email': 'test@test.com',
        'role': 'candidat',
        'created_at': '2024-01-01T00:00:00Z',
      };

  static Map<String, dynamic> get testOffre => {
        'id': 1,
        'entreprise_id': 1,
        'titre': 'Test Offre',
        'description': 'Description test',
        'type': 'emploi',
        'lieu': 'Paris',
        'statut': 'active',
        'created_at': '2024-01-01T00:00:00Z',
      };

  static Map<String, dynamic> get testProfilCandidat => {
        'id': 1,
        'user_id': 1,
        'nom': 'Doe',
        'prenom': 'John',
        'niveau_etude': 'Master',
        'competences': 'Python, Flutter',
        'created_at': '2024-01-01T00:00:00Z',
      };
}

