import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../providers/auth_provider.dart';
import 'candidat/candidat_home.dart';
import 'entreprise/entreprise_home.dart';
import 'admin/admin_home.dart';
import 'auth/login_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String? _userRole;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadUserRole();
  }

  Future<void> _loadUserRole() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final role = prefs.getString('user_role');
      
      // Si pas de rôle dans SharedPreferences, vérifier dans le provider
      if (role == null) {
        final authProvider = Provider.of<AuthProvider>(context, listen: false);
        if (authProvider.user != null) {
          setState(() {
            _userRole = authProvider.user!.role;
            _isLoading = false;
          });
          return;
        }
      }
      
      setState(() {
        _userRole = role;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Widget _getHomeScreen() {
    switch (_userRole) {
      case 'candidat':
        return const CandidatHome();
      case 'entreprise':
        return const EntrepriseHome();
      case 'admin':
        return const AdminHome();
      default:
        // Si pas de rôle, rediriger vers login
        return const LoginScreen();
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    // Si pas de rôle après chargement, rediriger vers login
    if (_userRole == null) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (_) => const LoginScreen()),
        );
      });
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return _getHomeScreen();
  }
}

