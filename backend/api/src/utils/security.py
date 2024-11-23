import jwt
from functools import wraps
from flask import request, jsonify, g
import datetime
from datetime import datetime, timedelta, UTC
import traceback
from models.usermodel import ModelUser
from config import Config



class SecurityToken():


    @classmethod
    def generateAccessToken(self, id):
        expiration_date = datetime.now(UTC) + timedelta(hours=Config.accessExpirationHours  , minutes=0)
        payload ={'user_id': id, 'exp': expiration_date,}
        
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
        return token
    
    @classmethod
    def accessToken_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Obtener el encabezado Authorization
            auth_header = request.headers.get('Authorization')
            # Verificar si el encabezado está presente y comienza con 'Bearer '
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'message': 'Token faltante o formato incorrecto!'}), 401
            
            # Extraer el token removiendo el prefijo 'Bearer '
            token = auth_header.split(" ")[1]

            if not token: 
                return jsonify({'message': 'no hay token!',
                                'active': -1}), 401

            try:
                
                payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
                try:
                    user = ModelUser.get_by_id(payload['user_id'])
                except Exception as e:
                    
                    traceback.print_exc()
                    return jsonify({'error':str(e)}), 500
                if user == None:
                    return jsonify({'message': ' Usuario no valido!',
                                'active': -1}), 401
                
                # Aquí almacenamos el usuario en el contexto global `g`
                g.currentUser = user
                return f(*args, **kwargs)
                
            except jwt.ExpiredSignatureError:   
                return jsonify({'message': 'Token has expired!',
                                'active': 0}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Token is invalid!',
                                'active': 0}), 401

        return decorated