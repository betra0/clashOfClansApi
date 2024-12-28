from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from config import Config
from services.ClanManager import memberClans
import time
import logging

# Crear una instancia del scheduler
scheduler = BackgroundScheduler()
scheduler.start()
logging.basicConfig(level=logging.INFO)
isError=False

def ejecutar_en_evento():
    print("¡Evento ejecutado en el tiempo programado!")

def refreshInfoClan():
    global isError
    errorId = "ErrorRefreshInfoClan"  # ID único para identificar el evento
    try:
        refreshAllInfoClan()
        logging.info("Información del clan actualizada exitosamente.")
        isError=False
        
    except Exception as e:
        logging.error(f"\n ocurrio Un error al ejecutar la funcion Programada 'refreshInfoClan' : {e}\n")
        if not scheduler.get_job(errorId) and not isError:
            isError=True
            logging.error(f"\n Preparandose para reintentar la ejecución de la función 'refreshInfoClan' en 30 segundos.\n")
            scheduler.add_job(
                refreshInfoClan,  # Función a ejecutar
                trigger=DateTrigger(run_date=(datetime.now() + timedelta(seconds=60))), 
                id=errorId 
            )
        logging.error(f"\n Error al ejecutar el Actualizar la Info del clan: {e}\n")
     

    # Verificar si el job ya existe
    """ existing_job = scheduler.get_job(job_id)
    if existing_job:
        print("El evento ya está programado. No se reprogramará.")
    else:
        print(f"Programando tarea para ejecutarse el: {new_time}")
        # Programar la función con un ID específico
        scheduler.add_job(
            ejecutar_en_evento,  # Función a ejecutar
            trigger=DateTrigger(run_date=new_time),  # Momento específico
            id=job_id  # ID único para evitar duplicados
        ) """

def ejecutar_evento_recurrente():
    logging.info("¡Evento ejecutado en el tiempo programado!")

def refresh_Membersclans():
    memberClans.get_members()

def refreshAllInfoClan():
    memberClans.refreshAllClanInfo()


if __name__ == "__main__":
    # Simular un cambio de valor
    """ new_event_time = datetime.now() + timedelta(seconds=30) """  # Evento en 30 segundos
    """ actualizar_event_time(new_event_time) """

    # Programar un evento recurrente cada hora
    scheduler.add_job(
        refreshInfoClan,  # Función a ejecutar
        trigger=IntervalTrigger(minutes=5),  # Intervalo de tiempo
        id="refreshInfoClanPeriodic"  # ID único para evitar duplicados
    )

    # Mantener el scheduler en ejecución
    try:
        while True:

            logging.info("¡Hola Mundo!")

            time.sleep(60*60*3)  # Pausa para evitar un uso excesivo de CPU
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
