import customtkinter as ctk
from tkinter import messagebox
from clase_autos import Auto
from administracion_autos import agregar_auto, listar_autos, obtener_auto, modificar_auto, eliminar_auto as eliminar_auto_db, buscar_autos, listar_autos_recomendables
from analisis_autos import analizar_diferencia
from archivos_txt import crear_respaldo, leer_respaldo, comparar_respaldo
from validaciones import normalizar_texto
from recomendaciones import procesar_recomendacion as procesar_recomendacion_gemini

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

        # Boton para gestionar el respaldo TXT
        self.boton_respaldo = ctk.CTkButton(
            self.frame_menu,
            text="Gestión de respaldos",
            width=200,
            height=50,
            command=self.mostrar_respaldo
        )
        self.boton_respaldo.pack(pady=15)

        # Boton para salir de la aplicacion
        self.boton_salir = ctk.CTkButton(
            self,
            text="Salir",
            width=200,
            height=40,
            fg_color="#A83232",
            hover_color="#852626",
            command=self.destroy
        )
        self.boton_salir.pack(pady=20)
        
    def crear_respaldo_interfaz(self, ventana):
        """Crea un respaldo de los autos registrados en MySQL"""

        resultado = crear_respaldo(self.conexion_db)

        if resultado:
            messagebox.showinfo(
                "Respaldo creado",
                "El respaldo se creo correctamente"
            )
        else:
            messagebox.showerror(
                "Error",
                "No se pudo crear el respaldo"
            )

    def leer_respaldo_interfaz(self, ventana):
        """Muestra los autos guardados en el archivo de respaldo"""

        autos = leer_respaldo()

        # Comprueba si existen datos guardados
        if not autos:
            messagebox.showwarning(
                "Respaldo vacio",
                "No hay datos guardados o no existe el archivo de respaldo"
            )
            return

        # Convierte las lineas del TXT en registros
        autos = [
            linea.strip().split("|")
            for linea in autos
        ]

        # Crea una ventana para consultar el respaldo
        ventana_respaldo = ctk.CTkToplevel(ventana)
        ventana_respaldo.title("Consultar respaldo")
        ventana_respaldo.geometry("1100x650")

        # Contenedor de la tabla
        frame_tabla = ctk.CTkScrollableFrame(ventana_respaldo)
        frame_tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        # Encabezados de la tabla
        columnas = [
            "ID",
            "Matricula",
            "Marca",
            "Modelo",
            "Año",
            "Precio",
            "Kilometraje",
            "Estado"
        ]

        for indice, columna in enumerate(columnas):
            etiqueta = ctk.CTkLabel(
                frame_tabla,
                text=columna,
                font=("Arial", 13, "bold")
            )
            etiqueta.grid(
                row=0,
                column=indice,
                padx=8,
                pady=12
            )

        # Muestra los datos de cada auto
        for fila, auto in enumerate(autos, start=1):

            datos = [
                auto[0],
                auto[1] if auto[1] else "-",
                auto[2],
                auto[3],
                auto[4],
                f"$ {float(auto[5]):,.2f}",
                auto[6],
                auto[14]
            ]

            for columna, dato in enumerate(datos):
                etiqueta = ctk.CTkLabel(
                    frame_tabla,
                    text=str(dato)
                )
                etiqueta.grid(
                    row=fila,
                    column=columna,
                    padx=8,
                    pady=10
                )
    
    def comparar_respaldo_interfaz(self, ventana):
        """Compara el respaldo TXT con los datos registrados en MySQL"""

        resultado = comparar_respaldo(self.conexion_db)

        if resultado:
            messagebox.showinfo(
                "Respaldo verificado",
                "El respaldo coincide con los datos de la base de datos"
            )

        else:
            messagebox.showwarning(
                "Diferencias encontradas",
                "El respaldo presenta diferencias con la base de datos"
            )
    # ==================================================
    # SECCION 3 - NAVEGACION ENTRE SECCIONES
    # ==================================================

    # Abre la seccion de administracion de autos
    def mostrar_autos(self):
        self.abrir_inventario()

    # Abre la seccion de comparacion de autos
    def mostrar_comparacion(self):
        self.abrir_ventana_comparacion()

    # Abre la seccion de respaldo TXT
    def mostrar_respaldo(self):
        """Muestra las opciones para gestionar los respaldos"""

        ventana = self.abrir_seccion("Gestión de respaldos")

        # Boton para crear un respaldo
        boton_crear = ctk.CTkButton(
            ventana,
            text="Crear respaldo",
            width=220,
            height=45,
            command=lambda: self.crear_respaldo_interfaz(ventana)
        )
        boton_crear.pack(pady=10)

        # Boton para consultar el respaldo
        boton_leer = ctk.CTkButton(
            ventana,
            text="Consultar respaldo",
            width=220,
            height=45,
            command=lambda: self.leer_respaldo_interfaz(ventana)
        )
        boton_leer.pack(pady=10)

        # Boton para comparar el respaldo
        boton_comparar = ctk.CTkButton(
            ventana,
            text="Comparar respaldos",
            width=220,
            height=45,
            command=lambda: self.comparar_respaldo_interfaz(ventana)
        )
        boton_comparar.pack(pady=10)

    # ==================================================
    # SECCION 3.1 - BOTON DE NAVEGACION
    # ==================================================

    def agregar_boton_volver(self, ventana):
        """Agrega un boton para cerrar la ventana actual y volver a la anterior"""

        boton_volver = ctk.CTkButton(
            ventana,
            text="Volver",
            width=150,
            height=35,
            command=ventana.destroy
        )
        boton_volver.pack(side="bottom", pady=15)


    # ==================================================
    # SECCION 4 - CREACION DE VENTANAS SECUNDARIAS
    # ==================================================

    def abrir_seccion(self, titulo):

        ventana = ctk.CTkToplevel(self)
        ventana.title(titulo)
        ventana.geometry("800x550")
        self.agregar_boton_volver(ventana)

        etiqueta = ctk.CTkLabel(
            ventana,
            text=titulo,
            font=("Arial", 24, "bold")
        )
        etiqueta.pack(pady=30)

        return ventana


    # ==================================================
    # SECCION 5 - ADMINISTRACION DE AUTOS
    # ==================================================

    def abrir_administracion_autos(self):
        """Crea el menu principal para administrar los autos"""

        ventana = ctk.CTkToplevel(self)
        ventana.title("Administracion de autos")
        ventana.geometry("850x600")
        self.agregar_boton_volver(ventana)

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

        # Boton para consultar el inventario completo
        boton_inventario = ctk.CTkButton(
            frame_opciones,
            text="Ver inventario",
            width=250,
            height=100,
            font=("Arial", 17, "bold"),
            command=self.abrir_inventario
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

    def abrir_formulario_agregar_auto(self, actualizar_tabla, entrada_busqueda):
        """Crea el formulario para registrar un auto nuevo"""

        ventana = ctk.CTkToplevel(self)
        ventana.title("Agregar auto")
        ventana.geometry("850x750")
        self.agregar_boton_volver(ventana)

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

        # Diccionarios para almacenar las entradas y las unidades
        entradas = {}
        unidades = {}

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

            # Campos especiales para potencia y torque
            if atributo in ("potencia", "torque"):

                frame_unidad = ctk.CTkFrame(
                    frame_campos,
                    fg_color="transparent"
                )
                frame_unidad.grid(
                    row=fila,
                    column=columna + 1,
                    padx=10,
                    pady=12
                )

                entrada = ctk.CTkEntry(
                    frame_unidad,
                    width=150,
                    placeholder_text="Ingrese el valor"
                )
                entrada.pack(side="left", padx=(0, 5))

                # Define las unidades disponibles
                if atributo == "potencia":
                    opciones = ["CV", "HP"]
                else:
                    opciones = ["Nm", "kgm"]

                unidad = ctk.CTkComboBox(
                    frame_unidad,
                    values=opciones,
                    width=90
                )
                unidad.pack(side="left")

                # Guarda la entrada y la unidad seleccionada
                entradas[atributo] = entrada
                unidades[atributo] = unidad

            else:

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

        campo_estado = ctk.CTkOptionMenu(
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
                unidades,
                campo_estado,
                ventana,
                actualizar_tabla,
                entrada_busqueda
            )
        )
        boton_guardar.pack(pady=25)


    # ==================================================
    # SECCION 7 - GUARDAR AUTO EN MYSQL
    # ==================================================

    def guardar_auto(self, entradas, unidades, campo_estado, ventana, actualizar_tabla, entrada_busqueda):
        """Recupera los datos del formulario y registra el auto"""

        # Obtiene los valores ingresados en el formulario
        datos = {}

        for atributo, entrada in entradas.items():
            datos[atributo] = entrada.get().strip()

        # Normaliza la capitalizacion de los datos descriptivos
        for atributo in [
            "marca", "modelo", "motor", "combustible",
            "transmision", "traccion", "color"
        ]:
            datos[atributo] = normalizar_texto(datos[atributo])

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

        # Combina los valores de potencia y torque con sus unidades
        datos["potencia"] = f"{datos['potencia']} {unidades['potencia'].get()}"
        datos["torque"] = f"{datos['torque']} {unidades['torque'].get()}"

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

            # Cierra el formulario de registro
            ventana.destroy()

            # Actualiza la tabla conservando la busqueda actual
            actualizar_tabla(entrada_busqueda.get())

        else:
            messagebox.showerror(
                "Error de registro",
                "No se pudo agregar el auto. Verifica los datos ingresados"
            )



    # ==================================================
    # SECCION 8 - INVENTARIO Y ADMINISTRACION DE AUTOS
    # ==================================================

    def abrir_inventario(self):
        """Muestra y permite administrar los autos registrados"""

        ventana = ctk.CTkToplevel(self)
        ventana.title("Inventario de autos")
        ventana.geometry("1100x700")
        self.agregar_boton_volver(ventana)

        # ==================================================
        # SUBSECCION 8.1 - TITULO
        # ==================================================

        titulo = ctk.CTkLabel(
            ventana,
            text="Inventario de autos",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=15)

        # ==================================================
        # SUBSECCION 8.2 - CONTROLES DE ADMINISTRACION
        # ==================================================

        frame_controles = ctk.CTkFrame(ventana)
        frame_controles.pack(fill="x", padx=20, pady=10)

        # Campo para ingresar el criterio de busqueda
        entrada_busqueda = ctk.CTkEntry(
            frame_controles,
            width=350,
            placeholder_text="Marca, modelo, matricula o caracteristica"
        )
        entrada_busqueda.pack(side="left", padx=10, pady=15)

        # ==================================================
        # SUBSECCION 8.3 - CONTENEDOR DE RESULTADOS
        # ==================================================

        frame_tabla = ctk.CTkScrollableFrame(ventana)
        frame_tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # ==================================================
        # SUBSECCION 8.4 - RECOMENDACION INTELIGENTE
        # ==================================================

        frame_recomendacion = ctk.CTkFrame(ventana)
        frame_recomendacion.pack(fill="x", padx=20, pady=(5, 15))

        # Texto introductorio
        ctk.CTkLabel(
            frame_recomendacion,
            text="¿No sabes que auto elegir?",
            font=("Arial", 18, "bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            frame_recomendacion,
            text="Conoce tus preferencias y encontra el auto que mejor se adapte a vos",
            font=("Arial", 13)
        ).pack(pady=5)

        # Boton para iniciar la recomendacion inteligente
        boton_recomendacion = ctk.CTkButton(
            frame_recomendacion,
            text="Recomendacion inteligente",
            width=220,
            height=40,
            command=self.abrir_formulario_recomendacion
        )
        boton_recomendacion.pack(pady=(10, 15))

        # ==================================================
        # SUBSECCION 8.5 - CARGAR Y MOSTRAR AUTOS
        # ==================================================

        def actualizar_tabla(busqueda=""):

            # Limpia los resultados anteriores
            for elemento in frame_tabla.winfo_children():
                elemento.destroy()

            # Obtiene todos los autos o filtra por busqueda
            if busqueda.strip():
                autos = buscar_autos(self.conexion_db, busqueda.strip())
            else:
                autos = listar_autos(self.conexion_db)

            # Muestra un mensaje si no hay resultados
            if not autos:
                etiqueta_vacia = ctk.CTkLabel(
                    frame_tabla,
                    text="No se encontraron autos",
                    font=("Arial", 16)
                )
                etiqueta_vacia.pack(pady=30)
                return

            # Encabezados de la tabla
            columnas = [
                "ID",
                "Matricula",
                "Marca",
                "Modelo",
                "Año",
                "Precio",
                "Kilometraje",
                "Estado",
                "Acciones"
            ]

            for indice, columna in enumerate(columnas):
                etiqueta = ctk.CTkLabel(
                    frame_tabla,
                    text=columna,
                    font=("Arial", 13, "bold")
                )
                etiqueta.grid(
                    row=0,
                    column=indice,
                    padx=8,
                    pady=12
                )

            # Muestra los datos de cada auto
            for fila, auto in enumerate(autos, start=1):

                datos = [
                    auto[0],
                    auto[1] if auto[1] else "-",
                    auto[2],
                    auto[3],
                    auto[4],
                    f"$ {auto[5]:,.2f}",
                    auto[6],
                    auto[14]
                ]

                for columna, dato in enumerate(datos):
                    etiqueta = ctk.CTkLabel(
                        frame_tabla,
                        text=str(dato)
                    )
                    etiqueta.grid(
                        row=fila,
                        column=columna,
                        padx=8,
                        pady=10
                    )

                # Boton para consultar los detalles
                boton_detalles = ctk.CTkButton(
                    frame_tabla,
                    text="Ver detalles",
                    width=100,
                    command=lambda id_auto=auto[0]: self.mostrar_detalles_auto(
                        id_auto,
                        ventana
                    )
                )
                boton_detalles.grid(
                    row=fila,
                    column=8,
                    padx=8,
                    pady=5
                )

        # ==================================================
        # SUBSECCION 8.6 - BOTONES DE BUSQUEDA
        # ==================================================

        boton_buscar = ctk.CTkButton(
            frame_controles,
            text="Buscar",
            width=100,
            command=lambda: actualizar_tabla(entrada_busqueda.get())
        )
        boton_buscar.pack(side="left", padx=5)

        boton_limpiar = ctk.CTkButton(
            frame_controles,
            text="Limpiar",
            width=100,
            fg_color="gray",
            command=lambda: (
                entrada_busqueda.delete(0, "end"),
                actualizar_tabla()
            )
        )
        boton_limpiar.pack(side="left", padx=5)

        # ==================================================
        # SUBSECCION 8.7 - BOTON PARA AGREGAR AUTOS
        # ==================================================

        boton_agregar = ctk.CTkButton(
            frame_controles,
            text="+ Agregar auto",
            width=140,
            command=lambda: self.abrir_formulario_agregar_auto(actualizar_tabla, entrada_busqueda)
        )
        boton_agregar.pack(side="right", padx=10)

        # Boton para comparar autos
        boton_comparar = ctk.CTkButton(
            frame_controles,
            text="Comparar autos",
            width=150,
            command=lambda: self.abrir_seleccion_comparacion()
        )
        boton_comparar.pack(side="right", padx=10)

        # Permite buscar presionando Enter
        entrada_busqueda.bind(
            "<Return>",
            lambda evento: actualizar_tabla(entrada_busqueda.get())
        )

        # Carga todos los autos al abrir el inventario
        actualizar_tabla()


    # ==================================================
    # SECCION 9 - DETALLES DEL AUTO
    # ==================================================

    def mostrar_detalles_auto(self, id_auto, ventana_inventario):
        """Muestra toda la informacion del auto seleccionado"""

        # Obtener los datos completos desde MySQL
        auto = obtener_auto(id_auto, self.conexion_db)

        if not auto:
            messagebox.showerror(
                "Error",
                "No se pudo encontrar el auto seleccionado"
            )
            return

        # Crear ventana de detalles
        ventana = ctk.CTkToplevel(self)
        ventana.title("Detalles del auto")
        ventana.geometry("650x750")
        ventana.resizable(False, False)
        self.agregar_boton_volver(ventana)

        # Titulo de la ventana
        titulo = ctk.CTkLabel(
            ventana,
            text=f"{auto[2]} {auto[3]}",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=(20, 5))

        subtitulo = ctk.CTkLabel(
            ventana,
            text="Informacion completa del auto",
            font=("Arial", 14)
        )
        subtitulo.pack(pady=(0, 20))

        # Contenedor con desplazamiento vertical
        frame_datos = ctk.CTkScrollableFrame(
            ventana,
            width=520,
            height=480
        )

        # Organizar los datos para mostrarlos
        datos = [
            ("ID interno", auto[0]),
            ("Matricula", auto[1]),
            ("Marca", auto[2]),
            ("Modelo", auto[3]),
            ("Año", auto[4]),
            ("Precio", f"$ {auto[5]:,.2f}"),
            ("Kilometraje", f"{auto[6]} km"),
            ("Motor", auto[7]),
            ("Potencia", auto[8]),
            ("Torque", auto[9]),
            ("Combustible", auto[10]),
            ("Transmision", auto[11]),
            ("Traccion", auto[12]),
            ("Color", auto[13]),
            ("Estado", auto[14])
        ]

        # Mostrar cada dato en una fila
        for fila, (nombre, valor) in enumerate(datos):

            if valor is None or valor == "":
                valor = "-"

            etiqueta = ctk.CTkLabel(
                frame_datos,
                text=f"{nombre}:",
                font=("Arial", 13, "bold"),
                anchor="w"
            )
            etiqueta.grid(
                row=fila,
                column=0,
                padx=20,
                pady=9,
                sticky="w"
            )

            contenido = ctk.CTkLabel(
                frame_datos,
                text=str(valor),
                font=("Arial", 13),
                anchor="w"
            )
            contenido.grid(
                row=fila,
                column=1,
                padx=20,
                pady=9,
                sticky="w"
            )

        # Boton para modificar el auto
        boton_modificar = ctk.CTkButton(
            ventana,
            text="Modificar auto",
            width=180,
            height=40,
            command=lambda: self.abrir_formulario_modificar_auto(
                id_auto,
                ventana,
                ventana_inventario
            )
        )
        boton_modificar.pack(side="bottom", pady=10)

        # Boton para eliminar el auto
        boton_eliminar = ctk.CTkButton(
            ventana,
            text="Eliminar auto",
            width=180,
            height=40,
            fg_color="#A83232",
            hover_color="#852626",
            command=lambda: self.confirmar_eliminacion_auto(
                id_auto,
                ventana,
                ventana_inventario
            )
        )
        boton_eliminar.pack(side="bottom", pady=10)

        # Muestra los datos ocupando el espacio restante
        frame_datos.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )


    # ==================================================
    # SECCION 10 - FORMULARIO PARA MODIFICAR AUTOS
    # ==================================================

    def abrir_formulario_modificar_auto(self, id_auto, ventana_detalles, ventana_inventario):
        """Abre un formulario con los datos actuales del auto"""

        # Recupera los datos del auto
        auto = obtener_auto(id_auto, self.conexion_db)

        if not auto:
            messagebox.showerror(
                "Error",
                "No se pudo encontrar el auto seleccionado"
            )
            return

        # Crea la ventana de modificacion
        ventana = ctk.CTkToplevel(self)
        ventana.title("Modificar auto")
        ventana.geometry("850x750")

        self.agregar_boton_volver(ventana)

        # Contenedor con desplazamiento
        frame_principal = ctk.CTkScrollableFrame(ventana)
        frame_principal.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # Titulo
        titulo = ctk.CTkLabel(
            frame_principal,
            text=f"Modificar {auto[2]} {auto[3]}",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)

        # Contenedor de los campos
        frame_campos = ctk.CTkFrame(frame_principal)
        frame_campos.pack(fill="x", padx=15, pady=10)

        # Relaciona los atributos con los datos actuales
        campos = [
            ("matricula", "Matricula", auto[1]),
            ("marca", "Marca", auto[2]),
            ("modelo", "Modelo", auto[3]),
            ("anio", "Año", auto[4]),
            ("precio", "Precio", auto[5]),
            ("kilometraje", "Kilometraje", auto[6]),
            ("motor", "Motor", auto[7]),
            ("potencia", "Potencia", auto[8]),
            ("torque", "Torque", auto[9]),
            ("combustible", "Combustible", auto[10]),
            ("transmision", "Transmision", auto[11]),
            ("traccion", "Traccion", auto[12]),
            ("color", "Color", auto[13])
        ]

        
        # Diccionarios para almacenar las entradas y las unidades
        entradas = {}
        unidades = {}

        # Distribuye los campos en dos columnas
        for indice, (atributo, nombre, valor) in enumerate(campos):

            fila = indice // 2
            columna = (indice % 2) * 2

            etiqueta = ctk.CTkLabel(
                frame_campos,
                text=nombre
            )
            etiqueta.grid(
                row=fila,
                column=columna,
                padx=10,
                pady=12,
                sticky="w"
            )

            # Campos especiales para potencia y torque
            if atributo in ("potencia", "torque"):

                frame_unidad = ctk.CTkFrame(
                    frame_campos,
                    fg_color="transparent"
                )
                frame_unidad.grid(
                    row=fila,
                    column=columna + 1,
                    padx=10,
                    pady=12
                )

                entrada = ctk.CTkEntry(
                    frame_unidad,
                    width=150
                )
                entrada.pack(side="left", padx=(0, 5))

                # Define las unidades disponibles
                if atributo == "potencia":
                    opciones = ["CV", "HP"]
                    unidad_default = "CV"
                else:
                    opciones = ["Nm", "kgm"]
                    unidad_default = "Nm"

                # Recupera el valor y la unidad guardados
                valor_actual = str(valor).strip() if valor is not None else ""
                partes = valor_actual.rsplit(" ", 1)

                # Comprueba la unidad sin distinguir mayusculas y minusculas
                if len(partes) == 2:
                    unidad_encontrada = next(
                        (opcion for opcion in opciones
                         if opcion.upper() == partes[1].strip().upper()),
                        None
                    )
                else:
                    unidad_encontrada = None

                if unidad_encontrada:
                    valor_actual = partes[0].strip()
                    unidad_actual = unidad_encontrada
                else:
                    unidad_actual = unidad_default

                entrada.insert(0, valor_actual)

                unidad = ctk.CTkComboBox(
                    frame_unidad,
                    values=opciones,
                    width=90
                )
                unidad.pack(side="left")
                unidad.set(unidad_actual)

                # Guarda la entrada y la unidad seleccionada
                entradas[atributo] = entrada
                unidades[atributo] = unidad

            else:

                entrada = ctk.CTkEntry(
                    frame_campos,
                    width=250
                )
                entrada.grid(
                    row=fila,
                    column=columna + 1,
                    padx=10,
                    pady=12
                )

                # Carga el valor actual del auto
                entrada.insert(0, str(valor) if valor is not None else "")

                entradas[atributo] = entrada


        # Campo para modificar el estado
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

        campo_estado = ctk.CTkOptionMenu(
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
        campo_estado.set(auto[14])

        # Boton para guardar los cambios
        boton_guardar = ctk.CTkButton(
            frame_principal,
            text="Guardar modificaciones",
            width=220,
            height=45,
            command=lambda: self.guardar_modificacion_auto(id_auto, entradas, unidades, campo_estado, ventana, ventana_detalles, ventana_inventario)
        )
        boton_guardar.pack(pady=25)


    # ==================================================
    # SECCION 11 - GUARDAR MODIFICACIONES
    # ==================================================

    
    def guardar_modificacion_auto(self, id_auto, entradas, unidades, campo_estado, ventana, ventana_detalles, ventana_inventario):
        """Recupera los datos modificados y actualiza el auto"""

        # Obtiene los valores ingresados
        datos = {}

        for atributo, entrada in entradas.items():
            datos[atributo] = entrada.get().strip()

        # Normaliza la capitalizacion de los datos descriptivos
        for atributo in [
            "marca", "modelo", "motor", "combustible",
            "transmision", "traccion", "color"
        ]:
            datos[atributo] = normalizar_texto(datos[atributo])

        # Convierte los campos numericos
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

        # Combina los valores de potencia y torque con sus unidades
        datos["potencia"] = f"{datos['potencia']} {unidades['potencia'].get()}"
        datos["torque"] = f"{datos['torque']} {unidades['torque'].get()}"

        # Convierte la matricula vacia en None
        if not datos["matricula"]:
            datos["matricula"] = None

        # Obtiene el estado seleccionado
        estado = campo_estado.get()

        # Crea el objeto con los datos actualizados
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

        # Intenta actualizar el registro en MySQL
        if modificar_auto(id_auto, auto, self.conexion_db):

            messagebox.showinfo(
                "Modificacion exitosa",
                "Los datos del auto fueron actualizados correctamente"
            )

            # Cierra los formularios y actualiza los detalles
            ventana.destroy()
            ventana_detalles.destroy()

            # Actualiza la ventana del inventario
            ventana_inventario.destroy()
            self.abrir_inventario()

        else:
            messagebox.showerror(
                "Error de modificacion",
                "No se pudieron actualizar los datos del auto"
            )



    # ==================================================
    # SECCION 12 - ELIMINAR AUTOS
    # ==================================================

    def confirmar_eliminacion_auto(
        self,
        id_auto,
        ventana_detalles,
        ventana_inventario
    ):
        """Solicita confirmacion antes de eliminar un auto"""

        # Solicita confirmacion al usuario
        confirmacion = messagebox.askyesno(
            "Confirmar eliminacion",
            "¿Estas seguro de que deseas eliminar este auto?\n"
            "Esta accion no se puede deshacer"
        )

        if not confirmacion:
            return

        # Intenta eliminar el registro de MySQL
        if eliminar_auto_db(id_auto, self.conexion_db):

            messagebox.showinfo(
                "Eliminacion exitosa",
                "El auto fue eliminado correctamente"
            )

            # Cierra las ventanas anteriores
            ventana_detalles.destroy()
            ventana_inventario.destroy()

            # Actualiza el inventario
            self.abrir_inventario()

        else:
            messagebox.showerror(
                "Error de eliminacion",
                "No se pudo eliminar el auto seleccionado"
            )


    # ==================================================
    # SECCION 13 - COMPARACION DE AUTOS
    # ==================================================

    def abrir_ventana_comparacion(self):
        """Crea la ventana principal para comparar autos"""

        # Crea la ventana secundaria
        ventana = ctk.CTkToplevel(self)
        ventana.title("Comparacion de autos")
        ventana.geometry("1000x700")

        # Boton para volver al menu principal
        self.agregar_boton_volver(ventana)

        # ==================================================
        # SUBSECCION 13.1 - TITULO
        # ==================================================

        titulo = ctk.CTkLabel(
            ventana,
            text="Comparacion de autos",
            font=("Arial", 25, "bold")
        )
        titulo.pack(pady=20)

        # Subtitulo
        subtitulo = ctk.CTkLabel(
            ventana,
            text="Selecciona dos autos para comparar sus caracteristicas",
            font=("Arial", 14)
        )
        subtitulo.pack(pady=5)

        # ==================================================
        # SUBSECCION 13.2 - CARGAR AUTOS
        # ==================================================

        # Obtiene todos los autos registrados en la base de datos
        autos = listar_autos(self.conexion_db)

        # Diccionario para relacionar cada opcion con el ID del auto
        opciones_autos = {}

        for auto in autos:
            nombre_auto = f"{auto[2]} {auto[3]} ({auto[4]}) - {auto[14]}"

            opciones_autos[nombre_auto] = auto[0]

        # Obtiene los nombres para los selectores
        lista_opciones = list(opciones_autos.keys())

        # ==================================================
        # SUBSECCION 13.3 - SELECTORES DE AUTOS
        # ==================================================

        if len(lista_opciones) < 2:
            ctk.CTkLabel(
                ventana,
                text="Necesitas al menos dos autos registrados para compararlos",
                font=("Arial", 14)
            ).pack(pady=30)

        else:

            # Selector del primer auto
            selector_auto_1 = ctk.CTkOptionMenu(
                ventana,
                values=lista_opciones,
                width=350
            )
            selector_auto_1.pack(pady=15)

            # Selector del segundo auto
            selector_auto_2 = ctk.CTkOptionMenu(
                ventana,
                values=lista_opciones,
                width=350
            )
            selector_auto_2.pack(pady=15)

        # ==================================================
        # SUBSECCION 13.4 - VALIDAR SELECCION
        # ==================================================

        def validar_seleccion(valor):
            """Evita que se seleccione el mismo auto dos veces"""

            if selector_auto_1.get() == selector_auto_2.get():

                if valor == "auto_1":
                    selector_auto_2.set(lista_opciones[1])

                else:
                    selector_auto_1.set(lista_opciones[0])

        # Asigna la validacion al primer selector
        selector_auto_1.configure(
            command=lambda valor: validar_seleccion("auto_1")
        )

        # Asigna la validacion al segundo selector
        selector_auto_2.configure(
            command=lambda valor: validar_seleccion("auto_2")
        )


    # ==================================================
    # SECCION 14 - SELECCION DE AUTOS PARA COMPARAR
    # ==================================================

    def abrir_seleccion_comparacion(self):
        """Muestra los autos disponibles para seleccionar y comparar"""

        # Crea la ventana de seleccion
        ventana = ctk.CTkToplevel(self)
        ventana.title("Seleccionar autos para comparar")
        ventana.geometry("1000x700")

        self.agregar_boton_volver(ventana)

        # ==================================================
        # SUBSECCION 14.1 - TITULO
        # ==================================================

        titulo = ctk.CTkLabel(
            ventana,
            text="Seleccion de autos",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=15)

        subtitulo = ctk.CTkLabel(
            ventana,
            text="Selecciona dos autos para realizar una comparacion",
            font=("Arial", 14)
        )
        subtitulo.pack(pady=5)

        # ==================================================
        # SUBSECCION 14.2 - LISTADO DE AUTOS
        # ==================================================

        frame_lista = ctk.CTkScrollableFrame(ventana)
        frame_lista.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        # Obtiene todos los autos registrados
        autos = listar_autos(self.conexion_db)

        if not autos:
            ctk.CTkLabel(
                frame_lista,
                text="No hay autos registrados",
                font=("Arial", 16)
            ).pack(pady=30)

            return

        # ==================================================
        # SUBSECCION 14.3 - MOSTRAR AUTOS
        # ==================================================

        # Guarda los autos seleccionados para comparar
        autos_seleccionados = []

        # Etiqueta para mostrar la cantidad seleccionada
        etiqueta_seleccion = ctk.CTkLabel(
            ventana,
            text="Autos seleccionados: 0/2",
            font=("Arial", 15, "bold")
        )
        etiqueta_seleccion.pack(pady=5)

        # Boton para iniciar la comparacion
        boton_comparar = ctk.CTkButton(
            ventana,
            text="Comparar seleccionados",
            width=200,
            state="disabled",
            command=lambda: self.mostrar_comparacion_autos(
                autos_seleccionados
            )
        )
        boton_comparar.pack(pady=10)

        # ==================================================
        # SUBSECCION 14.4 - AGREGAR AUTOS A LA COMPARACION
        # ==================================================

        def agregar_auto_comparacion(id_auto):
            """Agrega un auto a la lista temporal de comparacion"""

            # Comprueba que no se haya seleccionado anteriormente
            if id_auto in autos_seleccionados:
                messagebox.showwarning(
                    "Auto repetido",
                    "Este auto ya fue agregado a la comparacion"
                )
                return

            # Limita la seleccion a dos autos
            if len(autos_seleccionados) >= 2:
                messagebox.showwarning(
                    "Limite alcanzado",
                    "Solo podes seleccionar dos autos para comparar"
                )
                return

            # Agrega el ID del auto seleccionado
            autos_seleccionados.append(id_auto)

            # Actualiza el contador
            etiqueta_seleccion.configure(
                text=f"Autos seleccionados: {len(autos_seleccionados)}/2"
            )

            # Habilita el boton cuando hay dos autos seleccionados
            if len(autos_seleccionados) == 2:
                boton_comparar.configure(state="normal")

        def eliminar_auto_comparacion(id_auto):
            """Elimina un auto de la lista temporal de comparacion"""

            if id_auto in autos_seleccionados:
                autos_seleccionados.remove(id_auto)

                # Actualiza el contador
                etiqueta_seleccion.configure(
                    text=f"Autos seleccionados: {len(autos_seleccionados)}/2"
                )

                # Deshabilita el boton si quedan menos de dos autos
                if len(autos_seleccionados) < 2:
                    boton_comparar.configure(state="disabled")

        # Muestra cada auto registrado
        for fila, auto in enumerate(autos):

            frame_auto = ctk.CTkFrame(frame_lista)
            frame_auto.pack(fill="x", padx=10, pady=5)

            # Datos principales del auto
            nombre_auto = f"{auto[2]} {auto[3]} ({auto[4]})"

            matricula = auto[1] if auto[1] else "Sin patente"
            color = auto[13] if auto[13] else "Sin color"

            etiqueta_auto = ctk.CTkLabel(
                frame_auto,
                text=f"{nombre_auto} | Color: {color} | Patente: {matricula} | Estado: {auto[14]}",
                font=("Arial", 14)
            )
            etiqueta_auto.pack(side="left", padx=15, pady=12)

            # Boton para agregar o quitar el auto de la comparacion
            boton_agregar = ctk.CTkButton(
                frame_auto,
                text="+",
                width=40
            )
            boton_agregar.pack(side="right", padx=15, pady=8)

            def cambiar_seleccion(id_auto, boton):
                """Alterna la seleccion de un auto"""

                if id_auto in autos_seleccionados:
                    eliminar_auto_comparacion(id_auto)
                    boton.configure(text="+")

                else:
                    cantidad_anterior = len(autos_seleccionados)

                    agregar_auto_comparacion(id_auto)

                    # Comprueba si el auto se agrego correctamente
                    if len(autos_seleccionados) > cantidad_anterior:
                        boton.configure(text="-")

            boton_agregar.configure(
                command=lambda id_auto=auto[0], boton=boton_agregar:
                    cambiar_seleccion(id_auto, boton)
            )


    # ==================================================
    # SECCION 15 - COMPARACION DE AUTOS
    # ==================================================

    def mostrar_comparacion_autos(self, autos_seleccionados):
        """Muestra una comparacion entre dos autos"""

        # Recupera los datos completos de ambos autos
        auto_1 = obtener_auto(
            autos_seleccionados[0],
            self.conexion_db
        )

        auto_2 = obtener_auto(
            autos_seleccionados[1],
            self.conexion_db
        )

        # Comprueba que ambos autos existan
        if not auto_1 or not auto_2:
            messagebox.showerror(
                "Error",
                "No se pudieron obtener los datos de los autos seleccionados"
            )
            return

        # Crea la ventana de comparacion
        ventana = ctk.CTkToplevel(self)
        ventana.title("Comparacion de autos")
        ventana.geometry("1000x700")

        self.agregar_boton_volver(ventana)

        # Titulo principal
        etiqueta_titulo = ctk.CTkLabel(
            ventana,
            text="Comparacion de autos",
            font=("Arial", 26, "bold")
        )
        etiqueta_titulo.pack(pady=20)

        # Contenedor desplazable de la tabla comparativa
        frame_comparacion = ctk.CTkScrollableFrame(
            ventana,
            orientation="vertical"
        )
        frame_comparacion.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        # Organiza las columnas
        frame_comparacion.grid_columnconfigure(0, weight=1)
        frame_comparacion.grid_columnconfigure(1, weight=2)
        frame_comparacion.grid_columnconfigure(2, weight=2)


        # Encabezados con la identificacion de cada auto
        encabezados = [
            "Caracteristica",
            f"{auto_1[2]} {auto_1[3]}",
            f"{auto_2[2]} {auto_2[3]}"
        ]

        for columna, encabezado in enumerate(encabezados):
            etiqueta = ctk.CTkLabel(
                frame_comparacion,
                text=encabezado,
                font=("Arial", 16, "bold"),
                wraplength=250
            )
            etiqueta.grid(
                row=0,
                column=columna,
                padx=15,
                pady=15,
                sticky="ew"
            )

        # Caracteristicas que se van a comparar
        caracteristicas = [
            ("Marca", 2),
            ("Modelo", 3),
            ("Año", 4),
            ("Precio", 5),
            ("Kilometraje", 6),
            ("Motor", 7),
            ("Potencia", 8),
            ("Torque", 9),
            ("Combustible", 10),
            ("Transmision", 11),
            ("Traccion", 12),
            ("Color", 13),
            ("Patente", 1),
            ("Estado comercial", 14)
        ]

        # Genera las filas de la comparacion
        for fila, (nombre, indice) in enumerate(caracteristicas, start=1):

            valor_1 = auto_1[indice]
            valor_2 = auto_2[indice]

            # Aplica formato segun el tipo de dato
            if indice == 5:
                valor_1 = f"${valor_1:,.2f}" if valor_1 is not None else "No especificado"
                valor_2 = f"${valor_2:,.2f}" if valor_2 is not None else "No especificado"

            elif indice == 6:
                valor_1 = f"{valor_1:,.0f} km" if valor_1 is not None else "No especificado"
                valor_2 = f"{valor_2:,.0f} km" if valor_2 is not None else "No especificado"

            elif indice == 9:
                valor_1 = str(valor_1) if valor_1 is not None else "No especificado"
                valor_2 = str(valor_2) if valor_2 is not None else "No especificado"

            else:
                valor_1 = str(valor_1) if valor_1 is not None else "No especificado"
                valor_2 = str(valor_2) if valor_2 is not None else "No especificado"

            # Evita mostrar valores vacios como None
            if valor_1 is None:
                valor_1 = "No especificado"

            if valor_2 is None:
                valor_2 = "No especificado"

            etiqueta_caracteristica = ctk.CTkLabel(
                frame_comparacion,
                text=nombre,
                font=("Arial", 13, "bold")
            )
            etiqueta_caracteristica.grid(
                row=fila,
                column=0,
                padx=15,
                pady=8,
                sticky="w"
            )

            etiqueta_auto_1 = ctk.CTkLabel(
                frame_comparacion,
                text=str(valor_1),
                font=("Arial", 13)
            )
            etiqueta_auto_1.grid(
                row=fila,
                column=1,
                padx=15,
                pady=8
            )

            etiqueta_auto_2 = ctk.CTkLabel(
                frame_comparacion,
                text=str(valor_2),
                font=("Arial", 13)
            )
            etiqueta_auto_2.grid(
                row=fila,
                column=2,
                padx=15,
                pady=8
            )


        # ==================================================
        # RESUMEN DE DIFERENCIAS ENTRE LOS AUTOS
        # ==================================================

        # Identifica cada auto con sus datos principales
        nombre_auto_1 = (
            f"{auto_1[2]} {auto_1[3]} - "
            f"{auto_1[4]} - {auto_1[13]} - {auto_1[1]}"
        )

        nombre_auto_2 = (
            f"{auto_2[2]} {auto_2[3]} - "
            f"{auto_2[4]} - {auto_2[13]} - {auto_2[1]}"
        )

        # Calcula las diferencias principales
        resumen_precio = analizar_diferencia(
            "Precio",
            auto_1[5],
            auto_2[5],
            "$",
            True,
            nombre_auto_1,
            nombre_auto_2
        )

        resumen_kilometraje = analizar_diferencia(
            "Kilometraje",
            auto_1[6],
            auto_2[6],
            "km",
            True,
            nombre_auto_1,
            nombre_auto_2
        )

        resumen_potencia = analizar_diferencia(
            "Potencia",
            auto_1[8],
            auto_2[8],
            "CV",
            False,
            nombre_auto_1,
            nombre_auto_2
        )

        resumen_torque = analizar_diferencia(
            "Torque",
            auto_1[9],
            auto_2[9],
            "Nm",
            False,
            nombre_auto_1,
            nombre_auto_2
        )

        # Contenedor del resumen
        frame_resumen = ctk.CTkFrame(ventana)
        frame_resumen.pack(
            fill="x",
            padx=30,
            pady=15
        )

        etiqueta_resumen = ctk.CTkLabel(
            frame_resumen,
            text="Resumen de diferencias",
            font=("Arial", 18, "bold")
        )
        etiqueta_resumen.pack(pady=10)

        # Muestra los resultados
        for resultado in [
            resumen_precio,
            resumen_kilometraje,
            resumen_potencia,
            resumen_torque
        ]:
            etiqueta = ctk.CTkLabel(
                frame_resumen,
                text=resultado,
                font=("Arial", 13)
            )
            etiqueta.pack(pady=5)

    # ==================================================
    # SECCION 16 - FORMULARIO DE RECOMENDACION INTELIGENTE
    # ==================================================

    def abrir_formulario_recomendacion(self):
        """Muestra el formulario para conocer las preferencias del cliente"""

        # Crea la ventana del formulario
        ventana = ctk.CTkToplevel(self)
        ventana.title("Recomendacion inteligente")
        ventana.geometry("750x800")

        self.agregar_boton_volver(ventana)

        # Contenedor con desplazamiento
        frame_principal = ctk.CTkScrollableFrame(ventana)
        frame_principal.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        # ==================================================
        # SUBSECCION 16.1 - TITULO
        # ==================================================

        ctk.CTkLabel(
            frame_principal,
            text="Recomendacion inteligente",
            font=("Arial", 24, "bold")
        ).pack(pady=15)

        ctk.CTkLabel(
            frame_principal,
            text="Completa tus preferencias para encontrar el auto ideal",
            font=("Arial", 14)
        ).pack(pady=5)

        # ==================================================
        # SUBSECCION 16.2 - USO DEL AUTO
        # ==================================================

        ctk.CTkLabel(
            frame_principal,
            text="1. ¿Para que buscas el auto?",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(20, 10))

        uso_var = ctk.StringVar(value="")

        for opcion in [
            "Familiar",
            "Trabajo",
            "Uso urbano",
            "Viajes y ruta",
            "Deportivo y recreativo",
            "Uso mixto"
        ]:
            ctk.CTkRadioButton(
                frame_principal,
                text=opcion,
                variable=uso_var,
                value=opcion
            ).pack(anchor="w", padx=15, pady=3)

        # ==================================================
        # SUBSECCION 16.3 - PRESUPUESTO
        # ==================================================

        ctk.CTkLabel(
            frame_principal,
            text="2. ¿Que presupuesto tienes pensado?",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(25, 10))

        presupuesto_var = ctk.StringVar(value="")

        presupuestos = [
            "Economico - Hasta $20.000.000",
            "Medio - $20.000.000 a $35.000.000",
            "Alto - $35.000.000 a $60.000.000",
            "Premium o lujoso - Mas de $60.000.000",
            "Sin limite definido"
        ]

        for opcion in presupuestos:
            ctk.CTkRadioButton(
                frame_principal,
                text=opcion,
                variable=presupuesto_var,
                value=opcion
            ).pack(anchor="w", padx=15, pady=3)

        # ==================================================
        # SUBSECCION 16.4 - CARACTERISTICAS PRIORITARIAS
        # ==================================================

        ctk.CTkLabel(
            frame_principal,
            text="3. ¿Que caracteristicas priorizas?",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(25, 10))

        prioridades_vars = {}

        prioridades = [
            "Bajo consumo",
            "Comodidad",
            "Confiabilidad",
            "Potencia y rendimiento",
            "Seguridad",
            "Espacio y capacidad",
            "Tecnologia y equipamiento",
            "Bajo mantenimiento"
        ]

        for opcion in prioridades:
            variable = ctk.BooleanVar(value=False)
            prioridades_vars[opcion] = variable

            ctk.CTkCheckBox(
                frame_principal,
                text=opcion,
                variable=variable
            ).pack(anchor="w", padx=15, pady=3)

        # ==================================================
        # SUBSECCION 16.5 - TIPO DE TRANSMISION
        # ==================================================

        ctk.CTkLabel(
            frame_principal,
            text="4. ¿Que tipo de transmision prefieres?",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(25, 10))

        transmision_var = ctk.StringVar(value="")

        for opcion in ["Manual", "Automatica", "Indistinto"]:
            ctk.CTkRadioButton(
                frame_principal,
                text=opcion,
                variable=transmision_var,
                value=opcion
            ).pack(anchor="w", padx=15, pady=3)

       
        # ==================================================
        # SUBSECCION 16.6 - PROCESAR PREFERENCIAS
        # ==================================================

        def procesar_recomendacion():
            """Obtiene las preferencias y solicita una recomendacion a Gemini"""

            # Comprueba que se hayan completado las opciones obligatorias
            if not uso_var.get() or not presupuesto_var.get() or not transmision_var.get():
                messagebox.showwarning(
                    "Datos incompletos",
                    "Completa todas las opciones antes de generar la recomendacion"
                )
                return

            # Obtiene las caracteristicas seleccionadas
            prioridades = [
                opcion
                for opcion, variable in prioridades_vars.items()
                if variable.get()
            ]

            if not prioridades:
                messagebox.showwarning(
                    "Datos incompletos",
                    "Selecciona al menos una caracteristica prioritaria"
                )
                return

            # Obtiene los autos que no se encuentran vendidos
            autos = listar_autos_recomendables(self.conexion_db)

            if not autos:
                messagebox.showwarning(
                    "Sin autos disponibles",
                    "No hay autos para analizar en el inventario"
                )
                return

            # Organiza las respuestas del cliente
            preferencias = {
                "uso": uso_var.get(),
                "presupuesto": presupuesto_var.get(),
                "prioridades": ", ".join(prioridades),
                "transmision": transmision_var.get()
            }

            # Procesa la recomendacion y recupera los datos del auto elegido
            respuesta = procesar_recomendacion_gemini(
                autos,
                preferencias,
                self.conexion_db
            )

            # Comprueba que se haya podido procesar la recomendacion
            if respuesta is None:
                messagebox.showerror(
                    "Error en la recomendacion",
                    "No se pudo generar una recomendacion valida. Intenta nuevamente"
                )
                return
            
            # Muestra el resultado en una nueva ventana
            ventana_resultado = ctk.CTkToplevel(ventana)
            ventana_resultado.title("Resultado de la recomendacion")
            ventana_resultado.geometry("750x650")

            self.agregar_boton_volver(ventana_resultado)

            ctk.CTkLabel(
                ventana_resultado,
                text="Recomendacion para el cliente",
                font=("Arial", 22, "bold")
            ).pack(pady=15)

            # Obtiene los datos del resultado de Gemini y del auto recomendado
            resultado = respuesta["resultado"]
            auto = respuesta["auto"]

            # Contenedor principal del resultado
            frame_resultado = ctk.CTkScrollableFrame(ventana_resultado)
            frame_resultado.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=15
            )

            # Tarjeta principal del auto recomendado
            frame_auto = ctk.CTkFrame(frame_resultado, corner_radius=12)
            frame_auto.pack(fill="x", padx=10, pady=10)

            ctk.CTkLabel(
                frame_auto,
                text="AUTO RECOMENDADO",
                font=("Arial", 13, "bold"),
                text_color="gray"
            ).pack(anchor="w", padx=20, pady=(15, 5))

            ctk.CTkLabel(
                frame_auto,
                text=f"{auto[2]} {auto[3]} ({auto[4]})",
                font=("Arial", 24, "bold")
            ).pack(anchor="w", padx=20, pady=5)

            ctk.CTkLabel(
                frame_auto,
                text=f"${auto[5]:,.2f}",
                font=("Arial", 22, "bold"),
                text_color="#2FA572"
            ).pack(anchor="w", padx=20, pady=5)

            # Contenedor de las caracteristicas principales
            frame_caracteristicas = ctk.CTkFrame(
                frame_auto,
                fg_color="transparent"
            )
            frame_caracteristicas.pack(fill="x", padx=15, pady=(5, 15))

            # Organiza las caracteristicas en dos columnas
            caracteristicas = [
                ("KILOMETRAJE", f"{auto[6]:,} km"),
                ("MOTOR", auto[7]),
                ("POTENCIA", auto[8]),
                ("TORQUE", auto[9]),
                ("COMBUSTIBLE", auto[10]),
                ("TRANSMISION", auto[11])
            ]

            for i, (titulo, valor) in enumerate(caracteristicas):

                fila = i // 2
                columna = i % 2

                frame_dato = ctk.CTkFrame(
                    frame_caracteristicas,
                    corner_radius=8
                )
                frame_dato.grid(
                    row=fila,
                    column=columna,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

                ctk.CTkLabel(
                    frame_dato,
                    text=titulo,
                    font=("Arial", 10, "bold"),
                    text_color="gray"
                ).pack(anchor="w", padx=12, pady=(8, 2))

                ctk.CTkLabel(
                    frame_dato,
                    text=str(valor),
                    font=("Arial", 14, "bold")
                ).pack(anchor="w", padx=12, pady=(0, 8))

            # Distribuye el espacio entre las dos columnas
            frame_caracteristicas.grid_columnconfigure(0, weight=1)
            frame_caracteristicas.grid_columnconfigure(1, weight=1)

            # Obtiene los datos del resultado de Gemini y del auto recomendado
            resultado = respuesta["resultado"]
            auto = respuesta["auto"]

            # Tarjeta principal del auto recomendado
            frame_auto = ctk.CTkFrame(frame_resultado, corner_radius=12)
            frame_auto.pack(fill="x", padx=10, pady=10)

            # Seccion del nivel de ajuste
            frame_ajuste = ctk.CTkFrame(frame_resultado, corner_radius=12)
            frame_ajuste.pack(fill="x", padx=10, pady=10)

            nivel_ajuste = resultado.get("nivel_ajuste", "Ninguno")

            colores_ajuste = {
                "Alto": "#2FA572",
                "Medio": "#3B82F6",
                "Bajo": "#E59A32",
                "Ninguno": "#D9534F"
            }

            ctk.CTkLabel(
                frame_ajuste,
                text="NIVEL DE AJUSTE",
                font=("Arial", 13, "bold"),
                text_color="gray"
            ).pack(anchor="w", padx=20, pady=(12, 5))

            ctk.CTkLabel(
                frame_ajuste,
                text=nivel_ajuste,
                font=("Arial", 20, "bold"),
                text_color=colores_ajuste.get(nivel_ajuste, "gray")
            ).pack(anchor="w", padx=20, pady=(0, 12))

            # Seccion del analisis de Gemini
            frame_analisis = ctk.CTkFrame(frame_resultado, corner_radius=12)
            frame_analisis.pack(fill="x", padx=10, pady=10)

            ctk.CTkLabel(
                frame_analisis,
                text="ANALISIS DE LA RECOMENDACION",
                font=("Arial", 14, "bold")
            ).pack(anchor="w", padx=20, pady=(15, 5))

            ctk.CTkLabel(
                frame_analisis,
                text=resultado.get("analisis", "Sin analisis disponible"),
                font=("Arial", 13),
                justify="left",
                wraplength=650
            ).pack(anchor="w", padx=20, pady=(5, 15))

            # Obtiene los datos del resultado de Gemini y del auto recomendado
            resultado = respuesta["resultado"]
            auto = respuesta["auto"]

            # Organiza la informacion para mostrarla al cliente
            texto_resultado = f"""
            AUTO RECOMENDADO

            {auto[2]} {auto[3]} ({auto[4]})

            Precio: ${auto[5]:,.2f}
            Kilometraje: {auto[6]:,} km
            Motor: {auto[7]}
            Potencia: {auto[8]}
            Torque: {auto[9]}
            Combustible: {auto[10]}
            Transmision: {auto[11]}
            Traccion: {auto[12]}
            Color: {auto[13]}

            NIVEL DE AJUSTE

            {resultado.get("nivel_ajuste", "No especificado")}

            ANALISIS

            {resultado.get("analisis", "Sin analisis disponible")}

            VENTAJAS

            {chr(10).join("- " + ventaja for ventaja in resultado.get("ventajas", []))}

            ASPECTOS A CONSIDERAR

            {chr(10).join("- " + aspecto for aspecto in resultado.get("aspectos_a_considerar", []))}
            """

        # Seccion de ventajas y aspectos a considerar
            frame_detalles = ctk.CTkFrame(frame_resultado, fg_color="transparent")
            frame_detalles.pack(fill="x", padx=10, pady=5)

            # Tarjeta de ventajas
            frame_ventajas = ctk.CTkFrame(frame_detalles, corner_radius=12)
            frame_ventajas.pack(fill="x", pady=5)

            ctk.CTkLabel(
                frame_ventajas,
                text="VENTAJAS",
                font=("Arial", 14, "bold"),
                text_color="#2FA572"
            ).pack(anchor="w", padx=20, pady=(12, 5))

            for ventaja in resultado.get("ventajas", []):
                ctk.CTkLabel(
                    frame_ventajas,
                    text=f"✓  {ventaja}",
                    font=("Arial", 13),
                    justify="left",
                    wraplength=650
                ).pack(anchor="w", padx=20, pady=3)

            # Tarjeta de aspectos a considerar
            frame_aspectos = ctk.CTkFrame(frame_detalles, corner_radius=12)
            frame_aspectos.pack(fill="x", pady=5)

            ctk.CTkLabel(
                frame_aspectos,
                text="ASPECTOS A CONSIDERAR",
                font=("Arial", 14, "bold"),
                text_color="#E59A32"
            ).pack(anchor="w", padx=20, pady=(12, 5))

            for aspecto in resultado.get("aspectos_a_considerar", []):
                ctk.CTkLabel(
                    frame_aspectos,
                    text=f"•  {aspecto}",
                    font=("Arial", 13),
                    justify="left",
                    wraplength=650
                ).pack(anchor="w", padx=20, pady=3)

        boton_generar = ctk.CTkButton(
            frame_principal,
            text="Generar recomendacion",
            width=220,
            command=procesar_recomendacion
        )
        boton_generar.pack(pady=30)






