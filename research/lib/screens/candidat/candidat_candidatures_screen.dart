import 'package:flutter/material.dart';
import '../../services/candidature_service.dart';
import '../../models/candidature.dart';
import 'package:intl/intl.dart';

class CandidatCandidaturesScreen extends StatefulWidget {
  const CandidatCandidaturesScreen({super.key});

  @override
  State<CandidatCandidaturesScreen> createState() => _CandidatCandidaturesScreenState();
}

class _CandidatCandidaturesScreenState extends State<CandidatCandidaturesScreen> {
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

    final candidatures = await _service.getMesCandidatures();
    setState(() {
      _candidatures = candidatures;
      _isLoading = false;
    });
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
        title: const Text('Mes candidatures'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _candidatures.isEmpty
              ? const Center(child: Text('Aucune candidature'))
              : RefreshIndicator(
                  onRefresh: _loadCandidatures,
                  child: ListView.builder(
                    itemCount: _candidatures.length,
                    itemBuilder: (context, index) {
                      final candidature = _candidatures[index];
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        child: ListTile(
                          title: Text(
                            candidature.offre?.titre ?? 'Offre #${candidature.offreId}',
                            style: const TextStyle(fontWeight: FontWeight.bold),
                          ),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const SizedBox(height: 4),
                              Text(
                                'Postulé le: ${DateFormat('dd/MM/yyyy').format(candidature.datePostulation)}',
                              ),
                              if (candidature.offre?.lieu != null)
                                Text('Lieu: ${candidature.offre!.lieu}'),
                            ],
                          ),
                          trailing: Chip(
                            label: Text(
                              candidature.statut,
                              style: const TextStyle(color: Colors.white, fontSize: 12),
                            ),
                            backgroundColor: _getStatutColor(candidature.statut),
                          ),
                        ),
                      );
                    },
                  ),
                ),
    );
  }
}


