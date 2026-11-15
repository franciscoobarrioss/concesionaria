
class Auto:
    def __init__(self, matricula, marca, modelo, anio, precio, kilometraje, motor, potencia, torque, combustible, transmision, traccion, color, estado="Disponible"):

        # La matricula puede no estar asignada si el auto es 0 km
        # En ese caso, se utilizara none hasta que se le asigne una
        self.matricula = matricula

        # Datos generales del auto
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.precio = precio
        self.kilometraje = kilometraje
        self.color = color

        # Caracteristicas tecnicas del auto
        self.motor = motor
        self.potencia = potencia
        self.torque = torque
        self.combustible = combustible
        self.transmision = transmision
        self.traccion = traccion

        # Estado comercial del auto(Disponible, Reservado, Vendido)
        self.estado = estado

