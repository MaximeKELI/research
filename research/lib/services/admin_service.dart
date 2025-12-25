import 'package:dio/dio.dart';
import '../core/api_client.dart';

class AdminService {
  final ApiClient _apiClient = ApiClient();
  
  Dio get dio => _apiClient.dio;

  Future<Map<String, dynamic>?> getStatistiques() async {
    try {
      final response = await _apiClient.dio.get('/admin/statistiques');
      return response.data as Map<String, dynamic>;
    } on DioException {
      return null;
    } catch (e) {
      return null;
    }
  }

  Future<List<int>?> exportCSV(String dataType) async {
    try {
      final response = await _apiClient.dio.get(
        '/admin/export/csv',
        queryParameters: {'data_type': dataType},
        options: Options(
          responseType: ResponseType.bytes,
        ),
      );
      
      if (response.statusCode == 200) {
        return response.data as List<int>;
      }
      return null;
    } catch (e) {
      return null;
    }
  }

  Future<List<int>?> exportPDF() async {
    try {
      final response = await _apiClient.dio.get(
        '/admin/export/pdf',
        options: Options(
          responseType: ResponseType.bytes,
        ),
      );
      
      if (response.statusCode == 200) {
        return response.data as List<int>;
      }
      return null;
    } catch (e) {
      return null;
    }
  }
}

