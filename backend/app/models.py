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
    niveau_etude = Column(String)
    competences = Column(Text)
    cv_url = Column(String)
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
    secteur = Column(String)
    description = Column(Text)
    contact = Column(String)
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
    lieu = Column(String)
    salaire = Column(String)
    date_limite = Column(Date)
    statut = Column(SQLEnum(StatutOffre), default=StatutOffre.ACTIVE)
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

