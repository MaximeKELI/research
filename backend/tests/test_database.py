import pytest
from sqlalchemy.exc import IntegrityError
from app.models import User, ProfilCandidat, Entreprise, Offre, Candidature
from app.auth import get_password_hash


class TestDatabase:
    """Tests pour la base de données"""

    def test_create_user(self, db):
        """Test de création d'un utilisateur"""
        user = User(
            email="test@example.com",
            mot_de_passe=get_password_hash("password123"),
            role="candidat"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.role == "candidat"

    def test_user_unique_email(self, db):
        """Test de l'unicité de l'email"""
        user1 = User(
            email="unique@test.com",
            mot_de_passe=get_password_hash("pass"),
            role="candidat"
        )
        db.add(user1)
        db.commit()

        user2 = User(
            email="unique@test.com",  # Même email
            mot_de_passe=get_password_hash("pass"),
            role="entreprise"
        )
        db.add(user2)

        with pytest.raises(IntegrityError):
            db.commit()

    def test_create_profil_candidat(self, db):
        """Test de création d'un profil candidat"""
        user = User(
            email="candidat@test.com",
            mot_de_passe=get_password_hash("pass"),
            role="candidat"
        )
        db.add(user)
        db.commit()

        profil = ProfilCandidat(
            user_id=user.id,
            nom="Doe",
            prenom="John",
            niveau_etude="Master",
            competences="Python, Flutter"
        )
        db.add(profil)
        db.commit()
        db.refresh(profil)

        assert profil.id is not None
        assert profil.nom == "Doe"
        assert profil.user_id == user.id

    def test_profil_candidat_unique_user(self, db):
        """Test de l'unicité du user_id pour le profil candidat"""
        user = User(
            email="test@test.com",
            mot_de_passe=get_password_hash("pass"),
            role="candidat"
        )
        db.add(user)
        db.commit()

        profil1 = ProfilCandidat(user_id=user.id, nom="Doe", prenom="John")
        db.add(profil1)
        db.commit()

        profil2 = ProfilCandidat(user_id=user.id, nom="Smith", prenom="Jane")
        db.add(profil2)

        with pytest.raises(IntegrityError):
            db.commit()

    def test_create_entreprise(self, db):
        """Test de création d'une entreprise"""
        user = User(
            email="entreprise@test.com",
            mot_de_passe=get_password_hash("pass"),
            role="entreprise"
        )
        db.add(user)
        db.commit()

        entreprise = Entreprise(
            user_id=user.id,
            nom="Test Company",
            secteur="IT",
            description="Une entreprise de test",
            validee=False
        )
        db.add(entreprise)
        db.commit()
        db.refresh(entreprise)

        assert entreprise.id is not None
        assert entreprise.nom == "Test Company"
        assert entreprise.validee is False

    def test_create_offre(self, db):
        """Test de création d'une offre"""
        from app.models import TypeOffre, StatutOffre

        user = User(
            email="entreprise@test.com",
            mot_de_passe=get_password_hash("pass"),
            role="entreprise"
        )
        db.add(user)
        db.commit()

        entreprise = Entreprise(
            user_id=user.id,
            nom="Test Company",
            validee=True
        )
        db.add(entreprise)
        db.commit()

        offre = Offre(
            entreprise_id=entreprise.id,
            titre="Développeur Python",
            description="Recherche développeur",
            type=TypeOffre.EMPLOI,
            lieu="Paris",
            statut=StatutOffre.ACTIVE
        )
        db.add(offre)
        db.commit()
        db.refresh(offre)

        assert offre.id is not None
        assert offre.titre == "Développeur Python"
        assert offre.type == TypeOffre.EMPLOI

    def test_create_candidature(self, db):
        """Test de création d'une candidature"""
        from app.models import TypeOffre, StatutOffre, StatutCandidature

        # Créer candidat
        candidat_user = User(
            email="candidat@test.com",
            mot_de_passe=get_password_hash("pass"),
            role="candidat"
        )
        db.add(candidat_user)
        db.commit()

        profil = ProfilCandidat(
            user_id=candidat_user.id,
            nom="Doe",
            prenom="John"
        )
        db.add(profil)
        db.commit()

        # Créer entreprise et offre
        entreprise_user = User(
            email="entreprise@test.com",
            mot_de_passe=get_password_hash("pass"),
            role="entreprise"
        )
        db.add(entreprise_user)
        db.commit()

        entreprise = Entreprise(
            user_id=entreprise_user.id,
            nom="Test Company",
            validee=True
        )
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

        # Créer candidature
        candidature = Candidature(
            candidat_id=profil.id,
            offre_id=offre.id,
            statut=StatutCandidature.EN_ATTENTE
        )
        db.add(candidature)
        db.commit()
        db.refresh(candidature)

        assert candidature.id is not None
        assert candidature.candidat_id == profil.id
        assert candidature.offre_id == offre.id

    def test_cascade_delete_user(self, db):
        """Test de suppression en cascade d'un utilisateur"""
        from app.models import TypeOffre, StatutOffre

        user = User(
            email="test@test.com",
            mot_de_passe=get_password_hash("pass"),
            role="candidat"
        )
        db.add(user)
        db.commit()

        profil = ProfilCandidat(user_id=user.id, nom="Doe", prenom="John")
        db.add(profil)
        db.commit()

        profil_id = profil.id

        # Supprimer l'utilisateur
        db.delete(user)
        db.commit()

        # Vérifier que le profil a été supprimé en cascade
        deleted_profil = db.query(ProfilCandidat).filter(ProfilCandidat.id == profil_id).first()
        assert deleted_profil is None

    def test_foreign_key_constraints(self, db):
        """Test des contraintes de clé étrangère"""
        from app.models import TypeOffre, StatutOffre

        # Essayer de créer une offre avec un entreprise_id inexistant
        offre = Offre(
            entreprise_id=99999,  # ID inexistant
            titre="Test",
            description="Test",
            type=TypeOffre.EMPLOI,
            statut=StatutOffre.ACTIVE
        )
        db.add(offre)

        with pytest.raises(IntegrityError):
            db.commit()

