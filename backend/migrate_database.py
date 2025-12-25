"""
Script pour mettre à jour la base de données avec les nouveaux champs
"""
from sqlalchemy import text
from app.database import engine, Base
from app.models import User, ProfilCandidat, Entreprise, Offre, Candidature
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_database():
    """Ajouter les nouvelles colonnes à la base de données existante"""
    with engine.connect() as conn:
        try:
            # Vérifier si la colonne photo_url existe dans users
            result = conn.execute(text("PRAGMA table_info(users)"))
            columns = [row[1] for row in result]
            
            if 'photo_url' not in columns:
                logger.info("Ajout de la colonne photo_url à la table users...")
                conn.execute(text("ALTER TABLE users ADD COLUMN photo_url VARCHAR"))
                conn.commit()
                logger.info("✅ Colonne photo_url ajoutée à users")
            
            # Vérifier les colonnes de profils_candidats
            result = conn.execute(text("PRAGMA table_info(profils_candidats)"))
            columns = [row[1] for row in result]
            
            new_candidat_columns = {
                'date_naissance': 'DATE',
                'genre': 'VARCHAR',
                'telephone': 'VARCHAR',
                'adresse': 'VARCHAR',
                'ville': 'VARCHAR',
                'pays': 'VARCHAR',
                'code_postal': 'VARCHAR',
                'domaine_etude': 'VARCHAR',
                'annee_obtention': 'INTEGER',
                'annees_experience': 'INTEGER',
                'secteur_experience': 'VARCHAR',
                'statut_professionnel': 'VARCHAR',
                'disponibilite': 'VARCHAR',
                'salaire_souhaite': 'VARCHAR',
                'photo_url': 'VARCHAR'
            }
            
            for col_name, col_type in new_candidat_columns.items():
                if col_name not in columns:
                    logger.info(f"Ajout de la colonne {col_name} à la table profils_candidats...")
                    conn.execute(text(f"ALTER TABLE profils_candidats ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                    logger.info(f"✅ Colonne {col_name} ajoutée à profils_candidats")
            
            # Vérifier les colonnes de entreprises
            result = conn.execute(text("PRAGMA table_info(entreprises)"))
            columns = [row[1] for row in result]
            
            new_entreprise_columns = {
                'telephone': 'VARCHAR',
                'email_contact': 'VARCHAR',
                'adresse': 'VARCHAR',
                'ville': 'VARCHAR',
                'pays': 'VARCHAR',
                'code_postal': 'VARCHAR',
                'site_web': 'VARCHAR',
                'taille_entreprise': 'VARCHAR',
                'nombre_employes': 'INTEGER',
                'annee_creation': 'INTEGER',
                'type_entreprise': 'VARCHAR',
                'photo_url': 'VARCHAR'
            }
            
            for col_name, col_type in new_entreprise_columns.items():
                if col_name not in columns:
                    logger.info(f"Ajout de la colonne {col_name} à la table entreprises...")
                    conn.execute(text(f"ALTER TABLE entreprises ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                    logger.info(f"✅ Colonne {col_name} ajoutée à entreprises")
            
            # Vérifier les colonnes de offres
            result = conn.execute(text("PRAGMA table_info(offres)"))
            columns = [row[1] for row in result]
            
            new_offre_columns = {
                'ville': 'VARCHAR',
                'pays': 'VARCHAR',
                'type_contrat': 'VARCHAR',
                'salaire_min': 'INTEGER',
                'salaire_max': 'INTEGER',
                'experience_requise': 'VARCHAR',
                'niveau_etude_requis': 'VARCHAR',
                'competences_requises': 'TEXT',
                'avantages': 'TEXT',
                'nombre_vues': 'INTEGER DEFAULT 0',
                'nombre_candidatures': 'INTEGER DEFAULT 0'
            }
            
            for col_name, col_type in new_offre_columns.items():
                if col_name not in columns:
                    logger.info(f"Ajout de la colonne {col_name} à la table offres...")
                    # Gérer les valeurs par défaut
                    if 'DEFAULT' in col_type:
                        conn.execute(text(f"ALTER TABLE offres ADD COLUMN {col_name} {col_type}"))
                    else:
                        conn.execute(text(f"ALTER TABLE offres ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                    logger.info(f"✅ Colonne {col_name} ajoutée à offres")
            
            logger.info("✅ Migration terminée avec succès!")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la migration: {e}")
            conn.rollback()
            raise

if __name__ == "__main__":
    migrate_database()

