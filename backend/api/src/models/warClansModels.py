from database.db import MySQLConnectionManager
from utils.logger import Logger
from models.entities.member import Member 
from models.entities.members import Members
from models.entities.warOfClans import WarOfClans

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

            for member in warOfClans:
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
