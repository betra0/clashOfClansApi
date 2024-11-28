from flask import Blueprint, jsonify
import requests
from .test import testRoute
from .auth import authRoutes
from config import Config
from models.entities.members import Members
from models.entities.member import Member, RaidMember
from models.entities.raid import Raid


from services.ClanManager import memberClans
# Crear un blueprint  y registrar las rutas
RaizBlueprint = Blueprint('Raiz', __name__)



RaizBlueprint.register_blueprint(testRoute, url_prefix='/test')
RaizBlueprint.register_blueprint(authRoutes, url_prefix='/auth')


@RaizBlueprint.route('/', methods=['GET'])
def Raiz():
    return "Hello Word"


@RaizBlueprint.route('/clan', methods=['GET'])
def Clan():

    headers = {
    "Authorization": f"Bearer petjw29z"
    }
    ruta = Config.URL_COC+'clans/'+'%23/'+Config.ClanId
    response = requests.get(ruta, headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Clan not found'}), 404
    return response.json()






@RaizBlueprint.route('/members', methods=['GET'])
def MembersEndpoint():
    members = memberClans.get_members()

    return jsonify({'members': members.getdict(notNull=True)}), 200

@RaizBlueprint.route('/raids', methods=['GET'])
def Raids():
    mymembers = memberClans.get_members()
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
                 enemyDestroyed=items.get('enemyDistrictsDestroyed'))
    
    
    myRaid.members={RaidMember(id=NewM.get('tag'), 
                   username=NewM.get('name'), 
                   attacks=NewM.get('attacks'), 
                   resourcesLooted=NewM.get('capitalResourcesLooted'), 
                   attackLimit=NewM.get('attackLimit')+NewM.get('bonusAttackLimit')
            ) for NewM in items.get('members')}
        
    
    mymembers.add_raid(myRaid)
    
    
    
    #memberNotRaids = Members()
    #memberNotRaids.members= mymembers.members - membersRaids.members


    
    return jsonify({'raids': mymembers.getInfoRaid()}), 200