import 'package:flutter_test/flutter_test.dart';
import '../../lib/providers/auth_provider.dart';

void main() {
  late AuthProvider authProvider;

  setUp(() {
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

