from data.base_datos import conectar, agregar_usuario, eliminar_prestamo_por_usuario_isbn
from data.base_datos import registrar_prestamo, cerrar_prestamo
from types import SimpleNamespace

def test_flujo_prestamo_y_eliminacion_activo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # Semilla
    from data.base_datos import agregar_libro
    agregar_usuario("u1","Ana","estudiante")
    libro = SimpleNamespace(isbn="9780001112223", titulo="Py Fácil", autor="M. Gómez", genero="Tecnología", disponible=True)
    agregar_libro(libro)
    assert registrar_prestamo("9780001112223", "u1") is True
    # Eliminar préstamo ACTIVO por (usuario, isbn)
    assert eliminar_prestamo_por_usuario_isbn("u1","9780001112223") is True
