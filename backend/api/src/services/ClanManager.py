import time
import requests
from flask import jsonify
from config import Config  
from models.entities.member import Member
from models.entities.members import Members
from models.memberModel import ModelMember


class MemberManager:
    def __init__(self):
        self.last_called = None

    def get_members(self):
        now = time.time()

        # Calcular el tiempo desde la última llamada
        if self.last_called is None:
            elapsed_time = None
        else:
            elapsed_time = now - self.last_called

        dbMembers = ModelMember.getAllMembers()
        print('\n\n\n', 'dbMembersactual:', '\n\n\n', dbMembers.getdict(), '\n\n\n')
        if elapsed_time is not None and elapsed_time < 15:
            return  dbMembers
        
        headers = {
            "Authorization": f"Bearer {Config.TokenCoc}"
        }
        ruta = Config.URL_COC + '/clans/' + '%23' + Config.ClanId + '/members'
        response = requests.get(ruta, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error al Intentar obtener los miembros de la api de Clash of Clans: {response.status_code}")

        apiMembersList = response.json().get('items')
        apiMembersObject = Members()
        for item in apiMembersList:
            apiMembersObject.add_member(Member(
                id=item["tag"],
                username=item["name"],
                role=item["role"],
                townhall_level=item['townHallLevel'],
                trophies=item['trophies'],
                ranking=item['clanRank'],
                donations=item['donations'],
                troops_requested=item['donationsReceived'],
                experience_level=item['expLevel'],
            ))


        newMembers = Members()  # Crear un nuevo objeto Members
        newMembers.members = apiMembersObject.members - dbMembers.members

        deleteMembers = Members()  # Crear un nuevo objeto Members
        deleteMembers.members = dbMembers.members - apiMembersObject.members
        

        print('\n\n\n', 'newMembers:', '\n\n\n', newMembers.getdict(), '\n\n\n')
        print('\n\n\n', 'deleteMembers:', '\n\n\n', deleteMembers.getdict(), '\n\n\n')
        print('\n\n\n', 'actuales a Actualizar:', '\n\n\n', apiMembersObject.getdict(), '\n\n\n')

        try:
            ModelMember.refreshMembers(deleteMembers, newMembers, apiMembersObject)
        except Exception as e:
            print(f"Error al actualizar los miembros en la db: {e}")
            raise e

        try:
            actualMembers = ModelMember.getAllMembers()
            
            self.last_called = now
            return actualMembers
        except Exception as e:
            print(f"Error al extraer los miembros actualizados: {e}")
            raise e

memberClans = MemberManager()