from database.db import MySQLConnectionManager
from utils.logger import Logger
from models.entities.user_session import UserSession
#from models.entities.user_session import UserSession

class ModelSession():

    db = MySQLConnectionManager() 

    
    
    @classmethod
    def createSession(cls, session):
         conexion = cls.db.create_connection()
         cursor = conexion.cursor()
         try:
             sql = """INSERT INTO user_sessions 
             (refresh_token, user_id, user_agent, ip_address, expires_at) 
             VALUES (%s, %s, %s, %s, %s)"""
             cursor.execute(sql, (
                                  session.refresh_token, 
                                  session.user_id,
                                  session.user_agent, 
                                  session.ip_address, 
                                  session.expires_at))
             conexion.commit()
             return True
         except Exception as e:
             conexion.rollback()
             Logger.add_to_log('error', e)
             raise
         
         finally:
             cls.db.close_connection(conexion)
             
    @classmethod
    def get_by_token(cls, token):
        connection = cls.db.create_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            sql = """
            
            SELECT  
            refresh_token, user_id, user_agent, ip_address, created_at, expires_at
            FROM user_sessions
            WHERE refresh_token = %s"""

            cursor.execute(sql, (token,))
            res = cursor.fetchone()
            if res is not None:
                    return UserSession(
                        refresh_token=res['refresh_token'],                             
                        user_id=res['user_id'],                             
                        user_agent=res['user_agent'],                             
                        ip_address=res['ip_address'],                                                          
                        created_at=res['created_at'],                             
                        expires_at=res['expires_at'],                             
                    )
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        finally:
            cls.db.close_connection(connection)
