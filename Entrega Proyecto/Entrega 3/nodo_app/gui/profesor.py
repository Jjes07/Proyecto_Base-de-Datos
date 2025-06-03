import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db import get_connection

def mostrar_menu_profesor(profesor_info):
    window = tk.Tk()
    window.title("Profesor - Nodo")
    window.geometry("400x400")

    nombre = profesor_info["email"].split("@")[0]
    id_profesor = profesor_info["id_profesor"]

    tk.Label(window, text=f"Bienvenido/a, {nombre}", font=("Helvetica", 14)).pack(pady=10)

    ttk.Button(window, text="Ver mis cursos", command=lambda: ver_mis_cursos(id_profesor)).pack(pady=5)
    ttk.Button(window, text="Agregar interés en un curso", command=lambda: agregar_interes(id_profesor)).pack(pady=5)

    from main import mostrar_login
    def cerrar_sesion():
        window.destroy()
        mostrar_login()

    ttk.Button(window, text="Cerrar sesión", command=cerrar_sesion).pack(pady=20)
    window.mainloop()

def ver_mis_cursos(id_profesor):
    form = tk.Toplevel()
    form.title("Mis Cursos")
    form.geometry("400x300")

    tree = ttk.Treeview(form, columns=("ID", "Nombre"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.pack(expand=True, fill="both")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_curso, nombre FROM curso WHERE id_profesor = %s", (id_profesor,))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

    def abrir_menu():
        selected = tree.focus()
        if selected:
            values = tree.item(selected, 'values')
            id_curso, nombre_curso = values
            mostrar_menu_curso(int(id_curso), nombre_curso, id_profesor)

    ttk.Button(form, text="Ingresar al curso", command=abrir_menu).pack(pady=5)

def mostrar_menu_curso(id_curso, nombre_curso, id_profesor):
    form = tk.Toplevel()
    form.title(f"Curso: {nombre_curso}")
    form.geometry("400x400")

    tk.Label(form, text=f"Curso: {nombre_curso}", font=("Helvetica", 14)).pack(pady=10)

    ttk.Button(form, text="Ver estudiantes", command=lambda: listar_estudiantes(id_curso)).pack(pady=5)
    ttk.Button(form, text="Ver materiales", command=lambda: listar_materiales(id_curso)).pack(pady=5)
    ttk.Button(form, text="Agregar material", command=lambda: agregar_material(id_curso, id_profesor)).pack(pady=5)
    ttk.Button(form, text="Ver foros", command=lambda: listar_foros(id_curso, id_profesor)).pack(pady=5)
    ttk.Button(form, text="Crear foro", command=lambda: crear_foro(id_curso, id_profesor)).pack(pady=5)
    ttk.Button(form, text="Ver tareas", command=lambda: listar_tareas(id_curso, id_profesor)).pack(pady=5)
    ttk.Button(form, text="Crear tarea", command=lambda: crear_tarea(id_curso, id_profesor)).pack(pady=5)

    ttk.Button(form, text="Salir del curso", command=form.destroy).pack(pady=20)

def agregar_interes(id_profesor):
    id_curso = simpledialog.askinteger("Agregar interés", "Ingrese el ID del curso:")
    if id_curso:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO profesor_interesado_curso (id_profesor, id_curso) VALUES (%s, %s)", (id_profesor, id_curso))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Interés registrado")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def listar_estudiantes(id_curso):
    form = tk.Toplevel()
    form.title("Estudiantes del curso")
    tree = ttk.Treeview(form, columns=("Email",), show="headings")
    tree.heading("Email", text="Email")
    tree.pack(expand=True, fill="both")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.email FROM estudiante e
        JOIN matricula m ON m.id_estudiante = e.id_estudiante
        WHERE m.id_curso = %s
    """, (id_curso,))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def listar_materiales(id_curso):
    form = tk.Toplevel()
    form.title("Materiales")
    tree = ttk.Treeview(form, columns=("Título",), show="headings")
    tree.heading("Título", text="Título")
    tree.pack(expand=True, fill="both")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT titulo FROM material WHERE id_curso = %s", (id_curso,))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def agregar_material(id_curso, id_profesor):
    titulo = simpledialog.askstring("Agregar material", "Título del material:")
    if titulo:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO material (id_curso, id_profesor, titulo, nombre_archivo) VALUES (%s, %s, %s, %s)",
                           (id_curso, id_profesor, titulo, titulo + ".pdf"))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Material agregado")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def listar_foros(id_curso, id_profesor):
    form = tk.Toplevel()
    form.title("Foros")
    tree = ttk.Treeview(form, columns=("ID", "Nombre"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.pack(expand=True, fill="both")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_foro, nombre FROM foro WHERE id_curso = %s", (id_curso,))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

    def abrir_foro():
        selected = tree.focus()
        if selected:
            id_foro, nombre = tree.item(selected, 'values')
            ver_mensajes_foro(int(id_foro), id_profesor)

    ttk.Button(form, text="Ingresar al foro", command=abrir_foro).pack(pady=5)

def ver_mensajes_foro(id_foro, id_profesor):
    form = tk.Toplevel()
    form.title("Mensajes del Foro")
    tree = ttk.Treeview(form, columns=("ID", "Título", "Descripción"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Título", text="Título")
    tree.heading("Descripción", text="Descripción")
    tree.pack(expand=True, fill="both")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_mensaje, nombre, descripcion
        FROM mensajeforo
        WHERE id_foro = %s
    """, (id_foro,))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

    def agregar_mensaje():
        titulo = simpledialog.askstring("Nuevo mensaje", "Título del mensaje:")
        descripcion = simpledialog.askstring("Nuevo mensaje", "Contenido:")
        if titulo and descripcion:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO mensajeforo (nombre, descripcion, id_foro, id_profesor) VALUES (%s, %s, %s, %s)",
                               (titulo, descripcion, id_foro, id_profesor))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Mensaje publicado")
                form.destroy()
                ver_mensajes_foro(id_foro, id_profesor)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    ttk.Button(form, text="Agregar mensaje", command=agregar_mensaje).pack(pady=5)

def crear_foro(id_curso, id_profesor):
    nombre = simpledialog.askstring("Crear foro", "Nombre del foro:")
    if nombre:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO foro (id_curso, id_profesor, nombre, descripcion, fecha_creacion, fecha_terminacion) VALUES (%s, %s, %s, '', CURDATE(), CURDATE() + INTERVAL 30 DAY)",
                           (id_curso, id_profesor, nombre))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Foro creado")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def listar_tareas(id_curso, id_profesor):
    form = tk.Toplevel()
    form.title("Tareas")
    tree = ttk.Treeview(form, columns=("ID", "Nombre"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.pack(expand=True, fill="both")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_tarea, nombre FROM tarea WHERE id_curso = %s", (id_curso,))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

    def ver_entregas():
        selected = tree.focus()
        if selected:
            id_tarea, _ = tree.item(selected, 'values')
            ver_entregas_tarea(int(id_tarea))

    ttk.Button(form, text="Ver entregas", command=ver_entregas).pack(pady=5)

def ver_entregas_tarea(id_tarea):
    form = tk.Toplevel()
    form.title("Entregas de tarea")
    tree = ttk.Treeview(form, columns=("Estudiante", "Archivo"), show="headings")
    tree.heading("Estudiante", text="Estudiante")
    tree.heading("Archivo", text="Archivo")
    tree.pack(expand=True, fill="both")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.email, r.archivo_entrega
        FROM respuestatarea r
        JOIN estudiante e ON r.id_estudiante = e.id_estudiante
        WHERE r.id_tarea = %s
    """, (id_tarea,))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def crear_tarea(id_curso, id_profesor):
    nombre = simpledialog.askstring("Crear tarea", "Nombre de la tarea:")
    if nombre:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tarea (id_curso, id_profesor, nombre, descripcion, fecha_creacion, fecha_entrega, puntaje, archivo_profesor) VALUES (%s, %s, %s, '', CURDATE(), CURDATE() + INTERVAL 7 DAY, 5.0, %s)",
                           (id_curso, id_profesor, nombre, nombre + ".pdf"))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Tarea creada")
        except Exception as e:
            messagebox.showerror("Error", str(e))
