
from flask import  request, jsonify, Blueprint
from config import Config
from models.usermodel import ModelUser
from models.sessionModel import ModelSession
from utils.security import SecurityToken

tokenRoute = Blueprint('Token', __name__)


def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        # Si la app está detrás de un proxy, la IP puede estar en este encabezado
        return request.headers.get('X-Forwarded-For').split(',')[0]  # Obtener la primera IP
    return request.remote_addr  # Si no, usar la dirección IP directa


@tokenRoute.route('/', methods=['GET'])
def newAccessToken():
    token = request.cookies.get('refresh_token')
    
    if not token: 
        return jsonify({'message': 'No hay Token Refresh', 'success': False, 'active': -1}), 401
    
    session = ModelSession.get_by_token(token=token)
    
    if not session:
        return jsonify({'message': 'Sesión no encontrada', 'success': False}), 401
    
    if session.is_expired():  
        return jsonify({'message': 'Token Refresh ha expirado', 'success': False}), 401
    
    user = ModelUser.get_by_id(id=session.user_id)
    
    if not user or user.is_active <= 0:
        return jsonify({'message': 'Usuario no válido o inactivo', 'success': False}), 401
    
    # Generar el nuevo Access Token
    accessToken = SecurityToken.generateAccessToken(id=user.id)
    
    return jsonify({'success': True, 'data': {'access_token': accessToken}}), 200
    