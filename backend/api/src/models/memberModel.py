
from database.db import MySQLConnectionManager
from utils.logger import Logger
from models.entities.user import User
from models.entities.member import Member

class ModelMember():

    db = MySQLConnectionManager() 

    
    @classmethod
    def getAllMembers(cls):
        connection = cls.db.create_connection()
        cursor = connection.cursor(dictionary=True)
        """ if not connection.is_connected():
            raise Exception('Connection to MySQL database is closed for ERROR') """
        try:
            sql = "SELECT player_id as id, username, role, status, left_date, notes, created_at, updated_at FROM players WHERE status = 'active'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            members = {
            }
            for row in rows:
                members[row['id']] = Member(row['id'], row['username'], row['role'], row['status'], row['left_date'], row['notes'], row['created_at'], row['updated_at'])
            return members
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




    
    
    
    
    
