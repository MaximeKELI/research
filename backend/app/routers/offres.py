from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional
from datetime import date
from app.database import get_db
from app import auth
from app.models import User, Entreprise, Offre, TypeOffre, StatutOffre
from app.schemas import OffreCreate, OffreUpdate, OffreResponse

router = APIRouter()

@router.post("/", response_model=OffreResponse, status_code=status.HTTP_201_CREATED)
async def create_offre(
    offre_data: OffreCreate,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role.value != "entreprise":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seules les entreprises peuvent publier des offres"
        )
    
    entreprise = db.query(Entreprise).filter(Entreprise.user_id == current_user.id).first()
    if not entreprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil entreprise non trouvé"
        )
    
    if not entreprise.validee:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Votre entreprise n'est pas encore validée par l'administrateur"
        )
    
    db_offre = Offre(
        entreprise_id=entreprise.id,
        **offre_data.model_dump()
    )
    db.add(db_offre)
    db.commit()
    db.refresh(db_offre)
    return db_offre

@router.get("/", response_model=list[OffreResponse])
async def get_offres(
    skip: int = 0,
    limit: int = 20,
    type: Optional[TypeOffre] = None,
    lieu: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Offre).filter(Offre.statut == StatutOffre.ACTIVE)
    
    if type:
        query = query.filter(Offre.type == type)
    
    if lieu:
        query = query.filter(Offre.lieu.ilike(f"%{lieu}%"))
    
    if search:
        query = query.filter(
            or_(
                Offre.titre.ilike(f"%{search}%"),
                Offre.description.ilike(f"%{search}%")
            )
        )
    
    offres = query.order_by(Offre.created_at.desc()).offset(skip).limit(limit).all()
    return offres

@router.get("/{offre_id}", response_model=OffreResponse)
async def get_offre(offre_id: int, db: Session = Depends(get_db)):
    offre = db.query(Offre).filter(Offre.id == offre_id).first()
    if not offre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offre non trouvée"
        )
    return offre

@router.get("/entreprise/mes-offres", response_model=list[OffreResponse])
async def get_mes_offres(
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
    
    offres = db.query(Offre).filter(Offre.entreprise_id == entreprise.id).order_by(Offre.created_at.desc()).all()
    return offres

@router.put("/{offre_id}", response_model=OffreResponse)
async def update_offre(
    offre_id: int,
    offre_data: OffreUpdate,
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
    
    offre = db.query(Offre).filter(
        and_(Offre.id == offre_id, Offre.entreprise_id == entreprise.id)
    ).first()
    
    if not offre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offre non trouvée"
        )
    
    update_data = offre_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(offre, field, value)
    
    db.commit()
    db.refresh(offre)
    return offre

@router.delete("/{offre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_offre(
    offre_id: int,
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
    
    offre = db.query(Offre).filter(
        and_(Offre.id == offre_id, Offre.entreprise_id == entreprise.id)
    ).first()
    
    if not offre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offre non trouvée"
        )
    
    db.delete(offre)
    db.commit()
    return None

