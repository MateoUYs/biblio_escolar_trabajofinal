import sqlite3
from datetime import datetime

# Conexión y creación de tablas
def conectar():
    conn = sqlite3.connect('biblioteca.db')
    # Tabla Libros (ya existente)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            isbn TEXT PRIMARY KEY,
            titulo TEXT,
            autor TEXT,
            genero TEXT,
            disponible INTEGER DEFAULT 1
        )
    ''')

    # Tabla Usuarios
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    ''')

    # Tabla Préstamos
    conn.execute('''
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL,
            usuario_id TEXT NOT NULL,
            fecha_prestamo TEXT NOT NULL,
            fecha_devolucion TEXT,
            FOREIGN KEY (isbn) REFERENCES libros(isbn),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    return conn

# ===================== USUARIOS ======================

def agregar_usuario(usuario_id, nombre, tipo):
    conn = conectar()
    try:
        conn.execute(
            "INSERT INTO usuarios (id, nombre, tipo) VALUES (?, ?, ?)",
            (usuario_id, nombre, tipo)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"⚠️ El usuario con ID {usuario_id} ya existe.")
    finally:
        conn.close()

def obtener_usuarios():
    conn = conectar()
    cursor = conn.execute("SELECT id, nombre, tipo FROM usuarios")
    usuarios = [dict(zip(['id', 'nombre', 'tipo'], row)) for row in cursor.fetchall()]
    conn.close()
    return usuarios

# ===================== PRESTAMOS ======================

def registrar_prestamo(isbn, usuario_id):
    conn = conectar()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Verificar que el libro esté disponible
        disponible = conn.execute("SELECT disponible FROM libros WHERE isbn=?", (isbn,)).fetchone()
        if not disponible or disponible[0] == 0:
            print("⚠️ El libro no está disponible.")
            return False

        # Registrar préstamo
        conn.execute(
            "INSERT INTO prestamos (isbn, usuario_id, fecha_prestamo) VALUES (?, ?, ?)",
            (isbn, usuario_id, fecha)
        )

        # Marcar libro como no disponible
        conn.execute("UPDATE libros SET disponible=0 WHERE isbn=?", (isbn,))
        conn.commit()
        return True
    finally:
        conn.close()

def cerrar_prestamo(prestamo_id):
    conn = conectar()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Obtener ISBN
        isbn = conn.execute("SELECT isbn FROM prestamos WHERE id=?", (prestamo_id,)).fetchone()
        if not isbn:
            print("⚠️ Préstamo no encontrado.")
            return False

        # Actualizar fecha de devolución
        conn.execute(
            "UPDATE prestamos SET fecha_devolucion=? WHERE id=?",
            (fecha, prestamo_id)
        )

        # Marcar libro como disponible
        conn.execute("UPDATE libros SET disponible=1 WHERE isbn=?", (isbn[0],))
        conn.commit()
        return True
    finally:
        conn.close()

def obtener_prestamos():
    conn = conectar()
    cursor = conn.execute("""
        SELECT p.id, p.isbn, l.titulo, u.nombre, u.tipo, p.fecha_prestamo, p.fecha_devolucion
        FROM prestamos p
        JOIN libros l ON p.isbn = l.isbn
        JOIN usuarios u ON p.usuario_id = u.id
        ORDER BY p.fecha_prestamo DESC
    """)
    prestamos = [
        dict(zip(['id', 'isbn', 'titulo', 'usuario', 'tipo', 'fecha_prestamo', 'fecha_devolucion'], row))
        for row in cursor.fetchall()
    ]
    conn.close()
    return prestamos
