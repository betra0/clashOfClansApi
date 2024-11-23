from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
class Rol:
    profesor = 'profesor'
    alumno = 'alumno'
class isAdmin:
    false = 0
    nivel1 = 1
    


class User:
    def __init__(self, 
                 id = '', 
                 full_name = "", 
                 first_name = "",
                 last_name='',
                 email = '',
                 profile_picture='',
                 google_refresh_token='',
                 is_admin = isAdmin.false,
                 is_active=1, 
                 created_at=None):
        
        self.id = id
        self.full_name = full_name
        self.first_name = first_name
        self.last_name = last_name
        self.profile_picture = profile_picture
        self.google_refresh_token= google_refresh_token
        self.is_admin = is_admin
        self.email = email
        self.is_active = is_active
        self.created_at= created_at
    
    def getdict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'profile_picture': self.profile_picture,
            'is_admin': self.is_admin,
            'created_at': self.created_at,
            'is_active': self.is_active

        }
    
    def __str__(self):
        return f"User(id={self.id}, full_name='{self.full_name}', first_name='{self.first_name}', " \
               f"  email='{self.email}')"
    
    



