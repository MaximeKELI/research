import 'package:flutter/material.dart';
import '../../services/entreprise_service.dart';
import '../../models/entreprise.dart';

class EntrepriseService {
  // Service pour gérer le profil entreprise
  // À implémenter selon les besoins
}

class EntrepriseProfilScreen extends StatelessWidget {
  const EntrepriseProfilScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Profil Entreprise'),
      ),
      body: const Center(
        child: Text('Profil entreprise - À implémenter'),
      ),
    );
  }
}

