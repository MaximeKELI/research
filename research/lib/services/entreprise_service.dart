import '../core/api_client.dart';
import '../models/entreprise.dart';

class EntrepriseService {
  final ApiClient _apiClient = ApiClient();

  Future<Entreprise?> getProfil() async {
    try {
      final response = await _apiClient.dio.get('/entreprises/profil');
      return Entreprise.fromJson(response.data);
    } catch (e) {
      return null;
    }
  }

  Future<Entreprise?> createProfil({
    required String nom,
    String? secteur,
    String? description,
    String? contact,
  }) async {
    try {
      final response = await _apiClient.dio.post(
        '/entreprises/profil',
        data: {
          'nom': nom,
          'secteur': secteur,
          'description': description,
          'contact': contact,
        },
      );
      return Entreprise.fromJson(response.data);
    } catch (e) {
      return null;
    }
  }

  Future<Entreprise?> updateProfil({
    String? nom,
    String? secteur,
    String? description,
    String? contact,
  }) async {
    try {
      final data = <String, dynamic>{};
      if (nom != null) data['nom'] = nom;
      if (secteur != null) data['secteur'] = secteur;
      if (description != null) data['description'] = description;
      if (contact != null) data['contact'] = contact;

      final response = await _apiClient.dio.put(
        '/entreprises/profil',
        data: data,
      );
      return Entreprise.fromJson(response.data);
    } catch (e) {
      return null;
    }
  }
}

