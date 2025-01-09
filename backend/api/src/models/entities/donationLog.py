from datetime import datetime
from enum import Enum
from models.entities.member import Member, DonationLogMember




class DonationLog:
    """ un grupo con info sobre un asalto"""
    def __init__(self,
            clan_tag=None,
            donations=None,
            requests=None,
            logDate=None,
            members=set()
             ):
        
        self.clan_tag = clan_tag
        self.donations = donations
        self.requests = requests
        self.logDate = logDate
        self.members:set = members


        
    def getDonations(self):
        if self.donations is not None:
            return self.donations
        else:
            return sum([member.donationsLog for member in self.members])
    def getRequests(self):
        if self.requests is not None:
            return self.requests
        else:
            return sum([member.requestsLog for member in self.members])
    def add_member(self, member):
        if isinstance(member, DonationLogMember):
            self.members.add(member)
        else:
            raise ValueError("Only DonationLogMember instances can be added.")

    def remove_member(self, member):
        self.members.discard(member)  # No lanza error si no existe
    def __len__(self):
        return len(self.members)

    def __iter__(self):
        return iter(self.members)

    def __repr__(self):
        return f" tagClan {self.clan_tag}, date:{self.logDate} donations:{self.donations}, requests:{self.requests} )"
    def __eq__(self, other):
        return isinstance(other, DonationLog) and self.logDate == other.logDate and self.clan_tag == other.clan_tag

    def __hash__(self):
        return hash(self.logDate, self.clan_tag)
    
    def getIdsList(self):
        return [member.id for member in self.members]
    
    def getMembersdict(self, notNull=False):
        return {member.id: member.getdict(notNull) for member in self.members}
    def getIdNames(self):
        return {member.id: member.username for member in self.members}

    def convertTime(self, time):
        if isinstance(time, str):
            try:
                time = datetime.strptime(time, "%Y%m%dT%H%M%S.%fZ")
                
            except ValueError as e:
                print("Error al convertir el tiempo:", e)
                raise e
        return time
    def getdict(self, notNull=False):
        data = {
            'clan_tag': self.clan_tag,
            'donations': self.donations,
            'requests': self.requests,
            'logDate': self.logDate,
            'members': [member.getdict(notNull) for member in self.members],
        }

        if notNull:
            data = {key: value for key, value in data.items() if value is not None}

        return data
   

