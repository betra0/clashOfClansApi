from datetime import datetime
from enum import Enum

class Status(Enum):
    ACTIVE = 'active'
    LEFT = 'left'
    EXPELLED = 'expelled'

class Member:
    def __init__(self,
             id=None,
             username=None,
             clan_tag=None,
             role=None,
             townhall_level=None,
             trophies=None,
             best_trophies=None,
             ranking=None,
             donations=None,
             troops_requested=None,
             war_stars=None,
             experience_level=None,
             league=None,
             attack_count=None,
             defense_count=None,
             status=Status.ACTIVE.value,
             left_date=None,
             notes=None,
             created_at=None,
             updated_at=None):
        
        self.id = id
        self.username = username
        self.clan_tag = clan_tag
        self.role = role
        self.townhall_level = townhall_level
        self.trophies = trophies
        self.best_trophies = best_trophies
        self.ranking = ranking
        self.donations = donations
        self.troops_requested = troops_requested
        self.war_stars = war_stars
        self.experience_level = experience_level
        self.league = league
        self.attack_count = attack_count
        self.defense_count = defense_count
        self.status = status
        self.left_date = left_date
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def __eq__(self, other):
        return isinstance(other, Member) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"Member(id={self.id}, username='{self.username}')"
    def getdict(self, notNull=False):
        data = {
        'id': self.id,
        'username': self.username,
        'clan_tag': self.clan_tag,
        'role': self.role,
        'townhall_level': self.townhall_level,
        'trophies': self.trophies,
        'best_trophies': self.best_trophies,
        'ranking': self.ranking,
        'donations': self.donations,
        'troops_requested': self.troops_requested,
        'war_stars': self.war_stars,
        'experience_level': self.experience_level,
        'league': self.league,
        'attack_count': self.attack_count,
        'defense_count': self.defense_count,
        'status': self.status,
        'left_date': self.left_date.isoformat() if self.left_date else None,
        'notes': self.notes,
        'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
        'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }

    # Si `notNull` es True, excluye las claves con valores `None`
        if notNull:
            data = {key: value for key, value in data.items() if value is not None}

        return data
    
class RaidMember(Member):
    def __init__(self, 
                 id=None, 
                 username=None, 
                 attacks=0, 
                 resourcesLooted=0, 
                 attackLimit=5, 
                 **kwargs):
        # Pasar el ID al constructor de la clase padre
        super().__init__(id=id, username=username, **kwargs)

        
        self.attacks = attacks
        self.resourcesLooted = resourcesLooted
        self.attackLimit = attackLimit
    
    def getdict(self, notNull=False):
        data = {
        'id': self.id,
        'username': self.username,
        'attacks': self.attacks,
        'resourcesLooted': self.resourcesLooted,
        'attackLimit': self.attackLimit
        }

        # Si `notNull` es True, excluye las claves con valores `None`
        if notNull:
            data = {key: value for key, value in data.items() if value is not None}

        return data
    

