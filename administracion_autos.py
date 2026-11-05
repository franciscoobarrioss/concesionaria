import pymysql

def agregar_auto(auto, conexion_db):
    """Agrega un auto a la base de datos con los atributos proporcionados por el usuario"""
    sql = """
        INSERT INTO autos (
            matricula, marca, modelo, anio, precio, kilometraje,
            motor, potencia, torque, combustible, transmision,
            traccion, color
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """
    # Agrupa los atributos del auto en el mismo orden que las columnas del INSERT
    valores = (
        auto.matricula,
        auto.marca,
        auto.modelo,
        auto.anio,
        auto.precio,
        auto.kilometraje,
        auto.motor,
        auto.potencia,
        auto.torque,
        auto.combustible,
        auto.transmision,
        auto.traccion,
        auto.color
    )

    try:
        # Ejecuta la consulta SQL para guardar el auto en la base de datos
        with conexion_db.cursor() as cursor:
            cursor.execute(sql, valores)

        return True
    except pymysql.MySQLError as error:
        print("Error al agregar el auto:", error)
        return False

def listar_autos(conexion_db):
    """Obtiene todos los autos registrados en la base de datos"""
    sql = "SELECT * FROM autos"

    with conexion_db.cursor() as cursor:
        cursor.execute(sql)
        autos = cursor.fetchall()
    # Trae todos los autos encontrados en la base de datos

    return autos

def buscar_autos(conexion_db, busqueda):
    """Busca autos en la base de datos utilizando un texto general"""

     # Prepara la consulta y los valores de busqueda
    sql = "SELECT * FROM autos WHERE 1=1"
    valores = []

    busqueda = f"%{busqueda}%"

    # Busca coincidencias en las caracteristicas de texto del auto
    # LIKE permite buscar coincidencias parciales
    sql += """
        AND (
            matricula LIKE %s OR
            marca LIKE %s OR
            modelo LIKE %s OR
            motor LIKE %s OR
            combustible LIKE %s OR
            transmision LIKE %s OR
            traccion LIKE %s OR
            color LIKE %s
        )
    """
    # Agrega el texto de busqueda para cada columna
    valores.extend([busqueda] * 8)

    try:
        with conexion_db.cursor() as cursor:
            cursor.execute(sql, valores)

            # Recupera todos los autos que coinciden con la busqueda
            autos = cursor.fetchall()

        return autos
    
    except pymysql.MySQLError as error:
        print("Error al buscar autos:", error)
        return []