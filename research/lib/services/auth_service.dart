import 'package:shared_preferences/shared_preferences.dart';
import '../core/api_client.dart';
import '../models/user.dart';

class AuthService {
  final ApiClient _apiClient = ApiClient();

  Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      final formData = {
        'username': email, // OAuth2PasswordRequestForm utilise 'username'
        'password': password,
      };
      
      final response = await _apiClient.dio.post(
        '/auth/login',
        data: formData,
        options: Options(
          contentType: Headers.formUrlEncodedContentType,
        ),
      );
      
      final token = response.data['access_token'];
      await _apiClient.setToken(token);
      
      // Récupérer les infos utilisateur
      final userResponse = await _apiClient.dio.get('/auth/me');
      final user = User.fromJson(userResponse.data);
      
      // Sauvegarder les infos utilisateur
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('user_email', user.email);
      await prefs.setString('user_role', user.role);
      await prefs.setInt('user_id', user.id);
      
      return {
        'success': true,
        'user': user,
        'token': token,
      };
    } catch (e) {
      return {
        'success': false,
        'error': e.toString(),
      };
    }
  }

  Future<Map<String, dynamic>> register(
    String email,
    String password,
    String role,
  ) async {
    try {
      final response = await _apiClient.dio.post(
        '/auth/register',
        data: {
          'email': email,
          'mot_de_passe': password,
          'role': role,
        },
      );
      
      return {
        'success': true,
        'user': User.fromJson(response.data),
      };
    } catch (e) {
      return {
        'success': false,
        'error': e.toString(),
      };
    }
  }

  Future<void> logout() async {
    await _apiClient.clearToken();
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('user_email');
    await prefs.remove('user_role');
    await prefs.remove('user_id');
  }

  Future<bool> isLoggedIn() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    return token != null;
  }

  Future<String?> getUserRole() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('user_role');
  }
}

