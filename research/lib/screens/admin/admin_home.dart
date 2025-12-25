import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../screens/offres/offres_list_screen.dart';

class AdminHome extends StatelessWidget {
  const AdminHome({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('JobApp - Administration'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await Provider.of<AuthProvider>(context, listen: false).logout();
              if (context.mounted) {
                Navigator.of(context).pushReplacement(
                  MaterialPageRoute(builder: (_) => const OffresListScreen()),
                );
              }
            },
          ),
        ],
      ),
      body: const Center(
        child: Text('Espace Admin - À implémenter'),
      ),
    );
  }
}



