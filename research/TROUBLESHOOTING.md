# Guide de Dépannage - Application Flutter

## Problèmes d'Inscription et de Connexion

### 1. Vérifier que le Backend est Démarré

Le backend doit être en cours d'exécution sur `http://localhost:8000` pour que l'application Flutter fonctionne.

**Pour démarrer le backend :**
```bash
cd backend
source venv/bin/activate
python run.py
```

Vous devriez voir :
```
INFO: Uvicorn running on http://0.0.0.0:8000
```

### 2. Configuration de l'URL de l'API

L'URL de l'API est configurée dans `lib/core/config.dart` :

- **Linux/Desktop** : `http://localhost:8000` ✅ (actuellement configuré)
- **Android Emulator** : `http://10.0.2.2:8000`
- **iOS Simulator** : `http://localhost:8000`
- **Device physique** : `http://192.168.1.X:8000` (remplacer X par votre IP locale)

### 3. Erreurs Courantes

#### Erreur : "Impossible de se connecter au serveur"
- **Cause** : Le backend n'est pas démarré ou l'URL est incorrecte
- **Solution** : Vérifiez que le backend tourne sur le port 8000

#### Erreur : "Timeout de connexion"
- **Cause** : Le backend met trop de temps à répondre
- **Solution** : Vérifiez les logs du backend pour voir s'il y a des erreurs

#### Erreur : "Email déjà utilisé"
- **Cause** : Tentative d'inscription avec un email existant
- **Solution** : Utilisez un autre email ou connectez-vous avec cet email

#### Erreur : "Token non reçu du serveur"
- **Cause** : Le backend ne retourne pas le token correctement
- **Solution** : Vérifiez les logs du backend

### 4. Avertissements file_picker

Les avertissements concernant `file_picker` sont normaux et n'empêchent pas l'application de fonctionner. Ils peuvent être ignorés.

### 5. Test de Connexion

Pour tester si le backend répond correctement :

```bash
# Test d'inscription
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","mot_de_passe":"password123","role":"candidat"}'

# Test de connexion
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@test.com&password=password123"
```

### 6. Logs de Débogage

Pour voir les erreurs détaillées dans Flutter, lancez l'application avec :
```bash
flutter run -v
```

Les erreurs réseau apparaîtront dans la console.

### 7. Vérification de la Base de Données

Assurez-vous que la base de données SQLite est créée :
```bash
cd backend
source venv/bin/activate
python run.py
# La base de données sera créée automatiquement au premier lancement
```

## Corrections Appliquées

1. ✅ URL de l'API changée pour Linux (`localhost` au lieu de `10.0.2.2`)
2. ✅ Gestion d'erreurs améliorée dans `auth_service.dart`
3. ✅ Utilisation de `FormData` pour le login (form-urlencoded)
4. ✅ Messages d'erreur plus explicites

## Prochaines Étapes

1. Démarrer le backend : `cd backend && source venv/bin/activate && python run.py`
2. Lancer l'application Flutter : `cd research && flutter run`
3. Tester l'inscription avec un nouvel email
4. Tester la connexion avec les identifiants créés

