import pytest
from fastapi import status
from app.models import User, ProfilCandidat, Entreprise, Offre, Candidature
from app.auth import get_password_hash
from datetime import date, datetime


class TestAdmin:
    """Tests pour les fonctionnalités admin"""

    def test_get_statistiques(self, client, auth_token_admin):
        """Test de récupération des statistiques"""
        response = client.get(
            "/api/admin/statistiques",
            headers={"Authorization": f"Bearer {auth_token_admin}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Vérifier que les clés principales sont présentes
        assert "total_users" in data
        assert "total_candidats" in data
        assert "total_entreprises" in data
        assert "total_offres" in data
        assert "total_candidatures" in data
        assert "candidats_par_genre" in data
        assert "entreprises_par_secteur" in data
        assert "candidats_par_niveau" in data
        assert "evolution_mensuelle" in data

    def test_get_statistiques_unauthorized(self, client, auth_token_candidat):
        """Test que seuls les admins peuvent accéder aux statistiques"""
        response = client.get(
            "/api/admin/statistiques",
            headers={"Authorization": f"Bearer {auth_token_candidat}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_export_csv_candidats(self, client, auth_token_admin, db):
        """Test d'export CSV des candidats"""
        # Créer un candidat de test avec données complètes
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
            niveau_etude="Master",
            annees_experience=3
        )
        db.add(profil)
        db.commit()

        response = client.get(
            "/api/admin/export/csv?data_type=candidats",
            headers={"Authorization": f"Bearer {auth_token_admin}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "Export" in response.text
        assert "Test" in response.text

    def test_export_csv_entreprises(self, client, auth_token_admin, db):
        """Test d'export CSV des entreprises"""
        user = User(
            email="export_ent@test.com",
            mot_de_passe=get_password_hash("test123"),
            role="entreprise"
        )
        db.add(user)
        db.commit()
        
        entreprise = Entreprise(
            user_id=user.id,
            nom="Test Entreprise",
            secteur="Informatique",
            ville="Lyon",
            pays="France",
            nombre_employes=50
        )
        db.add(entreprise)
        db.commit()

        response = client.get(
            "/api/admin/export/csv?data_type=entreprises",
            headers={"Authorization": f"Bearer {auth_token_admin}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert "Test Entreprise" in response.text
        assert "Informatique" in response.text

    def test_export_csv_offres(self, client, auth_token_admin, db):
        """Test d'export CSV des offres"""
        from app.models import TypeOffre, StatutOffre
        
        user = User(
            email="export_offre@test.com",
            mot_de_passe=get_password_hash("test123"),
            role="entreprise"
        )
        db.add(user)
        db.commit()
        
        entreprise = Entreprise(
            user_id=user.id,
            nom="Test Entreprise"
        )
        db.add(entreprise)
        db.commit()
        
        offre = Offre(
            entreprise_id=entreprise.id,
            titre="Test Offre",
            description="Description test",
            type=TypeOffre.EMPLOI,
            statut=StatutOffre.ACTIVE,
            salaire_min=30000,
            salaire_max=50000
        )
        db.add(offre)
        db.commit()

        response = client.get(
            "/api/admin/export/csv?data_type=offres",
            headers={"Authorization": f"Bearer {auth_token_admin}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert "Test Offre" in response.text

    def test_export_pdf(self, client, auth_token_admin):
        """Test d'export PDF des statistiques"""
        response = client.get(
            "/api/admin/export/pdf",
            headers={"Authorization": f"Bearer {auth_token_admin}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/pdf"
        assert len(response.content) > 0

    def test_export_unauthorized(self, client, auth_token_candidat):
        """Test que seuls les admins peuvent exporter"""
        response = client.get(
            "/api/admin/export/csv?data_type=candidats",
            headers={"Authorization": f"Bearer {auth_token_candidat}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_statistiques_with_data(self, client, auth_token_admin, db):
        """Test des statistiques avec des données réelles"""
        # Créer plusieurs candidats avec différents genres
        for i, genre in enumerate(["M", "F", "M", "F", "M"]):
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
                niveau_etude="Master" if i % 2 == 0 else "Licence"
            )
            db.add(profil)
            db.commit()

        response = client.get(
            "/api/admin/statistiques",
            headers={"Authorization": f"Bearer {auth_token_admin}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Vérifier les statistiques par genre
        assert data["candidats_par_genre"]["M"] == 3
        assert data["candidats_par_genre"]["F"] == 2
        assert data["total_candidats"] >= 5

