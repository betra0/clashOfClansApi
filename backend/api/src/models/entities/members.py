from models.entities.member import Member
class Members:  
    """ un grupo de miembros del clan con la clase member """
    def __init__(self):
        self.members = set()

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
    
    def getdict(self):
        return {member.id: member.getdict() for member in self.members}
    def getIdNames(self):
        return {member.id: member.username for member in self.members}


