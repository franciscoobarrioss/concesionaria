def validar_marca(marca):
    """Comprueba que la marca del auto no este vacia"""

    if not marca.strip():
        return False

    return True

def validar_modelo(modelo):
    """Comprueba que el modelo del auto no este vacio"""

    if not modelo.strip():
        return False

    return True


def validar_anio(anio):
    """Comprueba que el año sea numerico y razonable"""

    anio = str(anio)

    if not anio.isdigit():
        return False

    anio = int(anio)

    if anio < 1900 or anio > 2026:
        return False

    return True


def validar_precio(precio):
    """Comprueba que el precio sea numerico y mayor que cero"""

    try:
        precio = float(precio)
    except ValueError:
        return False

    if precio <= 0:
        return False

    return True


def validar_kilometraje(kilometraje):
    """Comprueba que el kilometraje sea un numero entero y no negativo"""

    kilometraje = str(kilometraje)

    if not kilometraje.isdigit():
        return False

    kilometraje = int(kilometraje)

    if kilometraje < 0:
        return False

    return True


def validar_estado(estado):
    """Comprueba que el estado comercial sea valido"""

    estados_validos = ["Disponible", "Reservado", "Vendido"]

    if estado.strip().capitalize() not in estados_validos:
        return False

    return True
