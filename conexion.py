import pymysql


def conectar():
    # Conexion inicial al servidor MySQL
    conexion = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        port=3306,
        charset="utf8mb4",# utf8mb4 permite manejar tildes, la letra ñ y otros caracteres especiales
        autocommit=True
    )

    # Crea la base de datos si todavia no existe
    with conexion.cursor() as cursor:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS concesionaria"
        )

    # Selecciona la base de datos del proyecto
    conexion.select_db("concesionaria")

    # Crea la tabla de autos si todavia no existe
    with conexion.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS autos (
                id_auto INT AUTO_INCREMENT PRIMARY KEY,
                matricula VARCHAR(20) UNIQUE,
                marca VARCHAR(50) NOT NULL,
                modelo VARCHAR(60) NOT NULL,
                anio INT NOT NULL,
                precio DECIMAL(15, 2) NOT NULL,
                kilometraje INT NOT NULL,
                motor VARCHAR(50),
                potencia VARCHAR(30),
                torque VARCHAR(30),
                combustible VARCHAR(30),
                transmision VARCHAR(30),
                traccion VARCHAR(30),
                color VARCHAR(30)
            )
        """)
    
    return conexion


#Prueba para ver si la DB fue conectada correctamente
conexion = None

try:
    conexion = conectar()
    print("Conexion y base de datos correctas.")

except Exception as error:
    print("Error al conectar:", error)

finally:
    if conexion is not None:
        conexion.close()