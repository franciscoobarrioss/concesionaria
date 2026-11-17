from administracion_autos import listar_autos

def crear_respaldo(conexion_db):
    """Guarda los autos registrados en MySQL dentro de un archivo TXT"""

    autos = listar_autos(conexion_db)

    try:
        with open("respaldo.txt", "w", encoding="utf-8") as archivo:

            for auto in autos:
                datos = [str(dato) for dato in auto]
                archivo.write("|".join(datos) + "\n")

        print("Respaldo creado correctamente")
        return True

    except OSError as error:
        # Captura errores relacionados con la creacion, escritura o acceso al archivo
        print("Error al crear el respaldo:", error)
        return False

def leer_respaldo():
    """Lee los datos guardados en el archivo TXT"""

    try:
        with open("respaldo.txt", "r", encoding="utf-8") as archivo:
            autos = archivo.readlines()

        return autos

    except FileNotFoundError:
        # Captura el error que ocurre cuando el archivo TXT no existe en la ubicacion indicada
        print("No se encontro el archivo de respaldo")
        return []

def comparar_respaldo(conexion_db):
    """Compara los datos de MySQL con los del archivo TXT"""

    autos_db = listar_autos(conexion_db)
    autos_txt = leer_respaldo()

    # Convierte los registros de MySQL y del TXT a tuplas de texto para poder compararlos
    datos_db = [tuple(str(dato) for dato in auto) for auto in autos_db]
    datos_txt = [tuple(linea.strip().split("|")) for linea in autos_txt]

    if datos_db == datos_txt:
        print("El respaldo coincide con la base de datos")
        return True

    print("El respaldo presenta diferencias con la base de datos")
    return False