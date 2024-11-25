try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.select import Select
    from bs4 import BeautifulSoup
    from datetime import datetime, timedelta
    import os
    import time
    from src import data_base
    from src import send_mail
    import pandas as pd
    import re
except Exception as e:
    print(f"Error al importar las librerias en main, {e}")

def login():
    max_retries = 2
    retries = 0
    while retries < max_retries:
        try:
            global driver
            # Inicializar el navegador
            chrome_options = Options()
            chrome_options.binary_location = "/usr/bin/google-chrome"
            # chrome_options.add_argument("--headless") # visualizar el navegador
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(data_base.get_url())

            # Iniciar sesión
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(data_base.get_user())
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(data_base.get_password())

            message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Login"))).click()
            print(message)

            time.sleep(5)
            break

        except Exception as e:
            retries += 1
            print("Ocurrio un error al iniciar sesion, ", e)
            time.sleep(3)
            if retries == max_retries:
                data_base.log_to_db(2, "ERROR", f"Ocurrio un error al iniciar sesión, {e}", endpoint='fallido', status_code=500)
                send_mail.send_error_mail(f"Ocurrio un error al inciar sesión, {e}")
                raise
        finally:
            if retries == max_retries:
                driver.quit()
    
def scroll_down():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def scraple_data():
    max_retries = 5
    retries = 0
    login()

    while retries < max_retries:
        try:
            today = datetime.today().date()
            start_date = today
            end_date = today

            print(f"Procesando datos desde {start_date} hasta {end_date}")
            driver.get(data_base.get_url_home())
            rows = []
            headers = []
            max_columns = 0

            # Convertir las fechas a string
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')

            # Navegar al sitio
            driver.get(data_base.get_url_home())

            # Acciones para la iteración del scraping
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dt_inventory_start"))).clear()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dt_inventory_start"))).send_keys(start_date_str)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dt_inventory_end"))).clear()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dt_inventory_end"))).send_keys(end_date_str)

            # Selección de otros elementos en la interfaz
            Select(WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'nm_report')))).select_by_index(5)
            Select(WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'gu_warehouse')))).select_by_index(0)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchInventory"))).click()

            # Esperar a que los datos carguen
            WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.ID, 'tblAgedInventory')))
            print(f"Datos cargados correctamente para el rango {start_date_str} - {end_date_str}")

            scroll_down()

            # Extracción de datos y generación del CSV
            page_content = driver.page_source
            soup = BeautifulSoup(page_content, 'html.parser')
            table = soup.find(id='tblAgedInventory')

            if not table:
                print("No se encontró la tabla en la página.")
                raise Exception("Tabla no encontrada")

            for j, row in enumerate(table.find_all('tr')):
                cells = row.find_all(['td', 'th'])
                cell_values = [cell.get_text(strip=True) for cell in cells]

                # Cabecera
                if j == 0:
                    headers = cell_values
                    max_columns = len(headers)
                else:
                    # Ignorar filas no deseadas
                    if len(cell_values) == 5 and cell_values == ["PRODUCT", "TOTAL WEIGHT", "AVG WEIGHT", "BUNCHES", "STEMS"]:
                        continue
                    rows.append(cell_values)
                    max_columns = max(max_columns, len(cell_values))

            # Agregar columna de fecha a cada fila
            for row in rows:
                row.append(start_date_str)  # Fecha inicial como nueva columna

            # Completar filas para alinear con el máximo de columnas
            headers.append("DATE")
            for row in rows:
                row.extend([None] * (max_columns - len(row)))

            # Crear DataFrame y guardar datos
            df = pd.DataFrame(rows, columns=headers)
            print(df.head())
            file_path = os.path.join(os.path.dirname(__file__), 'unosof_data.csv')
            csv_filename = file_path
            df.to_csv(csv_filename, index=False)
            print(f"Datos del rango {start_date_str} - {end_date_str} guardados correctamente en '{csv_filename}'.")

            break

        except Exception as e:
            print(f"Ocurrió un error al realizar el webscraping: {e}")
            retries += 1
            time.sleep(5)

            if retries == max_retries:
                print("Límite máximo de intentos alcanzado. Finalizando.")
                break


def clean_value(value):
    try:
        value = re.sub(r'[^\d.]', '', value.replace(' ', '').replace(',', '.'))
        if value.count('.') > 1:
            parts = value.split('.')
            value = ''.join(parts[:-1]) + '.' + parts[-1]
        return float(value)
    except ValueError:
        return 0.0