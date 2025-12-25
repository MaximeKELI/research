import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../screens/offres/offres_list_screen.dart';
import 'entreprise_dashboard_screen.dart';
import 'entreprise_offres_screen.dart';
import 'entreprise_profil_screen.dart';

class EntrepriseHome extends StatefulWidget {
  const EntrepriseHome({super.key});

  @override
  State<EntrepriseHome> createState() => _EntrepriseHomeState();
}

class _EntrepriseHomeState extends State<EntrepriseHome> {
  int _currentIndex = 0;

  final List<Widget> _screens = [
    const EntrepriseDashboardScreen(),
    const EntrepriseOffresScreen(),
    const EntrepriseProfilScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.dashboard),
            label: 'Tableau de bord',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.work),
            label: 'Mes offres',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.business),
            label: 'Profil',
          ),
        ],
      ),
      appBar: AppBar(
        title: const Text('JobApp - Entreprise'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await Provider.of<AuthProvider>(context, listen: false).logout();
              if (mounted) {
                Navigator.of(context).pushReplacement(
                  MaterialPageRoute(builder: (_) => const OffresListScreen()),
                );
              }
            },
          ),
        ],
      ),
    );
  }
}

