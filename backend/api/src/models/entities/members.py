from models.entities.member import Member
from models.entities.raid import Raid
class Members:  
    """ un grupo de miembros del clan con la clase member """
    def __init__(self):
        self.members = set()
        self.raids = set()
    def add_raid(self, raid):
        if isinstance(raid, Raid):
            self.raids.add(raid)
        else:
            raise ValueError("Only Raid instances can be added.")
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
    
    def getIdsList(self):
        return [member.id for member in self.members]
    
    def getdict(self, notNull=False):
        return {member.id: member.getdict(notNull) for member in self.members}
    def getIdNames(self):
        return {member.id: member.username for member in self.members}
    def getInfoRaid(self):       
        data=[] 
        for raid in self.raids:
            
            membersNotRaid = self.members - raid.members 
            raidData = {
                "startTime": raid.startTime,
                "endTime": raid.endTime,
                "totalLoot": raid.totalLoot,
                "raidsCompleted": raid.raidsCompleted,
                "totalAttacks": raid.totalAttacks,
                "enemyDestroyed": raid.enemyDestroyed,
                "membersRaid": raid.getMembersdict(notNull=True),
                "membersNotRaid": {member.id: member.username for member in membersNotRaid},
                
            }
            data.append(raidData)
        return data
    


