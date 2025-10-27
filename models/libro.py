class Libro:
    def __init__(self, isbn, titulo, autor, genero):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.disponible = True

    def __str__(self):
        return f"{self.titulo} - {self.autor} (ISBN: {self.isbn})"

    def prestar(self):
        if self.disponible:
            self.disponible = False
            return True
        return False

    def devolver(self):
        if not self.disponible:
            self.disponible = True
            return True
        return False