import re


def obtener_numero(valor):
    """Extrae un valor numerico y normaliza potencia a CV y torque a Nm"""

    if valor is None:
        return None

    try:
        return float(valor)

    except (TypeError, ValueError):

        texto = str(valor).strip().upper().replace(",", ".")

        # Busca el primer numero, incluyendo valores negativos y decimales
        coincidencia = re.search(r"-?\d+(?:\.\d+)?", texto)

        if not coincidencia:
            return None

        numero = float(coincidencia.group())

        # Convierte HP a CV para comparar unidades equivalentes
        if "HP" in texto and "CV" not in texto:
            numero *= 1.01387

        # Convierte kgm a Nm para comparar unidades equivalentes
        if "KGM" in texto:
            numero *= 9.80665

        return numero


def analizar_diferencia(nombre, valor_1, valor_2, unidad, menor_es_mejor=False,
                         nombre_auto_1=None, nombre_auto_2=None):
    """Compara dos valores e identifica cual auto tiene ventaja"""

    numero_1 = obtener_numero(valor_1)
    numero_2 = obtener_numero(valor_2)

    if numero_1 is None or numero_2 is None:

        if nombre_auto_1 and nombre_auto_2:
            return f"{nombre}: Datos insuficientes para comparar"

        return f"No se pudo comparar {nombre} por falta de datos numericos"

    diferencia = abs(numero_1 - numero_2)

    if diferencia == 0:

        if nombre_auto_1 and nombre_auto_2:
            return f"{nombre}: Ambos autos tienen el mismo valor"

        return f"Ambos autos tienen el mismo valor de {nombre}"

    if menor_es_mejor:
        ganador = 1 if numero_1 < numero_2 else 2
    else:
        ganador = 1 if numero_1 > numero_2 else 2

    # Formato utilizado en la comparacion grafica
    if nombre_auto_1 and nombre_auto_2:

        nombre_ganador = nombre_auto_1 if ganador == 1 else nombre_auto_2

        if unidad == "$":
            diferencia_formateada = f"${diferencia:,.2f}"
        else:
            diferencia_formateada = f"{diferencia:,.2f} {unidad}"

        return (
            f"{nombre}: Diferencia de {diferencia_formateada} "
            f"- Destaca {nombre_ganador}"
        )

    # Formato utilizado en las pruebas individuales
    return (
        f"El Auto {ganador} tiene ventaja en {nombre} "
        f"por {diferencia:.2f} {unidad}"
    )
