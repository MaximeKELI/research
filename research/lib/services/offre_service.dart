import '../core/api_client.dart';
import '../models/offre.dart';

class OffreService {
  final ApiClient _apiClient = ApiClient();

  Future<List<Offre>> getOffres({
    int skip = 0,
    int limit = 20,
    String? type,
    String? lieu,
    String? search,
  }) async {
    try {
      final queryParams = <String, dynamic>{
        'skip': skip,
        'limit': limit,
      };
      if (type != null) queryParams['type'] = type;
      if (lieu != null) queryParams['lieu'] = lieu;
      if (search != null) queryParams['search'] = search;

      final response = await _apiClient.dio.get(
        '/offres',
        queryParameters: queryParams,
      );
      
      return (response.data as List)
          .map((json) => Offre.fromJson(json))
          .toList();
    } catch (e) {
      return [];
    }
  }

  Future<Offre?> getOffre(int offreId) async {
    try {
      final response = await _apiClient.dio.get('/offres/$offreId');
      return Offre.fromJson(response.data);
    } catch (e) {
      return null;
    }
  }

  Future<Offre?> createOffre({
    required String titre,
    required String description,
    required String type,
    String? lieu,
    String? salaire,
    DateTime? dateLimite,
  }) async {
    try {
      final data = {
        'titre': titre,
        'description': description,
        'type': type,
        'lieu': lieu,
        'salaire': salaire,
        'date_limite': dateLimite?.toIso8601String().split('T')[0],
      };

      final response = await _apiClient.dio.post('/offres', data: data);
      return Offre.fromJson(response.data);
    } catch (e) {
      return null;
    }
  }

  Future<List<Offre>> getMesOffres() async {
    try {
      final response = await _apiClient.dio.get('/offres/entreprise/mes-offres');
      return (response.data as List)
          .map((json) => Offre.fromJson(json))
          .toList();
    } catch (e) {
      return [];
    }
  }

  Future<bool> deleteOffre(int offreId) async {
    try {
      await _apiClient.dio.delete('/offres/$offreId');
      return true;
    } catch (e) {
      return false;
    }
  }
}



