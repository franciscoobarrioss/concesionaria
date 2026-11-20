
from conexion import conectar
from clase_autos import Auto
from administracion_autos import agregar_auto


# Autos de ejemplo para probar el sistema
AUTOS_DEMO = [
    Auto("AB123CD", "Toyota", "Corolla XEI", 2022, 28500000, 35000, "2.0", "170 CV", "203 Nm", "Nafta", "Automatica", "Delantera", "Blanco"),
    Auto("AC456EF", "Volkswagen", "Vento GLI", 2021, 32000000, 42000, "2.0 Turbo", "230 CV", "350 Nm", "Nafta", "Automatica", "Delantera", "Negro"),
    Auto("AD789GH", "Ford", "Ranger XLT", 2023, 45000000, 28000, "3.2 TDCi", "200 CV", "470 Nm", "Diesel", "Automatica", "4x4", "Gris"),
    Auto("AE234JK", "Chevrolet", "Onix Premier", 2022, 19500000, 30000, "1.0 Turbo", "116 CV", "160 Nm", "Nafta", "Automatica", "Delantera", "Rojo"),
    Auto("AF567LM", "Honda", "Civic Touring", 2020, 27000000, 55000, "1.5 Turbo", "173 CV", "220 Nm", "Nafta", "CVT", "Delantera", "Azul", "Reservado"),
    Auto("AG890NP", "Jeep", "Compass Limited", 2023, 42000000, 18000, "1.3 Turbo", "175 CV", "270 Nm", "Nafta", "Automatica", "4x2", "Gris"),
    Auto("AH123QR", "Renault", "Sandero RS", 2019, 16500000, 65000, "2.0", "145 CV", "198 Nm", "Nafta", "Manual", "Delantera", "Negro"),
    Auto("AJ456ST", "BMW", "330i Sportline", 2022, 58000000, 22000, "2.0 Turbo", "258 CV", "400 Nm", "Nafta", "Automatica", "Trasera", "Blanco"),
    Auto("AK789UV", "Fiat", "Cronos Precision", 2024, 23500000, 12000, "1.3", "99 CV", "127 Nm", "Nafta", "Manual", "Delantera", "Gris", "Vendido"),
    Auto("AL234WX", "Toyota", "Hilux SRX", 2021, 48000000, 48000, "2.8 TDI", "204 CV", "500 Nm", "Diesel", "Automatica", "4x4", "Blanco"),
    Auto("AM567YZ", "Peugeot", "208 GT", 2023, 26000000, 15000, "1.2 Turbo", "130 CV", "230 Nm", "Nafta", "Automatica", "Delantera", "Rojo"),
    Auto("AN890AB", "Audi", "A3 Sedan", 2022, 49000000, 25000, "1.4 TFSI", "150 CV", "250 Nm", "Nafta", "Automatica", "Delantera", "Negro", "Reservado"),
    Auto("AP123CD", "Mercedes-Benz", "C200", 2021, 62000000, 32000, "1.5 Turbo", "204 CV", "300 Nm", "Nafta", "Automatica", "Trasera", "Gris"),
    Auto("AQ456EF", "Nissan", "Sentra Advance", 2023, 29000000, 14000, "2.0", "145 CV", "197 Nm", "Nafta", "CVT", "Delantera", "Azul"),
    Auto("AR789GH", "Volkswagen", "Amarok V6", 2020, 46000000, 60000, "3.0 V6 TDI", "258 CV", "580 Nm", "Diesel", "Automatica", "4x4", "Negro"),
    Auto("AS234JK", "Ford", "Mustang GT", 2019, 75000000, 38000, "5.0 V8", "450 CV", "556 Nm", "Nafta", "Manual", "Trasera", "Rojo"),
    Auto("AT567LM", "Chevrolet", "Cruze LTZ", 2021, 22500000, 45000, "1.4 Turbo", "153 CV", "245 Nm", "Nafta", "Automatica", "Delantera", "Blanco", "Vendido"),
    Auto("AU890NP", "Honda", "HR-V EXL", 2024, 39000000, 8000, "1.5", "121 CV", "145 Nm", "Nafta", "CVT", "Delantera", "Gris"),
    Auto("AV123QR", "Fiat", "Pulse Impetus", 2023, 27500000, 16000, "1.0 Turbo", "120 CV", "200 Nm", "Nafta", "CVT", "Delantera", "Rojo"),
    Auto("AW456ST", "Hyundai", "Tucson Limited", 2022, 43000000, 27000, "2.0", "154 CV", "192 Nm", "Nafta", "Automatica", "4x2", "Blanco", "Reservado")
]


def cargar_autos():
    """Carga autos de ejemplo en la base de datos sin duplicar matriculas"""

    conexion_db = conectar()

    if conexion_db is None:
        print("No se pudo conectar con la base de datos")
        return

    agregados = 0
    existentes = 0

    try:
        with conexion_db.cursor() as cursor:

            for auto in AUTOS_DEMO:
                # Verificar si la matricula ya existe
                sql = "SELECT id_auto FROM autos WHERE matricula = %s"
                cursor.execute(sql, (auto.matricula,))
                resultado = cursor.fetchone()

                if resultado:
                    existentes += 1
                    continue

                # Agregar el auto si no existe
                if agregar_auto(auto, conexion_db):
                    agregados += 1
                else:
                    print(f"No se pudo agregar: {auto.marca} {auto.modelo}")

        print("\nCarga finalizada")
        print(f"Autos agregados: {agregados}")
        print(f"Autos que ya existian: {existentes}")

    except Exception as error:
        print(f"Error durante la carga: {error}")

    finally:
        conexion_db.close()


if __name__ == "__main__":
    cargar_autos()
