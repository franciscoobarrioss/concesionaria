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
    #Agrupa los atributos del auto en el mismo orden que las columnas del INSERT
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