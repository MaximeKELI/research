from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db, settings
from app import auth
from app.models import User, Role
from app.schemas import UserCreate, UserResponse, Token, Login
from app.auth import create_access_token, get_password_hash
from app.security.validation import sanitize_string, validate_file_upload
import uuid
from pathlib import Path
import logging

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Vérifier si l'email existe déjà
    existing_user = auth.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email déjà utilisé"
        )
    
    # Créer le nouvel utilisateur
    hashed_password = get_password_hash(user_data.mot_de_passe)
    db_user = User(
        email=user_data.email,
        mot_de_passe=hashed_password,
        role=user_data.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(auth.get_current_user)):
    return current_user

@router.post("/upload-photo")
async def upload_user_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Uploader une photo de profil pour n'importe quel utilisateur"""
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
    
    # Supprimer l'ancienne photo si existe
    if current_user.photo_url:
        old_file = Path(PHOTO_DIR) / current_user.photo_url.split('/')[-1]
        if old_file.exists():
            old_file.unlink()
    
    # Stocker le chemin relatif pour l'URL
    relative_path = f"photos/{unique_filename}"
    current_user.photo_url = relative_path
    db.commit()
    
    return {"message": "Photo uploadée avec succès", "photo_url": f"/uploads/{relative_path}"}



