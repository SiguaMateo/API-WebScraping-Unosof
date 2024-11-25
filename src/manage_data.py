try:
    import csv
    from src import data_base
    from src import send_mail
except Exception as e:
    print(f"Ocurrio un error al importar las liberias en manage data, {e}")

def save():
    try:
        with open("unosof_data.csv", mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)

            for row in reader:
                print("Ingreso al bucle")
                print(f"Fila leida: {row}")

                data_base.cursor.execute(data_base.insert_query, row)
                print(f"Datos gurdados correctamente")

        data_base.cursor.commit()        

    except Exception as e:
        message = f"Ocurrio un error al guardar los datos en la base de datos, {e}"
        print(message)
        data_base.log_to_db(1, "ERROR", message, endpoint='fallido', status_code=404)
        send_mail.send_error_mail(message)
