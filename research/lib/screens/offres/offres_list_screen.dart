import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/offre_provider.dart';
import '../../models/offre.dart';
import 'offre_detail_screen.dart';

class OffresListScreen extends StatefulWidget {
  const OffresListScreen({super.key});

  @override
  State<OffresListScreen> createState() => _OffresListScreenState();
}

class _OffresListScreenState extends State<OffresListScreen> {
  final _searchController = TextEditingController();
  String? _selectedType;
  String? _selectedLieu;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Provider.of<OffreProvider>(context, listen: false).loadOffres();
    });
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _search() {
    Provider.of<OffreProvider>(context, listen: false).loadOffres(
      type: _selectedType,
      lieu: _selectedLieu,
      search: _searchController.text.isEmpty ? null : _searchController.text,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Offres d\'emploi et stages'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              Provider.of<OffreProvider>(context, listen: false).refreshOffres();
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                TextField(
                  controller: _searchController,
                  decoration: InputDecoration(
                    hintText: 'Rechercher...',
                    prefixIcon: const Icon(Icons.search),
                    suffixIcon: IconButton(
                      icon: const Icon(Icons.clear),
                      onPressed: () {
                        _searchController.clear();
                        _search();
                      },
                    ),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  onSubmitted: (_) => _search(),
                ),
                const SizedBox(height: 12),
                Row(
                  children: [
                    Expanded(
                      child: DropdownButtonFormField<String>(
                        value: _selectedType,
                        decoration: const InputDecoration(
                          labelText: 'Type',
                          border: OutlineInputBorder(),
                          contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                        ),
                        items: const [
                          DropdownMenuItem(value: null, child: Text('Tous')),
                          DropdownMenuItem(value: 'stage', child: Text('Stage')),
                          DropdownMenuItem(value: 'emploi', child: Text('Emploi')),
                        ],
                        onChanged: (value) {
                          setState(() {
                            _selectedType = value;
                          });
                          _search();
                        },
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: TextField(
                        decoration: InputDecoration(
                          labelText: 'Lieu',
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                          contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                        ),
                        onChanged: (value) {
                          _selectedLieu = value.isEmpty ? null : value;
                          _search();
                        },
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          Expanded(
            child: Consumer<OffreProvider>(
              builder: (context, provider, _) {
                if (provider.isLoading) {
                  return const Center(child: CircularProgressIndicator());
                }

                if (provider.error != null) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text('Erreur: ${provider.error}'),
                        const SizedBox(height: 16),
                        ElevatedButton(
                          onPressed: () => provider.refreshOffres(),
                          child: const Text('Réessayer'),
                        ),
                      ],
                    ),
                  );
                }

                if (provider.offres.isEmpty) {
                  return const Center(
                    child: Text('Aucune offre trouvée'),
                  );
                }

                return RefreshIndicator(
                  onRefresh: () => provider.refreshOffres(),
                  child: ListView.builder(
                    itemCount: provider.offres.length,
                    itemBuilder: (context, index) {
                      final offre = provider.offres[index];
                      return _OffreCard(offre: offre);
                    },
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _OffreCard extends StatelessWidget {
  final Offre offre;

  const _OffreCard({required this.offre});

  @override
  Widget build(BuildContext context) {
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
            Text(
              offre.description,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Chip(
                  label: Text(offre.type),
                  labelStyle: const TextStyle(fontSize: 12),
                ),
                if (offre.lieu != null) ...[
                  const SizedBox(width: 8),
                  Icon(Icons.location_on, size: 16),
                  const SizedBox(width: 4),
                  Text(offre.lieu!),
                ],
              ],
            ),
          ],
        ),
        trailing: const Icon(Icons.chevron_right),
        onTap: () {
          Navigator.of(context).push(
            MaterialPageRoute(
              builder: (_) => OffreDetailScreen(offre: offre),
            ),
          );
        },
      ),
    );
  }
}



