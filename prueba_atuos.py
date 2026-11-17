from conexion import conectar
from clase_autos import Auto
from administracion_autos import agregar_auto, listar_autos, buscar_autos, modificar_auto, eliminar_auto, validar_auto
from archivos_txt import crear_respaldo, leer_respaldo, comparar_respaldo

# Crea un auto de prueba con datos ficticios
auto_prueba = Auto(
    None,
    "Toyota",
    "Corolla",
    2023,
    25000000,
    0,
    "2.0",
    "170 CV",
    "200 Nm",
    "Nafta",
    "Automatica",
    "Delantera",
    "Blanco"
)

# Establece la conexión con la base de datos
conexion_db = conectar()

# Intenta guardar el auto de prueba
# resultado = agregar_auto(auto_prueba, conexion_db)

# if resultado:
#     print("Auto guardado correctamente")
# else:
#     print("No se pudo guardar el auto")

# Trae los autos registrados en la base de datos
# autos = listar_autos(conexion_db)

# for auto in autos:
#     print(auto)

# Prueba la busqueda de autos por texto
# resultados = buscar_autos(conexion_db, "toyota")

# for auto in resultados:
#     print(auto)

# Prueba la modificacion de los autos
# Datos actualizados del auto
# auto_modificado = Auto(
#     None,
#     "Toyota1",
#     "Corolla",
#     2025,
#     27000000,
#     1500,
#     "2.0",
#     "170 CV",
#     "200 Nm",
#     "Nafta",
#     "Automatica",
#     "Delantera",
#     "Gris",
#     "Reservado"
# )

# # Modifica los datos del auto seleccionado
# resultado = modificar_auto(1, auto_modificado, conexion_db)

# if resultado:
#     print("Auto modificado correctamente")
# else:
#      print("No se pudo modificar el auto")

# resultados = buscar_autos(conexion_db, "toyota")

# for auto in resultados:
#     print(auto)

# Elimina el auto seleccionado
# resultado = eliminar_auto(1, conexion_db)

# if resultado:
#     print("Auto eliminado correctamente")
# else:
#     print("No se pudo eliminar el auto")

# resultados = buscar_autos(conexion_db, "toyota")

# for auto in resultados:
#     print(auto)

# Prueba las validaciones de texto

# from validaciones import validar_marca

# print(validar_marca("Toyota"))
# print(validar_marca(""))
# print(validar_marca("   "))

# from validaciones import validar_modelo

# print(validar_modelo("Corolla"))
# print(validar_modelo(""))
# print(validar_modelo("   "))

# from validaciones import validar_anio

# print(validar_anio("2026"))
# print(validar_anio("abc"))
# print(validar_anio("1890"))
# print(validar_anio("2027"))
# print(validar_anio("20.25"))

# from validaciones import validar_precio

# print(validar_precio("25000000"))
# print(validar_precio("25000000.50"))
# print(validar_precio("mucho"))
# print(validar_precio("-500"))
# print(validar_precio("0"))

# from validaciones import validar_kilometraje

# print(validar_kilometraje("0"))
# print(validar_kilometraje("25000"))
# print(validar_kilometraje("-500"))
# print(validar_kilometraje("muchos"))
# print(validar_kilometraje("25000.5"))

# from validaciones import validar_estado

# print(validar_estado("Disponible"))
# print(validar_estado("reservado"))
# print(validar_estado("VENDIDO"))
# print(validar_estado("En espera"))
# print(validar_estado(""))

# Prueba la funcion validar_auto la cual confirma que todos los datos son validos
# auto_prueba = Auto(
#     None,
#     "Toyota",
#     "Corolla",
#     2025,
#     27000000,
#     1500,
#     "2.0",
#     "170 CV",
#     "200 Nm",
#     "Nafta",
#     "Automatica",
#     "Delantera",
#     "Gris",
#     "Disponible"
# )

# print(validar_auto(auto_prueba))

# Prueba la creasion de respaldos de la db
#print(crear_respaldo(conexion_db))

# Prueba leer el respaldo
# autos_respaldo = leer_respaldo()

# for auto in autos_respaldo:
#     print(auto)

#Prueba el comparar respaldo
#print(comparar_respaldo(conexion_db))