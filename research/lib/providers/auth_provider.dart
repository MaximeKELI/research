import 'package:flutter/foundation.dart';
import '../models/user.dart';
import '../services/auth_service.dart';

class AuthProvider with ChangeNotifier {
  final AuthService _authService = AuthService();
  User? _user;
  bool _isLoading = false;
  String? _error;

  User? get user => _user;
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get isAuthenticated => _user != null;

  Future<bool> checkAuth() async {
    _isLoading = true;
    notifyListeners();

    final isLoggedIn = await _authService.isLoggedIn();
    if (isLoggedIn) {
      // Récupérer les infos utilisateur depuis le token
      try {
        // On pourrait faire un appel API pour récupérer les infos complètes
        // Pour l'instant, on utilise les données stockées
        _user = null; // À améliorer avec un appel API
      } catch (e) {
        _error = e.toString();
      }
    }

    _isLoading = false;
    notifyListeners();
    return isLoggedIn;
  }

  Future<bool> login(String email, String password) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    final result = await _authService.login(email, password);
    
    if (result['success'] == true) {
      _user = result['user'];
      _error = null;
      _isLoading = false;
      notifyListeners();
      return true;
    } else {
      _error = result['error'] ?? 'Erreur de connexion';
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<bool> register(String email, String password, String role) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    final result = await _authService.register(email, password, role);
    
    if (result['success'] == true) {
      _user = result['user'];
      _error = null;
      _isLoading = false;
      notifyListeners();
      return true;
    } else {
      _error = result['error'] ?? 'Erreur d\'inscription';
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<void> logout() async {
    await _authService.logout();
    _user = null;
    _error = null;
    notifyListeners();
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }
}



