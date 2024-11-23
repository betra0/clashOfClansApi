# Función para obtener la dirección IP del cliente


import requests
from flask import  request, jsonify, Blueprint
from config import Config
from models.usermodel import ModelUser
from models.entities.user import User
from models.entities.user_session import UserSession
from models.sessionModel import ModelSession
from datetime import datetime, timedelta, timezone
from utils.security import SecurityToken

googleRoutes = Blueprint('Google', __name__)


def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        # Si la app está detrás de un proxy, la IP puede estar en este encabezado
        return request.headers.get('X-Forwarded-For').split(',')[0]  # Obtener la primera IP
    return request.remote_addr  # Si no, usar la dirección IP directa


@googleRoutes.route('/', methods=['POST', 'GET'])

def auth_google():
    
    if request.method == 'POST':
        code = request.json.get('code')

        # URL para intercambiar el código por un token
        token_url = Config.tokenGoogleUrl

        # Datos para la solicitud de intercambio de token
        data = {
            'code': code,
            'client_id': Config.googleClientId,
            'client_secret': Config.googleClientSecret,
            'redirect_uri': Config.redirectUri,
            'grant_type': 'authorization_code'
        }


        # Solicitud a Google para obtener el access token
        response = requests.post(token_url, data=data)
        token_data = response.json()


        if not 'access_token' in token_data:
           return jsonify({'error': 'Failed to retrieve access token'}), 400

        if not 'refresh_token' in token_data:
            return jsonify({'error': 'Failed to retrieve refresh token '}), 400

        access_tokenG = token_data['access_token']
        refresh_tokenG = token_data['refresh_token']
        # Usar el access token para obtener los datos del usuario
        user_info_url = Config.tokenGoogleUrlInfo
        headers = {
            'Authorization': f'Bearer {access_tokenG}'
        }
        # Solicitud a Google para obtener la información del usuario
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()
        if not user_info :
            return jsonify({
            'success': False, 'message':'ERROR AL  RECUPERAR LA INFO DEL USER'
        }), 500

        # Verificar que los campos necesarios estén presentes
        required_fields = ['email', 'given_name', 'family_name', 'name', 'picture', 'sub']
        missing_fields = [field for field in required_fields if field not in user_info]

        if missing_fields:
            return jsonify({
                'success': False, 
                'message': f'Missing fields: {", ".join(missing_fields)}'
            })

        user = ModelUser.get_by_id(user_info['sub'])
        if not user:
            print('CREANDO AL USUARIO ')

            ModelUser.createUser(
                        User(
                        id=user_info['sub'],                             
                        email=user_info['email'],                       
                        full_name=user_info['name'],               
                        first_name=user_info['given_name'],            
                        last_name=user_info['family_name'],             
                        profile_picture=user_info['picture'],                 
                        google_refresh_token=refresh_tokenG,  #  el token de actualización
                        is_active=1
                        )
            )
            user = ModelUser.get_by_id(user_info['sub'])
        else:
            print('EL USUARIO YA EXISTE')
        #crear token de session (pendiente)
        session = UserSession(
            refresh_token=UserSession.generateToken(),
            user_id=user.id,
            user_agent=str(request.headers.get('User-Agent')),
            ip_address=str(get_client_ip()),
            expires_at=datetime.now(timezone.utc) + timedelta(days=Config.refreshExpirationDays)
        )
        print(session.getdict())
        try:

            if not ModelSession.createSession(session=session):
                return jsonify({
                'success': False, 'message':'ERROR AL CREAR LA SESION'
            }), 500
        except Exception as e:
            return jsonify({
                'success': False, 'e':str(e), 'message':'ERROR AL CREAR LA SESION'
            }), 500

        accessToken=SecurityToken.generateAccessToken(id=user.id)

        res= jsonify({'success':True, 'data':{'user':user.getdict(), 'access_token':accessToken}})
        res.set_cookie('refresh_token', session.refresh_token, httponly=True, secure=False, max_age=86400*Config.refreshExpirationDays) 
        return res, 200
    
    else:
        return 'Hola este es get de /auth/gOOGLE'