import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:intl/intl.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import '../../services/admin_service.dart';

class AdminDashboardScreen extends StatefulWidget {
  const AdminDashboardScreen({super.key});

  @override
  State<AdminDashboardScreen> createState() => _AdminDashboardScreenState();
}

class _AdminDashboardScreenState extends State<AdminDashboardScreen> {
  final _service = AdminService();
  Map<String, dynamic>? _stats;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadStats();
  }

  Future<void> _loadStats() async {
    setState(() {
      _isLoading = true;
    });

    final stats = await _service.getStatistiques();
    setState(() {
      _stats = stats;
      _isLoading = false;
    });
  }

  Future<void> _exportCSV(String dataType) async {
    try {
      final data = await _service.exportCSV(dataType);
      
      if (data != null) {
        final directory = await getApplicationDocumentsDirectory();
        final file = File('${directory.path}/${dataType}_${DateFormat('yyyyMMdd').format(DateTime.now())}.csv');
        await file.writeAsBytes(data);
        
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Fichier CSV exporté: ${file.path}'),
              backgroundColor: Colors.green,
            ),
          );
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Erreur lors de l\'export CSV'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Erreur lors de l\'export CSV'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _exportPDF() async {
    try {
      final data = await _service.exportPDF();
      
      if (data != null) {
        final directory = await getApplicationDocumentsDirectory();
        final file = File('${directory.path}/statistiques_${DateFormat('yyyyMMdd').format(DateTime.now())}.pdf');
        await file.writeAsBytes(data);
        
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Fichier PDF exporté: ${file.path}'),
              backgroundColor: Colors.green,
            ),
          );
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Erreur lors de l\'export PDF'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Erreur lors de l\'export PDF'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    if (_stats == null) {
      return Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('Erreur de chargement des statistiques'),
              ElevatedButton(
                onPressed: _loadStats,
                child: const Text('Réessayer'),
              ),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      body: RefreshIndicator(
        onRefresh: _loadStats,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Boutons d'export
              Row(
                children: [
                  Expanded(
                    child: ElevatedButton.icon(
                      onPressed: () => _exportPDF(),
                      icon: const Icon(Icons.picture_as_pdf),
                      label: const Text('Export PDF'),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: PopupMenuButton<String>(
                      child: ElevatedButton.icon(
                        onPressed: () {},
                        icon: const Icon(Icons.file_download),
                        label: const Text('Export CSV'),
                      ),
                      onSelected: _exportCSV,
                      itemBuilder: (context) => [
                        const PopupMenuItem(value: 'candidats', child: Text('Candidats')),
                        const PopupMenuItem(value: 'entreprises', child: Text('Entreprises')),
                        const PopupMenuItem(value: 'offres', child: Text('Offres')),
                        const PopupMenuItem(value: 'candidatures', child: Text('Candidatures')),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),
              
              // Statistiques générales
              _buildStatsCards(),
              const SizedBox(height: 24),
              
              // Graphiques
              if (_stats!['candidats_par_genre'] != null)
                _buildGenreChart(),
              const SizedBox(height: 24),
              
              if (_stats!['entreprises_par_secteur'] != null)
                _buildSecteurChart(),
              const SizedBox(height: 24),
              
              if (_stats!['candidats_par_niveau'] != null)
                _buildNiveauChart(),
              const SizedBox(height: 24),
              
              if (_stats!['evolution_mensuelle'] != null)
                _buildEvolutionChart(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStatsCards() {
    return GridView.count(
      crossAxisCount: 2,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisSpacing: 16,
      mainAxisSpacing: 16,
      children: [
        _buildStatCard('Utilisateurs', _stats!['total_users'] ?? 0, Icons.people, Colors.blue),
        _buildStatCard('Candidats', _stats!['total_candidats'] ?? 0, Icons.person, Colors.green),
        _buildStatCard('Entreprises', _stats!['total_entreprises'] ?? 0, Icons.business, Colors.orange),
        _buildStatCard('Offres', _stats!['total_offres'] ?? 0, Icons.work, Colors.purple),
        _buildStatCard('Candidatures', _stats!['total_candidatures'] ?? 0, Icons.description, Colors.red),
        _buildStatCard('Entreprises Validées', _stats!['total_entreprises_validees'] ?? 0, Icons.check_circle, Colors.teal),
      ],
    );
  }

  Widget _buildStatCard(String title, int value, IconData icon, Color color) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 40, color: color),
            const SizedBox(height: 8),
            Text(
              value.toString(),
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
            Text(
              title,
              style: const TextStyle(fontSize: 12),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildGenreChart() {
    final genreData = _stats!['candidats_par_genre'] as Map<String, dynamic>;
    if (genreData.isEmpty) return const SizedBox.shrink();

    final entries = genreData.entries.toList();
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Candidats par Genre',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 200,
              child: PieChart(
                PieChartData(
                  sections: entries.asMap().entries.map((entry) {
                    final index = entry.key;
                    final count = entry.value.value as int;
                    final total = genreData.values.fold<int>(0, (sum, v) => sum + (v as int));
                    final percentage = (count / total * 100);
                    
                    return PieChartSectionData(
                      value: count.toDouble(),
                      title: '${percentage.toStringAsFixed(1)}%',
                      color: _getColorForIndex(index),
                      radius: 80,
                    );
                  }).toList(),
                ),
              ),
            ),
            const SizedBox(height: 16),
            ...entries.asMap().entries.map((entry) {
              final index = entry.key;
              final genre = entry.value.key;
              final count = entry.value.value as int;
              return Padding(
                padding: const EdgeInsets.symmetric(vertical: 4.0),
                child: Row(
                  children: [
                    Container(
                      width: 16,
                      height: 16,
                      color: _getColorForIndex(index),
                    ),
                    const SizedBox(width: 8),
                    Text('$genre: $count'),
                  ],
                ),
              );
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildSecteurChart() {
    final secteurData = _stats!['entreprises_par_secteur'] as Map<String, dynamic>;
    if (secteurData.isEmpty) return const SizedBox.shrink();

    final entries = secteurData.entries.toList()..sort((a, b) => (b.value as int).compareTo(a.value as int));
    final top5 = entries.take(5).toList();

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Top 5 Secteurs d\'Entreprises',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 200,
              child: BarChart(
                BarChartData(
                  alignment: BarChartAlignment.spaceAround,
                  maxY: top5.map((e) => e.value as int).reduce((a, b) => a > b ? a : b).toDouble() * 1.2,
                  barTouchData: BarTouchData(enabled: false),
                  titlesData: FlTitlesData(
                    show: true,
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        getTitlesWidget: (value, meta) {
                          if (value.toInt() >= top5.length) return const Text('');
                          return Padding(
                            padding: const EdgeInsets.only(top: 8.0),
                            child: Text(
                              top5[value.toInt()].key,
                              style: const TextStyle(fontSize: 10),
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            ),
                          );
                        },
                      ),
                    ),
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: true),
                    ),
                    topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                    rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                  ),
                  gridData: FlGridData(show: true),
                  borderData: FlBorderData(show: false),
                  barGroups: top5.asMap().entries.map((entry) {
                    final index = entry.key;
                    final count = entry.value.value as int;
                    return BarChartGroupData(
                      x: index,
                      barRods: [
                        BarChartRodData(
                          toY: count.toDouble(),
                          color: _getColorForIndex(index),
                          width: 20,
                        ),
                      ],
                    );
                  }).toList(),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNiveauChart() {
    final niveauData = _stats!['candidats_par_niveau'] as Map<String, dynamic>;
    if (niveauData.isEmpty) return const SizedBox.shrink();

    final entries = niveauData.entries.toList();

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Candidats par Niveau d\'Étude',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 200,
              child: BarChart(
                BarChartData(
                  alignment: BarChartAlignment.spaceAround,
                  maxY: entries.map((e) => e.value as int).reduce((a, b) => a > b ? a : b).toDouble() * 1.2,
                  barTouchData: BarTouchData(enabled: false),
                  titlesData: FlTitlesData(
                    show: true,
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        getTitlesWidget: (value, meta) {
                          if (value.toInt() >= entries.length) return const Text('');
                          return Padding(
                            padding: const EdgeInsets.only(top: 8.0),
                            child: Text(
                              entries[value.toInt()].key,
                              style: const TextStyle(fontSize: 10),
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            ),
                          );
                        },
                      ),
                    ),
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: true),
                    ),
                    topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                    rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                  ),
                  gridData: FlGridData(show: true),
                  borderData: FlBorderData(show: false),
                  barGroups: entries.asMap().entries.map((entry) {
                    final index = entry.key;
                    final count = entry.value.value as int;
                    return BarChartGroupData(
                      x: index,
                      barRods: [
                        BarChartRodData(
                          toY: count.toDouble(),
                          color: _getColorForIndex(index),
                          width: 20,
                        ),
                      ],
                    );
                  }).toList(),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEvolutionChart() {
    final evolutionData = _stats!['evolution_mensuelle'] as List<dynamic>;
    if (evolutionData.isEmpty) return const SizedBox.shrink();

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Évolution Mensuelle des Inscriptions',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 200,
              child: LineChart(
                LineChartData(
                  gridData: FlGridData(show: true),
                  titlesData: FlTitlesData(
                    show: true,
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        getTitlesWidget: (value, meta) {
                          if (value.toInt() >= evolutionData.length) return const Text('');
                          final data = evolutionData[value.toInt()] as Map<String, dynamic>;
                          return Text(
                            data['mois'].toString().substring(5),
                            style: const TextStyle(fontSize: 10),
                          );
                        },
                      ),
                    ),
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: true),
                    ),
                    topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                    rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                  ),
                  borderData: FlBorderData(show: true),
                  lineBarsData: [
                    LineChartBarData(
                      spots: evolutionData.asMap().entries.map((entry) {
                        final index = entry.key;
                        final data = entry.value as Map<String, dynamic>;
                        return FlSpot(index.toDouble(), (data['count'] as int).toDouble());
                      }).toList(),
                      isCurved: true,
                      color: Colors.blue,
                      barWidth: 3,
                      dotData: FlDotData(show: true),
                      belowBarData: BarAreaData(show: false),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Color _getColorForIndex(int index) {
    final colors = [
      Colors.blue,
      Colors.green,
      Colors.orange,
      Colors.purple,
      Colors.red,
      Colors.teal,
      Colors.pink,
      Colors.amber,
    ];
    return colors[index % colors.length];
  }
}

