from apscheduler.schedulers.background import BackgroundScheduler
from data.base_datos import eliminar_prestamos_vencidos

def iniciar_tareas_automaticas():
    scheduler = BackgroundScheduler()
    scheduler.add_job(eliminar_prestamos_vencidos, 'interval', hours=24)
    scheduler.start()

from ui.ventana_principal import iniciar

if __name__ == "__main__":
    iniciar_tareas_automaticas()
    iniciar()  # tu función que lanza Tkinter
