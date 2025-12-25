from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app import auth
from app.models import User, ProfilCandidat
from app.schemas import ProfilCandidatCreate, ProfilCandidatUpdate, ProfilCandidatResponse
from app.auth import require_role
import os
import uuid
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = Path("uploads/cv")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/profil", response_model=ProfilCandidatResponse, status_code=status.HTTP_201_CREATED)
async def create_profil(
    profil_data: ProfilCandidatCreate,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role.value != "candidat":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les candidats peuvent créer un profil"
        )
    
    # Vérifier si le profil existe déjà
    existing_profil = db.query(ProfilCandidat).filter(ProfilCandidat.user_id == current_user.id).first()
    if existing_profil:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profil déjà créé"
        )
    
    db_profil = ProfilCandidat(
        user_id=current_user.id,
        **profil_data.model_dump()
    )
    db.add(db_profil)
    db.commit()
    db.refresh(db_profil)
    return db_profil

@router.get("/profil", response_model=ProfilCandidatResponse)
async def get_profil(
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role.value != "candidat":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux candidats"
        )
    
    profil = db.query(ProfilCandidat).filter(ProfilCandidat.user_id == current_user.id).first()
    if not profil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil non trouvé"
        )
    return profil

@router.put("/profil", response_model=ProfilCandidatResponse)
async def update_profil(
    profil_data: ProfilCandidatUpdate,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role.value != "candidat":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux candidats"
        )
    
    profil = db.query(ProfilCandidat).filter(ProfilCandidat.user_id == current_user.id).first()
    if not profil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil non trouvé"
        )
    
    update_data = profil_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profil, field, value)
    
    db.commit()
    db.refresh(profil)
    return profil

@router.post("/upload-cv")
async def upload_cv(
    file: UploadFile = File(...),
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role.value != "candidat":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux candidats"
        )
    
    # Vérifier que c'est un PDF
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seuls les fichiers PDF sont acceptés"
        )
    
    # Générer un nom unique
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Sauvegarder le fichier
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Mettre à jour le profil
    profil = db.query(ProfilCandidat).filter(ProfilCandidat.user_id == current_user.id).first()
    if not profil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil non trouvé. Créez d'abord votre profil."
        )
    
    # Supprimer l'ancien CV si existe
    if profil.cv_url:
        old_file = Path(profil.cv_url)
        if old_file.exists():
            old_file.unlink()
    
    profil.cv_url = str(file_path)
    db.commit()
    
    return {"message": "CV uploadé avec succès", "cv_url": str(file_path)}

