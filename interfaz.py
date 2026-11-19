import customtkinter as ctk
from tkinter import messagebox
from clase_autos import Auto
from administracion_autos import agregar_auto, listar_autos, obtener_auto, modificar_auto, eliminar_auto as eliminar_auto_db

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

    def abrir_formulario_agregar_auto(self):
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
    
    # ==================================================
    # SECCION 8 - INVENTARIO DE AUTOS
    # ==================================================

    def abrir_inventario(self):
        """Muestra los autos registrados en la base de datos"""

        ventana = ctk.CTkToplevel(self)
        ventana.title("Inventario de autos")
        ventana.geometry("1100x650")
        self.agregar_boton_volver(ventana)

        # ==================================================
        # SUBSECCION 8.1 - TITULO
        # ==================================================

        titulo = ctk.CTkLabel(
            ventana,
            text="Inventario de autos",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)

        # ==================================================
        # SUBSECCION 8.2 - TABLA DE AUTOS
        # ==================================================

        # Contenedor de la tabla
        frame_tabla = ctk.CTkFrame(ventana)
        frame_tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # Obtiene los autos registrados en MySQL
        autos = listar_autos(self.conexion_db)

        # Muestra un mensaje si no existen registros
        if not autos:
            etiqueta_vacia = ctk.CTkLabel(
                frame_tabla,
                text="No hay autos registrados",
                font=("Arial", 16)
            )
            etiqueta_vacia.pack(pady=30)
            return

        # ==================================================
        # SUBSECCION 8.3 - ENCABEZADOS
        # ==================================================

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

        # ==================================================
        # SUBSECCION 8.4 - DATOS DE LOS AUTOS
        # ==================================================

        # Recorre los registros y muestra sus datos principales
        for fila, auto in enumerate(autos, start=1):

            # Columnas seleccionadas de la tabla autos
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

            # Crea una etiqueta para cada dato
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
            
            # Boton para consultar los detalles del auto
            boton_detalles = ctk.CTkButton(
                frame_tabla,
                text="Ver detalles",
                width=100,
                command=lambda id_auto=auto[0]: self.mostrar_detalles_auto(id_auto, ventana)
            )
            boton_detalles.grid(
                row=fila,
                column=8,
                padx=8,
                pady=5
            )
    
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
        
        
        # ==================================================
        # BOTON PARA MODIFICAR EL AUTO
        # ==================================================

        boton_modificar = ctk.CTkButton(
            ventana,
            text="Modificar auto",
            width=180,
            height=40,
            command=lambda: self.abrir_formulario_modificar_auto(id_auto, ventana, ventana_inventario)
        )
        boton_modificar.pack(side="bottom", pady=10)

        # ==================================================
        # BOTON PARA ELIMINAR EL AUTO
        # ==================================================

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

        # Muestra el contenedor de datos ocupando el espacio restante
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

        # Diccionario para almacenar las entradas
        entradas = {}

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
            command=lambda: self.guardar_modificacion_auto(id_auto, entradas, campo_estado, ventana, ventana_detalles, ventana_inventario)
        )
        boton_guardar.pack(pady=25)


    # ==================================================
    # SECCION 11 - GUARDAR MODIFICACIONES
    # ==================================================

    def guardar_modificacion_auto(self, id_auto, entradas, campo_estado, ventana, ventana_detalles, ventana_inventario):
        """Recupera los datos modificados y actualiza el auto"""

        # Obtiene los valores ingresados
        datos = {}

        for atributo, entrada in entradas.items():
            datos[atributo] = entrada.get().strip()

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








