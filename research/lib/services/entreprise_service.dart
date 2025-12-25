import 'package:dio/dio.dart';
import '../core/api_client.dart';
import '../models/entreprise.dart';
import 'dart:io';

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

  Future<bool> uploadPhoto(File file) async {
    try {
      final formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(file.path, filename: file.path.split('/').last),
      });

      final response = await _apiClient.dio.post(
        '/entreprises/upload-photo',
        data: formData,
      );
      return response.statusCode == 200;
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) {
        return false;
      }
      if (e.response?.statusCode == 400) {
        return false;
      }
      return false;
    } catch (e) {
      return false;
    }
  }
}



