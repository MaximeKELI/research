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

@router.post("/upload-photo")
async def upload_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Uploader une photo de profil pour une entreprise"""
    if current_user.role.value != "entreprise":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux entreprises"
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
    
    # Mettre à jour le profil entreprise
    entreprise = db.query(Entreprise).filter(Entreprise.user_id == current_user.id).first()
    if not entreprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil entreprise non trouvé. Créez d'abord votre profil."
        )
    
    # Supprimer l'ancienne photo si existe
    if entreprise.photo_url:
        old_file = Path(PHOTO_DIR) / entreprise.photo_url.split('/')[-1]
        if old_file.exists():
            old_file.unlink()
    
    # Stocker le chemin relatif pour l'URL
    relative_path = f"photos/{unique_filename}"
    entreprise.photo_url = relative_path
    db.commit()
    
    return {"message": "Photo uploadée avec succès", "photo_url": f"/uploads/{relative_path}"}



