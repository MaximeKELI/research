import 'offre.dart';
import 'profil_candidat.dart';

class Candidature {
  final int id;
  final int candidatId;
  final int offreId;
  final DateTime datePostulation;
  final String statut; // 'en_attente', 'accepté', 'refusé'
  final Offre? offre;
  final ProfilCandidat? candidat;

  Candidature({
    required this.id,
    required this.candidatId,
    required this.offreId,
    required this.datePostulation,
    required this.statut,
    this.offre,
    this.candidat,
  });

  factory Candidature.fromJson(Map<String, dynamic> json) {
    return Candidature(
      id: json['id'],
      candidatId: json['candidat_id'],
      offreId: json['offre_id'],
      datePostulation: DateTime.parse(json['date_postulation']),
      statut: json['statut'],
      offre: json['offre'] != null ? Offre.fromJson(json['offre']) : null,
      candidat: json['candidat'] != null 
          ? ProfilCandidat.fromJson(json['candidat']) 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'candidat_id': candidatId,
      'offre_id': offreId,
      'date_postulation': datePostulation.toIso8601String(),
      'statut': statut,
    };
  }
}

