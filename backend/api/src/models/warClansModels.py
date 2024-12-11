from database.db import MySQLConnectionManager
from utils.logger import Logger
from models.entities.member import Member, WarMember
from models.entities.members import Members
from models.entities.warOfClans import WarOfClans
from models.entities.warAttack import WarAttack

class ModelWarOfClans():

    db = MySQLConnectionManager() 

    
    @classmethod
    def refreshWarOfClans(cls, warOfClans: WarOfClans):
        connection = cls.db.create_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            #insertar nueva gerra y si ya existe solo actualizar 
            sql="""
                
                INSERT INTO war (
                startTime, 
                preparationStartTime,
                endTime,
                state,
                teamSize,
                teamStars,
                enemyStars,
                attacksPerMember,
                enemyClanName,
                enemyClanTag,
                teamAttacks,
                enemyAttacks,
                teamDestructionPercentage,
                enemyDestructionPercentage,
                battleModifier
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON DUPLICATE KEY UPDATE 
                endTime = VALUES(endTime),
                state = VALUES(state),
                teamSize = VALUES(teamSize),
                teamStars = VALUES(teamStars),
                enemyStars = VALUES(enemyStars),
                attacksPerMember = VALUES(attacksPerMember),                
                enemyClanName = VALUES(enemyClanName),
                enemyClanTag = VALUES(enemyClanTag),
                teamAttacks = VALUES(teamAttacks),
                enemyAttacks = VALUES(enemyAttacks),
                teamDestructionPercentage = VALUES(teamDestructionPercentage),
                enemyDestructionPercentage = VALUES(enemyDestructionPercentage),
                battleModifier = VALUES(battleModifier);
                """

            cursor.execute(sql, (
                warOfClans.startTime,
                warOfClans.preparationStartTime,
                warOfClans.endTime,
                warOfClans.state,
                warOfClans.teamSize,
                warOfClans.teamStars,
                warOfClans.enemyStars,
                warOfClans.attacksPerMember,
                warOfClans.enemyClanName,
                warOfClans.enemyClanTag,
                warOfClans.teamAttacks,                
                warOfClans.enemyAttacks,
                warOfClans.teamDestructionPercentage,
                warOfClans.enemyDestructionPercentage,
                warOfClans.battleModifier
                )
            )

            connection.commit()
            #iteramos sobre los miembros del la intancia War
            for member in warOfClans:
                sql="""
                    INSERT IGNORE INTO warMembers (
                        warStartTime,
                        player_id
                    )
                    VALUES (%s, %s);
                    """
                cursor.execute(sql, (
                               warOfClans.startTime,
                               member.id
                               ))
                for atack in member.attacks:
                    sql="""
                        INSERT INTO warAttacks (
                            warStartTime,
                            player_id,
                            attackOrder,
                            defenderTag,
                            stars,
                            destructionPercentage,
                            duration
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        stars = VALUES(stars),
                        destructionPercentage = VALUES(destructionPercentage),
                        duration = VALUES(duration)
                    """

                    cursor.execute(sql, (
                        warOfClans.startTime,
                        member.id,
                        atack.order,
                        atack.defenderTag,
                        atack.stars,
                        atack.destructionPercentage,
                        atack.duration

                    ))

            connection.commit()
            return True
        except Exception as ex:
            connection.rollback()
            raise ex

        finally:
            cls.db.close_connection(connection)
            


    @classmethod
    def getWarsOfClans(self, amount=3):
        #recuperar las ultimas Guerras del clan 
        connection = self.db.create_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            sql = """
            WITH RecentWars AS (
                SELECT startTime
                FROM war
                ORDER BY startTime DESC
                LIMIT %s
            )
            SELECT 
                w.startTime,
                w.preparationStartTime,
                w.endTime,
                w.state,
                w.teamSize,
                w.teamStars,
                w.enemyStars,
                w.attacksPerMember,
                w.enemyClanName,
                w.enemyClanTag,
                w.teamAttacks,
                w.enemyAttacks,
                w.teamDestructionPercentage,
                w.enemyDestructionPercentage,
                w.battleModifier,
                wm.player_id,
                wa.attackOrder,
                wa.defenderTag,
                wa.stars,
                wa.destructionPercentage,
                wa.duration
            FROM war w
            JOIN RecentWars rw ON w.startTime = rw.startTime
            JOIN warMembers wm ON w.startTime = wm.warStartTime
            LEFT JOIN warAttacks wa ON w.startTime = wa.warStartTime AND wm.player_id = wa.player_id
            ORDER BY w.startTime DESC;
            """
            cursor.execute(sql, (amount,))
            
            rows = cursor.fetchall()
            #ordenar los datos usando las entidades WarOfClans, WarMember y WarAttack
            warsDict= {}
            membersDict = {}




            for row in rows:
                    # Si la guerra aún no está en el diccionario, la creamos
                start_time = row['startTime']
                #
                idMember = row['player_id']
                if f'{idMember} {start_time}' not in membersDict:
                    membersDict[f'{idMember} {start_time}'] = WarMember(
                        id=idMember,
                        attackLimit=row['attacksPerMember'],
                        startTimeWar=start_time,
                        attacks=set()
                    )
                # Añade un ataque si el jugador a realizado ataques 
                if row['attackOrder'] is not None and row['stars'] is not None:
                    membersDict[f'{idMember} {start_time}'].add_attack(
                        WarAttack(
                            attackerTag=idMember,
                            defenderTag=row['defenderTag'],
                            stars=row['stars'],
                            destructionPercentage=row['destructionPercentage'],
                            order=row['attackOrder'],
                            duration=row['duration']
                        )
                    )



                #
                if start_time not in warsDict:
                    warsDict[start_time] = WarOfClans(
                        startTime=row['startTime'],
                        preparationStartTime=row['preparationStartTime'],
                        endTime=row['endTime'],
                        state=row['state'],
                        teamSize=row['teamSize'],
                        teamStars=row['teamStars'],
                        enemyStars=row['enemyStars'],
                        attacksPerMember=row['attacksPerMember'],
                        enemyClanName=row['enemyClanName'],
                        enemyClanTag=row['enemyClanTag'],
                        teamAttacks=row['teamAttacks'],
                        enemyAttacks=row['enemyAttacks'],
                        teamDestructionPercentage=row['teamDestructionPercentage'],
                        enemyDestructionPercentage=row['enemyDestructionPercentage'],
                        battleModifier=row['battleModifier']
                    
                    )
            for key ,notMember in membersDict.items():
                warsDict[notMember.startTimeWar].add_member(notMember)

            wars_list = sorted(warsDict.values(), key=lambda war: war.startTime, reverse=True)
            
            return wars_list
        except Exception as ex:
            raise ex
        finally:
            self.db.close_connection(connection)
