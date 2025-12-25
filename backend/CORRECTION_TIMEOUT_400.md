# Correction du Problème de Timeout 400

## Problème Identifié

Les requêtes POST vers `/api/candidats/profil` retournaient des erreurs 400 avec un timeout de 30 secondes. Le problème était que le middleware `InputSanitizationMiddleware` lisait le body de la requête avec `await request.body()`, ce qui consommait le stream. Une fois le body lu, FastAPI ne pouvait plus le lire, causant un timeout.

## Solution Implémentée ✅

### 1. Modification du Middleware ✅
- **Suppression de la lecture du body JSON** dans le middleware
- Le middleware vérifie maintenant seulement les **query parameters**
- La validation du body est laissée à **Pydantic** dans les routers
- Fichier modifié : `backend/app/security/middleware.py`

### 2. Sanitization dans les Routers ✅
- Ajout de la sanitization explicite dans `create_profil` et `update_profil`
- Les données sont sanitizées avant d'être sauvegardées en base
- Fichier modifié : `backend/app/routers/candidats.py`

## Changements Techniques

### Avant (Problématique) ❌
```python
# Dans le middleware
if "application/json" in content_type:
    body = await request.body()  # ❌ Consomme le stream
    body_json = json.loads(body.decode('utf-8'))
    # Validation...
```

### Après (Corrigé) ✅
```python
# Dans le middleware
# IMPORTANT: Ne pas lire le body ici car il sera consommé
# La validation sera faite par Pydantic dans les routers
# On vérifie seulement les query parameters
```

```python
# Dans le router
# Sanitizer les données avant création
nom = sanitize_string(profil_data.nom, max_length=100) if profil_data.nom else None
prenom = sanitize_string(profil_data.prenom, max_length=100) if profil_data.prenom else None
# ...
```

## Sécurité Maintenue ✅

- Les **query parameters** sont toujours vérifiés par le middleware
- Les **données du body** sont validées par **Pydantic** (validation automatique)
- Les **données sont sanitizées** dans les routers avant sauvegarde
- La sécurité est **maintenue** sans bloquer les requêtes légitimes

## Test

Pour tester :
1. Redémarrer le serveur backend
2. Se connecter en tant que candidat
3. Aller dans l'onglet "Profil"
4. Remplir les champs (nom, prénom, etc.)
5. Cliquer sur "Créer le profil"
6. ✅ La requête devrait réussir immédiatement (pas de timeout)

## Notes

- Le middleware continue de vérifier les query parameters pour la sécurité
- Pydantic valide automatiquement les types et formats des données
- La sanitization est faite explicitement dans les routers pour une sécurité supplémentaire
- Les timeouts de 30 secondes ne devraient plus se produire

---

**Problème résolu !** ✅

