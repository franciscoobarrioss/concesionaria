# CONCESIONARIA - SISTEMA DE GESTION DE AUTOS

## DESCRIPCION

Aplicacion de escritorio desarrollada en Python para administrar el inventario de una concesionaria. Permite registrar, consultar, modificar y eliminar autos, comparar sus caracteristicas y obtener recomendaciones basadas en las preferencias del cliente.

## FUNCIONALIDADES

- Alta, consulta, modificacion y eliminacion de autos
- Busqueda de autos en el inventario
- Comparacion de dos autos
- Recomendaciones segun las preferencias del cliente mediante Gemini
- Gestion de estados: Disponible, Reservado y Vendido
- Conexion con base de datos MySQL
- Carga de datos de prueba para facilitar la demostracion del sistema

## TECNOLOGIAS UTILIZADAS

- Python 3
- CustomTkinter
- MySQL
- PyMySQL
- Google Gemini API
- python-dotenv

## REQUISITOS

- Python 3 instalado
- MySQL Server en funcionamiento
- MySQL Workbench (opcional, para consultar y administrar la base de datos)
- Una clave de API de Gemini para utilizar la funcion de recomendaciones con IA

## INSTALACION

1. Descargar o clonar el repositorio desde:

   https://github.com/franciscoobarrioss/concesionaria

2. Abrir una terminal en la carpeta del proyecto.

3. Instalar las dependencias necesarias:

   pip install customtkinter pymysql google-genai python-dotenv

## CONFIGURACION DE LA BASE DE DATOS

1. Verificar que el servidor MySQL este iniciado.
2. Abrir el archivo conexion.py.
3. Configurar los datos de conexion correspondientes al servidor MySQL (host, usuario y contrasena).
4. Ejecutar la aplicacion. La conexion crea automaticamente la base de datos concesionaria y la tabla autos si todavia no existen.

## CARGA DE AUTOS DE PRUEBA

El proyecto incluye el archivo cargar_datos.py, que permite insertar 20 autos de ejemplo en la base de datos.

Para ejecutarlo, abrir una terminal en la carpeta del proyecto y escribir:

   python cargar_datos.py

El script evita insertar nuevamente autos que ya existan, por lo que puede ejecutarse mas de una vez sin duplicar los registros de ejemplo.

## CONFIGURACION DE GEMINI

Para utilizar las recomendaciones mediante inteligencia artificial:

1. Crear un archivo llamado .env en la carpeta principal del proyecto.
2. Agregar la clave de API con este formato:

   GEMINI_API_KEY=tu_clave_de_api

3. Reemplazar el texto de ejemplo por una clave valida.

IMPORTANTE: No compartir ni subir el archivo .env a GitHub, ya que contiene una clave privada.

## EJECUCION DEL SISTEMA

Desde la terminal, dentro de la carpeta del proyecto, ejecutar:

   python main.py

## ESTRUCTURA DEL PROYECTO

main.py                  Punto de entrada de la aplicacion
interfaz.py              Interfaz grafica del sistema
conexion.py              Conexion y creacion de la base de datos
clase_autos.py           Clase que representa cada auto
administracion_autos.py  Operaciones de administracion de autos
validaciones.py          Validaciones de datos
analisis_autos.py        Funciones de analisis y comparacion
recomendaciones.py       Recomendaciones mediante Gemini
archivos_txt.py          Funciones para trabajar con archivos de texto
cargar_datos.py          Carga de autos de ejemplo en la base de datos
prueba_atuos.py          Archivo de pruebas de autos
prueba_conexion.py       Prueba de conexion a MySQL
respaldo.txt             Archivo de respaldo utilizado por el proyecto

## USO GENERAL

1. Iniciar la aplicacion desde main.py.
2. Utilizar las opciones de la interfaz para administrar el inventario.
3. Buscar autos y consultar sus datos.
4. Seleccionar autos para realizar comparaciones.
5. Ingresar las preferencias del cliente para generar una recomendacion.

## REPOSITORIO

GitHub:
https://github.com/franciscoobarrioss/concesionaria

## NOTAS

- La base de datos y la tabla se crean automaticamente desde conexion.py.
- Se recomienda ejecutar cargar_datos.py para contar con registros de ejemplo durante la prueba del sistema.
- La funcion de recomendaciones con Gemini requiere una clave de API valida.
- No subir contrasenas ni claves privadas al repositorio.