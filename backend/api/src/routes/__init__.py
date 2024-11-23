from flask import Blueprint, jsonify
import requests
from .test import testRoute
from .auth import authRoutes
from config import Config
from models.memberModel import ModelMember
import time
from datetime import datetime
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
    if elapsed_time == None or elapsed_time > 60:
        return jsonify({'members':dbMembers})
    
    response = requests.get(ruta, headers=headers)
    apiMembersList = response.json().get('items')


    apiMembersDict = {item["tag"]: item for item in apiMembersList}
    nombres = [item["name"] for item in apiMembersList]



    # Actualizar la última llamada con el tiempo actual
    last_called = now
    """ if response.status_code != 200:
        return jsonify({'error': 'Clan not found'}), 404
    return response.json() """


    return jsonify({'names':nombres})