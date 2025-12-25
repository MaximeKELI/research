import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../services/candidature_service.dart';
import '../../models/candidature.dart';

class EntrepriseCandidaturesScreen extends StatefulWidget {
  final int offreId;

  const EntrepriseCandidaturesScreen({super.key, required this.offreId});

  @override
  State<EntrepriseCandidaturesScreen> createState() => _EntrepriseCandidaturesScreenState();
}

class _EntrepriseCandidaturesScreenState extends State<EntrepriseCandidaturesScreen> {
  final _service = CandidatureService();
  List<Candidature> _candidatures = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadCandidatures();
  }

  Future<void> _loadCandidatures() async {
    setState(() {
      _isLoading = true;
    });

    final candidatures = await _service.getCandidaturesOffre(widget.offreId);
    setState(() {
      _candidatures = candidatures;
      _isLoading = false;
    });
  }

  Future<void> _updateStatut(int candidatureId, String statut) async {
    final success = await _service.updateStatutCandidature(candidatureId, statut);
    if (mounted) {
      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Statut mis à jour: $statut')),
        );
        _loadCandidatures();
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Erreur lors de la mise à jour')),
        );
      }
    }
  }

  Color _getStatutColor(String statut) {
    switch (statut) {
      case 'accepté':
        return Colors.green;
      case 'refusé':
        return Colors.red;
      default:
        return Colors.orange;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Candidatures reçues'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _candidatures.isEmpty
              ? const Center(child: Text('Aucune candidature reçue'))
              : RefreshIndicator(
                  onRefresh: _loadCandidatures,
                  child: ListView.builder(
                    itemCount: _candidatures.length,
                    itemBuilder: (context, index) {
                      final candidature = _candidatures[index];
                      final candidat = candidature.candidat;
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        child: ExpansionTile(
                          title: Text(
                            candidat != null
                                ? '${candidat.prenom} ${candidat.nom}'
                                : 'Candidat #${candidature.candidatId}',
                            style: const TextStyle(fontWeight: FontWeight.bold),
                          ),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const SizedBox(height: 4),
                              Text(
                                'Postulé le: ${DateFormat('dd/MM/yyyy').format(candidature.datePostulation)}',
                              ),
                              const SizedBox(height: 4),
                              Chip(
                                label: Text(
                                  candidature.statut,
                                  style: const TextStyle(color: Colors.white, fontSize: 12),
                                ),
                                backgroundColor: _getStatutColor(candidature.statut),
                              ),
                            ],
                          ),
                          children: [
                            if (candidat != null) ...[
                              Padding(
                                padding: const EdgeInsets.all(16.0),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    if (candidat.niveauEtude != null)
                                      Text('Niveau d\'étude: ${candidat.niveauEtude}'),
                                    if (candidat.competences != null) ...[
                                      const SizedBox(height: 8),
                                      Text('Compétences: ${candidat.competences}'),
                                    ],
                                    if (candidat.cvUrl != null) ...[
                                      const SizedBox(height: 8),
                                      const Text('CV disponible'),
                                    ],
                                    const SizedBox(height: 16),
                                    Row(
                                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                      children: [
                                        if (candidature.statut == 'en_attente') ...[
                                          ElevatedButton.icon(
                                            onPressed: () => _updateStatut(
                                              candidature.id,
                                              'accepté',
                                            ),
                                            icon: const Icon(Icons.check),
                                            label: const Text('Accepter'),
                                            style: ElevatedButton.styleFrom(
                                              backgroundColor: Colors.green,
                                              foregroundColor: Colors.white,
                                            ),
                                          ),
                                          ElevatedButton.icon(
                                            onPressed: () => _updateStatut(
                                              candidature.id,
                                              'refusé',
                                            ),
                                            icon: const Icon(Icons.close),
                                            label: const Text('Refuser'),
                                            style: ElevatedButton.styleFrom(
                                              backgroundColor: Colors.red,
                                              foregroundColor: Colors.white,
                                            ),
                                          ),
                                        ],
                                      ],
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ],
                        ),
                      );
                    },
                  ),
                ),
    );
  }
}


