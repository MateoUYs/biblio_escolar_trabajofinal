from data.base_datos import agregar_usuario, obtener_usuarios, es_docente

def test_agregar_usuario_y_es_docente(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    agregar_usuario("10","Jorge","docente")
    usuarios = obtener_usuarios()
    assert any(u["id"]=="10" for u in usuarios)
    assert es_docente("10") is True
