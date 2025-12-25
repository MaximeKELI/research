-- Schéma PostgreSQL pour JobApp
-- Ce fichier contient la structure de la base de données

-- Table Users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    mot_de_passe VARCHAR NOT NULL,
    role VARCHAR NOT NULL CHECK (role IN ('admin', 'entreprise', 'candidat')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table Profils Candidats
CREATE TABLE IF NOT EXISTS profils_candidats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    nom VARCHAR NOT NULL,
    prenom VARCHAR NOT NULL,
    niveau_etude VARCHAR,
    competences TEXT,
    cv_url VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Table Entreprises
CREATE TABLE IF NOT EXISTS entreprises (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    nom VARCHAR NOT NULL,
    secteur VARCHAR,
    description TEXT,
    contact VARCHAR,
    validee BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Table Offres
CREATE TABLE IF NOT EXISTS offres (
    id SERIAL PRIMARY KEY,
    entreprise_id INTEGER NOT NULL REFERENCES entreprises(id) ON DELETE CASCADE,
    titre VARCHAR NOT NULL,
    description TEXT NOT NULL,
    type VARCHAR NOT NULL CHECK (type IN ('stage', 'emploi')),
    lieu VARCHAR,
    salaire VARCHAR,
    date_limite DATE,
    statut VARCHAR DEFAULT 'active' CHECK (statut IN ('active', 'expirée')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Table Candidatures
CREATE TABLE IF NOT EXISTS candidatures (
    id SERIAL PRIMARY KEY,
    candidat_id INTEGER NOT NULL REFERENCES profils_candidats(id) ON DELETE CASCADE,
    offre_id INTEGER NOT NULL REFERENCES offres(id) ON DELETE CASCADE,
    date_postulation TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    statut VARCHAR DEFAULT 'en_attente' CHECK (statut IN ('en_attente', 'accepté', 'refusé')),
    UNIQUE(candidat_id, offre_id)
);

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_offres_entreprise ON offres(entreprise_id);
CREATE INDEX IF NOT EXISTS idx_offres_statut ON offres(statut);
CREATE INDEX IF NOT EXISTS idx_candidatures_candidat ON candidatures(candidat_id);
CREATE INDEX IF NOT EXISTS idx_candidatures_offre ON candidatures(offre_id);

-- Insertion d'un utilisateur admin par défaut (mot de passe: admin123)
-- À changer en production !
INSERT INTO users (email, mot_de_passe, role) 
VALUES ('admin@jobapp.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', 'admin')
ON CONFLICT (email) DO NOTHING;


