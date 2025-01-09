
from database.db import MySQLConnectionManager
from utils.logger import Logger
from models.entities.member import Member, DonationLogMember
from models.entities.members import Members
from models.entities.donationLog import DonationLog
from config import Config

class ModelMember():

    db = MySQLConnectionManager() 

    
    @classmethod
    def getAllMembers(cls, clan_tag=Config.ClanId):
        connection = cls.db.create_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            sql = """
            SELECT 
                p.player_id as id, 
                p.username, 
                p.clan_tag,
                p.role, 
                p.townhall_level,
                p.trophies, 
                p.best_trophies, 
                p.ranking, 
                p.donations, 
                p.troops_requested, 
                p.war_stars, 
                p.experience_level, 
                p.league, 
                p.attack_count, 
                p.defense_count, 
                p.status, 
                p.left_date, 
                p.notes, 
                p.created_at, 
                p.updated_at,
                pic.accumulatedDonations,
                pic.accumulatedTroopsRequested
            FROM players p
            INNER JOIN playersInClans pic ON p.player_id = pic.player_id
            WHERE p.status = 'active'
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
                    updated_at=row['updated_at'],
                    accumulatedDonations=row['accumulatedDonations'],
                    accumulatedTroopsRequested=row['accumulatedTroopsRequested']
                    
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
                    ON DUPLICATE KEY UPDATE
                        username = VALUES(username),
                        clan_tag = VALUES(clan_tag),
                        role = VALUES(role),
                        townhall_level = VALUES(townhall_level),
                        trophies = VALUES(trophies),
                        best_trophies = VALUES(best_trophies),
                        ranking = VALUES(ranking),
                        donations = VALUES(donations),
                        troops_requested = VALUES(troops_requested),
                        war_stars = VALUES(war_stars),
                        experience_level = VALUES(experience_level),
                        league = VALUES(league),
                        attack_count = VALUES(attack_count),
                        defense_count = VALUES(defense_count),
                        status = VALUES(status);
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
                    sql = f"""
                        INSERT INTO playersInClans (
                            player_id, 
                            clan_tag,
                            accumulatedDonations,
                            accumulatedTroopsRequested
                        )
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            accumulatedDonations = VALUES(accumulatedDonations),
                            accumulatedTroopsRequested = VALUES(accumulatedTroopsRequested);
                        """
                    cursor.execute(sql, (
                        newMember.id,
                        newMember.clan_tag,
                        newMember.accumulatedDonations,
                        newMember.accumulatedTroopsRequested,
                        
                    ))
                connection.commit()
            # Actualizar miembros existentes
            if updateMembers and updateMembers != {}:    
                for member in updateMembers:
                    sql = """
                    UPDATE players
                    SET 
                        username = %s,
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
                        member.username,
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
                    sql = f"""
                        UPDATE playersInClans 
                        SET

                            accumulatedDonations = %s,
                            accumulatedTroopsRequested = %s
                        WHERE player_id = %s AND clan_tag = %s
                        

                        """
                    cursor.execute(sql, (
                        member.accumulatedDonations,
                        member.accumulatedTroopsRequested,
                        member.id,
                        member.clan_tag
                    ))
                connection.commit()

        
        
        except Exception as ex:
            connection.rollback()
            raise ex

        finally:
            cls.db.close_connection(connection)    
    @classmethod       
    def insertDonationLog(self, donationLog:DonationLog):
        connection = self.db.create_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            try:
                sql = """
                INSERT INTO clan_donation_logs (
                    clan_tag,
                    donations,
                    requests,
                    log_date
                )
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    donationLog.clan_tag,
                    donationLog.getDonations(),
                    donationLog.getRequests(),
                    donationLog.logDate
                ))
            except Exception as ex:
                print('Error al insertar el clan_donation_logs:\n', ex)
                raise ex
            try:
                memberLog:DonationLogMember
                for memberLog in donationLog.members:

                    sql = """
                    INSERT INTO member_donation_logs (
                        clan_tag,
                        player_id,
                        donations,
                        requests,
                        log_date
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        donationLog.clan_tag,
                        memberLog.id,
                        memberLog.donationsLog,
                        memberLog.requestsLog,
                        donationLog.logDate
                    ))
                connection.commit()
            except Exception as ex:
                print('Error al insertar el member_donation_logs:\n', ex)
                raise ex
        except Exception as ex:
            connection.rollback()
            raise ex
        finally:
            self.db.close_connection(connection)








    @classmethod
    def getDonationLogs(self, clan_tag=f'#{Config.ClanId}', ofset=0, limit=30):
        connection = self.db.create_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            # Paso 1: Obtener las fechas limitadas
            sql_dates = """
            SELECT 
                cdl.clan_tag,
                cdl.donations AS clan_donations,
                cdl.requests AS clan_requests,
                cdl.log_date
            FROM clan_donation_logs cdl
            WHERE cdl.clan_tag = %s
            ORDER BY cdl.log_date DESC
            LIMIT %s OFFSET %s
            """
            cursor.execute(sql_dates, (clan_tag, limit, ofset))
            rows = cursor.fetchall()
            print(rows)

            # Paso 2: Obtener los registros de los miembros correspondientes a esas fechas
            log_dates:list = [row['log_date'] for row in rows]  # Extraer las fechas obtenidas
            if not log_dates:
                return []
            position = ','.join(['%s'] * len(log_dates))
            vars = (clan_tag, *log_dates)
            sql_members = f"""
            SELECT 
                mdl.player_id,
                mdl.donations AS player_donations,
                mdl.requests AS player_requests,
                mdl.log_date
            FROM member_donation_logs mdl
            WHERE mdl.clan_tag = %s
            AND mdl.log_date IN ({position})
            """
            print(sql_members)
            cursor.execute(sql_members, (vars))  # Pasar las fechas como tupla
            member_rows = cursor.fetchall()

            # Ahora procesas los logs y miembros
            donation_logs = []
            for row in rows:
                donation_log = next((log for log in donation_logs if log.logDate == row['log_date']), None)

                if not donation_log:
                    donation_log = DonationLog(
                        clan_tag=row['clan_tag'],
                        donations=row['clan_donations'],
                        requests=row['clan_requests'],
                        logDate=row['log_date'],
                        members=set()
                    )
                    donation_logs.append(donation_log)

                # Obtener miembros correspondientes a esta fecha
                for member_row in member_rows:
                    if member_row['log_date'] == row['log_date']:
                        player = DonationLogMember(
                            id=member_row['player_id'],
                            donationsLog=member_row['player_donations'],
                            requestsLog=member_row['player_requests']
                        )
                        donation_log.add_member(player)

            return donation_logs

        except Exception as ex:
            raise ex
        finally:
            self.db.close_connection(connection)




    
    
    
    
    
