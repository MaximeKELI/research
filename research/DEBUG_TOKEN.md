# 🔍 Debug du Token JWT

## Problème
Le backend retourne `401 Unauthorized` lors de la création d'offre, ce qui indique que le token n'est pas envoyé ou n'est pas valide.

## Vérifications Effectuées

### 1. Code Flutter - ApiClient
- ✅ L'interceptor ajoute automatiquement le token dans les headers
- ✅ Le token est récupéré depuis `SharedPreferences` avec la clé `access_token`
- ✅ Format du header: `Authorization: Bearer {token}`

### 2. Code Flutter - AuthService
- ✅ Après login, le token est sauvegardé via `_apiClient.setToken(token)`
- ✅ Après inscription, un login automatique est effectué pour obtenir le token

### 3. Code Backend - auth.py
- ✅ Le backend utilise `OAuth2PasswordBearer` pour extraire le token
- ✅ Le token est validé avec `jwt.decode()`
- ✅ Le format attendu est: `Bearer {token}`

## Solutions Appliquées

### 1. Ajout de logs de debug
- ✅ Logs dans `ApiClient` pour voir si le token est présent
- ✅ Logs dans `AuthService` pour vérifier la sauvegarde du token

### 2. Vérification de la sauvegarde
- ✅ Vérification que le token est bien sauvegardé après login
- ✅ Vérification que le token est bien récupéré dans l'interceptor

## Comment Déboguer

1. **Vérifier que le token est sauvegardé** :
   - Après login/inscription, vérifier dans les logs Flutter
   - Message attendu: `✅ Token sauvegardé avec succès`

2. **Vérifier que le token est envoyé** :
   - Lors d'une requête, vérifier dans les logs Flutter
   - Message attendu: `🔑 Token ajouté aux headers: {premiers caractères}...`

3. **Vérifier les erreurs** :
   - Si 401, vérifier le message: `❌ Erreur 401: Token invalide ou expiré`

## Prochaines Étapes

Si le problème persiste:
1. Vérifier que l'utilisateur est bien connecté (token présent dans SharedPreferences)
2. Vérifier que le token n'a pas expiré
3. Vérifier que le format du header est correct
4. Vérifier les logs du backend pour voir le header reçu

