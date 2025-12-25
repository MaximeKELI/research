import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../screens/offres/offres_list_screen.dart';
import 'candidat_profil_screen.dart';
import 'candidat_candidatures_screen.dart';

class CandidatHome extends StatefulWidget {
  const CandidatHome({super.key});

  @override
  State<CandidatHome> createState() => _CandidatHomeState();
}

class _CandidatHomeState extends State<CandidatHome> {
  int _currentIndex = 0;

  final List<Widget> _screens = [
    const OffresListScreen(),
    const CandidatCandidaturesScreen(),
    const CandidatProfilScreen(),
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
            icon: Icon(Icons.search),
            label: 'Offres',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.description),
            label: 'Mes candidatures',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'Profil',
          ),
        ],
      ),
      appBar: AppBar(
        title: const Text('JobApp - Candidat'),
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

