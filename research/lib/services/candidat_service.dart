import 'package:dio/dio.dart';
import '../core/api_client.dart';
import '../models/profil_candidat.dart';
import 'dart:io';

class CandidatService {
  final ApiClient _apiClient = ApiClient();

  Future<ProfilCandidat?> getProfil() async {
    try {
      final response = await _apiClient.dio.get('/candidats/profil');
      return ProfilCandidat.fromJson(response.data);
    } catch (e) {
      return null;
    }
  }

  Future<ProfilCandidat?> createProfil({
    required String nom,
    required String prenom,
    String? niveauEtude,
    String? competences,
  }) async {
    try {
      final response = await _apiClient.dio.post(
        '/candidats/profil',
        data: {
          'nom': nom,
          'prenom': prenom,
          'niveau_etude': niveauEtude,
          'competences': competences,
        },
      );
      return ProfilCandidat.fromJson(response.data);
    } catch (e) {
      return null;
    }
  }

  Future<ProfilCandidat?> updateProfil({
    String? nom,
    String? prenom,
    String? niveauEtude,
    String? competences,
  }) async {
    try {
      final data = <String, dynamic>{};
      if (nom != null) data['nom'] = nom;
      if (prenom != null) data['prenom'] = prenom;
      if (niveauEtude != null) data['niveau_etude'] = niveauEtude;
      if (competences != null) data['competences'] = competences;

      final response = await _apiClient.dio.put(
        '/candidats/profil',
        data: data,
      );
      return ProfilCandidat.fromJson(response.data);
    } catch (e) {
      return null;
    }
  }

  Future<bool> uploadCV(File file) async {
    try {
      final formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(file.path, filename: file.path.split('/').last),
      });

      await _apiClient.dio.post(
        '/candidats/upload-cv',
        data: formData,
      );
      return true;
    } catch (e) {
      return false;
    }
  }
}

