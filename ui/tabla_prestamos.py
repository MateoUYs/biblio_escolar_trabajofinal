import tkinter as tk
from tkinter import ttk, messagebox
from data.base_datos import (
    obtener_prestamos,
    obtener_usuarios,
    obtener_libros,
    registrar_prestamo,
    cerrar_prestamo
)

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
        self.menu_usuarios = None
        self.cargar_usuarios(frame_form)

        # Libro
        ttk.Label(frame_form, text="Libro:").grid(row=0, column=2, padx=5, pady=5)
        self.var_libro = tk.StringVar()
        self.menu_libros = None
        self.cargar_libros(frame_form)

        ttk.Button(
            frame_form,
            text="Registrar Préstamo",
            command=self.registrar_prestamo
        ).grid(row=0, column=4, padx=10, pady=5)

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
    # FUNCIONES AUXILIARES
    # ==========================

    def cargar_usuarios(self, frame_form):
        usuarios = obtener_usuarios()
        if usuarios:
            opciones_usuarios = [f"{u['id']} - {u['nombre']}" for u in usuarios]
            self.var_usuario.set("")  # No se selecciona nada por defecto
            if self.menu_usuarios:
                self.menu_usuarios.destroy()
            self.menu_usuarios = ttk.OptionMenu(frame_form, self.var_usuario, "", *opciones_usuarios)
            self.menu_usuarios.grid(row=0, column=1, padx=5, pady=5)
        else:
            ttk.Label(frame_form, text="⚠ No hay usuarios cargados").grid(row=0, column=1)

    def cargar_libros(self, frame_form):
        libros = obtener_libros()
        disponibles = [f"{l['isbn']} - {l['titulo']}" for l in libros if l['disponible'] == 1]
        if disponibles:
            self.var_libro.set("")  # No se selecciona nada por defecto
            if self.menu_libros:
                self.menu_libros.destroy()
            self.menu_libros = ttk.OptionMenu(frame_form, self.var_libro, "", *disponibles)
            self.menu_libros.grid(row=0, column=3, padx=5, pady=5)
        else:
            ttk.Label(frame_form, text="⚠ No hay libros disponibles").grid(row=0, column=3)

    # ==========================
    # FUNCIONES PRINCIPALES
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

        # 🔄 Actualizar combobox de libros después de registrar préstamos
        self.cargar_libros(self.menu_libros.master)

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
            # Limpiar selección para permitir volver a elegir otro
            self.var_usuario.set("")
            self.var_libro.set("")
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
