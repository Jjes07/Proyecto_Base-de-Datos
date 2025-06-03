import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection

def mostrar_menu_admin(admin_info):
    window = tk.Tk()
    window.title("Administrador - Nodo")
    window.geometry("400x400")

    nombre = admin_info["nombre"]

    tk.Label(window, text=f"Bienvenido/a, {nombre}", font=("Helvetica", 14)).pack(pady=10)

    ttk.Button(window, text="Matricular estudiante", command=lambda: matricular_estudiante(admin_info)).pack(pady=5)
    ttk.Button(window, text="Asignar profesor a curso", command=lambda: asignar_profesor()).pack(pady=5)
    ttk.Button(window, text="Listar cursos", command=lambda: listar_cursos()).pack(pady=5)
    ttk.Button(window, text="Ver detalle de curso", command=lambda: detalle_curso()).pack(pady=5)
    ttk.Button(window, text="Listar usuarios", command=lambda: listar_usuarios()).pack(pady=5)

    from main import mostrar_login
    def cerrar_sesion():
        window.destroy()
        mostrar_login()
    ttk.Button(window, text="Cerrar sesión", command=cerrar_sesion).pack(pady=20)

    window.mainloop()

def matricular_estudiante(admin_info):
    form = tk.Toplevel()
    form.title("Matricular Estudiante")
    form.geometry("300x300")

    tk.Label(form, text="ID Estudiante:").pack()
    entry_est = tk.Entry(form)
    entry_est.pack()

    tk.Label(form, text="ID Curso:").pack()
    entry_curso = tk.Entry(form)
    entry_curso.pack()

    tk.Label(form, text="Contraseña ingreso:").pack()
    entry_pass = tk.Entry(form)
    entry_pass.pack()

    def registrar():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO matricula (id_estudiante, id_admin, id_curso, fecha_matricula, estado, contraseña_ingreso)
                VALUES (%s, %s, %s, CURDATE(), 'activa', %s)
            """, (
                entry_est.get(),
                admin_info["id_admin"],
                entry_curso.get(),
                entry_pass.get()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Estudiante matriculado")
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(form, text="Matricular", command=registrar).pack(pady=10)

def asignar_profesor():
    form = tk.Toplevel()
    form.title("Asignar Profesor")
    form.geometry("300x250")

    tk.Label(form, text="ID Curso:").pack()
    entry_curso = tk.Entry(form)
    entry_curso.pack()

    tk.Label(form, text="ID Profesor:").pack()
    entry_prof = tk.Entry(form)
    entry_prof.pack()

    def asignar():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE curso SET id_profesor = %s WHERE id_curso = %s
            """, (entry_prof.get(), entry_curso.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Profesor asignado al curso.")
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(form, text="Asignar", command=asignar).pack(pady=10)

def listar_cursos():
    form = tk.Toplevel()
    form.title("Cursos disponibles")
    form.geometry("600x350")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT categoria FROM curso")
    categorias = cursor.fetchall()
    cat_text = ", ".join(c[0] for c in categorias if c[0])
    tk.Label(form, text="Categorías disponibles: " + cat_text).pack()
    conn.close()

    tk.Label(form, text="Filtrar por nombre o categoría:").pack()
    filtro = tk.Entry(form)
    filtro.pack()

    tree = ttk.Treeview(form, columns=("ID", "Nombre", "Categoría", "Profesor"), show='headings')
    for col in ("ID", "Nombre", "Categoría", "Profesor"):
        tree.heading(col, text=col)
    tree.pack(expand=True, fill="both")

    def buscar():
        conn = get_connection()
        cursor = conn.cursor()

        filtro_valor = filtro.get().strip()

        if filtro_valor:
            like = f"%{filtro_valor}%"
            query = """
                SELECT c.id_curso, c.nombre, c.categoria, p.email
                FROM curso c
                LEFT JOIN profesor p ON c.id_profesor = p.id_profesor
                WHERE c.nombre LIKE %s OR c.categoria LIKE %s
            """
            cursor.execute(query, (like, like))
        else:
            query = """
                SELECT c.id_curso, c.nombre, c.categoria, p.email
                FROM curso c
                LEFT JOIN profesor p ON c.id_profesor = p.id_profesor
            """
            cursor.execute(query)

        rows = cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", "end", values=row)
        conn.close()


    tk.Button(form, text="Buscar", command=buscar).pack(pady=5)

def detalle_curso():
    form = tk.Toplevel()
    form.title("Detalle de Curso")
    form.geometry("600x400")

    tk.Label(form, text="ID del curso:").pack()
    entry_id = tk.Entry(form)
    entry_id.pack()

    def consultar():
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT c.nombre, c.categoria, p.email
                FROM curso c
                LEFT JOIN profesor p ON c.id_profesor = p.id_profesor
                WHERE c.id_curso = %s
            """, (entry_id.get(),))
            curso = cursor.fetchone()

            cursor.execute("""
                SELECT e.email FROM estudiante e
                JOIN matricula m ON e.id_estudiante = m.id_estudiante
                WHERE m.id_curso = %s
            """, (entry_id.get(),))
            estudiantes = cursor.fetchall()
            conn.close()

            result = f"Curso: {curso[0]}\nCategoría: {curso[1]}\nProfesor: {curso[2]}\nEstudiantes:\n"
            result += "\n".join(e[0] for e in estudiantes) or "Sin estudiantes"
            messagebox.showinfo("Detalle", result)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(form, text="Ver Detalles", command=consultar).pack(pady=10)

def listar_usuarios():
    form = tk.Toplevel()
    form.title("Listado de Usuarios")
    form.geometry("600x400")

    tk.Label(form, text="Filtrar por tipo (admin / profesor / estudiante):").pack()
    entry_tipo = tk.Entry(form)
    entry_tipo.pack()

    tree = ttk.Treeview(form, columns=("ID", "Email", "Rol"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Email", text="Email")
    tree.heading("Rol", text="Rol")
    tree.pack(expand=True, fill="both")

    def buscar():
        tipo = entry_tipo.get().strip().lower()
        conn = get_connection()
        cursor = conn.cursor()

        tree.delete(*tree.get_children())

        try:
            if tipo == "admin":
                cursor.execute("SELECT id_admin, email FROM administrador ORDER BY id_admin")
                rows = cursor.fetchall()
                for r in rows:
                    tree.insert("", "end", values=(r[0], r[1], "Administrador"))

            elif tipo == "profesor":
                cursor.execute("SELECT id_profesor, email FROM profesor ORDER BY id_profesor")
                rows = cursor.fetchall()
                for r in rows:
                    tree.insert("", "end", values=(r[0], r[1], "Profesor"))

            elif tipo == "estudiante":
                cursor.execute("SELECT id_estudiante, email FROM estudiante ORDER BY id_estudiante")
                rows = cursor.fetchall()
                for r in rows:
                    tree.insert("", "end", values=(r[0], r[1], "Estudiante"))

            elif tipo == "":
                # Mostrar todos los roles
                cursor.execute("SELECT id_admin, email FROM administrador ORDER BY id_admin")
                for r in cursor.fetchall():
                    tree.insert("", "end", values=(r[0], r[1], "Administrador"))

                cursor.execute("SELECT id_profesor, email FROM profesor ORDER BY id_profesor")
                for r in cursor.fetchall():
                    tree.insert("", "end", values=(r[0], r[1], "Profesor"))

                cursor.execute("SELECT id_estudiante, email FROM estudiante ORDER BY id_estudiante")
                for r in cursor.fetchall():
                    tree.insert("", "end", values=(r[0], r[1], "Estudiante"))
            else:
                messagebox.showerror("Error", "Tipo inválido. Usa admin, profesor o estudiante.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        conn.close()

    tk.Button(form, text="Buscar", command=buscar).pack(pady=10)
