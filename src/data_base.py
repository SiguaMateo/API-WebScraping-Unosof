try:
    import pyodbc
    from dotenv import load_dotenv
    import os
except Exception as e:
    print(f"Ocurrio un error al importar las librerias de data_base, {e}")

load_dotenv()

try:
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={os.getenv("DATABASE_SERVER")};'
        f'DATABASE={os.getenv("DATABASE_NAME")};'
        f'UID={os.getenv("DATABASE_USER")};'
        f'PWD={os.getenv("DATABASE_PASSWORD")}'
    )
    cursor = conn.cursor()
    print("Conexion realizada con exito con la Base de Datos")
except Exception as e:
    print(f"Error en la conexion con la base de datos, {e}")

# def create_table_Box():
#     with conn.cursor() as cursor:
#         # Verificar si la tabla existe y eliminarla si es así
#         cursor.execute("""
#             IF EXISTS (SELECT * FROM sysobjects WHERE name='CajasProducidasUnosof_Dev' AND xtype='U')
#             BEGIN
#                 DROP TABLE CajasProducidasUnosof_Dev
#             END
#         """)
#         conn.commit()

#         # Crear una nueva tabla
#         cursor.execute("""
#             CREATE TABLE CajasProducidasUnosof_Dev (
#             id INT PRIMARY KEY IDENTITY(1,1),
#             box_product NVARCHAR(150),
#             box_total_weight NUMERIC(10,2),
#             box_avg_weight NUMERIC(10,2),
#             box_bounches INT,
#             box_stems INT,
#             box_r_date DATE
#             )
#         """)
#         conn.commit()

# create_table_Box()

# def create_table_Logs():
#     with conn.cursor() as cursor:
#         # Verificar si la tabla existe y eliminarla si es así
#         cursor.execute("""
#             IF EXISTS (SELECT * FROM sysobjects WHERE name='Logs_Info' AND xtype='U')
#             BEGIN
#                 DROP TABLE Logs_Info
#             END
#         """)
#         conn.commit()

#         # Crear una nueva tabla
#         cursor.execute("""
#             CREATE TABLE Logs_Info (
#             id INT PRIMARY KEY IDENTITY(1,1),
#             id_group INT NOT NULL,
#             log_time DATETIME DEFAULT GETDATE(),
#             log_level VARCHAR(20),
#             message TEXT,
#             endpoint VARCHAR(255),
#             status_code INT
#             )
#         """)
#         conn.commit()

# create_table_Logs()

def log_to_db(id_group, log_level, message, endpoint=None, status_code=None):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Logs_Info (id_group, log_level, message, endpoint, status_code)
            VALUES (?, ?, ?, ?, ?)
        """, id_group, log_level, message, endpoint, status_code)
        conn.commit()

url_login_query = """SELECT prm_valor
                FROM dbo.Parametros_Sistema
                WHERE id_grupo = 1 AND prm_descripcion = 'url_login'"""

user_query = """SELECT prm_valor
                FROM dbo.Parametros_Sistema
                WHERE id_grupo = 1 AND prm_descripcion = 'user_name'"""

password_query = """SELECT prm_valor
                FROM dbo.Parametros_Sistema
                WHERE id_grupo = 1 AND prm_descripcion = 'password'"""

user_mail_query = """SELECT prm_valor
                FROM dbo.Parametros_Sistema
                WHERE id_grupo = 5 AND prm_descripcion = 'user_mail'"""

password_mail_query = """SELECT prm_valor
                FROM dbo.Parametros_Sistema
                WHERE id_grupo = 5 AND prm_descripcion = 'password_mail'"""

url_home_query = """SELECT prm_valor
                FROM dbo.Parametros_Sistema
                WHERE id_grupo = 1 AND prm_descripcion = 'url_home'"""

insert_query = """INSERT INTO CajasProducidasUnosof_Dev VALUES (?,?,?,?,?,?)"""

def get_url():
    try:
        url = cursor.execute(url_login_query)
        result = cursor.fetchone()
        if result:
            url = result[0]
            print(f"URL obtenida: {url}")
            return url
        else:
            return None, "Error al obtener la url de la base de datos"
    except Exception as e:
        print(f"Ocurrio un error al obtener la url, {e}")

def get_user():
    try:
        user = cursor.execute(user_query)
        result = cursor.fetchone()
        if result:
            user = result[0]
            print(f"Usuario obtenido: {user}")
            return user.encode('utf-8').decode('utf-8')
    except Exception as e:
        print(f"Ocurrio un error al obtener el usuario, {e}")
        
def get_password():
    try:
        password = cursor.execute(password_query)
        result = cursor.fetchone()
        if result:
            password = result[0]
            print(f"Usuario obtenido: {password}")
            return password.encode('utf-8').decode('utf-8')
    except Exception as e:
        print(f"Ocurrio un error al obtener el usuario, {e}")

def get_url_home():
    try:
        home = cursor.execute(url_home_query)
        result = cursor.fetchone()
        if result:
            home = result[0]
            print(f"URL home obtenida: {home}")
            return home.encode('utf-8').decode('utf-8')
    except Exception as e:
        print(f"Ocurrio un error al obtener el usuario, {e}")

def get_user_mail():
    try:
        user_mail = cursor.execute(user_mail_query)
        result = cursor.fetchone()
        if result:
            user_mail = result[0]
            print(f"Usuario de correo obtenido: {user_mail}")
            return user_mail
    except Exception as e:
        print(f"Ocurrio un error al obtener el usuario de correo electronico, {e}")

def get_password_mail():
    try:
        passwd_mail =  cursor.execute(password_mail_query)
        result = cursor.fetchone()
        if result:
            passwd_mail = result[0]
            print(f"Contrasenia del correo obtenido: {passwd_mail}")
            return passwd_mail
    except Exception as e:
        print(f"Ocurrio un error al obtener la contrasenia del correo, {e}")