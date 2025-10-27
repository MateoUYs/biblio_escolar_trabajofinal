import sqlite3

def conectar():
    conn = sqlite3.connect('biblioteca.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            isbn TEXT PRIMARY KEY,
            titulo TEXT,
            autor TEXT,
            genero TEXT,
            disponible INTEGER DEFAULT 1
        )
    ''')
    return conn

def agregar_libro(libro):
    conn = conectar()
    try:
        conn.execute(
            "INSERT INTO libros (isbn, titulo, autor, genero, disponible) VALUES (?, ?, ?, ?, ?)",
            (libro.isbn, libro.titulo, libro.autor, libro.genero, 1 if libro.disponible else 0)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Error: El ISBN {libro.isbn} ya existe.")
    finally:
        conn.close()

def obtener_libros():
    conn = conectar()
    cursor = conn.execute("SELECT * FROM libros")
    libros = [dict(zip(['isbn', 'titulo', 'autor', 'genero', 'disponible'], row)) for row in cursor.fetchall()]
    conn.close()
    return libros