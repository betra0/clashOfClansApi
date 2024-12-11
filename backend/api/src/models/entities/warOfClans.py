from datetime import datetime
from enum import Enum
from models.entities.member import Member


class Status(Enum):
    INWAR = 'inWar'
    WARENED='warEnded'
    PRE='preparation'

class WarOfClans:
    """ un grupo con info sobre un Una guerra de clanes"""
    def __init__(self,
             teamSize=None,
             startTime=None,
             endTime=None,
             state=Status.INWAR.value,
             preparationStartTime=None,
             attacksPerMember=2,
             battleModifier=None,
             teamStars=0,
             enemyStars=0,
             enemyClanTag=None,
             enemyClanName=None,
             teamAttacks=0,
             enemyAttacks=0,
             teamDestructionPercentage=0,
             enemyDestructionPercentage=0,
             
             
             ):
        
        
            

        self.startTime = self.convertTime(startTime)
        self.members = set()
        self.endTime = self.convertTime(endTime)
        self.preparationStartTime = self.convertTime(preparationStartTime)
        self.state = state
        self.teamSize = teamSize
        self.attacksPerMember = attacksPerMember
        self.battleModifier = battleModifier
        self.teamStars = teamStars
        self.enemyStars = enemyStars
        self.enemyClanTag = enemyClanTag
        self.enemyClanName = enemyClanName
        self.teamAttacks = teamAttacks
        self.enemyAttacks = enemyAttacks
        self.teamDestructionPercentage = teamDestructionPercentage
        self.enemyDestructionPercentage = enemyDestructionPercentage


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
        return f"startTime: {self.startTime}, state: {self.state}, Members({list(self.members)})"
    def __eq__(self, other):
        return isinstance(other, WarOfClans) and self.startTime == other.startTime

    def __hash__(self):
        return hash(self.startTime)
    
    def getIdsList(self)->list:
        return [member.id for member in self.members]
    
    def getMembersdict(self, notNull=False):
        return {member.id: member.getdict(notNull) for member in self.members}
    def getIdNames(self)->dict:
        return {member.id: member.username for member in self.members}

    def convertTime(self, time):
        if isinstance(time, str):
            try:
                time = datetime.strptime(time, "%Y%m%dT%H%M%S.%fZ")
                
            except ValueError as e:
                print("Error al convertir el tiempo:", e)
                raise e
        return time