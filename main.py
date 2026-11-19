from conexion import conectar
from interfaz import Aplicacion


if __name__ == "__main__":

    conexion_db = conectar()

    app = Aplicacion(conexion_db)

    app.mainloop()
