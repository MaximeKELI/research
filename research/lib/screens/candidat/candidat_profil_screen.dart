import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'dart:io';
import '../../services/candidat_service.dart';
import '../../models/profil_candidat.dart';
import '../../core/config.dart';

class CandidatProfilScreen extends StatefulWidget {
  const CandidatProfilScreen({super.key});

  @override
  State<CandidatProfilScreen> createState() => _CandidatProfilScreenState();
}

class _CandidatProfilScreenState extends State<CandidatProfilScreen> {
  final _service = CandidatService();
  ProfilCandidat? _profil;
  bool _isLoading = true;
  bool _isEditing = false;

  final _nomController = TextEditingController();
  final _prenomController = TextEditingController();
  final _niveauEtudeController = TextEditingController();
  final _competencesController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadProfil();
  }

  @override
  void dispose() {
    _nomController.dispose();
    _prenomController.dispose();
    _niveauEtudeController.dispose();
    _competencesController.dispose();
    super.dispose();
  }

  Future<void> _loadProfil() async {
    setState(() {
      _isLoading = true;
    });

    final profil = await _service.getProfil();
    setState(() {
      _profil = profil;
      _isLoading = false;
    });

    if (profil != null) {
      _nomController.text = profil.nom;
      _prenomController.text = profil.prenom;
      _niveauEtudeController.text = profil.niveauEtude ?? '';
      _competencesController.text = profil.competences ?? '';
    }
  }

  Future<void> _saveProfil() async {
    if (_profil == null) {
      // Créer le profil
      final newProfil = await _service.createProfil(
        nom: _nomController.text,
        prenom: _prenomController.text,
        niveauEtude: _niveauEtudeController.text.isEmpty
            ? null
            : _niveauEtudeController.text,
        competences: _competencesController.text.isEmpty
            ? null
            : _competencesController.text,
      );
      if (newProfil != null) {
        setState(() {
          _profil = newProfil;
          _isEditing = false;
        });
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Profil créé avec succès')),
          );
        }
      }
    } else {
      // Mettre à jour le profil
      final updatedProfil = await _service.updateProfil(
        nom: _nomController.text,
        prenom: _prenomController.text,
        niveauEtude: _niveauEtudeController.text.isEmpty
            ? null
            : _niveauEtudeController.text,
        competences: _competencesController.text.isEmpty
            ? null
            : _competencesController.text,
      );
      if (updatedProfil != null) {
        setState(() {
          _profil = updatedProfil;
          _isEditing = false;
        });
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Profil mis à jour')),
          );
        }
      }
    }
  }

  Future<void> _uploadPhoto() async {
    // Vérifier si le profil existe, sinon le créer d'abord
    if (_profil == null) {
      // Vérifier que les champs obligatoires sont remplis
      if (_nomController.text.isEmpty || _prenomController.text.isEmpty) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Veuillez remplir au moins le nom et le prénom avant d\'uploader la photo'),
              backgroundColor: Colors.orange,
            ),
          );
        }
        return;
      }
      
      // Créer le profil d'abord
      final newProfil = await _service.createProfil(
        nom: _nomController.text,
        prenom: _prenomController.text,
        niveauEtude: _niveauEtudeController.text.isEmpty
            ? null
            : _niveauEtudeController.text,
        competences: _competencesController.text.isEmpty
            ? null
            : _competencesController.text,
      );
      
      if (newProfil == null) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Erreur lors de la création du profil. Veuillez réessayer.'),
              backgroundColor: Colors.red,
            ),
          );
        }
        return;
      }
      
      setState(() {
        _profil = newProfil;
      });
    }

    // Sélectionner une image
    final result = await FilePicker.platform.pickFiles(
      type: FileType.image,
    );

    if (result != null && result.files.single.path != null) {
      final file = File(result.files.single.path!);
      final success = await _service.uploadPhoto(file);

      if (mounted) {
        if (success) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Photo uploadée avec succès'),
              backgroundColor: Colors.green,
            ),
          );
          _loadProfil();
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Erreur lors de l\'upload de la photo. Vérifiez que le fichier est une image valide (JPG, PNG, max 2MB).'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    }
  }

  Future<void> _uploadCV() async {
    // Vérifier si le profil existe, sinon le créer d'abord
    if (_profil == null) {
      // Vérifier que les champs obligatoires sont remplis
      if (_nomController.text.isEmpty || _prenomController.text.isEmpty) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Veuillez remplir au moins le nom et le prénom avant d\'uploader le CV'),
              backgroundColor: Colors.orange,
            ),
          );
        }
        return;
      }
      
      // Créer le profil d'abord
      final newProfil = await _service.createProfil(
        nom: _nomController.text,
        prenom: _prenomController.text,
        niveauEtude: _niveauEtudeController.text.isEmpty
            ? null
            : _niveauEtudeController.text,
        competences: _competencesController.text.isEmpty
            ? null
            : _competencesController.text,
      );
      
      if (newProfil == null) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Erreur lors de la création du profil. Veuillez réessayer.'),
              backgroundColor: Colors.red,
            ),
          );
        }
        return;
      }
      
      setState(() {
        _profil = newProfil;
      });
    }

    // Maintenant uploader le CV
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
    );

    if (result != null && result.files.single.path != null) {
      final file = File(result.files.single.path!);
      final success = await _service.uploadCV(file);

      if (mounted) {
        if (success) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('CV uploadé avec succès'),
              backgroundColor: Colors.green,
            ),
          );
          _loadProfil();
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Erreur lors de l\'upload du CV. Vérifiez que le fichier est un PDF valide (max 5MB).'),
              backgroundColor: Colors.red,
            ),
          );
        }
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

    return Scaffold(
      appBar: AppBar(
        title: const Text('Mon Profil'),
        actions: [
          if (!_isEditing && _profil != null)
            IconButton(
              icon: const Icon(Icons.edit),
              onPressed: () {
                setState(() {
                  _isEditing = true;
                });
              },
            ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (_profil == null)
              Card(
                color: Colors.blue.shade50,
                child: const Padding(
                  padding: EdgeInsets.all(16.0),
                  child: Text(
                    'Créez votre profil pour commencer à postuler',
                    textAlign: TextAlign.center,
                  ),
                ),
              ),
            const SizedBox(height: 16),
            TextField(
              controller: _nomController,
              enabled: _isEditing || _profil == null,
              decoration: const InputDecoration(
                labelText: 'Nom',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _prenomController,
              enabled: _isEditing || _profil == null,
              decoration: const InputDecoration(
                labelText: 'Prénom',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _niveauEtudeController,
              enabled: _isEditing || _profil == null,
              decoration: const InputDecoration(
                labelText: 'Niveau d\'étude',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _competencesController,
              enabled: _isEditing || _profil == null,
              maxLines: 4,
              decoration: const InputDecoration(
                labelText: 'Compétences',
                border: OutlineInputBorder(),
                hintText: 'Listez vos compétences...',
              ),
            ),
            const SizedBox(height: 24),
            if (_profil?.cvUrl != null) ...[
              Card(
                child: ListTile(
                  leading: const Icon(Icons.picture_as_pdf, color: Colors.red),
                  title: const Text('CV téléchargé'),
                  trailing: const Icon(Icons.check_circle, color: Colors.green),
                ),
              ),
              const SizedBox(height: 8),
            ],
            ElevatedButton.icon(
              onPressed: _uploadCV,
              icon: const Icon(Icons.upload_file),
              label: Text(_profil?.cvUrl != null ? 'Remplacer le CV' : 'Télécharger le CV (PDF)'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 12),
              ),
            ),
            if (_profil == null)
              Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: Text(
                  'Note: Le profil sera créé automatiquement si vous uploadez un CV',
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: Colors.grey[600],
                    fontStyle: FontStyle.italic,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            const SizedBox(height: 24),
            if (_isEditing || _profil == null)
              ElevatedButton(
                onPressed: _saveProfil,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
                child: Text(_profil == null ? 'Créer le profil' : 'Enregistrer'),
              ),
            if (_isEditing && _profil != null)
              TextButton(
                onPressed: () {
                  setState(() {
                    _isEditing = false;
                  });
                  _loadProfil();
                },
                child: const Text('Annuler'),
              ),
          ],
        ),
      ),
    );
  }
}



