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


    @classmethod
    def getRaids(cls,  amount=3):
        connection = cls.db.create_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            sql = """
            WITH RecentRaids AS (
                SELECT startTime
                FROM raids
                ORDER BY startTime DESC
                LIMIT %s
            )
            SELECT 
                r.startTime,
                r.endTime,
                r.totalLoot,
                r.raidsCompleted,
                r.totalAttacks,
                r.enemyDestroyed,
                r.state,
                rm.player_id,
                rm.attacks,
                rm.resourcesLooted,
                rm.attackLimit
            FROM raids r
            JOIN RecentRaids rr ON r.startTime = rr.startTime
            JOIN raidMembers rm ON r.startTime = rm.raidStartTime
            ORDER BY r.startTime DESC;
            """
            cursor.execute(sql, (amount,))
            rows = cursor.fetchall()
            raidDict = {}
            for row in rows:
                if row['startTime'] not in raidDict:
                    raidDict[row['startTime']] = Raid(
                        startTime=row['startTime'],
                        endTime=row['endTime'],
                        totalLoot=row['totalLoot'],
                        raidsCompleted=row['raidsCompleted'],
                        totalAttacks=row['totalAttacks'],
                        enemyDestroyed=row['enemyDestroyed'],
                        state=row['state']
                    )
                raidDict[row['startTime']].add_member(
                    RaidMember(
                        id=row['player_id'],
                        attacks=row['attacks'],
                        resourcesLooted=row['resourcesLooted'],
                        attackLimit=row['attackLimit']
                    )
                )
            raidsList = sorted(raidDict.values(), key=lambda x: x.startTime, reverse=True)

            return raidsList
        except Exception as e:
            raise e
        finally:
            cls.db.close_connection(connection)