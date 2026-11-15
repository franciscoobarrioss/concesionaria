from conexion import conectar
from clase_autos import Auto
from administracion_autos import agregar_auto, listar_autos, buscar_autos, modificar_auto, eliminar_auto

# Crea un auto de prueba con datos ficticios
auto_prueba = Auto(
    None,
    "Toyota",
    "Corolla",
    2025,
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
resultados = buscar_autos(conexion_db, "toyota")

for auto in resultados:
    print(auto)

# Prueba la modificacion de los autos
# Datos actualizados del auto
# auto_modificado = Auto(
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
#     "Reservado"
# )

# # Modifica los datos del auto seleccionado
# resultado = modificar_auto(1, auto_modificado, conexion_db)

# if resultado:
#     print("Auto modificado correctamente")
# else:
#     print("No se pudo modificar el auto")

# resultados = buscar_autos(conexion_db, "toyota")

# for auto in resultados:
#     print(auto)

# Elimina el auto seleccionado
resultado = eliminar_auto(1, conexion_db)

if resultado:
    print("Auto eliminado correctamente")
else:
    print("No se pudo eliminar el auto")

resultados = buscar_autos(conexion_db, "toyota")

for auto in resultados:
    print(auto)