# Fonctionnalités Data Science et Statistiques

## ✅ Implémentations Complétées

### 1. Extension des Modèles de Données ✅

#### ProfilCandidat (Nouveaux champs ajoutés)
- `date_naissance` - Pour calculer l'âge
- `genre` - M, F, Autre
- `telephone` - Contact
- `adresse`, `ville`, `pays`, `code_postal` - Localisation complète
- `domaine_etude` - Domaine d'études (Informatique, Commerce, etc.)
- `annee_obtention` - Année d'obtention du diplôme
- `annees_experience` - Nombre d'années d'expérience
- `secteur_experience` - Secteur d'activité
- `statut_professionnel` - Étudiant, Employé, Chômeur, etc.
- `disponibilite` - Immédiate, 1 mois, 3 mois, etc.
- `salaire_souhaite` - Attentes salariales

#### Entreprise (Nouveaux champs ajoutés)
- `telephone`, `email_contact` - Contacts supplémentaires
- `adresse`, `ville`, `pays`, `code_postal` - Localisation complète
- `site_web` - Site web de l'entreprise
- `taille_entreprise` - Startup, PME, Grande entreprise
- `nombre_employes` - Nombre d'employés
- `annee_creation` - Année de création
- `type_entreprise` - Privée, Publique, ONG, etc.

#### Offre (Nouveaux champs ajoutés)
- `ville`, `pays` - Localisation détaillée
- `type_contrat` - CDI, CDD, Stage, Freelance, etc.
- `salaire_min`, `salaire_max` - Fourchette salariale
- `experience_requise` - 0-2 ans, 3-5 ans, etc.
- `niveau_etude_requis` - Niveau d'étude requis
- `competences_requises` - Compétences spécifiques
- `avantages` - Avantages proposés
- `nombre_vues`, `nombre_candidatures` - Statistiques

### 2. Endpoints Admin pour Statistiques ✅

#### `/api/admin/statistiques` (GET)
Retourne des statistiques complètes :
- Totaux (utilisateurs, candidats, entreprises, offres, candidatures)
- **Candidats par genre** - Distribution par genre
- **Entreprises par secteur** - Top secteurs
- **Candidats par niveau d'étude** - Distribution éducative
- **Candidats par ville** - Top 10 villes
- **Offres par type** - Stage vs Emploi
- **Candidatures par statut** - En attente, Accepté, Refusé
- **Évolution mensuelle** - Inscriptions sur 6 mois
- **Candidats par expérience** - Distribution par années d'expérience

#### `/api/admin/export/csv` (GET)
Exporte les données en CSV :
- Paramètre `data_type` : `candidats`, `entreprises`, `offres`, `candidatures`
- Retourne un fichier CSV téléchargeable

#### `/api/admin/export/pdf` (GET)
Exporte les statistiques en PDF :
- Rapport complet avec tableaux
- Statistiques par genre, secteur, niveau, etc.
- Format professionnel avec ReportLab

### 3. Tableau de Bord Admin Flutter ✅

#### Fonctionnalités
- **Cartes de statistiques** - Vue d'ensemble avec icônes
- **Graphique en camembert** - Candidats par genre
- **Graphique en barres** - Top 5 secteurs d'entreprises
- **Graphique en barres** - Candidats par niveau d'étude
- **Graphique linéaire** - Évolution mensuelle des inscriptions
- **Export PDF** - Bouton pour télécharger le rapport PDF
- **Export CSV** - Menu déroulant pour exporter candidats, entreprises, offres, candidatures
- **Pull-to-refresh** - Actualisation des données

#### Packages Flutter ajoutés
- `fl_chart: ^0.66.0` - Graphiques interactifs
- `csv: ^5.0.2` - Export CSV
- `flutter_datetime_picker_plus: ^2.1.0` - Sélecteur de dates

### 4. Packages Backend ajoutés ✅
- `pandas==2.1.3` - Analyse de données
- `openpyxl==3.1.2` - Export Excel (pour usage futur)
- `reportlab==4.0.7` - Génération PDF

## 📋 À Compléter (Formulaires)

### Formulaire de Profil Candidat
Les champs sont disponibles dans le modèle, mais le formulaire Flutter doit être étendu pour collecter :
- Date de naissance (date picker)
- Genre (dropdown)
- Téléphone, adresse, ville, pays, code postal
- Domaine d'étude, année d'obtention
- Années d'expérience, secteur d'expérience
- Statut professionnel, disponibilité
- Salaire souhaité

### Formulaire de Profil Entreprise
Les champs sont disponibles dans le modèle, mais le formulaire Flutter doit être étendu pour collecter :
- Téléphone, email de contact
- Adresse complète (adresse, ville, pays, code postal)
- Site web
- Taille entreprise, nombre d'employés
- Année de création, type d'entreprise

### Formulaire de Création d'Offre
Les champs sont disponibles dans le modèle, mais le formulaire Flutter doit être étendu pour collecter :
- Localisation détaillée (ville, pays)
- Type de contrat
- Fourchette salariale (min, max)
- Expérience requise, niveau d'étude requis
- Compétences requises, avantages

## 🎯 Utilisation

### Pour l'Admin
1. Se connecter en tant qu'admin
2. Accéder au tableau de bord
3. Voir les statistiques en temps réel
4. Exporter les données en CSV ou PDF

### Pour l'Analyse de Données
Les données collectées permettent d'analyser :
- **Démographie** : Répartition par genre, âge, localisation
- **Éducation** : Niveaux d'étude, domaines, années d'obtention
- **Expérience** : Années d'expérience, secteurs
- **Marché du travail** : Types de contrats, salaires, disponibilités
- **Tendances** : Évolution temporelle des inscriptions
- **Géographie** : Répartition géographique des candidats et entreprises
- **Secteurs** : Secteurs d'activité les plus représentés

## 📊 Exemples d'Analyses Possibles

1. **Analyse démographique** : Qui sont nos candidats ? (genre, âge, localisation)
2. **Analyse éducative** : Quels sont les niveaux et domaines d'étude les plus représentés ?
3. **Analyse d'expérience** : Quelle est la distribution de l'expérience professionnelle ?
4. **Analyse géographique** : Où se trouvent nos utilisateurs ?
5. **Analyse sectorielle** : Quels sont les secteurs les plus actifs ?
6. **Analyse temporelle** : Comment évolue la plateforme dans le temps ?
7. **Analyse de matching** : Quels types d'offres attirent le plus de candidatures ?

## 🔧 Prochaines Étapes Recommandées

1. **Étendre les formulaires Flutter** pour collecter toutes les données
2. **Ajouter des validations** pour s'assurer de la qualité des données
3. **Créer des rapports automatiques** (quotidiens, hebdomadaires, mensuels)
4. **Ajouter des filtres avancés** dans le tableau de bord admin
5. **Implémenter des prédictions** (ML) basées sur les données historiques
6. **Créer des dashboards personnalisés** pour différents rôles

---

**Note** : Les modèles de base de données et les endpoints sont prêts. Il suffit d'étendre les formulaires Flutter pour collecter toutes les données nécessaires à l'analyse.

