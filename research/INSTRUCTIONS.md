# Instructions de Démarrage - Application Flutter

## Prérequis

- Flutter SDK 3.7 ou supérieur
- Android Studio / Xcode (pour iOS)
- Un émulateur ou un appareil physique

## Installation

### 1. Vérifier l'Installation de Flutter

```bash
flutter doctor
```

Assurez-vous que tous les composants nécessaires sont installés.

### 2. Installer les Dépendances

```bash
cd research
flutter pub get
```

### 3. Configuration de l'URL de l'API

Modifier le fichier `lib/core/config.dart`:

```dart
class ApiConfig {
  // Pour Android Emulator
  static const String baseUrl = 'http://10.0.2.2:8000';
  
  // Pour iOS Simulator
  // static const String baseUrl = 'http://localhost:8000';
  
  // Pour appareil physique (remplacer par votre IP locale)
  // static const String baseUrl = 'http://192.168.1.100:8000';
  
  static const String apiPrefix = '/api';
  static String get apiUrl => '$baseUrl$apiPrefix';
}
```

**Important**: Pour un appareil physique, utilisez l'IP locale de votre machine (pas localhost).

### 4. Lancer l'Application

```bash
# Voir les appareils disponibles
flutter devices

# Lancer sur un appareil spécifique
flutter run -d <device_id>

# Ou simplement
flutter run
```

## Permissions Android

Pour l'upload de fichiers PDF, ajouter dans `android/app/src/main/AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
```

## Permissions iOS

Pour l'upload de fichiers PDF, ajouter dans `ios/Runner/Info.plist`:

```xml
<key>NSPhotoLibraryUsageDescription</key>
<string>Nous avons besoin d'accéder à vos fichiers pour télécharger votre CV</string>
```

## Build pour Production

### Android

```bash
flutter build apk --release
# ou pour app bundle
flutter build appbundle --release
```

### iOS

```bash
flutter build ios --release
```

## Dépannage

### Erreur de connexion à l'API
- Vérifiez que le backend est démarré
- Vérifiez l'URL dans `config.dart`
- Pour un appareil physique, assurez-vous que le téléphone et l'ordinateur sont sur le même réseau WiFi
- Vérifiez le firewall

### Erreur d'import
- Exécutez `flutter pub get`
- Vérifiez que toutes les dépendances sont installées

### Erreur de build
- Nettoyez le projet: `flutter clean`
- Réinstallez les dépendances: `flutter pub get`
- Rebuild: `flutter build apk`

## Structure de l'Application

```
lib/
├── main.dart              # Point d'entrée
├── core/                  # Configuration et API client
├── models/                # Modèles de données
├── services/              # Services API
├── providers/             # State management (Provider)
└── screens/              # Écrans de l'application
    ├── auth/             # Authentification
    ├── candidat/         # Espace candidat
    ├── entreprise/       # Espace entreprise
    ├── admin/            # Espace admin
    └── offres/           # Liste et détails des offres
```

## Fonctionnalités Testées

- ✅ Authentification (login/register)
- ✅ Gestion de profil candidat
- ✅ Upload de CV
- ✅ Recherche et filtrage d'offres
- ✅ Postulation aux offres
- ✅ Gestion des candidatures
- ✅ Publication d'offres (entreprise)
- ✅ Gestion des candidatures reçues (entreprise)

## Notes

- L'application utilise Provider pour la gestion d'état
- Les tokens JWT sont stockés dans SharedPreferences
- Les appels API sont gérés via Dio avec intercepteurs pour l'authentification
- L'interface est optimisée pour les appareils à faible performance

