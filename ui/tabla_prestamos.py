import tkinter as tk
from tkinter import ttk, messagebox
from data.base_datos import obtener_prestamos, obtener_usuarios, obtener_libros, registrar_prestamo

class TablaPrestamos:
    def __init__(self, root):
        self.root = root
        self.root.title("Préstamos")
        self.root.geometry("800x400")

        # ==========================
        # FORMULARIO REGISTRAR PRÉSTAMO
        # ==========================
        frame_form = ttk.Frame(self.root, padding="10")
        frame_form.pack(fill="x")

        # --- Usuario ---
        ttk.Label(frame_form, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.var_usuario = tk.StringVar()
        usuarios = obtener_usuarios()
        if usuarios:
            opciones_usuarios = [f"{u['id']} - {u['nombre']}" for u in usuarios]
            self.var_usuario.set(opciones_usuarios[0])
            ttk.OptionMenu(frame_form, self.var_usuario, *opciones_usuarios).grid(row=0, column=1, padx=5, pady=5)
        else:
            ttk.Label(frame_form, text="⚠ No hay usuarios cargados").grid(row=0, column=1)

        # --- Libro ---
        ttk.Label(frame_form, text="Libro:").grid(row=0, column=2, padx=5, pady=5)
        self.var_libro = tk.StringVar()
        libros = obtener_libros()
        disponibles = [f"{l['isbn']} - {l['titulo']}" for l in libros if l['disponible'] == 1]
        if disponibles:
            self.var_libro.set(disponibles[0])
            ttk.OptionMenu(frame_form, self.var_libro, *disponibles).grid(row=0, column=3, padx=5, pady=5)
        else:
            ttk.Label(frame_form, text="⚠ No hay libros disponibles").grid(row=0, column=3)

        # --- Botón ---
        ttk.Button(frame_form, text="Registrar Préstamo", command=self.registrar_prestamo).grid(row=0, column=4, padx=10, pady=5)

        # ==========================
        # TABLA DE PRÉSTAMOS
        # ==========================
        frame_tabla = ttk.Frame(self.root, padding="10")
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("ID", "ISBN", "Título", "Usuario", "Tipo", "Fecha Préstamo", "Fecha Devolución")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100, anchor="center")

        self.tabla.pack(fill="both", expand=True)
        self.cargar_prestamos()

    # ==========================
    # FUNCIONES
    # ==========================

    def cargar_prestamos(self):
        """Carga todos los préstamos en la tabla"""
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        prestamos = obtener_prestamos()
        for p in prestamos:
            self.tabla.insert("", "end", values=(
                p['id'],
                p['isbn'],
                p['titulo'],
                p['usuario'],
                p['tipo'],
                p['fecha_prestamo'],
                p['fecha_devolucion'] if p['fecha_devolucion'] else "—"
            ))

    def registrar_prestamo(self):
        """Registra un nuevo préstamo en la base de datos"""
        usuario_str = self.var_usuario.get()
        libro_str = self.var_libro.get()

        if not usuario_str or not libro_str:
            messagebox.showerror("Error", "Debe seleccionar un usuario y un libro.")
            return

        usuario_id = usuario_str.split(" - ")[0]
        isbn = libro_str.split(" - ")[0]

        exito = registrar_prestamo(isbn, usuario_id)
        if exito:
            messagebox.showinfo("Éxito", "Préstamo registrado correctamente.")
            self.cargar_prestamos()
        else:
            messagebox.showerror("Error", "No se pudo registrar el préstamo.")
