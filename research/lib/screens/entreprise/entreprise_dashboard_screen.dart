import 'package:flutter/material.dart';
import 'entreprise_create_offre_screen.dart';

class EntrepriseDashboardScreen extends StatelessWidget {
  const EntrepriseDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    const Icon(Icons.business, size: 64, color: Colors.blue),
                    const SizedBox(height: 16),
                    const Text(
                      'Bienvenue sur votre tableau de bord',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      'Gérez vos offres et candidatures',
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (_) => const EntrepriseCreateOffreScreen(),
                  ),
                );
              },
              icon: const Icon(Icons.add),
              label: const Text('Publier une nouvelle offre'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
            ),
            const SizedBox(height: 16),
            Card(
              child: ListTile(
                leading: const Icon(Icons.work),
                title: const Text('Mes offres'),
                subtitle: const Text('Consultez et gérez vos offres'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () {
                  // Navigation gérée par le bottom nav
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}


