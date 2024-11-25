try:
    from fastapi import FastAPI
    from hypercorn.config import Config
    from hypercorn.asyncio import serve
    from src import main, manage_data
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    import time
    import asyncio
except Exception as e:
    print(f"Ocurrio un error al importar las librerias en la app, {e}")

app = FastAPI(
    title="API WebScraping de la página web UNOSOF de Starflowers CIA. Ltda.",
    description="La API obtiene data de View Inventory Totals",
    version="1.0.0"
)

@app.get("/", description="Endpoint raiz")
def default_endpoint():
    return {" message ": " En ejecucion la API WebScraping de UNOSOF "}

@app.get("/get-data-unosof", description="Endpoint WebScraping")
def web_scraping_main():
    try:
        main.scraple_data()
        main.driver.quit()
        time.sleep(5)
        manage_data.save()
        return {" message ": " Obteniendo datos "}
    except Exception as e:
        print(f"Ocurrio un error con el Endpoint get-data-UNOSOF, {e}")

def schedule_scraping_tasks():
    try:
        scheduler = BackgroundScheduler()

        # Programar el scraping de ventas todos los días a las 8 PM
        scheduler.add_job(
            web_scraping_main,
            CronTrigger(hour=12, minute=45),
            id='scrape_unosof',
            replace_existing=True
        )

        # Iniciar el scheduler
        scheduler.start()
        print("Scheduler iniciado. Tareas programadas.")
    except Exception as e:
        print(f"Ocurrio un error en el evento programado")

@app.on_event("startup")
def startup_event():
    schedule_scraping_tasks()

# Configurar el servidor
config = Config()
config.bind = ["0.0.0.0:9993"]

# Función asíncrona para ejecutar el servidor
async def run():
    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(run())