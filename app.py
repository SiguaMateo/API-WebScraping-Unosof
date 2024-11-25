try:
    from fastapi import FastAPI
    from hypercorn.config import Config
    from hypercorn.asyncio import serve
    from src import main, manage_data
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
def get_data():
    try:
        main.scraple_data()
        main.driver.quit()
        time.sleep(5)
        manage_data.save()
        return {" message ": " Obteniendo datos "}
    except Exception as e:
        print(f"Ocurrio un error con el Endpoint get-data-UNOSOF, {e}")

# Configurar el servidor
config = Config()
config.bind = ["0.0.0.0:9993"]

# Función asíncrona para ejecutar el servidor
async def run():
    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(run())