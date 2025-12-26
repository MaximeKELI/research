import pytest
from fastapi import status


class TestIntegration:
    """Tests d'intégration pour vérifier la communication complète"""

    def test_full_workflow_candidat(self, client, db):
        """Test du workflow complet d'un candidat"""
        # 1. Inscription
        response = client.post(
            "/api/auth/register",
            json={
                "email": "workflow@test.com",
                "mot_de_passe": "password123",
                "role": "candidat"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        user_id = response.json()["id"]

        # 2. Connexion
        response = client.post(
            "/api/auth/login",
            data={
                "username": "workflow@test.com",
                "password": "password123"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        token = response.json()["access_token"]

        # 3. Créer le profil
        response = client.post(
            "/api/candidats/profil",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "nom": "Workflow",
                "prenom": "Test",
                "niveau_etude": "Master",
                "competences": "Python, Flutter"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        profil_data = response.json()
        assert profil_data["nom"] == "Workflow"
        profil_id = profil_data["id"]

        # 4. Récupérer le profil
        response = client.get(
            "/api/candidats/profil",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["nom"] == "Workflow"

    def test_full_workflow_entreprise(self, client, db):
        """Test du workflow complet d'une entreprise"""
        # 1. Inscription
        response = client.post(
            "/api/auth/register",
            json={
                "email": "entreprise_workflow@test.com",
                "mot_de_passe": "password123",
                "role": "entreprise"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED

        # 2. Connexion
        response = client.post(
            "/api/auth/login",
            data={
                "username": "entreprise_workflow@test.com",
                "password": "password123"
            }
        )
        token = response.json()["access_token"]

        # 3. Créer le profil entreprise
        response = client.post(
            "/api/entreprises/profil",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "nom": "Workflow Company",
                "secteur": "IT",
                "description": "Une entreprise de test"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED

        # 4. Valider l'entreprise (en tant qu'admin)
        from app.models import Entreprise, User
        entreprise = db.query(Entreprise).filter(
            Entreprise.nom == "Workflow Company"
        ).first()
        entreprise.validee = True
        db.commit()

        # 5. Créer une offre
        response = client.post(
            "/api/offres",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "titre": "Développeur Full Stack",
                "description": "Recherche développeur expérimenté",
                "type": "emploi",
                "lieu": "Paris"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        offre_id = response.json()["id"]

        # 6. Récupérer les offres de l'entreprise
        response = client.get(
            "/api/offres/entreprise/mes-offres",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) > 0

    def test_candidat_postule_workflow(self, client, db):
        """Test du workflow complet: candidat postule à une offre"""
        from app.models import Entreprise, User, Offre, TypeOffre, StatutOffre
        from app.auth import get_password_hash

        # 1. Créer entreprise et offre
        entreprise_user = User(
            email="ent_integration@test.com",
            mot_de_passe=get_password_hash("test"),
            role="entreprise"
        )
        db.add(entreprise_user)
        db.commit()

        entreprise = Entreprise(
            user_id=entreprise_user.id,
            nom="Integration Test",
            validee=True
        )
        db.add(entreprise)
        db.commit()

        offre = Offre(
            entreprise_id=entreprise.id,
            titre="Offre Integration",
            description="Description",
            type=TypeOffre.EMPLOI,
            statut=StatutOffre.ACTIVE
        )
        db.add(offre)
        db.commit()

        # 2. Candidat s'inscrit
        response = client.post(
            "/api/auth/register",
            json={
                "email": "cand_integration@test.com",
                "mot_de_passe": "password123",
                "role": "candidat"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED

        # 3. Candidat se connecte
        response = client.post(
            "/api/auth/login",
            data={
                "username": "cand_integration@test.com",
                "password": "password123"
            }
        )
        token = response.json()["access_token"]

        # 4. Candidat crée son profil
        response = client.post(
            "/api/candidats/profil",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "nom": "Integration",
                "prenom": "Test"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED

        # 5. Candidat postule
        response = client.post(
            "/api/candidatures",
            headers={"Authorization": f"Bearer {token}"},
            json={"offre_id": offre.id}
        )
        assert response.status_code == status.HTTP_201_CREATED

        # 6. Entreprise voit la candidature
        entreprise_token_response = client.post(
            "/api/auth/login",
            data={
                "username": "ent_integration@test.com",
                "password": "test"
            }
        )
        entreprise_token = entreprise_token_response.json()["access_token"]

        response = client.get(
            f"/api/candidatures/entreprise/{offre.id}",
            headers={"Authorization": f"Bearer {entreprise_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        candidatures = response.json()
        assert len(candidatures) > 0

        # 7. Entreprise accepte la candidature
        candidature_id = candidatures[0]["id"]
        response = client.put(
            f"/api/candidatures/{candidature_id}",
            headers={"Authorization": f"Bearer {entreprise_token}"},
            json={"statut": "accepté"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["statut"] == "accepté"

        # 8. Candidat voit le statut mis à jour
        response = client.get(
            "/api/candidatures/mes-candidatures",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        candidatures = response.json()
        assert any(c["statut"] == "accepté" for c in candidatures)



