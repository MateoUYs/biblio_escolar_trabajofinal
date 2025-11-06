from data.base_datos import conectar

def test_conectar_crea_tablas():
    conn = conectar()
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = {r[0] for r in cur.fetchall()}
    conn.close()
    assert {"libros", "usuarios", "prestamos"}.issubset(tablas)
