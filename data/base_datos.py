import sqlite3
from datetime import datetime

# ===================== CONEXIÓN Y TABLAS ======================

def conectar():
    conn = sqlite3.connect('biblioteca.db')
    # Tabla Libros
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

# ===================== LIBROS ======================

def agregar_libro(libro):
    """Agrega un libro a la base de datos."""
    conn = conectar()
    try:
        conn.execute(
            "INSERT INTO libros (isbn, titulo, autor, genero, disponible) VALUES (?, ?, ?, ?, ?)",
            (libro.isbn, libro.titulo, libro.autor, libro.genero, 1 if libro.disponible else 0)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"⚠️ El libro con ISBN {libro.isbn} ya existe.")
    finally:
        conn.close()

def obtener_libros():
    conn = conectar()
    cursor = conn.execute("SELECT * FROM libros")
    libros = [dict(zip(['isbn', 'titulo', 'autor', 'genero', 'disponible'], row)) for row in cursor.fetchall()]
    conn.close()
    return libros

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

def obtener_usuario(usuario_id: str):
    """Devuelve {id, nombre, tipo} o None."""
    conn = conectar()
    cur = conn.execute("SELECT id, nombre, tipo FROM usuarios WHERE id=?", (usuario_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {"id": row[0], "nombre": row[1], "tipo": row[2]}

def listar_docentes():
    conn = conectar()
    cur = conn.execute("SELECT id, nombre, tipo FROM usuarios WHERE tipo='docente' ORDER BY nombre")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "nombre": r[1], "tipo": r[2]} for r in rows]

# ===================== PRÉSTAMOS ======================

def registrar_prestamo(isbn, usuario_id):
    conn = conectar()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        disponible = conn.execute("SELECT disponible FROM libros WHERE isbn=?", (isbn,)).fetchone()
        if not disponible or disponible[0] == 0:
            print("⚠️ El libro no está disponible.")
            return False

        conn.execute(
            "INSERT INTO prestamos (isbn, usuario_id, fecha_prestamo) VALUES (?, ?, ?)",
            (isbn, usuario_id, fecha)
        )
        conn.execute("UPDATE libros SET disponible=0 WHERE isbn=?", (isbn,))
        conn.commit()
        return True
    finally:
        conn.close()

def cerrar_prestamo(prestamo_id):
    conn = conectar()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        isbn = conn.execute("SELECT isbn FROM prestamos WHERE id=?", (prestamo_id,)).fetchone()
        if not isbn:
            print("⚠️ Préstamo no encontrado.")
            return False

        conn.execute("UPDATE prestamos SET fecha_devolucion=? WHERE id=?", (fecha, prestamo_id))
        conn.execute("UPDATE libros SET disponible=1 WHERE isbn=?", (isbn[0],))
        conn.commit()
        return True
    finally:
        conn.close()

def obtener_prestamos():
    """Incluye también el usuario_id para poder operar desde la UI."""
    conn = conectar()
    cursor = conn.execute("""
        SELECT 
            p.id,
            p.isbn,
            l.titulo,
            u.id   AS usuario_id,
            u.nombre AS usuario_nombre,
            u.tipo,
            p.fecha_prestamo,
            p.fecha_devolucion
        FROM prestamos p
        JOIN libros l ON p.isbn = l.isbn
        JOIN usuarios u ON p.usuario_id = u.id
        ORDER BY p.fecha_prestamo DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "isbn": r[1],
            "titulo": r[2],
            "usuario_id": r[3],
            "usuario": r[4],
            "tipo": r[5],
            "fecha_prestamo": r[6],
            "fecha_devolucion": r[7],
        }
        for r in rows
    ]

# ===================== PERMISOS Y ELIMINACIONES ======================

def es_docente(usuario_id: str) -> bool:
    conn = conectar()
    cur = conn.execute("SELECT 1 FROM usuarios WHERE id=? AND tipo='docente'", (usuario_id,))
    ok = cur.fetchone() is not None
    conn.close()
    return ok

def eliminar_libro(isbn: str) -> bool:
    """Elimina un libro por ISBN si NO tiene préstamos activos."""
    conn = conectar()
    cur = conn.execute(
        "SELECT 1 FROM prestamos WHERE isbn=? AND fecha_devolucion IS NULL LIMIT 1",
        (isbn,)
    )
    hay_activos = cur.fetchone() is not None
    if hay_activos:
        conn.close()
        return False

    cur2 = conn.execute("DELETE FROM libros WHERE isbn=?", (isbn,))
    conn.commit()
    afectadas = cur2.rowcount
    conn.close()
    return afectadas > 0

def eliminar_usuario(usuario_id: str) -> bool:
    """Elimina un usuario si no tiene préstamos (ni activos ni históricos)."""
    conn = conectar()
    try:
        cur = conn.execute("SELECT 1 FROM usuarios WHERE id=?", (usuario_id,))
        if cur.fetchone() is None:
            return False

        cur = conn.execute("SELECT 1 FROM prestamos WHERE usuario_id=? LIMIT 1", (usuario_id,))
        if cur.fetchone() is not None:
            return False

        cur2 = conn.execute("DELETE FROM usuarios WHERE id=?", (usuario_id,))
        conn.commit()
        return cur2.rowcount > 0
    finally:
        conn.close()

def eliminar_prestamo_por_usuario_isbn(usuario_id: str, isbn: str) -> bool:
    """
    Elimina el préstamo ACTIVO del par (usuario_id, isbn).
    Repone disponibilidad del libro si no quedan otros préstamos activos de ese ISBN.
    """
    conn = conectar()
    try:
        row = conn.execute(
            "SELECT id FROM prestamos WHERE usuario_id=? AND isbn=? AND fecha_devolucion IS NULL ORDER BY fecha_prestamo DESC LIMIT 1",
            (usuario_id, isbn)
        ).fetchone()
        if row is None:
            return False

        prestamo_id = row[0]
        cur = conn.execute("DELETE FROM prestamos WHERE id=?", (prestamo_id,))

        still_active = conn.execute(
            "SELECT 1 FROM prestamos WHERE isbn=? AND fecha_devolucion IS NULL LIMIT 1",
            (isbn,)
        ).fetchone() is not None

        if not still_active:
            conn.execute("UPDATE libros SET disponible=1 WHERE isbn=?", (isbn,))

        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()

def eliminar_historial_devoluciones() -> int:
    """
    Elimina todos los préstamos con fecha_devolucion (historial).
    No modifica disponibilidad (ya estaban devueltos).
    """
    conn = conectar()
    try:
        cur = conn.execute("DELETE FROM prestamos WHERE fecha_devolucion IS NOT NULL")
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()
