from datetime import datetime
from enum import Enum

class Status(Enum):
    ACTIVE = 'active'
    LEFT = 'left'
    EXPELLED = 'expelled'

class Member:
    def __init__(self,
                 id='',
                 username='',
                 clan_tag=None,
                 role='member',
                 status=Status.ACTIVE.value,
                 left_date=None,
                 notes=None,
                 created_at=None,
                 updated_at=None):
        
        self.id = id
        self.username = username
        self.clan_tag = clan_tag
        self.role = role
        self.status = status
        self.left_date = left_date
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def getdict(self):
        return {
            'id': self.id,
            'username': self.username,
            'clan_tag': self.clan_tag,
            'role': self.role,
            'status': self.status,
            'left_date': self.left_date.isoformat() if self.left_date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }

    def __str__(self):
        return (f"Player(id={self.id}, username='{self.username}', clan_tag='{self.clan_tag}', "
                f"role='{self.role}', status='{self.status}', created_at='{self.created_at}', "
                f"updated_at='{self.updated_at}')")