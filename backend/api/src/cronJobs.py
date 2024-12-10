from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
from config import Config
from services.ClanManager import memberClans

# Crear una instancia del scheduler
scheduler = BackgroundScheduler()
scheduler.start()

def ejecutar_en_evento():
    print("¡Evento ejecutado en el tiempo programado!")

def actualizar_event_time(new_time):
    job_id = "evento_unico"  # ID único para identificar el evento

    # Verificar si el job ya existe
    existing_job = scheduler.get_job(job_id)
    if existing_job:
        print("El evento ya está programado. No se reprogramará.")
    else:
        print(f"Programando tarea para ejecutarse el: {new_time}")
        # Programar la función con un ID específico
        scheduler.add_job(
            ejecutar_en_evento,  # Función a ejecutar
            trigger=DateTrigger(run_date=new_time),  # Momento específico
            id=job_id  # ID único para evitar duplicados
        )
def refresh_clans():
    memberClans.get_members()
    


if __name__ == "__main__":
    # Simular un cambio de valor
    new_event_time = datetime.now() + timedelta(seconds=30)  # Evento en 30 segundos
    actualizar_event_time(new_event_time)

    # Mantener el script vivo en desarrollo
    try:
        while True:
            pass  # Mantiene el script activo
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()