
from database.db import MySQLConnectionManager
from utils.logger import Logger
from models.entities.member import Member 
from models.entities.members import Members

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
            members = Members()
            for row in rows:
                members.add_member(
                    Member(
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
                    )
                )
                
            return members

        except Exception as ex:
            raise Exception(f"Error retrieving members: {ex}")

        finally:
            cls.db.close_connection(connection)

    @classmethod
    def refreshMembers(cls, deleteMembers:Members, insertMembers:Members, updateMembers:Members):
        connection = cls.db.create_connection()
        cursor = connection.cursor(dictionary=True)
        position = ','.join(['%s'] * len(deleteMembers))
        try:
            if deleteMembers:
                sql = f"""
                UPDATE players
                SET status = 'left'
                WHERE player_id IN ({position})
                """
                cursor.execute(sql, deleteMembers.getIdsList())
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
                for member in updateMembers:
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
                        member.role,
                        member.townhall_level,
                        member.trophies,
                        member.best_trophies,
                        member.ranking,
                        member.donations,
                        member.troops_requested,
                        member.war_stars,
                        member.experience_level,
                        member.league,
                        member.attack_count,
                        member.defense_count,
                        member.status,
                        member.id
                    ))
                connection.commit()

        
        
        except Exception as ex:
            connection.rollback()
            raise ex

        finally:
            cls.db.close_connection(connection)    
            

            




    
    
    
    
    
