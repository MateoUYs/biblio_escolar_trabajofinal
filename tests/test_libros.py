from data.base_datos import conectar, agregar_usuario, agregar_libro, obtener_libros

def test_agregar_y_listar_libro(tmp_path, monkeypatch):
    # Forzamos DB en carpeta temporal
    monkeypatch.chdir(tmp_path)
    from data.base_datos import agregar_libro as add, conectar as cn
    class L:  # mini objeto libro
        def __init__(self): 
            self.isbn="9781234567897"; self.titulo="Demo"; self.autor="Autor"; self.genero="Educación"; self.disponible=True
    add(L())
    libros = obtener_libros()
    assert any(l["isbn"]=="9781234567897" for l in libros)
