"""
Configuration et gestion de la base de données PostgreSQL
"""
from sqlmodel import SQLModel, create_engine, Session
from app.config import parametres


# Création du moteur de base de données
moteur = create_engine(
    parametres.DATABASE_URL,
    echo=parametres.DEBUG,
    pool_pre_ping=True,
    pool_size=10,  
    max_overflow=20 
)


def creer_tables():
    SQLModel.metadata.create_all(moteur)
    print("Tables créées avec succès")


def obtenir_session():
    with Session(moteur) as session:
        yield session
