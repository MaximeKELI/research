import 'package:flutter_test/flutter_test.dart';
import '../lib/models/user.dart';
import '../lib/models/profil_candidat.dart';
import '../lib/models/entreprise.dart';
import '../lib/models/offre.dart';
import '../lib/models/candidature.dart';

void main() {
  group('User Model', () {
    test('should create User from JSON', () {
      final json = {
        'id': 1,
        'email': 'test@test.com',
        'role': 'candidat',
        'created_at': '2024-01-01T00:00:00Z',
      };

      final user = User.fromJson(json);

      expect(user.id, 1);
      expect(user.email, 'test@test.com');
      expect(user.role, 'candidat');
    });

    test('should convert User to JSON', () {
      final user = User(
        id: 1,
        email: 'test@test.com',
        role: 'candidat',
        createdAt: DateTime.parse('2024-01-01T00:00:00Z'),
      );

      final json = user.toJson();

      expect(json['id'], 1);
      expect(json['email'], 'test@test.com');
      expect(json['role'], 'candidat');
    });
  });

  group('ProfilCandidat Model', () {
    test('should create ProfilCandidat from JSON', () {
      final json = {
        'id': 1,
        'user_id': 1,
        'nom': 'Doe',
        'prenom': 'John',
        'niveau_etude': 'Master',
        'competences': 'Python, Flutter',
        'cv_url': null,
        'created_at': '2024-01-01T00:00:00Z',
      };

      final profil = ProfilCandidat.fromJson(json);

      expect(profil.id, 1);
      expect(profil.nom, 'Doe');
      expect(profil.prenom, 'John');
      expect(profil.niveauEtude, 'Master');
      expect(profil.competences, 'Python, Flutter');
    });
  });

  group('Entreprise Model', () {
    test('should create Entreprise from JSON', () {
      final json = {
        'id': 1,
        'user_id': 1,
        'nom': 'Test Company',
        'secteur': 'IT',
        'description': 'Description',
        'contact': 'contact@test.com',
        'validee': true,
        'created_at': '2024-01-01T00:00:00Z',
      };

      final entreprise = Entreprise.fromJson(json);

      expect(entreprise.id, 1);
      expect(entreprise.nom, 'Test Company');
      expect(entreprise.validee, true);
    });
  });

  group('Offre Model', () {
    test('should create Offre from JSON', () {
      final json = {
        'id': 1,
        'entreprise_id': 1,
        'titre': 'Développeur Python',
        'description': 'Description',
        'type': 'emploi',
        'lieu': 'Paris',
        'salaire': '3000€',
        'date_limite': '2024-12-31',
        'statut': 'active',
        'created_at': '2024-01-01T00:00:00Z',
      };

      final offre = Offre.fromJson(json);

      expect(offre.id, 1);
      expect(offre.titre, 'Développeur Python');
      expect(offre.type, 'emploi');
      expect(offre.lieu, 'Paris');
    });
  });

  group('Candidature Model', () {
    test('should create Candidature from JSON', () {
      final json = {
        'id': 1,
        'candidat_id': 1,
        'offre_id': 1,
        'date_postulation': '2024-01-01T00:00:00Z',
        'statut': 'en_attente',
      };

      final candidature = Candidature.fromJson(json);

      expect(candidature.id, 1);
      expect(candidature.candidatId, 1);
      expect(candidature.offreId, 1);
      expect(candidature.statut, 'en_attente');
    });
  });
}

