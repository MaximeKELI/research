import pytest
from fastapi import status


class TestCandidats:
    """Tests pour les candidats"""

    def test_create_profil_candidat(self, client, auth_token_candidat):
        """Test de création de profil candidat"""
        response = client.post(
            "/api/candidats/profil",
            headers={"Authorization": f"Bearer {auth_token_candidat}"},
            json={
                "nom": "Doe",
                "prenom": "John",
                "niveau_etude": "Master",
                "competences": "Python, Flutter, PostgreSQL"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nom"] == "Doe"
        assert data["prenom"] == "John"
        assert data["niveau_etude"] == "Master"

    def test_create_profil_unauthorized(self, client, auth_token_entreprise):
        """Test de création de profil par une entreprise (non autorisé)"""
        response = client.post(
            "/api/candidats/profil",
            headers={"Authorization": f"Bearer {auth_token_entreprise}"},
            json={
                "nom": "Doe",
                "prenom": "John"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_profil_candidat(self, client, auth_token_candidat, db):
        """Test de récupération du profil candidat"""
        # Créer d'abord le profil
        from app.models import ProfilCandidat, User
        user = db.query(User).filter(User.email == "candidat@test.com").first()
        profil = ProfilCandidat(
            user_id=user.id,
            nom="Doe",
            prenom="John"
        )
        db.add(profil)
        db.commit()

        response = client.get(
            "/api/candidats/profil",
            headers={"Authorization": f"Bearer {auth_token_candidat}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nom"] == "Doe"
        assert data["prenom"] == "John"

    def test_get_profil_not_found(self, client, auth_token_candidat):
        """Test de récupération d'un profil inexistant"""
        response = client.get(
            "/api/candidats/profil",
            headers={"Authorization": f"Bearer {auth_token_candidat}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_profil_candidat(self, client, auth_token_candidat, db):
        """Test de mise à jour du profil candidat"""
        # Créer d'abord le profil
        from app.models import ProfilCandidat, User
        user = db.query(User).filter(User.email == "candidat@test.com").first()
        profil = ProfilCandidat(
            user_id=user.id,
            nom="Doe",
            prenom="John"
        )
        db.add(profil)
        db.commit()

        response = client.put(
            "/api/candidats/profil",
            headers={"Authorization": f"Bearer {auth_token_candidat}"},
            json={
                "nom": "Smith",
                "competences": "Python, Django, FastAPI"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nom"] == "Smith"
        assert data["competences"] == "Python, Django, FastAPI"

    def test_upload_cv(self, client, auth_token_candidat, db):
        """Test d'upload de CV"""
        # Créer d'abord le profil
        from app.models import ProfilCandidat, User
        user = db.query(User).filter(User.email == "candidat@test.com").first()
        profil = ProfilCandidat(
            user_id=user.id,
            nom="Doe",
            prenom="John"
        )
        db.add(profil)
        db.commit()

        # Créer un fichier PDF de test
        pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 1\ntrailer\n<<\n/Root 1 0 R\n>>\n%%EOF"

        response = client.post(
            "/api/candidats/upload-cv",
            headers={"Authorization": f"Bearer {auth_token_candidat}"},
            files={"file": ("test_cv.pdf", pdf_content, "application/pdf")}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "cv_url" in data

    def test_upload_cv_not_pdf(self, client, auth_token_candidat, db):
        """Test d'upload d'un fichier non-PDF"""
        # Créer d'abord le profil
        from app.models import ProfilCandidat, User
        user = db.query(User).filter(User.email == "candidat@test.com").first()
        profil = ProfilCandidat(
            user_id=user.id,
            nom="Doe",
            prenom="John"
        )
        db.add(profil)
        db.commit()

        response = client.post(
            "/api/candidats/upload-cv",
            headers={"Authorization": f"Bearer {auth_token_candidat}"},
            files={"file": ("test.txt", b"test content", "text/plain")}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST



