"""
Tests approfondis pour les nouveaux champs ajoutés aux modèles
"""
import pytest
from fastapi import status
from datetime import date
from app.models import User, ProfilCandidat, Entreprise, Offre
from app.auth import get_password_hash


class TestNewFieldsProfilCandidat:
    """Tests pour les nouveaux champs de ProfilCandidat"""

    def test_create_profil_with_all_new_fields(self, client, auth_token_candidat, db):
        """Test de création d'un profil avec tous les nouveaux champs"""
        response = client.post(
            "/api/candidats/profil",
            headers={"Authorization": f"Bearer {auth_token_candidat}"},
            json={
                "nom": "Doe",
                "prenom": "John",
                "date_naissance": "1995-05-15",
                "genre": "M",
                "telephone": "+33612345678",
                "adresse": "123 Rue de la Paix",
                "ville": "Paris",
                "pays": "France",
                "code_postal": "75001",
                "niveau_etude": "Master",
                "domaine_etude": "Informatique",
                "annee_obtention": 2020,
                "competences": "Python, Flutter, PostgreSQL",
                "annees_experience": 3,
                "secteur_experience": "Tech",
                "statut_professionnel": "Employé",
                "disponibilite": "Immédiate",
                "salaire_souhaite": "40000-50000"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        # Vérifier tous les champs
        assert data["nom"] == "Doe"
        assert data["prenom"] == "John"
        assert data["date_naissance"] == "1995-05-15"
        assert data["genre"] == "M"
        assert data["telephone"] == "+33612345678"
        assert data["adresse"] == "123 Rue de la Paix"
        assert data["ville"] == "Paris"
        assert data["pays"] == "France"
        assert data["code_postal"] == "75001"
        assert data["domaine_etude"] == "Informatique"
        assert data["annee_obtention"] == 2020
        assert data["annees_experience"] == 3
        assert data["secteur_experience"] == "Tech"
        assert data["statut_professionnel"] == "Employé"
        assert data["disponibilite"] == "Immédiate"
        assert data["salaire_souhaite"] == "40000-50000"

    def test_update_profil_with_new_fields(self, client, auth_token_candidat, db):
        """Test de mise à jour d'un profil avec les nouveaux champs"""
        # Créer d'abord un profil
        from app.models import ProfilCandidat, User
        user = db.query(User).filter(User.email == "candidat@test.com").first()
        profil = ProfilCandidat(
            user_id=user.id,
            nom="Doe",
            prenom="John"
        )
        db.add(profil)
        db.commit()
        
        # Mettre à jour avec les nouveaux champs
        response = client.put(
            "/api/candidats/profil",
            headers={"Authorization": f"Bearer {auth_token_candidat}"},
            json={
                "ville": "Lyon",
                "pays": "France",
                "annees_experience": 5,
                "statut_professionnel": "Chômeur"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["ville"] == "Lyon"
        assert data["pays"] == "France"
        assert data["annees_experience"] == 5
        assert data["statut_professionnel"] == "Chômeur"


class TestNewFieldsEntreprise:
    """Tests pour les nouveaux champs d'Entreprise"""

    def test_create_entreprise_with_all_new_fields(self, client, auth_token_entreprise, db):
        """Test de création d'une entreprise avec tous les nouveaux champs"""
        response = client.post(
            "/api/entreprises/profil",
            headers={"Authorization": f"Bearer {auth_token_entreprise}"},
            json={
                "nom": "Tech Corp",
                "secteur": "Informatique",
                "description": "Une grande entreprise tech",
                "contact": "contact@techcorp.com",
                "telephone": "+33123456789",
                "email_contact": "hr@techcorp.com",
                "adresse": "456 Avenue des Champs",
                "ville": "Paris",
                "pays": "France",
                "code_postal": "75008",
                "site_web": "https://techcorp.com",
                "taille_entreprise": "Grande entreprise",
                "nombre_employes": 500,
                "annee_creation": 2010,
                "type_entreprise": "Privée"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        # Vérifier tous les champs
        assert data["nom"] == "Tech Corp"
        assert data["telephone"] == "+33123456789"
        assert data["email_contact"] == "hr@techcorp.com"
        assert data["ville"] == "Paris"
        assert data["pays"] == "France"
        assert data["site_web"] == "https://techcorp.com"
        assert data["taille_entreprise"] == "Grande entreprise"
        assert data["nombre_employes"] == 500
        assert data["annee_creation"] == 2010
        assert data["type_entreprise"] == "Privée"


class TestNewFieldsOffre:
    """Tests pour les nouveaux champs d'Offre"""

    def test_create_offre_with_all_new_fields(self, client, auth_token_entreprise, db):
        """Test de création d'une offre avec tous les nouveaux champs"""
        from app.models import Entreprise, User, TypeOffre, StatutOffre
        
        # Créer une entreprise d'abord
        user = db.query(User).filter(User.email == "entreprise@test.com").first()
        entreprise = Entreprise(
            user_id=user.id,
            nom="Test Entreprise",
            validee=True
        )
        db.add(entreprise)
        db.commit()
        
        response = client.post(
            "/api/offres",
            headers={"Authorization": f"Bearer {auth_token_entreprise}"},
            json={
                "titre": "Développeur Full Stack",
                "description": "Poste de développeur",
                "type": "emploi",
                "lieu": "Paris",
                "ville": "Paris",
                "pays": "France",
                "type_contrat": "CDI",
                "salaire_min": 45000,
                "salaire_max": 60000,
                "experience_requise": "3-5 ans",
                "niveau_etude_requis": "Master",
                "competences_requises": "Python, React, PostgreSQL",
                "avantages": "Télétravail, mutuelle, tickets restaurant",
                "date_limite": "2024-12-31"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        # Vérifier tous les champs
        assert data["titre"] == "Développeur Full Stack"
        assert data["ville"] == "Paris"
        assert data["pays"] == "France"
        assert data["type_contrat"] == "CDI"
        assert data["salaire_min"] == 45000
        assert data["salaire_max"] == 60000
        assert data["experience_requise"] == "3-5 ans"
        assert data["niveau_etude_requis"] == "Master"
        assert "Python" in data["competences_requises"]
        assert "Télétravail" in data["avantages"]
        assert data["nombre_vues"] == 0
        assert data["nombre_candidatures"] == 0


class TestPhotoUpload:
    """Tests pour l'upload de photos"""

    def test_upload_photo_candidat(self, client, auth_token_candidat, db):
        """Test d'upload de photo pour un candidat"""
        from app.models import ProfilCandidat, User
        
        # Créer un profil d'abord
        user = db.query(User).filter(User.email == "candidat@test.com").first()
        profil = ProfilCandidat(
            user_id=user.id,
            nom="Doe",
            prenom="John"
        )
        db.add(profil)
        db.commit()
        
        # Créer une image PNG de test (1x1 pixel)
        png_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
        
        response = client.post(
            "/api/candidats/upload-photo",
            headers={"Authorization": f"Bearer {auth_token_candidat}"},
            files={"file": ("test.png", png_content, "image/png")}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "photo_url" in data
        assert "photos/" in data["photo_url"]

    def test_upload_photo_entreprise(self, client, auth_token_entreprise, db):
        """Test d'upload de photo pour une entreprise"""
        from app.models import Entreprise, User
        
        # Créer une entreprise d'abord
        user = db.query(User).filter(User.email == "entreprise@test.com").first()
        entreprise = Entreprise(
            user_id=user.id,
            nom="Test Entreprise"
        )
        db.add(entreprise)
        db.commit()
        
        # Créer une image PNG de test
        png_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
        
        response = client.post(
            "/api/entreprises/upload-photo",
            headers={"Authorization": f"Bearer {auth_token_entreprise}"},
            files={"file": ("test.png", png_content, "image/png")}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "photo_url" in data
        assert "photos/" in data["photo_url"]


class TestAdminStatisticsWithNewFields:
    """Tests pour les statistiques admin avec les nouveaux champs"""

    def test_statistiques_include_new_fields(self, client, auth_token_admin, db):
        """Test que les statistiques incluent les données des nouveaux champs"""
        from app.models import User, ProfilCandidat, Entreprise
        
        # Créer des données de test avec les nouveaux champs
        for i, genre in enumerate(["M", "F", "M"]):
            user = User(
                email=f"stat{i}@test.com",
                mot_de_passe=get_password_hash("test123"),
                role="candidat"
            )
            db.add(user)
            db.commit()
            
            profil = ProfilCandidat(
                user_id=user.id,
                nom=f"Stat{i}",
                prenom="Test",
                genre=genre,
                ville="Paris" if i % 2 == 0 else "Lyon",
                pays="France",
                annees_experience=i + 1,
                statut_professionnel="Employé" if i % 2 == 0 else "Étudiant"
            )
            db.add(profil)
            db.commit()
        
        # Créer des entreprises avec nouveaux champs
        for i in range(2):
            user = User(
                email=f"ent{i}@test.com",
                mot_de_passe=get_password_hash("test123"),
                role="entreprise"
            )
            db.add(user)
            db.commit()
            
            entreprise = Entreprise(
                user_id=user.id,
                nom=f"Entreprise {i}",
                secteur="Tech" if i == 0 else "Commerce",
                ville="Paris",
                nombre_employes=(i + 1) * 50
            )
            db.add(entreprise)
            db.commit()
        
        response = client.get(
            "/api/admin/statistiques",
            headers={"Authorization": f"Bearer {auth_token_admin}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Vérifier que les statistiques incluent les nouveaux champs
        assert "candidats_par_genre" in data or "candidats_by_genre" in data
        assert "entreprises_par_secteur" in data or "entreprises_by_secteur" in data


class TestExportWithNewFields:
    """Tests pour les exports avec les nouveaux champs"""

    def test_export_csv_candidats_includes_new_fields(self, client, auth_token_admin, db):
        """Test que l'export CSV des candidats inclut les nouveaux champs"""
        from app.models import User, ProfilCandidat
        
        user = User(
            email="export@test.com",
            mot_de_passe=get_password_hash("test123"),
            role="candidat"
        )
        db.add(user)
        db.commit()
        
        profil = ProfilCandidat(
            user_id=user.id,
            nom="Export",
            prenom="Test",
            genre="M",
            ville="Paris",
            pays="France",
            annees_experience=5,
            statut_professionnel="Employé"
        )
        db.add(profil)
        db.commit()
        
        response = client.get(
            "/api/admin/export/csv?data_type=candidats",
            headers={"Authorization": f"Bearer {auth_token_admin}"}
        )
        assert response.status_code == status.HTTP_200_OK
        csv_content = response.text
        
        # Vérifier que les nouveaux champs sont dans le CSV
        assert "Genre" in csv_content or "genre" in csv_content.lower()
        assert "Ville" in csv_content or "ville" in csv_content.lower()
        assert "Pays" in csv_content or "pays" in csv_content.lower()
        assert "Paris" in csv_content
        assert "France" in csv_content

