import pytest
from fastapi import status
from datetime import date, timedelta


class TestOffres:
    """Tests pour les offres"""

    def test_create_offre(self, client, auth_token_entreprise, db):
        """Test de création d'une offre"""
        # Créer d'abord le profil entreprise
        from app.models import Entreprise, User
        user = db.query(User).filter(User.email == "entreprise@test.com").first()
        entreprise = Entreprise(
            user_id=user.id,
            nom="Test Company",
            validee=True
        )
        db.add(entreprise)
        db.commit()

        response = client.post(
            "/api/offres",
            headers={"Authorization": f"Bearer {auth_token_entreprise}"},
            json={
                "titre": "Développeur Python",
                "description": "Recherche développeur Python expérimenté",
                "type": "emploi",
                "lieu": "Paris",
                "salaire": "3000-4000€",
                "date_limite": (date.today() + timedelta(days=30)).isoformat()
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["titre"] == "Développeur Python"
        assert data["type"] == "emploi"

    def test_create_offre_entreprise_not_validated(self, client, auth_token_entreprise, db):
        """Test de création d'offre par entreprise non validée"""
        from app.models import Entreprise, User
        user = db.query(User).filter(User.email == "entreprise@test.com").first()
        entreprise = Entreprise(
            user_id=user.id,
            nom="Test Company",
            validee=False  # Non validée
        )
        db.add(entreprise)
        db.commit()

        response = client.post(
            "/api/offres",
            headers={"Authorization": f"Bearer {auth_token_entreprise}"},
            json={
                "titre": "Développeur Python",
                "description": "Description",
                "type": "emploi"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_offres(self, client, db):
        """Test de récupération de la liste des offres"""
        # Créer une offre de test
        from app.models import Offre, Entreprise, User, TypeOffre, StatutOffre
        user = User(email="test@test.com", mot_de_passe="test", role="entreprise")
        db.add(user)
        db.commit()
        entreprise = Entreprise(user_id=user.id, nom="Test", validee=True)
        db.add(entreprise)
        db.commit()
        offre = Offre(
            entreprise_id=entreprise.id,
            titre="Test Offre",
            description="Description test",
            type=TypeOffre.EMPLOI,
            statut=StatutOffre.ACTIVE
        )
        db.add(offre)
        db.commit()

        response = client.get("/api/offres")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_offres_with_filters(self, client, db):
        """Test de récupération avec filtres"""
        from app.models import Offre, Entreprise, User, TypeOffre, StatutOffre
        user = User(email="test@test.com", mot_de_passe="test", role="entreprise")
        db.add(user)
        db.commit()
        entreprise = Entreprise(user_id=user.id, nom="Test", validee=True)
        db.add(entreprise)
        db.commit()
        offre = Offre(
            entreprise_id=entreprise.id,
            titre="Stage Python",
            description="Stage en développement",
            type=TypeOffre.STAGE,
            lieu="Lyon",
            statut=StatutOffre.ACTIVE
        )
        db.add(offre)
        db.commit()

        # Test avec filtre type
        response = client.get("/api/offres?type=stage")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(o["type"] == "stage" for o in data)

        # Test avec filtre lieu
        response = client.get("/api/offres?lieu=Lyon")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0

        # Test avec recherche
        response = client.get("/api/offres?search=Python")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0

    def test_get_offre_detail(self, client, db):
        """Test de récupération d'une offre spécifique"""
        from app.models import Offre, Entreprise, User, TypeOffre, StatutOffre
        user = User(email="test@test.com", mot_de_passe="test", role="entreprise")
        db.add(user)
        db.commit()
        entreprise = Entreprise(user_id=user.id, nom="Test", validee=True)
        db.add(entreprise)
        db.commit()
        offre = Offre(
            entreprise_id=entreprise.id,
            titre="Test Offre",
            description="Description test",
            type=TypeOffre.EMPLOI,
            statut=StatutOffre.ACTIVE
        )
        db.add(offre)
        db.commit()

        response = client.get(f"/api/offres/{offre.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == offre.id
        assert data["titre"] == "Test Offre"

    def test_get_mes_offres(self, client, auth_token_entreprise, db):
        """Test de récupération des offres d'une entreprise"""
        from app.models import Entreprise, User, Offre, TypeOffre, StatutOffre
        user = db.query(User).filter(User.email == "entreprise@test.com").first()
        entreprise = Entreprise(user_id=user.id, nom="Test Company", validee=True)
        db.add(entreprise)
        db.commit()
        offre = Offre(
            entreprise_id=entreprise.id,
            titre="Test Offre",
            description="Description",
            type=TypeOffre.EMPLOI,
            statut=StatutOffre.ACTIVE
        )
        db.add(offre)
        db.commit()

        response = client.get(
            "/api/offres/entreprise/mes-offres",
            headers={"Authorization": f"Bearer {auth_token_entreprise}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_delete_offre(self, client, auth_token_entreprise, db):
        """Test de suppression d'une offre"""
        from app.models import Entreprise, User, Offre, TypeOffre, StatutOffre
        user = db.query(User).filter(User.email == "entreprise@test.com").first()
        entreprise = Entreprise(user_id=user.id, nom="Test Company", validee=True)
        db.add(entreprise)
        db.commit()
        offre = Offre(
            entreprise_id=entreprise.id,
            titre="Test Offre",
            description="Description",
            type=TypeOffre.EMPLOI,
            statut=StatutOffre.ACTIVE
        )
        db.add(offre)
        db.commit()
        offre_id = offre.id

        response = client.delete(
            f"/api/offres/{offre_id}",
            headers={"Authorization": f"Bearer {auth_token_entreprise}"}
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Vérifier que l'offre a été supprimée
        response = client.get(f"/api/offres/{offre_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND



