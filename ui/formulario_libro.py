import tkinter as tk
from tkinter import messagebox
from models.libro import Libro
from data.base_datos import agregar_libro

class FormularioLibro:
    def __init__(self, root):
        self.root = root
        self.root.title("Agregar Libro")
        self.root.geometry("300x200")

        # Campos
        tk.Label(root, text="ISBN:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_isbn = tk.Entry(root)
        self.entry_isbn.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Título:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_titulo = tk.Entry(root)
        self.entry_titulo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Autor:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_autor = tk.Entry(root)
        self.entry_autor.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Género:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_genero = tk.Entry(root)
        self.entry_genero.grid(row=3, column=1, padx=5, pady=5)

        # Botón
        tk.Button(root, text="Agregar", command=self.agregar).grid(row=4, column=0, columnspan=2, pady=10)

    def agregar(self):
        isbn = self.entry_isbn.get()
        titulo = self.entry_titulo.get()
        autor = self.entry_autor.get()
        genero = self.entry_genero.get()

        if not all([isbn, titulo, autor, genero]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        libro = Libro(isbn, titulo, autor, genero)
        agregar_libro(libro)
        messagebox.showinfo("Éxito", f"Libro {titulo} agregado")
        self.root.destroy()