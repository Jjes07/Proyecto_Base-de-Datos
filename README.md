# Base de Datos - S2561-0701

# Estudiante(s): Juan José Escobar, jjescobars@eafit.edu.co

# Profesor: Edwin Nelson Montoya Múnera, emontoya@eafit.edu.co

# Proyecto Final - Aplicación de Nodo EAFIT

# 1. Breve descripción de la actividad

Este proyecto consiste en el diseño e implementación de una aplicación para la gestión de cursos en línea ofrecidos por Nodo (EAFIT). La aplicación permite a administradores, profesores y estudiantes realizar tareas relacionadas con la gestión de contenidos, usuarios, tareas, foros y materiales de los cursos.

## 1.1. Aspectos que se cumplieron

* Implementación completa del modelo relacional basado en el enunciado.
* Aplicación funcional desarrollada en Python con interfaz gráfica (Tkinter).
* Conexión a base de datos MySQL.
* Login de usuario con autenticación por correo y contraseña.
* Diferenciación de funcionalidades por rol (admin, profesor, estudiante).
* Acciones disponibles:

  * Admin: matricular estudiantes, asignar profesores, ver reportes.
  * Profesor: ver cursos, subir materiales y tareas, participar y crear foros, revisar entregas.
  * Estudiante: ver cursos, descargar materiales, entregar tareas, participar en foros.
* Agregado de intereses por parte de los profesores.
* Interacción completa con foros y mensajes.

## 1.2. Aspectos no cumplidos

* No se implementó manejo de archivos reales (solo se simula con nombres).
* No se implementó validación avanzada de formularios.
* No se integró despliegue en nube o servidor de producción.
* No se implementó un manejo de errores completo. 

# 2. Información general de diseño de alto nivel

* Arquitectura basada en tres capas: interfaz (Tkinter), lógica de negocio (Python), y persistencia (MySQL).
* Separación modular por rol: admin.py, profesor.py, estudiante.py.
* Uso de funciones reutilizables para consultas y operaciones CRUD.

# 3. Ambiente de desarrollo

* Lenguaje: Python 3.13
* Base de datos: MySQL Workbench 8.0
* Librerías:

  * mysql-connector-python 8.1.0
  * tkinter (estándar en Python)

## Cómo se compila y ejecuta

1. Crear la base de datos usando los scripts `proyecto_ddl.sql` y `proyecto_dml.sql`.
2. Ejecutar `main.py` con su IDE de preferencia o desde consola con Python 3:

```bash
python main.py
```

## Detalles técnicos

* Login por correo/contraseña, detección automática del rol.
* Interfaz gráfica basada en ventanas y menús por rol.
* Conexiones a base de datos en `db.py`.

## Configuración de parámetros

* Conexión MySQL en `db.py`:

```python
host = "localhost"
user = "admin_nodo"
password = "1234"
database = "nodo"
```
# Organización de archivos

```
/Entrega Proyecto/
├── Entrega 1/
|   ├── Avance 1-v.2 
├── Entrega 2/
|   ├── Diagrama - modelo lógico
|   ├── Diagrama - WorkBench
|   ├── proyecto_ddl.sql
|   ├── proyecto_dml.sql
|   ├── proyecto_query.sql
├── Entrega 3/
|   ├── nodo_app
|   ├── img_doc
```

## Organización del código

```
/nodo_app/
├── db.py
├── main.py
├── auth.py
├── gui/
│   ├── admin.py
│   ├── profesor.py
│   └── estudiante.py
```

## Resultados

* Login por rol
* Vista de cursos
* Entrega de tareas y participación en foros
* Reportes para administrador

* [Login](img_doc/login.png)
* [Menú Administrador](img_doc/menu_admin.png)
* [Menú Profesor](img_doc/menu_profe.png)
* [Menú Curso de Profesor](img_doc/menu_profe_curso.png)
* [Menú Estudiante](img_doc/menu_est.png)
* [Menú Curso de Estudiante](img_doc/menu_est_curso.png)

# 4. Ambiente de ejecución

* Igual al de desarrollo: Python 3.13, MySQL Workbench local.
* Puede ejecutarse en cualquier PC con acceso a la base de datos MySQL.

# IP o nombres de dominio

* Localhost (127.0.0.1)
* Puerto 3306

## Configuración

Ver archivo `db.py` para los datos de conexión. Se requiere ejecutar el script sql llamado `proyecto_ddl` para crear la base y permitir la conexión.

## Lanzamiento del servidor

* No aplica: aplicación de escritorio en local.

## Mini guía para usuario

1. Crear la base de datos con MySQL usando el script `proyecto_ddl`.
2. Insertar registros ejecutando `proyecto_dml` o ingresar los datos manualmente a la base.
3. Ejecutar el archivo `main.py`
4. Ingresar con credenciales válidas. Los correos y contraseñas se pueden encontrar en la base de datos.
5. Navegar según el rol:

   * Admin: asignaciones y reportes.
   * Profesor: intereses, listado de cursos y creación de contenido.
   * Estudiante: participación y entregas en cursos.

# 5. Otra información relevante

* El proyecto fue desarrollado como una aplicación de escritorio con interfaz gráfica simple utilizando Tkinter, sin integración con servicios en la nube como AWS ni despliegue web.
* Aunque el modelo de base de datos contempla el manejo de usuarios no matriculados, esta funcionalidad no fue implementada en la lógica de la aplicación. Sería una mejora futura valiosa para ofrecer una experiencia más completa y realista.

# Referencias:

* [Interfaces Gráficas con Tkinter](https://docs.python.org/es/3.13/library/tkinter.html#tkinter-life-preserver)
* [Conexion a la base de datos desde python](https://dev.mysql.com/doc/connector-python/en/)
* [Playlist: Python and MySQL](https://www.youtube.com/watch?v=x7SwgcpACng&list=PLB5jA40tNf3tRMbTpBA0N7lfDZNLZAa9G)

