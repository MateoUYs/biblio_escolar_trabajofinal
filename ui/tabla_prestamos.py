import tkinter as tk
from tkinter import ttk, messagebox
from data.base_datos import obtener_prestamos, obtener_usuarios, obtener_libros, registrar_prestamo, cerrar_prestamo

class TablaPrestamos:
    def __init__(self, root):
        self.root = root
        self.root.title("Préstamos")
        self.root.geometry("850x450")

        # ==========================
        # FORMULARIO REGISTRAR PRÉSTAMO
        # ==========================
        frame_form = ttk.Frame(self.root, padding="10")
        frame_form.pack(fill="x")

        # Usuario
        ttk.Label(frame_form, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.var_usuario = tk.StringVar()
        usuarios = obtener_usuarios()
        if usuarios:
            opciones_usuarios = [f"{u['id']} - {u['nombre']}" for u in usuarios]
            self.var_usuario.set(opciones_usuarios[0])
            ttk.OptionMenu(frame_form, self.var_usuario, *opciones_usuarios).grid(row=0, column=1, padx=5, pady=5)
        else:
            ttk.Label(frame_form, text="⚠ No hay usuarios cargados").grid(row=0, column=1)

        # Libro
        ttk.Label(frame_form, text="Libro:").grid(row=0, column=2, padx=5, pady=5)
        self.var_libro = tk.StringVar()
        libros = obtener_libros()
        disponibles = [f"{l['isbn']} - {l['titulo']}" for l in libros if l['disponible'] == 1]
        if disponibles:
            self.var_libro.set(disponibles[0])
            ttk.OptionMenu(frame_form, self.var_libro, *disponibles).grid(row=0, column=3, padx=5, pady=5)
        else:
            ttk.Label(frame_form, text="⚠ No hay libros disponibles").grid(row=0, column=3)

        ttk.Button(frame_form, text="Registrar Préstamo", command=self.registrar_prestamo).grid(row=0, column=4, padx=10, pady=5)

        # ==========================
        # TABLA DE PRÉSTAMOS
        # ==========================
        frame_tabla = ttk.Frame(self.root, padding="10")
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("ID", "ISBN", "Título", "Usuario", "Tipo", "Fecha Préstamo", "Fecha Devolución")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="browse")
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=110, anchor="center")

        self.tabla.pack(fill="both", expand=True)

        # ==========================
        # BOTÓN DEVOLVER
        # ==========================
        frame_botones = ttk.Frame(self.root, padding="10")
        frame_botones.pack(fill="x")

        ttk.Button(frame_botones, text="Devolver Préstamo", command=self.devolver_prestamo).pack(side="right")

        self.cargar_prestamos()

    # ==========================
    # FUNCIONES
    # ==========================

    def cargar_prestamos(self):
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

    def devolver_prestamo(self):
        selected = self.tabla.focus()
        if not selected:
            messagebox.showerror("Error", "Seleccione un préstamo para devolver.")
            return

        valores = self.tabla.item(selected, "values")
        prestamo_id = valores[0]
        fecha_devolucion = valores[6]

        if fecha_devolucion != "—":
            messagebox.showwarning("Aviso", "Este préstamo ya fue devuelto.")
            return

        exito = cerrar_prestamo(prestamo_id)
        if exito:
            messagebox.showinfo("Éxito", "Préstamo devuelto correctamente.")
            self.cargar_prestamos()
        else:
            messagebox.showerror("Error", "No se pudo devolver el préstamo.")
