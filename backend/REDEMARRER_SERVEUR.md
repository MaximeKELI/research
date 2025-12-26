# 🔄 Redémarrer le Serveur Backend

## Problème
Le serveur backend retourne **404 Not Found** pour `/api/offres` alors que la route existe.

## Cause
Le serveur backend qui tourne depuis 22:47 n'a pas rechargé les modifications récentes des routes (changement de `"/"` à `""`).

## Solution

### Option 1: Redémarrer manuellement
1. Arrêter le serveur actuel (Ctrl+C dans le terminal où il tourne)
2. Redémarrer avec: `python run.py`

### Option 2: Attendre le rechargement automatique
Le serveur utilise `WatchFiles` qui devrait recharger automatiquement, mais parfois il faut forcer en touchant un fichier:
```bash
touch app/routers/offres.py
```

## Vérification
Après redémarrage, tester avec:
```bash
curl -X POST http://localhost:8000/api/offres \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{"titre":"Test","description":"Test","type":"emploi"}'
```

Devrait retourner **201 Created** (ou **401 Unauthorized** si le token est invalide, mais **PAS 404**).

