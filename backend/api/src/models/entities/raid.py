from datetime import datetime
from enum import Enum
from models.entities.member import Member



class Status(Enum):
    INWAR = 'inWar'
    ENDED='Ended'
    PRE='preparation'

class Raid:
    """ un grupo con info sobre un asalto"""
    def __init__(self,
             startTime=None,
             endTime=None,
             totalLoot=None,
             raidsCompleted=None,
             totalAttacks=None,
             enemyDestroyed=None,
             state=Status.ENDED.value,
             
             ):
        
        if isinstance(startTime, str):
            try:
                startTime = datetime.strptime(startTime, "%Y%m%dT%H%M%S.%fZ")
                
            except ValueError as e:
                print("Error al convertir el tiempo:", e)
                raise e
        if isinstance(endTime, str):
            try:
                endTime = datetime.strptime(endTime, "%Y%m%dT%H%M%S.%fZ")
                
            except ValueError as e:
                print("Error al convertir el tiempo:", e)
                raise e
            

        self.startTime = startTime
        self.members = set()
        self.endTime = endTime
        self.totalLoot = totalLoot
        self.raidsCompleted = raidsCompleted
        self.totalAttacks = totalAttacks
        self.enemyDestroyed = enemyDestroyed
        self.state = state

    def add_member(self, member):
        if isinstance(member, Member):
            self.members.add(member)
        else:
            raise ValueError("Only Member instances can be added.")

    def remove_member(self, member):
        self.members.discard(member)  # No lanza error si no existe
    def __len__(self):
        return len(self.members)

    def __iter__(self):
        return iter(self.members)

    def __repr__(self):
        return f"Members({list(self.members)})"
    def __eq__(self, other):
        return isinstance(other, Raid) and self.startTime == other.startTime

    def __hash__(self):
        return hash(self.startTime)
    
    def getIdsList(self):
        return [member.id for member in self.members]
    
    def getMembersdict(self, notNull=False):
        return {member.id: member.getdict(notNull) for member in self.members}
    def getIdNames(self):
        return {member.id: member.username for member in self.members}

    def isMemberInRaid(self, member)->bool:
        salida = False
        if member in self.members:
            salida = True
        if not salida:
            if member.created_at <= self.startTime:
                salida = True
        return salida
   

