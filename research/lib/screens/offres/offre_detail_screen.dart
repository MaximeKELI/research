import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../models/offre.dart';
import '../../services/candidature_service.dart';
import 'package:intl/intl.dart';

class OffreDetailScreen extends StatelessWidget {
  final Offre offre;

  const OffreDetailScreen({super.key, required this.offre});

  Future<void> _postuler(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    final userRole = prefs.getString('user_role');

    if (userRole != 'candidat') {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Seuls les candidats peuvent postuler'),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    final service = CandidatureService();
    final candidature = await service.postuler(offre.id);

    if (context.mounted) {
      if (candidature != null) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Candidature envoyée avec succès !'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Erreur lors de la candidature'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Détails de l\'offre'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              offre.titre,
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Chip(
                  label: Text(offre.type.toUpperCase()),
                  backgroundColor: Theme.of(context).colorScheme.primaryContainer,
                ),
                if (offre.lieu != null) ...[
                  const SizedBox(width: 8),
                  Icon(Icons.location_on, size: 20),
                  const SizedBox(width: 4),
                  Text(offre.lieu!),
                ],
              ],
            ),
            if (offre.salaire != null) ...[
              const SizedBox(height: 8),
              Row(
                children: [
                  const Icon(Icons.attach_money, size: 20),
                  const SizedBox(width: 4),
                  Text(offre.salaire!),
                ],
              ),
            ],
            if (offre.dateLimite != null) ...[
              const SizedBox(height: 8),
              Row(
                children: [
                  const Icon(Icons.calendar_today, size: 20),
                  const SizedBox(width: 4),
                  Text('Date limite: ${DateFormat('dd/MM/yyyy').format(offre.dateLimite!)}'),
                ],
              ),
            ],
            if (offre.entreprise != null) ...[
              const SizedBox(height: 16),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(12.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Entreprise',
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                              fontWeight: FontWeight.bold,
                            ),
                      ),
                      const SizedBox(height: 8),
                      Text(offre.entreprise!.nom),
                      if (offre.entreprise!.secteur != null)
                        Text('Secteur: ${offre.entreprise!.secteur}'),
                    ],
                  ),
                ),
              ),
            ],
            const SizedBox(height: 24),
            Text(
              'Description',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 8),
            Text(
              offre.description,
              style: Theme.of(context).textTheme.bodyLarge,
            ),
            const SizedBox(height: 32),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () => _postuler(context),
                icon: const Icon(Icons.send),
                label: const Text('Postuler'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}



