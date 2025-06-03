import tkinter as tk
from tkinter import messagebox
from auth import autenticar
from gui.admin import mostrar_menu_admin
from gui.profesor import mostrar_menu_profesor
from gui.estudiante import mostrar_menu_estudiante

def abrir_menu(usuario):
    rol = usuario["rol"]
    datos = usuario["datos"]
    nombre = datos["nombre"] if "nombre" in datos else datos.get("email")

    messagebox.showinfo("Bienvenido", f"{rol.capitalize()}: {nombre}")

    # Aquí conectamos con las ventanas por rol (placeholder por ahora)
    if rol == "administrador":
        print("Abrir menú administrador")
        mostrar_menu_admin(datos)
    elif rol == "profesor":
        print("Abrir menú profesor")
        mostrar_menu_profesor(datos)
    elif rol == "estudiante":
        print("Abrir menú estudiante")
        mostrar_menu_estudiante(datos)

def mostrar_login():
    root = tk.Tk()
    root.title("Login - Nodo LMS")
    root.geometry("300x200")

    tk.Label(root, text="Correo:").pack(pady=5)
    entry_email = tk.Entry(root)
    entry_email.pack()

    tk.Label(root, text="Contraseña:").pack(pady=5)
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    def login():
        email = entry_email.get()
        password = entry_password.get()
        usuario = autenticar(email, password)
        if usuario:
            root.destroy()
            abrir_menu(usuario)
        else:
            messagebox.showerror("Error", "Credenciales inválidas")

    tk.Button(root, text="Iniciar sesión", command=login).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    mostrar_login()
