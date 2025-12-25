class ProfilCandidat {
  final int id;
  final int userId;
  final String nom;
  final String prenom;
  final String? niveauEtude;
  final String? competences;
  final String? cvUrl;
  final DateTime createdAt;

  ProfilCandidat({
    required this.id,
    required this.userId,
    required this.nom,
    required this.prenom,
    this.niveauEtude,
    this.competences,
    this.cvUrl,
    required this.createdAt,
  });

  factory ProfilCandidat.fromJson(Map<String, dynamic> json) {
    return ProfilCandidat(
      id: json['id'],
      userId: json['user_id'],
      nom: json['nom'],
      prenom: json['prenom'],
      niveauEtude: json['niveau_etude'],
      competences: json['competences'],
      cvUrl: json['cv_url'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'nom': nom,
      'prenom': prenom,
      'niveau_etude': niveauEtude,
      'competences': competences,
      'cv_url': cvUrl,
      'created_at': createdAt.toIso8601String(),
    };
  }
}

