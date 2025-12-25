import 'package:flutter_test/flutter_test.dart';
import 'package:research/providers/auth_provider.dart';
import 'package:research/services/auth_service.dart';
import 'package:mocktail/mocktail.dart';

class MockAuthService extends Mock implements AuthService {}

void main() {
  late AuthProvider authProvider;
  late MockAuthService mockAuthService;

  setUp(() {
    mockAuthService = MockAuthService();
    authProvider = AuthProvider();
  });

  group('AuthProvider', () {
    test('initial state should be unauthenticated', () {
      expect(authProvider.isAuthenticated, false);
      expect(authProvider.user, isNull);
      expect(authProvider.isLoading, false);
    });

    test('clearError should clear error message', () {
      // Simuler une erreur
      authProvider.clearError();
      expect(authProvider.error, isNull);
    });
  });
}

