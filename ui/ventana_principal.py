import tkinter as tk
from tkinter import ttk
from ui.formulario_libro import FormularioLibro
from data.base_datos import obtener_libros
from ui.tabla_prestamos import TablaPrestamos


class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("BiblioEscolar - Gestión de Biblioteca")
        self.root.geometry("600x400")

        # Menú
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Salir", command=self.root.quit)

        menu_libros = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Libros", menu=menu_libros)
        menu_libros.add_command(label="Agregar Libro", command=self.abrir_formulario_libro)
        menu_libros.add_command(label="Actualizar Lista", command=self.actualizar_tabla)

        # Área de trabajo
        self.frame_principal = ttk.Frame(self.root, padding="10")
        self.frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        tk.Label(self.frame_principal, text="Bienvenido a BiblioEscolar", font=("Arial", 14)).grid(row=0, column=0, pady=10)

        # Tabla de libros
        self.tabla_libros = ttk.Treeview(self.frame_principal, columns=("ISBN", "Título", "Autor", "Género", "Disponible"), show="headings")
        self.tabla_libros.heading("ISBN", text="ISBN")
        self.tabla_libros.heading("Título", text="Título")
        self.tabla_libros.heading("Autor", text="Autor")
        self.tabla_libros.heading("Género", text="Género")
        self.tabla_libros.heading("Disponible", text="Disponible")
        self.tabla_libros.column("ISBN", width=80)
        self.tabla_libros.column("Título", width=150)
        self.tabla_libros.column("Autor", width=100)
        self.tabla_libros.column("Género", width=100)
        self.tabla_libros.column("Disponible", width=80)
        self.tabla_libros.grid(row=1, column=0, pady=10)

        # Cargar libros al inicio
        self.actualizar_tabla()

    def abrir_formulario_libro(self):
        formulario = tk.Toplevel(self.root)
        FormularioLibro(formulario)

    def actualizar_tabla(self):
        # Limpiar tabla
        for item in self.tabla_libros.get_children():
            self.tabla_libros.delete(item)
        # Cargar libros desde la base de datos
        libros = obtener_libros()
        for libro in libros:
            self.tabla_libros.insert("", "end", values=(
                libro["isbn"],
                libro["titulo"],
                libro["autor"],
                libro["genero"],
                "Sí" if libro["disponible"] else "No"
            ))

def iniciar():
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar()