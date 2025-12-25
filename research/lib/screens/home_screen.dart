import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';
import 'candidat/candidat_home.dart';
import 'entreprise/entreprise_home.dart';
import 'admin/admin_home.dart';
import 'offres/offres_list_screen.dart';
import 'auth/login_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String? _userRole;

  @override
  void initState() {
    super.initState();
    _loadUserRole();
  }

  Future<void> _loadUserRole() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _userRole = prefs.getString('user_role');
    });
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
        return const OffresListScreen();
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_userRole == null) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return _getHomeScreen();
  }
}

