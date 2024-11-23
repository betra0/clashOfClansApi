
from database.db import MySQLConnectionManager
from utils.logger import Logger
from models.entities.user import User

class ModelUser():

    db = MySQLConnectionManager() 

    
    
    @classmethod
    def get_by_id(cls, id):
            connection = cls.db.create_connection()
            cursor = connection.cursor(dictionary=True)
            try:
                sql = """SELECT  id, email, full_name, first_name, last_name, profile_picture, is_admin, google_refresh_token, created_at, is_active
                FROM users WHERE id = %s"""
                cursor.execute(sql, (id,))
                row = cursor.fetchone()

                if row is not None:
                        return User(
                            id=row['id'],                             
                            email=row['email'],                       
                            full_name=row['full_name'],               #  el nombre completo
                            first_name=row['first_name'],             #  el primer nombre
                            last_name=row['last_name'],               #  el apellido
                            profile_picture=row['profile_picture'],    #  la foto de perfil
                            is_admin=row['is_admin'],                   #  el estado de administrador
                            google_refresh_token=row['google_refresh_token'],  #  el token de actualización
                            created_at=row['created_at'],             #  la fecha de creación
                            is_active=row['is_active']                  #  el estado de activo

                        )
                else:
                    return None
            except Exception as ex:
                raise Exception(ex)
            finally:
                cls.db.close_connection(connection)

    @classmethod
    def createUser(cls, user):
        conexion = cls.db.create_connection()
        cursor = conexion.cursor()
        try:
            sql = """INSERT INTO users 
            (id, email, full_name, first_name, last_name, profile_picture, is_admin, google_refresh_token) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (user.id, user.email, 
                                 user.full_name, user.first_name, user.last_name, user.profile_picture,
                                 user.is_admin, user.google_refresh_token))

            conexion.commit()
            return True

        except Exception as e:
            conexion.rollback()
            Logger.add_to_log('error', e)
            raise
    

        finally:
            cls.db.close_connection(conexion)




    
    
    
    
    
