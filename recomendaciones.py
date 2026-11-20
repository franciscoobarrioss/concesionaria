import os
import json
from dotenv import load_dotenv
from google import genai
from administracion_autos import obtener_auto

# La clave API se obtiene desde el archivo .env para evitar exponerla en el codigo
def obtener_clave_api():
    """Obtiene la clave de acceso a Gemini desde el archivo .env"""

    load_dotenv()
    return os.getenv("GEMINI_API_KEY")

def crear_cliente():
    """Crea el cliente para comunicarse con Gemini"""

    clave = obtener_clave_api()

    if not clave:
        return None

    cliente = genai.Client(api_key=clave)
    return cliente

# Configuracion de la conexion con Gemini
# Se utiliza el modelo gemini-3.5-flash-lite para generar las respuestas

# if __name__ == "__main__":
#     cliente = crear_cliente()

#     if cliente:
#         respuesta = cliente.models.generate_content(
#             model="gemini-3.5-flash-lite",
#             contents="Responde solamente: Conexion exitosa"
#         )

#         print(respuesta.text)
#     else:
#         print("No se encontro la clave API")


def generar_recomendacion(autos, preferencias):
    """Recomienda el auto mas adecuado segun el inventario y las preferencias"""

    cliente = crear_cliente()

    if not cliente:
        return "No se pudo establecer la conexion con Gemini"

    # Organiza los datos de los autos para enviarlos a Gemini
    inventario = []

    for auto in autos:
        datos_auto = f"""
        ID: {auto[0]}
        Marca: {auto[2]}
        Modelo: {auto[3]}
        Año: {auto[4]}
        Precio: ${auto[5]}
        Kilometraje: {auto[6]} km
        Motor: {auto[7]}
        Potencia: {auto[8]}
        Torque: {auto[9]}
        Combustible: {auto[10]}
        Transmision: {auto[11]}
        Traccion: {auto[12]}
        Color: {auto[13]}
        Estado: {auto[14]}
        """

        inventario.append(datos_auto)

    # Convierte el inventario en un texto organizado
    inventario_texto = "\n".join(inventario)

    
    prompt = f"""
    Actua como un asesor comercial especializado en autos de una concesionaria.

    Tu objetivo es analizar las preferencias del cliente y recomendar
    el auto que mejor se adapte a sus necesidades dentro del inventario.

    INVENTARIO DE AUTOS:
    {inventario_texto}

    PREFERENCIAS DEL CLIENTE:
    Uso principal: {preferencias["uso"]}
    Presupuesto: {preferencias["presupuesto"]}
    Caracteristicas prioritarias: {preferencias["prioridades"]}
    Transmision preferida: {preferencias["transmision"]}

    CRITERIOS DE ANALISIS:

    1. Evalua cada auto considerando el conjunto de preferencias.
    2. Da especial importancia al presupuesto y al uso principal.
    3. Considera las caracteristicas prioritarias y la transmision.
    4. No elijas un auto solamente porque cumple una preferencia.
    5. No consideres que un auto es adecuado para uso familiar,
       deportivo o de trabajo si no existen datos suficientes para justificarlo.
    6. Si un auto supera el presupuesto, indicarlo claramente.
    7. Los autos reservados pueden recomendarse, pero debes indicar
       que su estado es Reservado.
    8. No recomiendes autos vendidos ni autos que no esten en el inventario.
    9. No inventes precios, caracteristicas, consumos ni datos tecnicos.
    10. Si falta informacion, reconoce que no es posible evaluar ese aspecto.
    11. Tu objetivo es encontrar la mejor opcion disponible para el cliente,
    no buscar una coincidencia perfecta.
    12. Evalua las preferencias en conjunto. No descartes automaticamente
        un auto por incumplir una sola condicion.
    13. Si el auto mas adecuado supera el presupuesto, analiza cuanto
        lo supera y si sigue siendo una alternativa razonable.
    14. Si ningun auto cumple todas las preferencias, selecciona el que
        presente la mejor coincidencia general y explica sus desventajas.
    15. La falta de informacion sobre una caracteristica no significa
        que el auto no la cumpla. Indica que no hay datos suficientes
        para evaluarla.
    16. Utiliza null solamente cuando no exista ninguna opcion que
        razonablemente pueda recomendarse al cliente.
    17. Utiliza siempre la palabra "auto" y nunca "vehiculo".
    18. No califiques caracteristicas como modernas, confiables,
        eficientes o adecuadas si no existen datos suficientes
        para justificarlo.
    19. No descartes autos basandote unicamente en su categoria,
        marca o modelo. Evalua solamente las caracteristicas
        disponibles y las preferencias del cliente.
    20. No afirmes que dos autos son identicos. Compara
        unicamente sus datos registrados en el inventario.
    21. Evita repetir informacion entre el analisis, las ventajas
        y los aspectos a considerar.
    22. No confundas el estado "Disponible" con una entrega inmediata
    y no atribuyas caracteristicas que no esten registradas
    en el inventario.

    FORMATO DE RESPUESTA:

    Devuelve exclusivamente un objeto JSON valido, sin bloques de codigo,
    introducciones ni texto adicional.

    Utiliza exactamente esta estructura:

    {{
        "auto_recomendado_id": null,
        "nivel_ajuste": "Alto, Medio, Bajo o Ninguno",
        "motivo_sin_recomendacion": "",
        "analisis": "",
        "ventajas": [],
        "aspectos_a_considerar": [],
        "alternativas": [
            {{
                "id": 0,
                "motivo": ""
            }}
        ]
    }}

    REGLAS PARA COMPLETAR LA RESPUESTA:

    - auto_recomendado_id debe contener el ID real de MySQL del auto elegido.
    - Utiliza null solamente cuando no exista ninguna opcion
        que pueda recomendarse razonablemente.
    - Si existe una opcion cercana, devuelve su ID real
        y asigna el nivel de ajuste "Bajo".
    - No utilices null solamente porque el auto supera
        el presupuesto o no cumple una preferencia secundaria.
    - nivel_ajuste debe representar la coincidencia general con las preferencias.
    - motivo_sin_recomendacion se utiliza solamente cuando no se recomienda
      ningun auto.
    - analisis debe contener una explicacion clara y profesional de la decision.
    - ventajas y aspectos_a_considerar deben ser listas de textos breves.
    - alternativas debe contener otros autos del inventario que puedan interesar.
    - Cada alternativa debe incluir su ID real y una explicacion breve.
    - No incluyas como alternativa el mismo auto recomendado.
    - Si no hay alternativas, devuelve una lista vacia.
    - No agregues caracteristicas que no aparezcan en el inventario.
    - Evita repeticiones, exageraciones comerciales y expresiones innecesarias.
    - Escribe en español natural, claro y profesional.
    """

    try:
        respuesta = cliente.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return respuesta.text

    except Exception as error:
        print(f"Error al generar la recomendacion: {error}")
        return None


# if __name__ == "__main__":

#     auto1 = """
#     Marca: Toyota
#     Modelo: Corolla
#     Año: 2022
#     Precio: 25000000
#     Kilometraje: 30000
#     Combustible: Nafta
#     Transmision: Automatica
#     """

#     auto2 = """
#     Marca: Volkswagen
#     Modelo: Vento
#     Año: 2021
#     Precio: 22000000
#     Kilometraje: 45000
#     Combustible: Nafta
#     Transmision: Manual
#     """

#     preferencias = """
#     Presupuesto maximo: 26000000
#     Uso: Familiar y urbano
#     Prioridades: Comodidad, consumo y confiabilidad
#     """

#     recomendacion = generar_recomendacion(auto1, auto2, preferencias)

#     print(recomendacion)

def interpretar_respuesta(respuesta):
    """Interpreta la respuesta JSON generada por Gemini"""

    try:
        resultado = json.loads(respuesta)

        if not isinstance(resultado, dict):
            print("La respuesta de Gemini no tiene el formato esperado")
            return None

        return resultado

    except (json.JSONDecodeError, TypeError) as error:
        print("Error al interpretar la respuesta de Gemini:", error)
        return None

def validar_id_recomendado(resultado, autos):
    """Comprueba que el ID recomendado exista en el inventario"""

    if not isinstance(resultado, dict):
        return None

    id_recomendado = resultado.get("auto_recomendado_id")

    if id_recomendado is None:
        return None

    try:
        id_recomendado = int(id_recomendado)

    except (TypeError, ValueError):
        print("El ID recomendado no es valido")
        return None

    # Comprueba que el ID pertenezca a un auto del inventario
    for auto in autos:
        if auto[0] == id_recomendado and auto[14] != "Vendido":
            return id_recomendado

    print("El ID recomendado no existe en el inventario")
    return None

def procesar_recomendacion(autos, preferencias, conexion_db):
    """Procesa la recomendacion y recupera los datos del auto elegido"""

    # Genera la respuesta de Gemini
    respuesta = generar_recomendacion(autos, preferencias)

    # Interpreta la respuesta JSON
    resultado = interpretar_respuesta(respuesta)

    if resultado is None:
        return None

    # Comprueba que el ID recomendado exista
    id_recomendado = validar_id_recomendado(resultado, autos)

    if id_recomendado is None:
        return None

    # Recupera los datos completos del auto desde MySQL
    auto_recomendado = obtener_auto(id_recomendado, conexion_db)

    if auto_recomendado is None:
        print("No se pudo recuperar el auto recomendado")
        return None

    return {
        "resultado": resultado,
        "auto": auto_recomendado
    }