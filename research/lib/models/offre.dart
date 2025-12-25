import 'entreprise.dart';

class Offre {
  final int id;
  final int entrepriseId;
  final String titre;
  final String description;
  final String type; // 'stage' ou 'emploi'
  final String? lieu;
  final String? salaire;
  final DateTime? dateLimite;
  final String statut; // 'active' ou 'expirée'
  final DateTime createdAt;
  final Entreprise? entreprise;

  Offre({
    required this.id,
    required this.entrepriseId,
    required this.titre,
    required this.description,
    required this.type,
    this.lieu,
    this.salaire,
    this.dateLimite,
    required this.statut,
    required this.createdAt,
    this.entreprise,
  });

  factory Offre.fromJson(Map<String, dynamic> json) {
    return Offre(
      id: json['id'],
      entrepriseId: json['entreprise_id'],
      titre: json['titre'],
      description: json['description'],
      type: json['type'],
      lieu: json['lieu'],
      salaire: json['salaire'],
      dateLimite: json['date_limite'] != null 
          ? DateTime.parse(json['date_limite']) 
          : null,
      statut: json['statut'],
      createdAt: DateTime.parse(json['created_at']),
      entreprise: json['entreprise'] != null 
          ? Entreprise.fromJson(json['entreprise']) 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'entreprise_id': entrepriseId,
      'titre': titre,
      'description': description,
      'type': type,
      'lieu': lieu,
      'salaire': salaire,
      'date_limite': dateLimite?.toIso8601String(),
      'statut': statut,
      'created_at': createdAt.toIso8601String(),
    };
  }
}



