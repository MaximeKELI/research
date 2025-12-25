import '../core/api_client.dart';
import '../models/candidature.dart';

class CandidatureService {
  final ApiClient _apiClient = ApiClient();

  Future<Candidature?> postuler(int offreId) async {
    try {
      final response = await _apiClient.dio.post(
        '/candidatures/',
        data: {'offre_id': offreId},
      );
      return Candidature.fromJson(response.data);
    } catch (e) {
      return null;
    }
  }

  Future<List<Candidature>> getMesCandidatures() async {
    try {
      final response = await _apiClient.dio.get('/candidatures/mes-candidatures');
      return (response.data as List)
          .map((json) => Candidature.fromJson(json))
          .toList();
    } catch (e) {
      return [];
    }
  }

  Future<List<Candidature>> getCandidaturesOffre(int offreId) async {
    try {
      final response = await _apiClient.dio.get('/candidatures/entreprise/$offreId');
      return (response.data as List)
          .map((json) => Candidature.fromJson(json))
          .toList();
    } catch (e) {
      return [];
    }
  }

  Future<bool> updateStatutCandidature(int candidatureId, String statut) async {
    try {
      await _apiClient.dio.put(
        '/candidatures/$candidatureId',
        data: {'statut': statut},
      );
      return true;
    } catch (e) {
      return false;
    }
  }
}



