from flask import Blueprint, jsonify
import requests
from .test import testRoute
from .auth import authRoutes
from config import Config
from models.memberModel import ModelMember
import time
from datetime import datetime
from models.entities.member import Member
# Crear un blueprint  y registrar las rutas
RaizBlueprint = Blueprint('Raiz', __name__)



RaizBlueprint.register_blueprint(testRoute, url_prefix='/test')
RaizBlueprint.register_blueprint(authRoutes, url_prefix='/auth')
last_called = None

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
def Members():
    global last_called

    # Obtener el tiempo actual
    now = time.time()

    # Calcular el tiempo desde la última llamada
    if last_called is None:
        elapsed_time = None
    else:
        elapsed_time = now - last_called
    

    print('\n\n\n' , 'last_called:', '\n\n\n', elapsed_time, '\n\n\n')

    headers = {
    "Authorization": f"Bearer {Config.TokenCoc}"
    }
   
    ruta = Config.URL_COC+'/clans/'+'%23'+Config.ClanId+'/members'

    dbMembers = ModelMember.getAllMembers()
    print('\n\n\n' , 'dbMembers:', '\n\n\n', dbMembers, '\n\n\n')
    if elapsed_time != None and elapsed_time < 3:
        return jsonify({'members':dbMembers})
    print('\n\n\n' , 'ruta:', '\n', ruta, '\n\n\n')
    response = requests.get(ruta, headers=headers)
    if response.status_code != 200:
        
        return jsonify({'error': 'Error al obtener los miembros', 'status_code': response.status_code}), 404
    apiMembersList = response.json().get('items')


    apiMembersDict = {item["tag"]: Member( 
            id=item["tag"], 
            username=item["name"], 
            role=item["role"], 
            townhall_level=item['townHallLevel'], 
            trophies=item['trophies'], 
            ranking=item['clanRank'],
            donations=item['donations'],
            troops_requested=item['donationsReceived'],
            experience_level=item['expLevel'],

            ) for item in apiMembersList}
    nombres = [item["name"] for item in apiMembersList]
    newMembers = [ member for k, member in apiMembersDict.items() if k not in dbMembers]
    deleteMembers = [k for k, v in dbMembers.items() if k not in apiMembersDict]

    print('\n\n\n' , 'newMembers:', '\n\n\n', newMembers, '\n\n\n')
    print('\n\n\n' , 'deleteMembers:', '\n\n\n', deleteMembers, '\n\n\n')

    try:	
        ModelMember.refreshMembers(deleteMembers, newMembers, apiMembersDict)
    except Exception as e:
        print(f"ErrorA: {e}")
        raise e 
    try:
        actualMembers = ModelMember.getAllMembers()
        formatMembers = {k: v.getdict() for k, v in actualMembers.items()}
        print('\n\n\n' , 'actualMembers:', '\n\n\n', formatMembers, '\n\n\n')
        last_called = now
        return jsonify({'members':formatMembers})
    except Exception as e:
        print(f"Error: {e}")
        raise e
        return jsonify({'error': 'Error al obtener los miembros'}), 500

    # Actualizar la última llamada con el tiempo actual
    
    """ if response.status_code != 200:
        return jsonify({'error': 'Clan not found'}), 404
    return response.json() """


    return jsonify({'names':'hello'})