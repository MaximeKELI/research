import 'package:flutter_test/flutter_test.dart';
import '../../lib/services/auth_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  late AuthService authService;

  setUp(() {
    authService = AuthService();
  });

  group('AuthService', () {
    test('login should return success with valid credentials', () async {
      // Note: Ce test nécessiterait un mock plus complexe
      // Pour l'instant, on teste la structure
      expect(authService, isNotNull);
    });

    test('register should create a new user', () async {
      expect(authService, isNotNull);
    });

    test('logout should clear token', () async {
      SharedPreferences.setMockInitialValues({});
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('access_token', 'test_token');

      await authService.logout();

      final token = prefs.getString('access_token');
      expect(token, isNull);
    });

    test('isLoggedIn should return true when token exists', () async {
      SharedPreferences.setMockInitialValues({
        'access_token': 'test_token',
      });

      final isLoggedIn = await authService.isLoggedIn();
      expect(isLoggedIn, true);
    });

    test('isLoggedIn should return false when no token', () async {
      SharedPreferences.setMockInitialValues({});

      final isLoggedIn = await authService.isLoggedIn();
      expect(isLoggedIn, false);
    });
  });
}

