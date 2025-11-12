"""
Service de sécurité
Gestion du hachage et de la vérification des mots de passe
"""
from passlib.context import CryptContext


# Configuration du contexte de hachage
contexte_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hacher_mot_de_passe(mot_de_passe: str) -> str:
    
    return contexte_pwd.hash(mot_de_passe)


def verifier_mot_de_passe(mot_de_passe_clair: str, mot_de_passe_hash: str) -> bool:
   
    return contexte_pwd.verify(mot_de_passe_clair, mot_de_passe_hash)
