from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import auth
from app.models import User, Entreprise, Offre, Candidature, ProfilCandidat
from app.schemas import EntrepriseResponse, OffreResponse
from app.auth import require_role

router = APIRouter()

@router.get("/entreprises/pending", response_model=list[EntrepriseResponse])
async def get_entreprises_pending(
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    entreprises = db.query(Entreprise).filter(Entreprise.validee == False).all()
    return entreprises

@router.put("/entreprises/{entreprise_id}/validate")
async def validate_entreprise(
    entreprise_id: int,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    entreprise = db.query(Entreprise).filter(Entreprise.id == entreprise_id).first()
    if not entreprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entreprise non trouvée"
        )
    
    entreprise.validee = True
    db.commit()
    return {"message": "Entreprise validée avec succès"}

@router.delete("/entreprises/{entreprise_id}")
async def delete_entreprise(
    entreprise_id: int,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    entreprise = db.query(Entreprise).filter(Entreprise.id == entreprise_id).first()
    if not entreprise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entreprise non trouvée"
        )
    
    db.delete(entreprise)
    db.commit()
    return {"message": "Entreprise supprimée avec succès"}

@router.get("/offres", response_model=list[OffreResponse])
async def get_all_offres(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    offres = db.query(Offre).order_by(Offre.created_at.desc()).offset(skip).limit(limit).all()
    return offres

@router.delete("/offres/{offre_id}")
async def delete_offre_admin(
    offre_id: int,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    offre = db.query(Offre).filter(Offre.id == offre_id).first()
    if not offre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offre non trouvée"
        )
    
    db.delete(offre)
    db.commit()
    return {"message": "Offre supprimée avec succès"}

@router.get("/statistiques")
async def get_statistiques(
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    total_users = db.query(func.count(User.id)).scalar()
    total_candidats = db.query(func.count(ProfilCandidat.id)).scalar()
    total_entreprises = db.query(func.count(Entreprise.id)).scalar()
    total_entreprises_validees = db.query(func.count(Entreprise.id)).filter(Entreprise.validee == True).scalar()
    total_offres = db.query(func.count(Offre.id)).scalar()
    total_candidatures = db.query(func.count(Candidature.id)).scalar()
    
    return {
        "total_users": total_users,
        "total_candidats": total_candidats,
        "total_entreprises": total_entreprises,
        "total_entreprises_validees": total_entreprises_validees,
        "total_offres": total_offres,
        "total_candidatures": total_candidatures
    }

