# 🔄 Guide de Migration de la Base de Données

## Problème Résolu ✅

Si vous rencontrez l'erreur :
```
sqlite3.OperationalError: no such column: users.photo_url
```

Cela signifie que votre base de données n'a pas été mise à jour avec les nouveaux champs.

## Solution Rapide

Exécutez simplement le script de migration :

```bash
cd backend
source venv/bin/activate
python migrate_database.py
```

## Ce que fait le script

Le script `migrate_database.py` :
1. ✅ Vérifie quelles colonnes existent déjà
2. ✅ Ajoute uniquement les colonnes manquantes
3. ✅ Préserve toutes les données existantes
4. ✅ Peut être exécuté plusieurs fois sans problème (idempotent)

## Colonnes Ajoutées

### Table `users`
- `photo_url` - URL de la photo de profil

### Table `profils_candidats`
- `date_naissance`, `genre`, `telephone`, `adresse`, `ville`, `pays`, `code_postal`
- `domaine_etude`, `annee_obtention`, `annees_experience`, `secteur_experience`
- `statut_professionnel`, `disponibilite`, `salaire_souhaite`, `photo_url`

### Table `entreprises`
- `telephone`, `email_contact`, `adresse`, `ville`, `pays`, `code_postal`
- `site_web`, `taille_entreprise`, `nombre_employes`, `annee_creation`
- `type_entreprise`, `photo_url`

### Table `offres`
- `ville`, `pays`, `type_contrat`, `salaire_min`, `salaire_max`
- `experience_requise`, `niveau_etude_requis`, `competences_requises`
- `avantages`, `nombre_vues`, `nombre_candidatures`

## Vérification

Après la migration, vérifiez que tout fonctionne :

```bash
# Tester l'import
python -c "from app.routers import auth; print('✅ OK')"

# Lancer l'application
python run.py
```

## Note Importante

⚠️ **Ne supprimez pas la base de données existante !** 

Le script de migration préserve toutes vos données. Si vous supprimez `jobapp.db`, vous perdrez toutes les données utilisateurs, offres, candidatures, etc.

---

**Le script est sûr et peut être exécuté à tout moment.** ✅

