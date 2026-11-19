import customtkinter as ctk
from tkinter import messagebox
from clase_autos import Auto
from administracion_autos import agregar_auto

# ==================================================
# CLASE PRINCIPAL DE LA APLICACION
# ==================================================

class Aplicacion(ctk.CTk):

    def __init__(self, conexion_db):
        super().__init__()

        # Guarda la conexion con la base de datos
        self.conexion_db = conexion_db

        # Configuracion general de la ventana
        self.title("Concesionaria")
        self.geometry("1000x650")

        # Configuracion visual
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")


        # ==================================================
        # SECCION 1 - TITULO Y SUBTITULO
        # ==================================================

        self.etiqueta_titulo = ctk.CTkLabel(
            self,
            text="Sistema de gestion de autos",
            font=("Arial", 26, "bold")
        )
        self.etiqueta_titulo.pack(pady=30)

        self.etiqueta_subtitulo = ctk.CTkLabel(
            self,
            text="Administracion de inventario y comparacion de autos",
            font=("Arial", 15)
        )
        self.etiqueta_subtitulo.pack(pady=10)


        # ==================================================
        # SECCION 2 - MENU PRINCIPAL
        # ==================================================

        self.frame_menu = ctk.CTkFrame(self)
        self.frame_menu.pack(pady=40, padx=30, fill="x")

        # Boton para administrar autos
        self.boton_autos = ctk.CTkButton(
            self.frame_menu,
            text="Administrar autos",
            width=200,
            height=50,
            command=self.mostrar_autos
        )
        self.boton_autos.pack(pady=15)

        # Boton para comparar autos
        self.boton_comparar = ctk.CTkButton(
            self.frame_menu,
            text="Comparar autos",
            width=200,
            height=50,
            command=self.mostrar_comparacion
        )
        self.boton_comparar.pack(pady=15)

        # Boton para gestionar el respaldo TXT
        self.boton_respaldo = ctk.CTkButton(
            self.frame_menu,
            text="Respaldo TXT",
            width=200,
            height=50,
            command=self.mostrar_respaldo
        )
        self.boton_respaldo.pack(pady=15)


    # ==================================================
    # SECCION 3 - NAVEGACION ENTRE SECCIONES
    # ==================================================

    # Abre la seccion de administracion de autos
    def mostrar_autos(self):
        self.abrir_administracion_autos()

    # Abre la seccion de comparacion de autos
    def mostrar_comparacion(self):
        self.abrir_seccion("Comparacion de autos")

    # Abre la seccion de respaldo TXT
    def mostrar_respaldo(self):
        self.abrir_seccion("Respaldo TXT")


    # ==================================================
    # SECCION 4 - CREACION DE VENTANAS SECUNDARIAS
    # ==================================================

    def abrir_seccion(self, titulo):

        ventana = ctk.CTkToplevel(self)
        ventana.title(titulo)
        ventana.geometry("800x550")

        etiqueta = ctk.CTkLabel(
            ventana,
            text=titulo,
            font=("Arial", 24, "bold")
        )
        etiqueta.pack(pady=30)

    
    # ==================================================
    # SECCION 5 - ADMINISTRACION DE AUTOS
    # ==================================================

    def abrir_administracion_autos(self):
        """Crea el menu principal para administrar los autos"""

        ventana = ctk.CTkToplevel(self)
        ventana.title("Administracion de autos")
        ventana.geometry("850x600")

        # ==================================================
        # SUBSECCION 5.1 - CONTENEDOR PRINCIPAL
        # ==================================================

        frame_principal = ctk.CTkFrame(ventana)
        frame_principal.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        # ==================================================
        # SUBSECCION 5.2 - TITULO Y DESCRIPCION
        # ==================================================

        titulo = ctk.CTkLabel(
            frame_principal,
            text="Administracion de autos",
            font=("Arial", 26, "bold")
        )
        titulo.pack(pady=(30, 5))

        descripcion = ctk.CTkLabel(
            frame_principal,
            text="Selecciona una opcion para continuar",
            font=("Arial", 14)
        )
        descripcion.pack(pady=(5, 30))

        # ==================================================
        # SUBSECCION 5.3 - MENU DE OPCIONES
        # ==================================================

        frame_opciones = ctk.CTkFrame(frame_principal)
        frame_opciones.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=20
        )

        # Configura las columnas del menu
        frame_opciones.grid_columnconfigure((0, 1), weight=1)

        # Boton para registrar un auto
        boton_agregar = ctk.CTkButton(
            frame_opciones,
            text="Agregar auto",
            width=250,
            height=100,
            font=("Arial", 17, "bold"),
            command=self.abrir_formulario_agregar_auto
        )
        boton_agregar.grid(
            row=0,
            column=0,
            padx=20,
            pady=25
        )

        # Boton para buscar un auto
        boton_buscar = ctk.CTkButton(
            frame_opciones,
            text="Buscar auto",
            width=250,
            height=100,
            font=("Arial", 17, "bold"),
            command=lambda: self.abrir_seccion("Buscar auto")
        )
        boton_buscar.grid(
            row=0,
            column=1,
            padx=20,
            pady=25
        )

        # Boton para consultar el inventario completo
        boton_inventario = ctk.CTkButton(
            frame_opciones,
            text="Ver inventario",
            width=250,
            height=100,
            font=("Arial", 17, "bold"),
            command=lambda: self.abrir_seccion("Inventario de autos")
        )
        boton_inventario.grid(
            row=1,
            column=0,
            padx=20,
            pady=25
        )

        # Boton para modificar o eliminar autos
        boton_gestionar = ctk.CTkButton(
            frame_opciones,
            text="Gestionar autos",
            width=250,
            height=100,
            font=("Arial", 17, "bold"),
            command=lambda: self.abrir_seccion("Gestionar autos")
        )
        boton_gestionar.grid(
            row=1,
            column=1,
            padx=20,
            pady=25
        )
    
    # ==================================================
    # SECCION 6 - FORMULARIO PARA AGREGAR AUTOS
    # ==================================================

    def abrir_formulario_agregar_auto(self):
        """Crea el formulario para registrar un auto nuevo"""

        ventana = ctk.CTkToplevel(self)
        ventana.title("Agregar auto")
        ventana.geometry("850x750")

        # Contenedor principal con desplazamiento
        frame_principal = ctk.CTkScrollableFrame(ventana)
        frame_principal.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # ==================================================
        # SUBSECCION 6.1 - TITULO
        # ==================================================

        titulo = ctk.CTkLabel(
            frame_principal,
            text="Registrar nuevo auto",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)

        # ==================================================
        # SUBSECCION 6.2 - CAMPOS DEL FORMULARIO
        # ==================================================

        frame_campos = ctk.CTkFrame(frame_principal)
        frame_campos.pack(fill="x", padx=15, pady=10)

        # Relaciona los atributos de Auto con sus etiquetas
        campos = [
            ("matricula", "Matricula"),
            ("marca", "Marca"),
            ("modelo", "Modelo"),
            ("anio", "Año"),
            ("precio", "Precio"),
            ("kilometraje", "Kilometraje"),
            ("motor", "Motor"),
            ("potencia", "Potencia"),
            ("torque", "Torque"),
            ("combustible", "Combustible"),
            ("transmision", "Transmision"),
            ("traccion", "Traccion"),
            ("color", "Color")
        ]

        # Diccionario para almacenar las entradas
        entradas = {}

        # Distribuye los campos en dos columnas
        for indice, (atributo, etiqueta_texto) in enumerate(campos):

            fila = indice // 2
            columna = (indice % 2) * 2

            etiqueta = ctk.CTkLabel(
                frame_campos,
                text=etiqueta_texto
            )
            etiqueta.grid(
                row=fila,
                column=columna,
                padx=10,
                pady=12,
                sticky="w"
            )

            entrada = ctk.CTkEntry(
                frame_campos,
                width=250,
                placeholder_text=f"Ingrese {etiqueta_texto.lower()}"
            )
            entrada.grid(
                row=fila,
                column=columna + 1,
                padx=10,
                pady=12
            )

            # Guarda la entrada asociada a su atributo
            entradas[atributo] = entrada

        # ==================================================
        # SUBSECCION 6.3 - ESTADO COMERCIAL
        # ==================================================

        etiqueta_estado = ctk.CTkLabel(
            frame_campos,
            text="Estado"
        )
        etiqueta_estado.grid(
            row=7,
            column=0,
            padx=10,
            pady=12,
            sticky="w"
        )

        campo_estado = ctk.CTkComboBox(
            frame_campos,
            values=["Disponible", "Reservado", "Vendido"],
            width=250
        )
        campo_estado.grid(
            row=7,
            column=1,
            padx=10,
            pady=12
        )
        campo_estado.set("Disponible")

        # ==================================================
        # SUBSECCION 6.4 - BOTON DE REGISTRO
        # ==================================================

        boton_guardar = ctk.CTkButton(
            frame_principal,
            text="Guardar auto",
            width=220,
            height=45,
            command=lambda: self.guardar_auto(
                entradas,
                campo_estado,
                ventana
            )
        )
        boton_guardar.pack(pady=25)


    # ==================================================
    # SECCION 7 - GUARDAR AUTO EN MYSQL
    # ==================================================

    def guardar_auto(self, entradas, campo_estado, ventana):
        """Recupera los datos del formulario y registra el auto"""

        # Obtiene los valores ingresados en el formulario
        datos = {}

        for atributo, entrada in entradas.items():
            datos[atributo] = entrada.get().strip()

        # Convierte los campos numericos a sus tipos correspondientes
        try:
            datos["anio"] = int(datos["anio"])
            datos["precio"] = float(datos["precio"])
            datos["kilometraje"] = int(datos["kilometraje"])

        except ValueError:
            messagebox.showerror(
                "Datos incorrectos",
                "El año, precio y kilometraje deben tener valores numericos"
            )
            return

        # Convierte la matricula vacia en None
        if not datos["matricula"]:
            datos["matricula"] = None

        # Obtiene el estado seleccionado
        estado = campo_estado.get()

        # Crea el objeto Auto con los datos del formulario
        auto = Auto(
            datos["matricula"],
            datos["marca"],
            datos["modelo"],
            datos["anio"],
            datos["precio"],
            datos["kilometraje"],
            datos["motor"],
            datos["potencia"],
            datos["torque"],
            datos["combustible"],
            datos["transmision"],
            datos["traccion"],
            datos["color"],
            estado
        )

        # Intenta guardar el auto en la base de datos
        if agregar_auto(auto, self.conexion_db):

            messagebox.showinfo(
                "Registro exitoso",
                "El auto fue agregado correctamente"
            )

            # Limpia los campos despues del registro
            for entrada in entradas.values():
                entrada.delete(0, "end")

            campo_estado.set("Disponible")

        else:
            messagebox.showerror(
                "Error de registro",
                "No se pudo agregar el auto. Verifica los datos ingresados"
            )




