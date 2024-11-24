from flask import Blueprint, jsonify
import requests
from .test import testRoute
from .auth import authRoutes
from config import Config
from models.memberModel import ModelMember
import time
from datetime import datetime
from models.entities.member import Member
from services.members import memberClans
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
def Members():
    members = memberClans.get_members()
    formatMembers = {k: v.getdict() for k, v in members.items()}
    return jsonify({'members': formatMembers}), 200

