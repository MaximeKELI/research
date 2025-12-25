import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../core/api_client.dart';
import '../models/user.dart';

class AuthService {
  final ApiClient _apiClient = ApiClient();

  Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      // Pour form-urlencoded, utiliser un Map directement
      final formData = {
        'username': email, // OAuth2PasswordRequestForm utilise 'username'
        'password': password,
      };
      
      final response = await _apiClient.dio.post(
        '/auth/login',
        data: formData,
        options: Options(
          contentType: Headers.formUrlEncodedContentType,
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        ),
      );
      
      if (response.statusCode == 200 && response.data != null) {
        final token = response.data['access_token'];
        if (token == null) {
          return {
            'success': false,
            'error': 'Token non reçu du serveur',
          };
        }
        
        await _apiClient.setToken(token);
        
        // Récupérer les infos utilisateur
        try {
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
          // Si la récupération de l'utilisateur échoue, on retourne quand même le succès
          return {
            'success': true,
            'user': null,
            'token': token,
          };
        }
      } else {
        return {
          'success': false,
          'error': 'Réponse invalide du serveur',
        };
      }
    } on DioException catch (e) {
      String errorMessage = 'Erreur de connexion';
      if (e.response != null) {
        errorMessage = e.response?.data['detail'] ?? 
                      e.response?.data['message'] ?? 
                      'Erreur ${e.response?.statusCode}';
      } else if (e.type == DioExceptionType.connectionTimeout) {
        errorMessage = 'Timeout de connexion. Vérifiez que le serveur est démarré.';
      } else if (e.type == DioExceptionType.connectionError) {
        errorMessage = 'Impossible de se connecter au serveur. Vérifiez l\'URL de l\'API.';
      }
      
      return {
        'success': false,
        'error': errorMessage,
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
      
      if (response.statusCode == 201 && response.data != null) {
        return {
          'success': true,
          'user': User.fromJson(response.data),
        };
      } else {
        return {
          'success': false,
          'error': 'Réponse invalide du serveur',
        };
      }
    } on DioException catch (e) {
      String errorMessage = 'Erreur d\'inscription';
      if (e.response != null) {
        errorMessage = e.response?.data['detail'] ?? 
                      e.response?.data['message'] ?? 
                      'Erreur ${e.response?.statusCode}';
        
        // Gérer les erreurs spécifiques
        if (e.response?.statusCode == 400) {
          final detail = e.response?.data['detail'];
          if (detail is String) {
            errorMessage = detail;
          } else if (detail is List && detail.isNotEmpty) {
            errorMessage = detail[0]['msg'] ?? detail.toString();
          }
        }
      } else if (e.type == DioExceptionType.connectionTimeout) {
        errorMessage = 'Timeout de connexion. Vérifiez que le serveur est démarré.';
      } else if (e.type == DioExceptionType.connectionError) {
        errorMessage = 'Impossible de se connecter au serveur. Vérifiez l\'URL de l\'API.';
      }
      
      return {
        'success': false,
        'error': errorMessage,
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

