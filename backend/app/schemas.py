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
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas pour ProfilCandidat
class ProfilCandidatBase(BaseModel):
    nom: str
    prenom: str
    niveau_etude: Optional[str] = None
    competences: Optional[str] = None

class ProfilCandidatCreate(ProfilCandidatBase):
    pass

class ProfilCandidatUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    niveau_etude: Optional[str] = None
    competences: Optional[str] = None
    cv_url: Optional[str] = None

class ProfilCandidatResponse(ProfilCandidatBase):
    id: int
    user_id: int
    cv_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas pour Entreprise
class EntrepriseBase(BaseModel):
    nom: str
    secteur: Optional[str] = None
    description: Optional[str] = None
    contact: Optional[str] = None

class EntrepriseCreate(EntrepriseBase):
    pass

class EntrepriseUpdate(BaseModel):
    nom: Optional[str] = None
    secteur: Optional[str] = None
    description: Optional[str] = None
    contact: Optional[str] = None

class EntrepriseResponse(EntrepriseBase):
    id: int
    user_id: int
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


