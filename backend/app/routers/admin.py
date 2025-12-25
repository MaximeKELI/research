from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.database import get_db
from app import auth
from app.models import User, Entreprise, Offre, Candidature, ProfilCandidat
from app.schemas import EntrepriseResponse, OffreResponse
from app.auth import require_role
from datetime import datetime, timedelta
import csv
import io
from typing import Dict, List
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

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
    """Statistiques générales"""
    total_users = db.query(func.count(User.id)).scalar()
    total_candidats = db.query(func.count(ProfilCandidat.id)).scalar()
    total_entreprises = db.query(func.count(Entreprise.id)).scalar()
    total_entreprises_validees = db.query(func.count(Entreprise.id)).filter(Entreprise.validee == True).scalar()
    total_offres = db.query(func.count(Offre.id)).scalar()
    total_candidatures = db.query(func.count(Candidature.id)).scalar()
    
    # Statistiques par genre (candidats)
    candidats_par_genre = db.query(
        ProfilCandidat.genre,
        func.count(ProfilCandidat.id).label('count')
    ).group_by(ProfilCandidat.genre).all()
    genre_stats = {genre or 'Non spécifié': count for genre, count in candidats_par_genre}
    
    # Statistiques par secteur (entreprises)
    entreprises_par_secteur = db.query(
        Entreprise.secteur,
        func.count(Entreprise.id).label('count')
    ).group_by(Entreprise.secteur).all()
    secteur_stats = {secteur or 'Non spécifié': count for secteur, count in entreprises_par_secteur}
    
    # Statistiques par niveau d'étude
    candidats_par_niveau = db.query(
        ProfilCandidat.niveau_etude,
        func.count(ProfilCandidat.id).label('count')
    ).group_by(ProfilCandidat.niveau_etude).all()
    niveau_stats = {niveau or 'Non spécifié': count for niveau, count in candidats_par_niveau}
    
    # Statistiques par ville (candidats)
    candidats_par_ville = db.query(
        ProfilCandidat.ville,
        func.count(ProfilCandidat.id).label('count')
    ).group_by(ProfilCandidat.ville).order_by(func.count(ProfilCandidat.id).desc()).limit(10).all()
    ville_stats = {ville or 'Non spécifié': count for ville, count in candidats_par_ville}
    
    # Statistiques par type d'offre
    offres_par_type = db.query(
        Offre.type,
        func.count(Offre.id).label('count')
    ).group_by(Offre.type).all()
    type_offre_stats = {str(type_offre): count for type_offre, count in offres_par_type}
    
    # Statistiques par statut de candidature
    candidatures_par_statut = db.query(
        Candidature.statut,
        func.count(Candidature.id).label('count')
    ).group_by(Candidature.statut).all()
    statut_candidature_stats = {str(statut): count for statut, count in candidatures_par_statut}
    
    # Évolution mensuelle (inscriptions)
    six_mois_avant = datetime.now() - timedelta(days=180)
    inscriptions_mensuelles = db.query(
        extract('year', User.created_at).label('year'),
        extract('month', User.created_at).label('month'),
        func.count(User.id).label('count')
    ).filter(User.created_at >= six_mois_avant).group_by(
        extract('year', User.created_at),
        extract('month', User.created_at)
    ).order_by('year', 'month').all()
    
    evolution_mensuelle = [
        {
            'mois': f"{int(year)}-{int(month):02d}",
            'count': count
        }
        for year, month, count in inscriptions_mensuelles
    ]
    
    # Statistiques d'expérience
    candidats_par_experience = db.query(
        ProfilCandidat.annees_experience,
        func.count(ProfilCandidat.id).label('count')
    ).group_by(ProfilCandidat.annees_experience).all()
    experience_stats = {
        f"{exp or 0} ans": count 
        for exp, count in candidats_par_experience
    }
    
    return {
        "total_users": total_users or 0,
        "total_candidats": total_candidats or 0,
        "total_entreprises": total_entreprises or 0,
        "total_entreprises_validees": total_entreprises_validees or 0,
        "total_offres": total_offres or 0,
        "total_candidatures": total_candidatures or 0,
        "candidats_par_genre": genre_stats,
        "entreprises_par_secteur": secteur_stats,
        "candidats_par_niveau": niveau_stats,
        "candidats_par_ville": ville_stats,
        "offres_par_type": type_offre_stats,
        "candidatures_par_statut": statut_candidature_stats,
        "evolution_mensuelle": evolution_mensuelle,
        "candidats_par_experience": experience_stats
    }

@router.get("/export/csv")
async def export_csv(
    data_type: str = "candidats",  # candidats, entreprises, offres, candidatures
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Exporter les données en CSV"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    if data_type == "candidats":
        writer.writerow([
            'ID', 'Nom', 'Prénom', 'Email', 'Genre', 'Date Naissance', 'Téléphone',
            'Ville', 'Pays', 'Niveau Étude', 'Domaine Étude', 'Années Expérience',
            'Secteur Expérience', 'Statut Professionnel', 'Disponibilité', 'Date Création'
        ])
        
        candidats = db.query(ProfilCandidat, User).join(User, ProfilCandidat.user_id == User.id).all()
        for profil, user in candidats:
            writer.writerow([
                profil.id, profil.nom, profil.prenom, user.email,
                profil.genre or '', profil.date_naissance or '', profil.telephone or '',
                profil.ville or '', profil.pays or '', profil.niveau_etude or '',
                profil.domaine_etude or '', profil.annees_experience or '',
                profil.secteur_experience or '', profil.statut_professionnel or '',
                profil.disponibilite or '', profil.created_at
            ])
    
    elif data_type == "entreprises":
        writer.writerow([
            'ID', 'Nom', 'Email', 'Secteur', 'Ville', 'Pays', 'Taille',
            'Nombre Employés', 'Année Création', 'Type', 'Validée', 'Date Création'
        ])
        
        entreprises = db.query(Entreprise, User).join(User, Entreprise.user_id == User.id).all()
        for entreprise, user in entreprises:
            writer.writerow([
                entreprise.id, entreprise.nom, user.email, entreprise.secteur or '',
                entreprise.ville or '', entreprise.pays or '', entreprise.taille_entreprise or '',
                entreprise.nombre_employes or '', entreprise.annee_creation or '',
                entreprise.type_entreprise or '', entreprise.validee, entreprise.created_at
            ])
    
    elif data_type == "offres":
        writer.writerow([
            'ID', 'Titre', 'Entreprise', 'Type', 'Lieu', 'Salaire Min', 'Salaire Max',
            'Expérience Requise', 'Date Limite', 'Statut', 'Vues', 'Candidatures', 'Date Création'
        ])
        
        offres = db.query(Offre, Entreprise).join(Entreprise, Offre.entreprise_id == Entreprise.id).all()
        for offre, entreprise in offres:
            writer.writerow([
                offre.id, offre.titre, entreprise.nom, str(offre.type),
                offre.lieu or '', offre.salaire_min or '', offre.salaire_max or '',
                offre.experience_requise or '', offre.date_limite or '',
                str(offre.statut), offre.nombre_vues, offre.nombre_candidatures, offre.created_at
            ])
    
    elif data_type == "candidatures":
        writer.writerow([
            'ID', 'Candidat', 'Offre', 'Entreprise', 'Date Postulation', 'Statut'
        ])
        
        candidatures = db.query(
            Candidature, ProfilCandidat, Offre, Entreprise
        ).join(
            ProfilCandidat, Candidature.candidat_id == ProfilCandidat.id
        ).join(
            Offre, Candidature.offre_id == Offre.id
        ).join(
            Entreprise, Offre.entreprise_id == Entreprise.id
        ).all()
        
        for candidature, candidat, offre, entreprise in candidatures:
            writer.writerow([
                candidature.id, f"{candidat.nom} {candidat.prenom}",
                offre.titre, entreprise.nom, candidature.date_postulation, str(candidature.statut)
            ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={data_type}_{datetime.now().strftime('%Y%m%d')}.csv"}
    )

@router.get("/export/pdf")
async def export_pdf_statistiques(
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Exporter les statistiques en PDF"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Titre
    title = Paragraph("Rapport Statistiques JobApp", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Récupérer les statistiques
    stats = await get_statistiques(current_user, db)
    
    # Tableau des statistiques générales
    data = [
        ['Métrique', 'Valeur'],
        ['Total Utilisateurs', str(stats['total_users'])],
        ['Total Candidats', str(stats['total_candidats'])],
        ['Total Entreprises', str(stats['total_entreprises'])],
        ['Entreprises Validées', str(stats['total_entreprises_validees'])],
        ['Total Offres', str(stats['total_offres'])],
        ['Total Candidatures', str(stats['total_candidatures'])],
    ]
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Statistiques par genre
    if stats['candidats_par_genre']:
        story.append(Paragraph("Candidats par Genre", styles['Heading2']))
        genre_data = [['Genre', 'Nombre']]
        for genre, count in stats['candidats_par_genre'].items():
            genre_data.append([genre, str(count)])
        
        genre_table = Table(genre_data)
        genre_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(genre_table)
        story.append(Spacer(1, 20))
    
    # Statistiques par secteur
    if stats['entreprises_par_secteur']:
        story.append(Paragraph("Entreprises par Secteur", styles['Heading2']))
        secteur_data = [['Secteur', 'Nombre']]
        for secteur, count in list(stats['entreprises_par_secteur'].items())[:10]:
            secteur_data.append([secteur, str(count)])
        
        secteur_table = Table(secteur_data)
        secteur_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(secteur_table)
    
    doc.build(story)
    buffer.seek(0)
    
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=statistiques_{datetime.now().strftime('%Y%m%d')}.pdf"}
    )



