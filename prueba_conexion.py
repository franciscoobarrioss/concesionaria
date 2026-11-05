from conexion import conectar

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