import os
from dotenv import load_dotenv
from google import genai

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

def generar_recomendacion(auto1, auto2, preferencias):
    """Genera una recomendacion comparando dos autos segun las preferencias del cliente"""

    cliente = crear_cliente()

    if not cliente:
        return "No se pudo establecer la conexion con Gemini"

    prompt = f"""
    Actua como un asesor especializado en autos de una concesionaria.

    Compara los siguientes autos:

    AUTO 1:
    {auto1}

    AUTO 2:
    {auto2}

    PREFERENCIAS DEL CLIENTE:
    {preferencias}

    Analiza las caracteristicas de ambos autos y recomienda
    cual se adapta mejor a las necesidades del cliente.

    Explica las ventajas y desventajas de cada uno y justifica
    tu recomendacion utilizando solamente los datos proporcionados.
    Si falta informacion, indicarlo sin inventar datos.
    """

    try:
        respuesta = cliente.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return respuesta.text

    except Exception as error:
        print(f"Error al generar la recomendacion: {error}")
        return "No se pudo generar la recomendacion"