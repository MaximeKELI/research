import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

from app.database import Base, get_db
from app.main import app
from app.models import User
from app.auth import get_password_hash

# Base de données de test en mémoire SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Créer une nouvelle base de données pour chaque test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Créer un client de test avec une base de données de test"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_candidat(db):
    """Créer un utilisateur candidat de test"""
    user = User(
        email="candidat@test.com",
        mot_de_passe=get_password_hash("test123"),
        role="candidat"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_user_entreprise(db):
    """Créer un utilisateur entreprise de test"""
    user = User(
        email="entreprise@test.com",
        mot_de_passe=get_password_hash("test123"),
        role="entreprise"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_user_admin(db):
    """Créer un utilisateur admin de test"""
    user = User(
        email="admin@test.com",
        mot_de_passe=get_password_hash("test123"),
        role="admin"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_token_candidat(client, test_user_candidat):
    """Obtenir un token JWT pour un candidat"""
    response = client.post(
        "/api/auth/login",
        data={"username": "candidat@test.com", "password": "test123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_token_entreprise(client, test_user_entreprise):
    """Obtenir un token JWT pour une entreprise"""
    response = client.post(
        "/api/auth/login",
        data={"username": "entreprise@test.com", "password": "test123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_token_admin(client, test_user_admin):
    """Obtenir un token JWT pour un admin"""
    response = client.post(
        "/api/auth/login",
        data={"username": "admin@test.com", "password": "test123"}
    )
    return response.json()["access_token"]


