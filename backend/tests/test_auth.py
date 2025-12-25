import pytest
from fastapi import status


class TestAuth:
    """Tests pour l'authentification"""

    def test_register_candidat(self, client):
        """Test d'inscription d'un candidat"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "nouveau@test.com",
                "mot_de_passe": "password123",
                "role": "candidat"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "nouveau@test.com"
        assert data["role"] == "candidat"
        assert "id" in data

    def test_register_entreprise(self, client):
        """Test d'inscription d'une entreprise"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "entreprise@test.com",
                "mot_de_passe": "password123",
                "role": "entreprise"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "entreprise@test.com"
        assert data["role"] == "entreprise"

    def test_register_duplicate_email(self, client, test_user_candidat):
        """Test d'inscription avec un email déjà utilisé"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "candidat@test.com",
                "mot_de_passe": "password123",
                "role": "candidat"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_success(self, client, test_user_candidat):
        """Test de connexion réussie"""
        response = client.post(
            "/api/auth/login",
            data={
                "username": "candidat@test.com",
                "password": "test123"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user_candidat):
        """Test de connexion avec mauvais mot de passe"""
        response = client.post(
            "/api/auth/login",
            data={
                "username": "candidat@test.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, client):
        """Test de connexion avec utilisateur inexistant"""
        response = client.post(
            "/api/auth/login",
            data={
                "username": "nonexistent@test.com",
                "password": "password123"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user(self, client, auth_token_candidat):
        """Test de récupération de l'utilisateur actuel"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {auth_token_candidat}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "candidat@test.com"
        assert data["role"] == "candidat"

    def test_get_current_user_no_token(self, client):
        """Test sans token d'authentification"""
        response = client.get("/api/auth/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


