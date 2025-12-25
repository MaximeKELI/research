import pytest
from fastapi import status


class TestCandidatures:
    """Tests pour les candidatures"""

    def test_postuler(self, client, auth_token_candidat, db):
        """Test de postulation à une offre"""
        # Créer le profil candidat
        from app.models import ProfilCandidat, User
        user = db.query(User).filter(User.email == "candidat@test.com").first()
        profil = ProfilCandidat(user_id=user.id, nom="Doe", prenom="John")
        db.add(profil)
        db.commit()

        # Créer une offre
        from app.models import Offre, Entreprise, TypeOffre, StatutOffre
        entreprise_user = User(email="ent@test.com", mot_de_passe="test", role="entreprise")
        db.add(entreprise_user)
        db.commit()
        entreprise = Entreprise(user_id=entreprise_user.id, nom="Test", validee=True)
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

        response = client.post(
            "/api/candidatures/",
            headers={"Authorization": f"Bearer {auth_token_candidat}"},
            json={"offre_id": offre.id}
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["offre_id"] == offre.id
        assert data["statut"] == "en_attente"

    def test_postuler_twice(self, client, auth_token_candidat, db):
        """Test de double postulation (non autorisée)"""
        from app.models import ProfilCandidat, User, Offre, Entreprise, TypeOffre, StatutOffre
        user = db.query(User).filter(User.email == "candidat@test.com").first()
        profil = ProfilCandidat(user_id=user.id, nom="Doe", prenom="John")
        db.add(profil)
        db.commit()

        entreprise_user = User(email="ent@test.com", mot_de_passe="test", role="entreprise")
        db.add(entreprise_user)
        db.commit()
        entreprise = Entreprise(user_id=entreprise_user.id, nom="Test", validee=True)
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

        # Première postulation
        client.post(
            "/api/candidatures/",
            headers={"Authorization": f"Bearer {auth_token_candidat}"},
            json={"offre_id": offre.id}
        )

        # Deuxième postulation (doit échouer)
        response = client.post(
            "/api/candidatures/",
            headers={"Authorization": f"Bearer {auth_token_candidat}"},
            json={"offre_id": offre.id}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_mes_candidatures(self, client, auth_token_candidat, db):
        """Test de récupération des candidatures d'un candidat"""
        from app.models import ProfilCandidat, User, Offre, Entreprise, Candidature, TypeOffre, StatutOffre
        user = db.query(User).filter(User.email == "candidat@test.com").first()
        profil = ProfilCandidat(user_id=user.id, nom="Doe", prenom="John")
        db.add(profil)
        db.commit()

        entreprise_user = User(email="ent@test.com", mot_de_passe="test", role="entreprise")
        db.add(entreprise_user)
        db.commit()
        entreprise = Entreprise(user_id=entreprise_user.id, nom="Test", validee=True)
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

        candidature = Candidature(candidat_id=profil.id, offre_id=offre.id)
        db.add(candidature)
        db.commit()

        response = client.get(
            "/api/candidatures/mes-candidatures",
            headers={"Authorization": f"Bearer {auth_token_candidat}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_update_statut_candidature(self, client, auth_token_entreprise, db):
        """Test de mise à jour du statut d'une candidature"""
        from app.models import (
            ProfilCandidat, User, Offre, Entreprise, Candidature,
            TypeOffre, StatutOffre, StatutCandidature
        )
        # Créer candidat
        candidat_user = User(email="cand@test.com", mot_de_passe="test", role="candidat")
        db.add(candidat_user)
        db.commit()
        profil = ProfilCandidat(user_id=candidat_user.id, nom="Doe", prenom="John")
        db.add(profil)
        db.commit()

        # Créer entreprise
        entreprise_user = db.query(User).filter(User.email == "entreprise@test.com").first()
        entreprise = Entreprise(user_id=entreprise_user.id, nom="Test", validee=True)
        db.add(entreprise)
        db.commit()

        # Créer offre
        offre = Offre(
            entreprise_id=entreprise.id,
            titre="Test Offre",
            description="Description",
            type=TypeOffre.EMPLOI,
            statut=StatutOffre.ACTIVE
        )
        db.add(offre)
        db.commit()

        # Créer candidature
        candidature = Candidature(candidat_id=profil.id, offre_id=offre.id)
        db.add(candidature)
        db.commit()

        # Mettre à jour le statut
        response = client.put(
            f"/api/candidatures/{candidature.id}",
            headers={"Authorization": f"Bearer {auth_token_entreprise}"},
            json={"statut": "accepté"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["statut"] == "accepté"

