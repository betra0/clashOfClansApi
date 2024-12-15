import time
import requests
from flask import jsonify
from config import Config  
from models.entities.member import Member, WarMember
from models.entities.members import Members
from models.memberModel import ModelMember
from models.entities.warOfClans import WarOfClans
from models.entities.warAttack import WarAttack
from models.warClansModels import ModelWarOfClans
from models.entities.raid import Raid
from models.entities.member import Member, RaidMember
import json
import os
from models.raidModel import ModelRaid
import logging

logging.basicConfig(level=logging.INFO)

class MemberManager:
    def __init__(self):
        self.last_called = None

    def get_members(self, onlyRefresk=False, refreshDb=None):
        #cuando RefreskDb es True se refresca la db Si o si 
        #si es none se refresca solo si es necesario 
        #si es False no se refresca la db
        now = time.time()
        logging.info(f"Obteniendo los miembros del clan")
        
        # Calcular el tiempo desde la última llamada
        if self.last_called is None:
            elapsed_time = None
        else:
            elapsed_time = now - self.last_called

        dbMembers = ModelMember.getAllMembers()

        if refreshDb is not True:
            if refreshDb is False or (refreshDb is None and elapsed_time is not None and elapsed_time < 15):
                return dbMembers

        
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
            self.last_called = now
            if not onlyRefresk:
                actualMembers = ModelMember.getAllMembers()
            
                return actualMembers
        except Exception as e:
            print(f"Error al extraer los miembros actualizados: {e}")
            raise e

    def getRaids(self, members:Members, AmountRaids=3,):
        
        raidList =ModelRaid.getRaids(amount=AmountRaids)
        members.raids=raidList
        return members

    def getwars(self, members:Members, AmountWars=3):
        listWars =ModelWarOfClans.getWarsOfClans(amount=AmountWars)
        members.wars=listWars
        return members

    def getAllClanInfo(self, AmountWars=3, AmountRaids=3, refreshDb=None):
        memberOfClans = self.get_members(refreshDb=refreshDb)
        memberOfClans = self.getRaids(memberOfClans, AmountRaids=AmountRaids)
        memberOfClans= self.getwars(members=memberOfClans, AmountWars=AmountWars)

        return memberOfClans
    





    def refreshWarOfClans(self):
        logging.info("actualizando la informacion de la guerra")
        ruta = Config.URL_COC + '/clans/' + '%23' + Config.ClanId + '/currentwar'
        headers = {
            "Authorization": f"Bearer {Config.TokenCoc}"
        }
        response = requests.get(ruta, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error al Intentar obtener los miembros de la api de Clash of Clans: {response.status_code}")
        responseJson = response.json()
        print('\n\n\n',os.getcwd(), '\n\n\n')
        """ with open('backend/api/src/currentwarWarEnd.json', 'r', encoding='utf-8') as file:
            responseJson = json.load(file) """
        
        if responseJson == None or responseJson.get('state') == 'notInWar':
            print('\n\n\n','no hay guerra :(', '\n\n\n')

            return None

        claninfo = responseJson.get('clan')
        enemyClanInfo = responseJson.get('opponent')
        #crea una Intancia de War
        currentWar = WarOfClans(
            teamSize=responseJson.get('teamSize'),
            startTime=responseJson.get('startTime'),
            endTime=responseJson.get('endTime'),
            state=responseJson.get('state'),
            preparationStartTime=responseJson.get('preparationStartTime'),
            attacksPerMember=responseJson.get('attacksPerMember'),
            battleModifier=responseJson.get('battleModifier'),
            teamStars=claninfo.get('stars'),
            enemyStars=enemyClanInfo.get('stars'),
            enemyClanTag=enemyClanInfo.get('tag'),
            enemyClanName=enemyClanInfo.get('name'),
            teamAttacks=claninfo.get('attacks'),
            enemyAttacks=enemyClanInfo.get('attacks'),
            teamDestructionPercentage=claninfo.get('destructionPercentage'),
            enemyDestructionPercentage=enemyClanInfo.get('destructionPercentage'),
        )
        #obtener los miembros Q participaron de la api COC 
        premembers = claninfo.get('members')
    
        currentWar.members = set(
            WarMember(
                id=preMiembro["tag"],
                username=preMiembro["name"],
                mapPosition=preMiembro["mapPosition"],
                attacks=set(
                    WarAttack(
                        attackerTag=preMiembro["tag"],
                        defenderTag=preAtack["defenderTag"],
                        stars=preAtack["stars"],
                        destructionPercentage=preAtack["destructionPercentage"],
                        order=preAtack["order"],
                        duration=preAtack["duration"]
                    )
                        for preAtack in preMiembro.get("attacks", [])  # Devuelve una lista vacía si 'attacks' es None
                        if preAtack is not None  # Asegura que 'preAtack' no sea None 
                )
            )
            for preMiembro in premembers
        )
        print('\n\n\n', 'currentWar:', '\n\n\n', currentWar, '\n\n\n')

        # Guardar el objeto WarOfClans en la base de datos
        try:   
            if ModelWarOfClans.refreshWarOfClans(currentWar):
                return currentWar
            else:
                raise Exception("Error al actualizar la guerra en la db")
        except Exception as e:
            print(f"\n Error al actualizar la guerra en la db: {e}")
            raise e







    def refreshRaids(self,):
        logging.info("actualizando la informacion de los asaltos")
        headers = {
            "Authorization": f"Bearer {Config.TokenCoc}"
        }
        ruta = Config.URL_COC + '/clans/' + '%23' + Config.ClanId + '/capitalraidseasons'
        response = requests.get(ruta, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error al Intentar obtener los miembros de la api de Clash of Clans: {response.status_code}")
        res=response.json()
        items=res.get('items')[0]


        myRaid= Raid(startTime=items.get('startTime'), 
                     endTime=items.get('endTime'), 
                     totalLoot=items.get('capitalTotalLoot'), 
                     raidsCompleted=items.get('raidsCompleted'), 
                     totalAttacks=items.get('totalAttacks'), 
                     enemyDestroyed=items.get('enemyDistrictsDestroyed'),
                     state=items.get('state')
                     )


        myRaid.members={RaidMember(id=NewM.get('tag'), 
                       username=NewM.get('name'), 
                       attacks=NewM.get('attacks'), 
                       resourcesLooted=NewM.get('capitalResourcesLooted'), 
                       attackLimit=NewM.get('attackLimit')+NewM.get('bonusAttackLimit')
                ) for NewM in items.get('members')}

        # Guardar el objeto Raid en la base de datos
        try:
            if ModelRaid.refreshRaids(myRaid):
                return myRaid
            else:
                raise Exception("Error al actualizar el asalto en la db")
        except Exception as e:
            print(f"\n Error al actualizar el asalto en la db: {e}")
            raise e
        

        


    def refreshAllClanInfo(self, ):
        logging.info("Comemnzando a refrescar la informacion del clan")    
        try:
            self.get_members(refreshDb=True, onlyRefresk=True)
        except Exception as e:
            logging.error(f"Error al intentar obtener los miembros del clan: {e}")
            raise e
        try:
            self.refreshWarOfClans()
        except Exception as e:
            logging.error(f"Error al intentar obtener la informacion de la guerra: {e}")
            raise e
        try:
            self.refreshRaids()
        except Exception as e:
            logging.error(f"Error al intentar obtener la informacion de los asaltos: {e}")
            raise e
        logging.info("Se ha actualizado la informacion del clan")




memberClans = MemberManager()
