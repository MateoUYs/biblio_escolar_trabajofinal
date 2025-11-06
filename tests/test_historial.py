from data.base_datos import agregar_usuario, eliminar_historial_devoluciones
from data.base_datos import registrar_prestamo, cerrar_prestamo
from types import SimpleNamespace

def test_eliminar_historial(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    from data.base_datos import agregar_libro
    agregar_usuario("u2","Luis","estudiante")
    libro = SimpleNamespace(isbn="9789998887776", titulo="Hist Edu", autor="A. Pérez", genero="Educación", disponible=True)
    agregar_libro(libro)
    registrar_prestamo("9789998887776", "u2")
    # Cerramos el préstamo para que pase a historial
    from data.base_datos import conectar
    conn = conectar()
    pid = conn.execute("SELECT id FROM prestamos LIMIT 1").fetchone()[0]
    conn.close()
    assert cerrar_prestamo(pid) is True
    borrados = eliminar_historial_devoluciones()
    assert borrados >= 1
