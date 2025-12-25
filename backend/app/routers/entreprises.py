from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app import auth
from app.models import User, Entreprise
from app.schemas import EntrepriseCreate, EntrepriseUpdate, EntrepriseResponse
from app.security.validation import sanitize_string, validate_file_upload
import uuid
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

PHOTO_DIR = Path("uploads/photos")
PHOTO_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/profil", response_model=EntrepriseResponse, status_code=status.HTTP_201_CREATED)
async def create_profil_entreprise(
    entreprise_data: EntrepriseCreate,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role.value != "entreprise":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seules les entreprises peuvent créer un profil"
        )
    
    # Vérifier si le profil existe déjà
    existing_entreprise = db.query(Entreprise).filter(Entreprise.user_id == current_user.id).first()
    if existing_entreprise:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profil entreprise déjà créé"
        )
    
    db_entreprise = Entreprise(
        user_id=current_user.id,
        **entreprise_data.model_dump()
    )
    db.add(db_entreprise)
    db.commit()
    db.refresh(db_entreprise)
    return db_entreprise

@router.get("/profil", response_model=EntrepriseResponse)
async def get_profil_entreprise(
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role.value != "entreprise":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux entreprises"
        )
    
    entreprise = db.query(Entreprise).filter(Entreprise.user_id == current_user.id).first()
    if not entreprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil entreprise non trouvé"
        )
    return entreprise

@router.put("/profil", response_model=EntrepriseResponse)
async def update_profil_entreprise(
    entreprise_data: EntrepriseUpdate,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role.value != "entreprise":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux entreprises"
        )
    
    entreprise = db.query(Entreprise).filter(Entreprise.user_id == current_user.id).first()
    if not entreprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil entreprise non trouvé"
        )
    
    update_data = entreprise_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entreprise, field, value)
    
    db.commit()
    db.refresh(entreprise)
    return entreprise



