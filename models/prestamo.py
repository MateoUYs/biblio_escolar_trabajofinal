class Prestamo:
    def __init__(self, libro, usuario, fecha_prestamo, fecha_devolucion=None):
        self.libro = libro
        self.usuario = usuario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

    def __str__(self):
        estado = "Devuelto" if self.fecha_devolucion else "Prestado"
        return f"Prestamo: {self.libro} a {self.usuario} - {estado} ({self.fecha_prestamo})"