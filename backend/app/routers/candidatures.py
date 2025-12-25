from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import auth
from app.models import User, ProfilCandidat, Entreprise, Candidature, Offre, StatutCandidature
from app.schemas import CandidatureCreate, CandidatureUpdate, CandidatureResponse

router = APIRouter()

@router.post("/", response_model=CandidatureResponse, status_code=status.HTTP_201_CREATED)
async def postuler(
    candidature_data: CandidatureCreate,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role.value != "candidat":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les candidats peuvent postuler"
        )
    
    profil = db.query(ProfilCandidat).filter(ProfilCandidat.user_id == current_user.id).first()
    if not profil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil candidat non trouvé. Créez d'abord votre profil."
        )
    
    # Vérifier que l'offre existe
    offre = db.query(Offre).filter(Offre.id == candidature_data.offre_id).first()
    if not offre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offre non trouvée"
        )
    
    # Vérifier si déjà postulé
    existing = db.query(Candidature).filter(
        Candidature.candidat_id == profil.id,
        Candidature.offre_id == candidature_data.offre_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous avez déjà postulé à cette offre"
        )
    
    db_candidature = Candidature(
        candidat_id=profil.id,
        offre_id=candidature_data.offre_id
    )
    db.add(db_candidature)
    db.commit()
    db.refresh(db_candidature)
    return db_candidature

@router.get("/mes-candidatures", response_model=list[CandidatureResponse])
async def get_mes_candidatures(
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
            detail="Profil candidat non trouvé"
        )
    
    candidatures = db.query(Candidature).filter(
        Candidature.candidat_id == profil.id
    ).order_by(Candidature.date_postulation.desc()).all()
    
    return candidatures

@router.get("/entreprise/{offre_id}", response_model=list[CandidatureResponse])
async def get_candidatures_offre(
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
    
    # Vérifier que l'offre appartient à l'entreprise
    offre = db.query(Offre).filter(
        Offre.id == offre_id,
        Offre.entreprise_id == entreprise.id
    ).first()
    
    if not offre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offre non trouvée ou n'appartient pas à votre entreprise"
        )
    
    candidatures = db.query(Candidature).filter(
        Candidature.offre_id == offre_id
    ).order_by(Candidature.date_postulation.desc()).all()
    
    return candidatures

@router.put("/{candidature_id}", response_model=CandidatureResponse)
async def update_statut_candidature(
    candidature_id: int,
    candidature_data: CandidatureUpdate,
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
    
    candidature = db.query(Candidature).join(Offre).filter(
        Candidature.id == candidature_id,
        Offre.entreprise_id == entreprise.id
    ).first()
    
    if not candidature:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidature non trouvée"
        )
    
    if candidature_data.statut:
        candidature.statut = candidature_data.statut
    
    db.commit()
    db.refresh(candidature)
    return candidature


