from database.db import MySQLConnectionManager
from utils.logger import Logger
from models.entities.member import Member, RaidMember
from models.entities.members import Members
from models.entities.raid import Raid



class ModelRaid():

    db = MySQLConnectionManager() 

    
    @classmethod
    def refreshRaids(cls, raid: Raid):
        connection = cls.db.create_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            sql="""
                
                INSERT INTO raids (
                startTime, 
                endTime,
                totalLoot,
                raidsCompleted,
                totalAttacks,
                enemyDestroyed,
                state
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                )
                ON DUPLICATE KEY UPDATE 
                endTime = VALUES(endTime),
                totalLoot = VALUES(totalLoot),
                raidsCompleted = VALUES(raidsCompleted),
                totalAttacks = VALUES(totalAttacks),
                enemyDestroyed = VALUES(enemyDestroyed),
                state = VALUES(state);
                """
            cursor.execute(sql, (
                raid.startTime,
                raid.endTime,
                raid.totalLoot,
                raid.raidsCompleted,
                raid.totalAttacks,
                raid.enemyDestroyed,
                raid.state
            ))
            #insertar miembros que participaron en el asalto
            raidMember: RaidMember
            for raidMember in raid:
                sql = """
                INSERT INTO raidMembers (
                raidStartTime,
                player_id,
                attacks,
                resourcesLooted,
                attackLimit
                ) VALUES (
                    %s, %s, %s, %s, %s
                )
                ON DUPLICATE KEY UPDATE 
                attacks = VALUES(attacks),
                resourcesLooted = VALUES(resourcesLooted),
                attackLimit = VALUES(attackLimit);
                """
                cursor.execute(sql, (
                    raid.startTime,
                    raidMember.id,
                    raidMember.attacks,
                    raidMember.resourcesLooted,
                    raidMember.attackLimit
                ))
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cls.db.close_connection(connection)