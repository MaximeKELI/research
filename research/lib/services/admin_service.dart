import 'package:dio/dio.dart';
import '../core/api_client.dart';

class AdminService {
  final ApiClient _apiClient = ApiClient();

  Future<Map<String, dynamic>?> getStatistiques() async {
    try {
      final response = await _apiClient.dio.get('/admin/statistiques');
      return response.data as Map<String, dynamic>;
    } on DioException catch (e) {
      return null;
    } catch (e) {
      return null;
    }
  }

  Future<bool> exportCSV(String dataType) async {
    try {
      final response = await _apiClient.dio.get(
        '/admin/export/csv',
        queryParameters: {'data_type': dataType},
        options: Options(
          responseType: ResponseType.bytes,
        ),
      );
      
      // Sauvegarder le fichier (sera géré par l'écran)
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  Future<bool> exportPDF() async {
    try {
      final response = await _apiClient.dio.get(
        '/admin/export/pdf',
        options: Options(
          responseType: ResponseType.bytes,
        ),
      );
      
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}

