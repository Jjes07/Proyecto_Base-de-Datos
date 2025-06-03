from db import get_connection

def autenticar(email, contraseña):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Administrador
    cursor.execute("SELECT * FROM administrador WHERE email = %s AND contraseña = %s", (email, contraseña))
    admin = cursor.fetchone()
    if admin:
        conn.close()
        return {'rol': 'administrador', 'datos': admin}

    # 2. Profesor
    cursor.execute("SELECT * FROM profesor WHERE email = %s AND contraseña = %s", (email, contraseña))
    profe = cursor.fetchone()
    if profe:
        conn.close()
        return {'rol': 'profesor', 'datos': profe}

    # 3. Estudiante
    cursor.execute("SELECT * FROM estudiante WHERE email = %s AND contraseña = %s", (email, contraseña))
    est = cursor.fetchone()
    if est:
        conn.close()
        return {'rol': 'estudiante', 'datos': est}

    conn.close()
    return None  # Credenciales inválidas

