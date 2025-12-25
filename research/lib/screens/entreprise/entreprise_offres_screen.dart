import 'package:flutter/material.dart';
import '../../services/offre_service.dart';
import '../../models/offre.dart';
import '../../screens/offres/offre_detail_screen.dart';
import 'entreprise_candidatures_screen.dart';

class EntrepriseOffresScreen extends StatefulWidget {
  const EntrepriseOffresScreen({super.key});

  @override
  State<EntrepriseOffresScreen> createState() => _EntrepriseOffresScreenState();
}

class _EntrepriseOffresScreenState extends State<EntrepriseOffresScreen> {
  final _service = OffreService();
  List<Offre> _offres = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadOffres();
  }

  Future<void> _loadOffres() async {
    setState(() {
      _isLoading = true;
    });

    final offres = await _service.getMesOffres();
    setState(() {
      _offres = offres;
      _isLoading = false;
    });
  }

  Future<void> _deleteOffre(int offreId) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Supprimer l\'offre'),
        content: const Text('Êtes-vous sûr de vouloir supprimer cette offre ?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('Annuler'),
          ),
          TextButton(
            onPressed: () => Navigator.of(context).pop(true),
            child: const Text('Supprimer', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      final success = await _service.deleteOffre(offreId);
      if (mounted) {
        if (success) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Offre supprimée')),
          );
          _loadOffres();
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Erreur lors de la suppression')),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mes offres'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _offres.isEmpty
              ? const Center(child: Text('Aucune offre publiée'))
              : RefreshIndicator(
                  onRefresh: _loadOffres,
                  child: ListView.builder(
                    itemCount: _offres.length,
                    itemBuilder: (context, index) {
                      final offre = _offres[index];
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        child: ListTile(
                          title: Text(
                            offre.titre,
                            style: const TextStyle(fontWeight: FontWeight.bold),
                          ),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const SizedBox(height: 4),
                              Text(offre.description, maxLines: 2, overflow: TextOverflow.ellipsis),
                              const SizedBox(height: 8),
                              Row(
                                children: [
                                  Chip(
                                    label: Text(offre.type),
                                    labelStyle: const TextStyle(fontSize: 12),
                                  ),
                                  const SizedBox(width: 8),
                                  Chip(
                                    label: Text(offre.statut),
                                    labelStyle: const TextStyle(fontSize: 12),
                                    backgroundColor: offre.statut == 'active'
                                        ? Colors.green.shade100
                                        : Colors.grey.shade300,
                                  ),
                                ],
                              ),
                            ],
                          ),
                          trailing: PopupMenuButton(
                            itemBuilder: (context) => [
                              const PopupMenuItem(
                                value: 'view',
                                child: Text('Voir'),
                              ),
                              const PopupMenuItem(
                                value: 'candidatures',
                                child: Text('Candidatures'),
                              ),
                              const PopupMenuItem(
                                value: 'delete',
                                child: Text('Supprimer', style: TextStyle(color: Colors.red)),
                              ),
                            ],
                            onSelected: (value) {
                              if (value == 'view') {
                                Navigator.of(context).push(
                                  MaterialPageRoute(
                                    builder: (_) => OffreDetailScreen(offre: offre),
                                  ),
                                );
                              } else if (value == 'candidatures') {
                                Navigator.of(context).push(
                                  MaterialPageRoute(
                                    builder: (_) => EntrepriseCandidaturesScreen(offreId: offre.id),
                                  ),
                                );
                              } else if (value == 'delete') {
                                _deleteOffre(offre.id);
                              }
                            },
                          ),
                        ),
                      );
                    },
                  ),
                ),
    );
  }
}



