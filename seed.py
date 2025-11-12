from sqlmodel import Session, select

from app.database import moteur
from app.modeles.role import Role
from app.modeles.permission import Permission
from app.modeles.role_permission import RolePermission
from app.modeles.utilisateur import Utilisateur
from app.modeles.canal import Canal
from app.services.securite import hacher_mot_de_passe


def initialiser_permissions(session: Session):
    """Créer les permissions de base"""
    permissions_base = [
        # Permissions utilisateurs
        {"code": "lire_utilisateurs", "nom": "Lire les utilisateurs", "categorie": "utilisateurs"},
        {"code": "creer_utilisateurs", "nom": "Créer des utilisateurs", "categorie": "utilisateurs"},
        {"code": "modifier_utilisateurs", "nom": "Modifier des utilisateurs", "categorie": "utilisateurs"},
        {"code": "supprimer_utilisateurs", "nom": "Supprimer des utilisateurs", "categorie": "utilisateurs"},
        
        # Permissions rôles
        {"code": "lire_roles", "nom": "Lire les rôles", "categorie": "roles"},
        {"code": "gerer_roles", "nom": "Gérer les rôles", "categorie": "roles"},
        
        # Permissions permissions
        {"code": "lire_permissions", "nom": "Lire les permissions", "categorie": "permissions"},
        {"code": "gerer_permissions", "nom": "Gérer les permissions", "categorie": "permissions"},
        
        # Permissions canaux
        {"code": "lire_canaux", "nom": "Lire les canaux", "categorie": "canaux"},
        {"code": "creer_canaux", "nom": "Créer des canaux", "categorie": "canaux"},
        {"code": "modifier_canaux", "nom": "Modifier des canaux", "categorie": "canaux"},
        {"code": "supprimer_canaux", "nom": "Supprimer des canaux", "categorie": "canaux"},
        
        # Permissions messages
        {"code": "lire_messages", "nom": "Lire les messages", "categorie": "messages"},
        {"code": "envoyer_messages", "nom": "Envoyer des messages", "categorie": "messages"},
        {"code": "modifier_messages", "nom": "Modifier des messages", "categorie": "messages"},
        {"code": "supprimer_messages", "nom": "Supprimer des messages", "categorie": "messages"},
    ]
    
    permissions_creees = []
    for perm_data in permissions_base:
        # Vérifier si la permission existe déjà
        statement = select(Permission).where(Permission.code == perm_data["code"])
        perm_existante = session.exec(statement).first()
        
        if not perm_existante:
            permission = Permission(**perm_data)
            session.add(permission)
            permissions_creees.append(perm_data["code"])
    
    session.commit()
    return permissions_creees


def initialiser_roles(session: Session):
    """Créer les rôles de base"""
    roles_base = [
        {"nom": "admin", "description": "Administrateur avec tous les droits"},
        {"nom": "moderateur", "description": "Modérateur avec droits limités"},
        {"nom": "utilisateur", "description": "Utilisateur standard"},
        {"nom": "invite", "description": "Invité avec accès en lecture seule"},
    ]
    
    roles_crees = []
    for role_data in roles_base:
        statement = select(Role).where(Role.nom == role_data["nom"])
        role_existant = session.exec(statement).first()
        
        if not role_existant:
            role = Role(**role_data)
            session.add(role)
            roles_crees.append(role_data["nom"])
    
    session.commit()
    return roles_crees


def attribuer_permissions_aux_roles(session: Session):
    """Attribuer les permissions aux rôles"""
    # Récupérer tous les rôles et permissions
    roles = {role.nom: role for role in session.exec(select(Role)).all()}
    permissions = {perm.code: perm for perm in session.exec(select(Permission)).all()}
    
    # Définir les permissions pour chaque rôle
    attributions = {
        "admin": list(permissions.keys()),  # Admin a toutes les permissions
        
        "moderateur": [
            "lire_utilisateurs",
            "lire_roles",
            "lire_permissions",
            "lire_canaux",
            "creer_canaux",
            "modifier_canaux",
            "lire_messages",
            "envoyer_messages",
            "modifier_messages",
            "supprimer_messages",
        ],
        
        "utilisateur": [
            "lire_canaux",
            "lire_messages",
            "envoyer_messages",
            "modifier_messages",  # Seulement ses propres messages
        ],
        
        "invite": [
            "lire_canaux",
            "lire_messages",
        ],
    }
    
    for role_nom, permissions_codes in attributions.items():
        if role_nom not in roles:
            continue
        
        role = roles[role_nom]
        
        for perm_code in permissions_codes:
            if perm_code not in permissions:
                continue
            
            permission = permissions[perm_code]
            
            # Vérifier si l'association existe déjà
            statement = select(RolePermission).where(
                RolePermission.role_id == role.id,
                RolePermission.permission_id == permission.id
            )
            association_existante = session.exec(statement).first()
            
            if not association_existante:
                association = RolePermission(role_id=role.id, permission_id=permission.id)
                session.add(association)
    
    session.commit()


def creer_utilisateur_admin(session: Session):
    """Créer un utilisateur admin par défaut"""
    statement = select(Utilisateur).where(Utilisateur.nom_utilisateur == "admin")
    admin_existant = session.exec(statement).first()
    
    if not admin_existant:
        # Récupérer le rôle admin
        statement = select(Role).where(Role.nom == "admin")
        role_admin = session.exec(statement).first()
        
        if role_admin:
            admin = Utilisateur(
                nom_utilisateur="admin",
                email="admin@example.com",
                mot_de_passe_hash=hacher_mot_de_passe("admin123"),
                prenom="Super",
                nom="Admin",
                role_id=role_admin.id,
                est_actif=True,
                est_verifie=True
            )
            session.add(admin)
            session.commit()
            return True
    
    return False


def creer_canaux_par_defaut(session: Session):
    """Créer des canaux par défaut"""
    canaux_base = [
        {"nom": "general", "description": "Canal général pour tous", "type_canal": "public"},
        {"nom": "support", "description": "Canal de support technique", "type_canal": "public"},
        {"nom": "admin", "description": "Canal réservé aux admins", "type_canal": "prive", "role_minimum_requis": "admin"},
    ]
    
    canaux_crees = []
    for canal_data in canaux_base:
        statement = select(Canal).where(Canal.nom == canal_data["nom"])
        canal_existant = session.exec(statement).first()
        
        if not canal_existant:
            canal = Canal(**canal_data)
            session.add(canal)
            canaux_crees.append(canal_data["nom"])
    
    session.commit()
    return canaux_crees


def executer_seed():
    """Exécuter tous les seeds"""
    print("Démarrage du seed de la base de données...")
    
    with Session(moteur) as session:
        # 1. Créer les permissions
        print("📝 Création des permissions...")
        permissions = initialiser_permissions(session)
        if permissions:
            print(f"   {len(permissions)} permissions créées")
        else:
            print("   Permissions déjà existantes")
        
        # 2. Créer les rôles
        print("👥 Création des rôles...")
        roles = initialiser_roles(session)
        if roles:
            print(f"    {len(roles)} rôles créés")
        else:
            print("   ℹ  Rôles déjà existants")
        
        # 3. Attribuer les permissions aux rôles
        print("🔗 Attribution des permissions aux rôles...")
        attribuer_permissions_aux_roles(session)
        print("   ✅ Permissions attribuées")
        
        # 4. Créer l'utilisateur admin
        print("👤 Création de l'utilisateur admin...")
        admin_cree = creer_utilisateur_admin(session)
        if admin_cree:
            print("    Admin créé (login: admin, password: admin123)")
        else:
            print("   ℹ  Admin déjà existant")
        
        # 5. Créer les canaux par défaut
        print("💬 Création des canaux par défaut...")
        canaux = creer_canaux_par_defaut(session)
        if canaux:
            print(f"    {len(canaux)} canaux créés")
        else:
            print("   ℹ  Canaux déjà existants")
    
    print("\n Seed terminé avec succès!")
    print("\n Informations de connexion admin:")
    print("   Nom d'utilisateur: admin")
    print("   Mot de passe: admin123")
    print("   ⚠  Changez ce mot de passe en production!")


if __name__ == "__main__":
    executer_seed()
