class Usuario:
    def __init__(self, id, nombre, tipo="alumno"):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo  # "alumno" o "docente"
        self.libros_prestados = []

    def __str__(self):
        return f"{self.nombre} ({self.tipo}, ID: {self.id})"