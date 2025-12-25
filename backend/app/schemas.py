from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from app.models import Role, TypeOffre, StatutOffre, StatutCandidature

# Schemas pour User
class UserBase(BaseModel):
    email: EmailStr
    role: Role

class UserCreate(UserBase):
    mot_de_passe: str

class UserResponse(UserBase):
    id: int
    photo_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas pour ProfilCandidat
class ProfilCandidatBase(BaseModel):
    nom: str
    prenom: str
    date_naissance: Optional[date] = None
    genre: Optional[str] = None
    telephone: Optional[str] = None
    adresse: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    code_postal: Optional[str] = None
    niveau_etude: Optional[str] = None
    domaine_etude: Optional[str] = None
    annee_obtention: Optional[int] = None
    competences: Optional[str] = None
    annees_experience: Optional[int] = None
    secteur_experience: Optional[str] = None
    statut_professionnel: Optional[str] = None
    disponibilite: Optional[str] = None
    salaire_souhaite: Optional[str] = None

class ProfilCandidatCreate(ProfilCandidatBase):
    pass

class ProfilCandidatUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    date_naissance: Optional[date] = None
    genre: Optional[str] = None
    telephone: Optional[str] = None
    adresse: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    code_postal: Optional[str] = None
    niveau_etude: Optional[str] = None
    domaine_etude: Optional[str] = None
    annee_obtention: Optional[int] = None
    competences: Optional[str] = None
    annees_experience: Optional[int] = None
    secteur_experience: Optional[str] = None
    statut_professionnel: Optional[str] = None
    disponibilite: Optional[str] = None
    salaire_souhaite: Optional[str] = None
    cv_url: Optional[str] = None

class ProfilCandidatResponse(ProfilCandidatBase):
    id: int
    user_id: int
    cv_url: Optional[str] = None
    photo_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas pour Entreprise
class EntrepriseBase(BaseModel):
    nom: str
    secteur: Optional[str] = None
    description: Optional[str] = None
    contact: Optional[str] = None
    telephone: Optional[str] = None
    email_contact: Optional[str] = None
    adresse: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    code_postal: Optional[str] = None
    site_web: Optional[str] = None
    taille_entreprise: Optional[str] = None
    nombre_employes: Optional[int] = None
    annee_creation: Optional[int] = None
    type_entreprise: Optional[str] = None

class EntrepriseCreate(EntrepriseBase):
    pass

class EntrepriseUpdate(BaseModel):
    nom: Optional[str] = None
    secteur: Optional[str] = None
    description: Optional[str] = None
    contact: Optional[str] = None
    telephone: Optional[str] = None
    email_contact: Optional[str] = None
    adresse: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    code_postal: Optional[str] = None
    site_web: Optional[str] = None
    taille_entreprise: Optional[str] = None
    nombre_employes: Optional[int] = None
    annee_creation: Optional[int] = None
    type_entreprise: Optional[str] = None

class EntrepriseResponse(EntrepriseBase):
    id: int
    user_id: int
    photo_url: Optional[str] = None
    validee: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas pour Offre
class OffreBase(BaseModel):
    titre: str
    description: str
    type: TypeOffre
    lieu: Optional[str] = None
    salaire: Optional[str] = None
    date_limite: Optional[date] = None

class OffreCreate(OffreBase):
    pass

class OffreUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    type: Optional[TypeOffre] = None
    lieu: Optional[str] = None
    salaire: Optional[str] = None
    date_limite: Optional[date] = None
    statut: Optional[StatutOffre] = None

class OffreResponse(OffreBase):
    id: int
    entreprise_id: int
    statut: StatutOffre
    created_at: datetime
    entreprise: Optional[EntrepriseResponse] = None
    
    class Config:
        from_attributes = True

# Schemas pour Candidature
class CandidatureBase(BaseModel):
    offre_id: int

class CandidatureCreate(CandidatureBase):
    pass

class CandidatureUpdate(BaseModel):
    statut: Optional[StatutCandidature] = None

class CandidatureResponse(CandidatureBase):
    id: int
    candidat_id: int
    date_postulation: datetime
    statut: StatutCandidature
    offre: Optional[OffreResponse] = None
    candidat: Optional[ProfilCandidatResponse] = None
    
    class Config:
        from_attributes = True

# Schema pour l'authentification
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Schema pour login
class Login(BaseModel):
    email: EmailStr
    mot_de_passe: str



