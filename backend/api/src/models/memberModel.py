
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

        try:
            sql = """
            SELECT 
                player_id as id, 
                username, 
                clan_tag,
                role, 
                townhall_level,
                trophies, 
                best_trophies, 
                ranking, 
                donations, 
                troops_requested, 
                war_stars, 
                experience_level, 
                league, 
                attack_count, 
                defense_count, 
                status, 
                left_date, 
                notes, 
                created_at, 
                updated_at
            FROM players 
            WHERE status = 'active'
            """
            cursor.execute(sql)
            rows = cursor.fetchall()

            # Crear una lista de instancias de `Member`
            members = {
                row['id']: Member(
                    id=row['id'],
                    username=row['username'],
                    clan_tag=row['clan_tag'],
                    role=row['role'],
                    townhall_level=row['townhall_level'],
                    trophies=row['trophies'],
                    best_trophies=row['best_trophies'],
                    ranking=row['ranking'],
                    donations=row['donations'],
                    troops_requested=row['troops_requested'],
                    war_stars=row['war_stars'],
                    experience_level=row['experience_level'],
                    league=row['league'],
                    attack_count=row['attack_count'],
                    defense_count=row['defense_count'],
                    status=row['status'],
                    left_date=row['left_date'],
                    notes=row['notes'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ) for row in rows
            }
            return members

        except Exception as ex:
            raise Exception(f"Error retrieving members: {ex}")

        finally:
            cls.db.close_connection(connection)

    @classmethod
    def refreshMembers(cls, deleteMembers: list, insertMembers: list, updateMembers:dict):
        connection = cls.db.create_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            if deleteMembers:
                sql = """
                UPDATE players
                SET status = 'left'
                WHERE player_id IN (%s)
                """
                cursor.execute(sql, (','.join(map(str, deleteMembers)),))
                connection.commit()

            # Insertar nuevos miembros
            if insertMembers:
                for newMember in insertMembers:
                    sql = """
                    INSERT INTO players (
                        player_id,
                        username,
                        clan_tag,
                        role,
                        townhall_level,
                        trophies,
                        best_trophies,
                        ranking,
                        donations,
                        troops_requested,
                        war_stars,
                        experience_level,
                        league,
                        attack_count,
                        defense_count,
                        status

                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        newMember.id, 
                        newMember.username, 
                        newMember.clan_tag, 
                        newMember.role, 
                        newMember.townhall_level, 
                        newMember.trophies, 
                        newMember.best_trophies, 
                        newMember.ranking, 
                        newMember.donations, 
                        newMember.troops_requested, 
                        newMember.war_stars, 
                        newMember.experience_level, 
                        newMember.league, 
                        newMember.attack_count, 
                        newMember.defense_count,
                        newMember.status


                    ))
                connection.commit()
            # Actualizar miembros existentes
            if updateMembers and updateMembers != {}:    
                for member_id, member_data in updateMembers.items():
                    sql = """
                    UPDATE players
                    SET 

                        role = %s,
                        townhall_level = %s,
                        trophies = %s,
                        best_trophies = %s,
                        ranking = %s,
                        donations = %s,
                        troops_requested = %s,
                        war_stars = %s,
                        experience_level = %s,
                        league = %s,
                        attack_count = %s,
                        defense_count = %s,
                        status = %s

                    WHERE player_id = %s
                    """
                    cursor.execute(sql, (
                        member_data.role,
                        member_data.townhall_level,
                        member_data.trophies,
                        member_data.best_trophies,
                        member_data.ranking,
                        member_data.donations,
                        member_data.troops_requested,
                        member_data.war_stars,
                        member_data.experience_level,
                        member_data.league,
                        member_data.attack_count,
                        member_data.defense_count,
                        member_data.status,
                        member_id
                    ))
                connection.commit()

        
        
        except Exception as ex:
            connection.rollback()
            raise ex

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




    
    
    
    
    
