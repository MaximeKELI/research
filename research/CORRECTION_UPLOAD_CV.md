# Correction du Problème d'Upload de CV

## Problème Identifié

L'utilisateur essayait d'uploader un CV avant de créer son profil, ce qui causait une erreur 404 car le backend nécessite un profil existant pour l'upload.

## Solution Implémentée ✅

### 1. Création Automatique du Profil ✅
- Si l'utilisateur essaie d'uploader un CV sans avoir de profil, le profil est créé automatiquement
- Vérification que le nom et le prénom sont remplis avant l'upload

### 2. Messages d'Erreur Améliorés ✅
- Message clair si le nom/prénom ne sont pas remplis
- Message d'erreur détaillé si l'upload échoue
- Note informative pour guider l'utilisateur

### 3. Gestion des Erreurs ✅
- Gestion explicite des erreurs 404 (profil inexistant)
- Gestion des erreurs 400 (fichier invalide, trop gros, etc.)
- Messages d'erreur clairs pour l'utilisateur

## Fichiers Modifiés

1. **`research/lib/screens/candidat/candidat_profil_screen.dart`**
   - Fonction `_uploadCV()` améliorée pour créer le profil automatiquement
   - Messages d'erreur améliorés
   - Note informative ajoutée

2. **`research/lib/services/candidat_service.dart`**
   - Gestion améliorée des erreurs dans `uploadCV()`

## Nouveau Flux

### Avant (Problématique) ❌
1. Utilisateur upload un CV
2. Backend retourne 404 (profil n'existe pas)
3. Erreur silencieuse ou message générique

### Après (Corrigé) ✅
1. Utilisateur remplit au moins nom et prénom
2. Utilisateur upload un CV
3. **Le profil est créé automatiquement** si nécessaire
4. Le CV est uploadé avec succès
5. Message de confirmation affiché

## Test

Pour tester :
1. Se connecter en tant que candidat
2. Aller dans l'onglet "Profil"
3. Remplir au moins le nom et le prénom
4. Cliquer sur "Télécharger le CV (PDF)"
5. Sélectionner un fichier PDF
6. ✅ Le profil est créé automatiquement et le CV est uploadé

## Notes

- Le profil est créé avec les informations saisies dans le formulaire
- Si le nom ou le prénom sont vides, un message d'aide s'affiche
- Le CV doit être un PDF valide (max 5MB)

---

**Problème résolu !** ✅

