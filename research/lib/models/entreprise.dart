class Entreprise {
  final int id;
  final int userId;
  final String nom;
  final String? secteur;
  final String? description;
  final String? contact;
  final bool validee;
  final DateTime createdAt;

  Entreprise({
    required this.id,
    required this.userId,
    required this.nom,
    this.secteur,
    this.description,
    this.contact,
    required this.validee,
    required this.createdAt,
  });

  factory Entreprise.fromJson(Map<String, dynamic> json) {
    return Entreprise(
      id: json['id'],
      userId: json['user_id'],
      nom: json['nom'],
      secteur: json['secteur'],
      description: json['description'],
      contact: json['contact'],
      validee: json['validee'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'nom': nom,
      'secteur': secteur,
      'description': description,
      'contact': contact,
      'validee': validee,
      'created_at': createdAt.toIso8601String(),
    };
  }
}

