import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db import get_connection

def mostrar_menu_estudiante(est_info):
    window = tk.Tk()
    window.title("Estudiante - Nodo")
    window.geometry("400x400")

    nombre = est_info["email"].split("@")[0]
    id_est = est_info["id_estudiante"]

    tk.Label(window, text=f"Bienvenido/a, {nombre}", font=("Helvetica", 14)).pack(pady=10)

    ttk.Button(window, text="Ver mis cursos", command=lambda: ver_mis_cursos(id_est)).pack(pady=5)

    from main import mostrar_login
    def cerrar_sesion():
        window.destroy()
        mostrar_login()

    ttk.Button(window, text="Cerrar sesión", command=cerrar_sesion).pack(pady=20)
    window.mainloop()

def ver_mis_cursos(id_est):
    form = tk.Toplevel()
    form.title("Mis Cursos")
    form.geometry("400x300")

    tree = ttk.Treeview(form, columns=("ID", "Nombre"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.pack(expand=True, fill="both")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id_curso, c.nombre
        FROM curso c
        JOIN matricula m ON m.id_curso = c.id_curso
        WHERE m.id_estudiante = %s
    """, (id_est,))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

    def abrir_menu():
        selected = tree.focus()
        if selected:
            values = tree.item(selected, 'values')
            id_curso, nombre_curso = values
            mostrar_menu_curso(int(id_curso), nombre_curso, id_est)

    ttk.Button(form, text="Ingresar al curso", command=abrir_menu).pack(pady=5)

def mostrar_menu_curso(id_curso, nombre_curso, id_est):
    form = tk.Toplevel()
    form.title(f"Curso: {nombre_curso}")
    form.geometry("400x400")

    tk.Label(form, text=f"Curso: {nombre_curso}", font=("Helvetica", 14)).pack(pady=10)

    ttk.Button(form, text="Ver materiales", command=lambda: listar_materiales(id_curso, id_est)).pack(pady=5)
    ttk.Button(form, text="Ver tareas", command=lambda: listar_tareas(id_curso, id_est)).pack(pady=5)
    ttk.Button(form, text="Ver foros", command=lambda: listar_foros(id_curso, id_est)).pack(pady=5)
    ttk.Button(form, text="Ver compañeros", command=lambda: listar_estudiantes(id_curso)).pack(pady=5)

    ttk.Button(form, text="Salir del curso", command=form.destroy).pack(pady=20)

def listar_materiales(id_curso, id_est):
    form = tk.Toplevel()
    form.title("Materiales")
    tree = ttk.Treeview(form, columns=("ID", "Título"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Título", text="Título")
    tree.pack(expand=True, fill="both")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_material, titulo FROM material WHERE id_curso = %s", (id_curso,))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

    def descargar():
        selected = tree.focus()
        if selected:
            id_material, _ = tree.item(selected, 'values')
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO descarga_material (id_estudiante, id_material) VALUES (%s, %s)",
                               (id_est, id_material))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Material descargado")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    ttk.Button(form, text="Descargar", command=descargar).pack(pady=5)

def listar_tareas(id_curso, id_est):
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

    def entregar():
        selected = tree.focus()
        if selected:
            id_tarea, _ = tree.item(selected, 'values')
            archivo = simpledialog.askstring("Entrega", "Nombre del archivo (.pdf, .zip, etc):")
            if archivo:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO respuestatarea (archivo_entrega, fecha_envio, id_tarea, id_estudiante) VALUES (%s, CURDATE(), %s, %s)",
                                   (archivo, id_tarea, id_est))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Éxito", "Tarea entregada")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    ttk.Button(form, text="Entregar tarea", command=entregar).pack(pady=5)

def listar_foros(id_curso, id_est):
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
            ver_mensajes_foro(int(id_foro), id_est)

    ttk.Button(form, text="Ingresar al foro", command=abrir_foro).pack(pady=5)

def ver_mensajes_foro(id_foro, id_est):
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
                cursor.execute("INSERT INTO mensajeforo (nombre, descripcion, id_foro, id_estudiante) VALUES (%s, %s, %s, %s)",
                               (titulo, descripcion, id_foro, id_est))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Mensaje enviado")
                form.destroy()
                ver_mensajes_foro(id_foro, id_est)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    ttk.Button(form, text="Agregar mensaje", command=agregar_mensaje).pack(pady=5)

def listar_estudiantes(id_curso):
    form = tk.Toplevel()
    form.title("Compañeros")
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
