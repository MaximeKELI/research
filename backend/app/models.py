from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Date, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class Role(str, enum.Enum):
    ADMIN = "admin"
    ENTREPRISE = "entreprise"
    CANDIDAT = "candidat"

class TypeOffre(str, enum.Enum):
    STAGE = "stage"
    EMPLOI = "emploi"

class StatutOffre(str, enum.Enum):
    ACTIVE = "active"
    EXPIREE = "expirée"

class StatutCandidature(str, enum.Enum):
    EN_ATTENTE = "en_attente"
    ACCEPTE = "accepté"
    REFUSE = "refusé"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)
    role = Column(SQLEnum(Role), nullable=False)
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    profil_candidat = relationship("ProfilCandidat", back_populates="user", uselist=False)
    entreprise = relationship("Entreprise", back_populates="user", uselist=False)

class ProfilCandidat(Base):
    __tablename__ = "profils_candidats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    date_naissance = Column(Date, nullable=True)  # Pour calculer l'âge
    genre = Column(String, nullable=True)  # M, F, Autre
    telephone = Column(String, nullable=True)
    adresse = Column(String, nullable=True)
    ville = Column(String, nullable=True)
    pays = Column(String, nullable=True)
    code_postal = Column(String, nullable=True)
    niveau_etude = Column(String, nullable=True)
    domaine_etude = Column(String, nullable=True)  # Informatique, Commerce, etc.
    annee_obtention = Column(Integer, nullable=True)
    competences = Column(Text, nullable=True)
    annees_experience = Column(Integer, nullable=True)  # Nombre d'années d'expérience
    secteur_experience = Column(String, nullable=True)  # Secteur d'activité
    statut_professionnel = Column(String, nullable=True)  # Étudiant, Employé, Chômeur, etc.
    disponibilite = Column(String, nullable=True)  # Immédiate, 1 mois, 3 mois, etc.
    salaire_souhaite = Column(String, nullable=True)
    cv_url = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    user = relationship("User", back_populates="profil_candidat")
    candidatures = relationship("Candidature", back_populates="candidat")

class Entreprise(Base):
    __tablename__ = "entreprises"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    nom = Column(String, nullable=False)
    secteur = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    contact = Column(String, nullable=True)
    telephone = Column(String, nullable=True)
    email_contact = Column(String, nullable=True)
    adresse = Column(String, nullable=True)
    ville = Column(String, nullable=True)
    pays = Column(String, nullable=True)
    code_postal = Column(String, nullable=True)
    site_web = Column(String, nullable=True)
    taille_entreprise = Column(String, nullable=True)  # Startup, PME, Grande entreprise
    nombre_employes = Column(Integer, nullable=True)
    annee_creation = Column(Integer, nullable=True)
    type_entreprise = Column(String, nullable=True)  # Privée, Publique, ONG, etc.
    photo_url = Column(String, nullable=True)
    validee = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    user = relationship("User", back_populates="entreprise")
    offres = relationship("Offre", back_populates="entreprise")

class Offre(Base):
    __tablename__ = "offres"
    
    id = Column(Integer, primary_key=True, index=True)
    entreprise_id = Column(Integer, ForeignKey("entreprises.id"), nullable=False)
    titre = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    type = Column(SQLEnum(TypeOffre), nullable=False)
    lieu = Column(String, nullable=True)
    ville = Column(String, nullable=True)
    pays = Column(String, nullable=True)
    type_contrat = Column(String, nullable=True)  # CDI, CDD, Stage, Freelance, etc.
    salaire_min = Column(Integer, nullable=True)  # Salaire minimum
    salaire_max = Column(Integer, nullable=True)  # Salaire maximum
    salaire = Column(String, nullable=True)  # Gardé pour compatibilité
    experience_requise = Column(String, nullable=True)  # 0-2 ans, 3-5 ans, etc.
    niveau_etude_requis = Column(String, nullable=True)
    competences_requises = Column(Text, nullable=True)
    avantages = Column(Text, nullable=True)  # Avantages proposés
    date_limite = Column(Date, nullable=True)
    statut = Column(SQLEnum(StatutOffre), default=StatutOffre.ACTIVE)
    nombre_vues = Column(Integer, default=0)  # Statistiques
    nombre_candidatures = Column(Integer, default=0)  # Statistiques
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    entreprise = relationship("Entreprise", back_populates="offres")
    candidatures = relationship("Candidature", back_populates="offre")

class Candidature(Base):
    __tablename__ = "candidatures"
    
    id = Column(Integer, primary_key=True, index=True)
    candidat_id = Column(Integer, ForeignKey("profils_candidats.id"), nullable=False)
    offre_id = Column(Integer, ForeignKey("offres.id"), nullable=False)
    date_postulation = Column(DateTime(timezone=True), server_default=func.now())
    statut = Column(SQLEnum(StatutCandidature), default=StatutCandidature.EN_ATTENTE)
    
    # Relations
    candidat = relationship("ProfilCandidat", back_populates="candidatures")
    offre = relationship("Offre", back_populates="candidatures")



