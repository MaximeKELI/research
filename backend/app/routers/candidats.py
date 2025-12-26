from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app import auth
from app.models import User, ProfilCandidat
from app.schemas import ProfilCandidatCreate, ProfilCandidatUpdate, ProfilCandidatResponse
from app.auth import require_role
from app.security.validation import sanitize_string, validate_file_upload
import os
import uuid
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

UPLOAD_DIR = Path("uploads/cv")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

PHOTO_DIR = Path("uploads/photos")
PHOTO_DIR.mkdir(parents=True, exist_ok=True)

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
    
    # Sanitizer les données avant création
    nom = sanitize_string(profil_data.nom, max_length=100) if profil_data.nom else None
    prenom = sanitize_string(profil_data.prenom, max_length=100) if profil_data.prenom else None
    niveau_etude = sanitize_string(profil_data.niveau_etude, max_length=50) if profil_data.niveau_etude else None
    competences = sanitize_string(profil_data.competences, max_length=1000) if profil_data.competences else None
    
    # Sanitizer les nouveaux champs
    telephone = sanitize_string(profil_data.telephone, max_length=20) if profil_data.telephone else None
    adresse = sanitize_string(profil_data.adresse, max_length=255) if profil_data.adresse else None
    ville = sanitize_string(profil_data.ville, max_length=100) if profil_data.ville else None
    pays = sanitize_string(profil_data.pays, max_length=100) if profil_data.pays else None
    code_postal = sanitize_string(profil_data.code_postal, max_length=20) if profil_data.code_postal else None
    domaine_etude = sanitize_string(profil_data.domaine_etude, max_length=100) if profil_data.domaine_etude else None
    secteur_experience = sanitize_string(profil_data.secteur_experience, max_length=100) if profil_data.secteur_experience else None
    statut_professionnel = sanitize_string(profil_data.statut_professionnel, max_length=50) if profil_data.statut_professionnel else None
    disponibilite = sanitize_string(profil_data.disponibilite, max_length=50) if profil_data.disponibilite else None
    salaire_souhaite = sanitize_string(profil_data.salaire_souhaite, max_length=50) if profil_data.salaire_souhaite else None
    genre = sanitize_string(profil_data.genre, max_length=10) if profil_data.genre else None
    
    # Utiliser les données sanitizées
    db_profil = ProfilCandidat(
        user_id=current_user.id,
        nom=nom,
        prenom=prenom,
        date_naissance=profil_data.date_naissance,
        genre=genre,
        telephone=telephone,
        adresse=adresse,
        ville=ville,
        pays=pays,
        code_postal=code_postal,
        niveau_etude=niveau_etude,
        domaine_etude=domaine_etude,
        annee_obtention=profil_data.annee_obtention,
        competences=competences,
        annees_experience=profil_data.annees_experience,
        secteur_experience=secteur_experience,
        statut_professionnel=statut_professionnel,
        disponibilite=disponibilite,
        salaire_souhaite=salaire_souhaite
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
    
    # Sanitizer et mettre à jour les champs
    if profil_data.nom is not None:
        profil.nom = sanitize_string(profil_data.nom, max_length=100)
    if profil_data.prenom is not None:
        profil.prenom = sanitize_string(profil_data.prenom, max_length=100)
    if profil_data.niveau_etude is not None:
        profil.niveau_etude = sanitize_string(profil_data.niveau_etude, max_length=50)
    if profil_data.competences is not None:
        profil.competences = sanitize_string(profil_data.competences, max_length=1000)
    
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
    
    # Lire le contenu du fichier
    content = await file.read()
    
    # Validation sécurisée du fichier
    is_valid, error_msg = validate_file_upload(file.filename, content)
    if not is_valid:
        logger.warning(f"Invalid file upload attempt: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    # Sanitizer le nom de fichier
    safe_filename = sanitize_string(file.filename, max_length=255)
    if not safe_filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filename"
        )
    
    # Générer un nom unique sécurisé
    file_extension = Path(safe_filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Sauvegarder le fichier
    with open(file_path, "wb") as buffer:
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
    
    # Stocker le chemin relatif pour l'URL
    relative_path = f"cv/{unique_filename}"
    profil.cv_url = relative_path
    db.commit()
    
    return {"message": "CV uploadé avec succès", "cv_url": f"/uploads/{relative_path}"}

@router.post("/upload-photo")
async def upload_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Uploader une photo de profil pour un candidat"""
    if current_user.role.value != "candidat":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux candidats"
        )
    
    # Lire le contenu du fichier
    content = await file.read()
    
    # Validation sécurisée du fichier image
    is_valid, error_msg = validate_file_upload(file.filename, content, max_size=2 * 1024 * 1024, file_type="image")
    if not is_valid:
        logger.warning(f"Invalid photo upload attempt: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    # Sanitizer le nom de fichier
    safe_filename = sanitize_string(file.filename, max_length=255)
    if not safe_filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filename"
        )
    
    # Générer un nom unique sécurisé
    file_extension = Path(safe_filename).suffix.lower()
    # S'assurer que l'extension est valide
    if file_extension not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        file_extension = '.jpg'  # Par défaut
    
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = PHOTO_DIR / unique_filename
    
    # Sauvegarder le fichier
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    # Mettre à jour le profil
    profil = db.query(ProfilCandidat).filter(ProfilCandidat.user_id == current_user.id).first()
    if not profil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil non trouvé. Créez d'abord votre profil."
        )
    
    # Supprimer l'ancienne photo si existe
    if profil.photo_url:
        old_file = Path(PHOTO_DIR) / profil.photo_url.split('/')[-1]
        if old_file.exists():
            old_file.unlink()
    
    # Stocker le chemin relatif pour l'URL
    relative_path = f"photos/{unique_filename}"
    profil.photo_url = relative_path
    db.commit()
    
    return {"message": "Photo uploadée avec succès", "photo_url": f"/uploads/{relative_path}"}

