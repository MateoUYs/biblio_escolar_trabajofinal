import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt  # para el gráfico
from ui.formulario_libro import FormularioLibro
from ui.formulario_usuario import FormularioUsuario
from ui.tabla_prestamos import TablaPrestamos
from ui.form_login import FormLoginDocente
from data.base_datos import (
    obtener_libros, es_docente, eliminar_libro,
    eliminar_usuario, obtener_usuarios,
    obtener_prestamos, eliminar_prestamo_por_usuario_isbn,
    eliminar_historial_devoluciones
)

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("BiblioEscolar - Gestión de Biblioteca")
        self.root.geometry("900x560")

        # ===== Estilo general (look bibliotecoso) =====
        self.root.configure(bg="#f9f6ef")  # fondo papel suave
        # Estilo de menús
        self.root.option_add("*Menu.background", "#f3e6d0")        # beige papel
        self.root.option_add("*Menu.foreground", "#3e2f1c")        # marrón madera
        self.root.option_add("*Menu.activeBackground", "#e0c8a0")  # hover
        self.root.option_add("*Menu.activeForeground", "#000000")
        self.root.option_add("*Menu.font", ("Segoe UI", 10, "bold"))

        # Estilo básico ttk para que combine (opcional, suave)
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background="#f9f6ef")
        style.configure("TLabel", background="#f9f6ef", foreground="#2c2418")
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Treeview", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        # Estado de sesión (docente logueado)
        self.usuario_actual = None  # dict: {"id","nombre","tipo"} o None

        # ===== Menú =====
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Salir", command=self.root.quit)

        menu_libros = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Libros", menu=menu_libros)
        menu_libros.add_command(label="Agregar Libro", command=self.abrir_formulario_libro)
        menu_libros.add_command(label="Actualizar Lista", command=self.actualizar_tabla)
        menu_libros.add_separator()
        menu_libros.add_command(label="Eliminar Libro (docente)", command=self.abrir_eliminar_libro)
        menu_libros.add_separator()
        menu_libros.add_command(label="Gráfico por género", command=self.mostrar_grafico_libros_por_genero)

        menu_usuarios = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Usuarios", menu=menu_usuarios)
        menu_usuarios.add_command(label="Agregar Usuario", command=self.abrir_formulario_usuario)
        menu_usuarios.add_separator()
        menu_usuarios.add_command(label="Eliminar Usuario (docente)", command=self.abrir_eliminar_usuario)

        menu_prestamos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Préstamos", menu=menu_prestamos)
        menu_prestamos.add_command(label="Ver / Registrar Préstamos", command=self.abrir_tabla_prestamos)
        menu_prestamos.add_separator()
        menu_prestamos.add_command(label="Eliminar Préstamo (Usuario+ISBN) (docente)", command=self.abrir_eliminar_prestamo)
        menu_prestamos.add_command(label="Eliminar HISTORIAL de devoluciones (docente)", command=self.abrir_eliminar_historial)

        menu_sesion = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sesión", menu=menu_sesion)
        menu_sesion.add_command(label="Iniciar sesión (Docente)", command=self.abrir_login_docente)
        menu_sesion.add_command(label="Cerrar sesión", command=self.cerrar_sesion)

        # ===== Layout base con GRID =====
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        cont = ttk.Frame(self.root, padding=10)
        cont.grid(row=0, column=0, sticky="nsew")
        cont.rowconfigure(1, weight=1)   # fila de la tabla crece
        cont.columnconfigure(0, weight=1)

        ttk.Label(cont, text="Bienvenido a BiblioEscolar", font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, pady=(0, 8), sticky="w"
        )

        # Tabla + scrollbar
        tabla_frame = ttk.Frame(cont)
        tabla_frame.grid(row=1, column=0, sticky="nsew")
        tabla_frame.rowconfigure(0, weight=1)
        tabla_frame.columnconfigure(0, weight=1)

        self.tabla_libros = ttk.Treeview(
            tabla_frame,
            columns=("ISBN", "Título", "Autor", "Género", "Disponible"),
            show="headings", height=12
        )
        self.tabla_libros.heading("ISBN", text="ISBN")
        self.tabla_libros.heading("Título", text="Título")
        self.tabla_libros.heading("Autor", text="Autor")
        self.tabla_libros.heading("Género", text="Género")
        self.tabla_libros.heading("Disponible", text="Disponible")

        self.tabla_libros.column("ISBN", width=120, anchor="w")
        self.tabla_libros.column("Título", width=260, anchor="w")
        self.tabla_libros.column("Autor", width=200, anchor="w")
        self.tabla_libros.column("Género", width=150, anchor="w")
        self.tabla_libros.column("Disponible", width=110, anchor="center")

        vsb = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_libros.yview)
        self.tabla_libros.configure(yscrollcommand=vsb.set)
        self.tabla_libros.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        # Botonera
        botones = ttk.Frame(cont)
        botones.grid(row=2, column=0, pady=8, sticky="w")
        ttk.Button(botones, text="Agregar Libro", command=self.abrir_formulario_libro).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(botones, text="Agregar Usuario", command=self.abrir_formulario_usuario).grid(row=0, column=1, padx=6)
        ttk.Button(botones, text="Préstamos", command=self.abrir_tabla_prestamos).grid(row=0, column=2, padx=6)

        # Barra de estado (docente logueado)
        self.status = ttk.Label(cont, text="Sesión: Invitado", relief="sunken", anchor="w")
        self.status.grid(row=3, column=0, sticky="we", pady=(6, 0))

        self.actualizar_tabla()

    # ===== Sesión =====
    def abrir_login_docente(self):
        win = tk.Toplevel(self.root)
        FormLoginDocente(win, on_login=self._set_usuario_actual)

    def _set_usuario_actual(self, usuario):
        self.usuario_actual = usuario  # dict con id/nombre/tipo
        self._refrescar_status()

    def cerrar_sesion(self):
        self.usuario_actual = None
        self._refrescar_status()
        messagebox.showinfo("Sesión", "Sesión cerrada.")

    def _refrescar_status(self):
        if self.usuario_actual:
            u = self.usuario_actual
            self.status.config(text=f"Docente: {u['nombre']} (ID: {u['id']})")
        else:
            self.status.config(text="Sesión: Invitado")

    # ===== Acciones UI =====
    def abrir_formulario_libro(self):
        ventana = tk.Toplevel(self.root)
        FormularioLibro(ventana)

    def abrir_formulario_usuario(self):
        ventana = tk.Toplevel(self.root)
        FormularioUsuario(ventana)

    def abrir_tabla_prestamos(self):
        ventana = tk.Toplevel(self.root)
        TablaPrestamos(ventana)

    # -------- Eliminar LIBRO (docente) --------
    def abrir_eliminar_libro(self):
        win = tk.Toplevel(self.root)
        win.title("Eliminar Libro (solo docente)")
        win.geometry("400x200")

        if self.usuario_actual and self.usuario_actual.get("tipo") == "docente":
            tk.Label(win, text=f"Docente activo: {self.usuario_actual['nombre']} (ID: {self.usuario_actual['id']})")\
                .grid(row=0, column=0, columnspan=2, padx=8, pady=(12, 6), sticky="w")

            tk.Label(win, text="ISBN del libro:").grid(row=1, column=0, padx=8, pady=8, sticky="e")
            entry_isbn = tk.Entry(win)
            entry_isbn.grid(row=1, column=1, padx=8, pady=8)

            def _eliminar():
                isbn = entry_isbn.get().strip()
                if not isbn:
                    messagebox.showerror("Error", "Ingresá el ISBN.")
                    return
                ok = eliminar_libro(isbn)
                if ok:
                    messagebox.showinfo("Éxito", f"Se eliminó el libro ISBN {isbn}.")
                    win.destroy()
                    self.actualizar_tabla()
                else:
                    messagebox.showwarning(
                        "No eliminado",
                        "No se pudo eliminar.\n"
                        "Posibles causas:\n"
                        "• Tiene un préstamo activo.\n"
                        "• El ISBN no existe."
                    )

            ttk.Button(win, text="Eliminar", command=_eliminar).grid(row=2, column=0, columnspan=2, pady=12)

        else:
            tk.Label(win, text="ID Docente:").grid(row=0, column=0, padx=8, pady=(12, 6), sticky="e")
            entry_id = tk.Entry(win)
            entry_id.grid(row=0, column=1, padx=8, pady=(12, 6))

            tk.Label(win, text="ISBN del libro:").grid(row=1, column=0, padx=8, pady=8, sticky="e")
            entry_isbn = tk.Entry(win)
            entry_isbn.grid(row=1, column=1, padx=8, pady=8)

            def _eliminar():
                docente_id = entry_id.get().strip()
                isbn = entry_isbn.get().strip()
                if not docente_id or not isbn:
                    messagebox.showerror("Error", "Completá todos los campos.")
                    return
                if not es_docente(docente_id):
                    messagebox.showerror("Permisos", "El ID ingresado no corresponde a un docente.")
                    return
                ok = eliminar_libro(isbn)
                if ok:
                    messagebox.showinfo("Éxito", f"Se eliminó el libro ISBN {isbn}.")
                    win.destroy()
                    self.actualizar_tabla()
                else:
                    messagebox.showwarning(
                        "No eliminado",
                        "No se pudo eliminar.\n"
                        "Posibles causas:\n"
                        "• Tiene un préstamo activo.\n"
                        "• El ISBN no existe."
                    )

            ttk.Button(win, text="Eliminar", command=_eliminar).grid(row=2, column=0, columnspan=2, pady=12)

    # -------- Eliminar USUARIO (docente) con listado de usuarios --------
    def abrir_eliminar_usuario(self):
        win = tk.Toplevel(self.root)
        win.title("Eliminar Usuario (solo docente)")
        win.geometry("600x380")

        def cargar_tabla(tabla_widget):
            tabla_widget.delete(*tabla_widget.get_children())
            usuarios = obtener_usuarios()
            for u in usuarios:
                tabla_widget.insert("", "end", values=(u["id"], u["nombre"], u["tipo"]))

        if self.usuario_actual and self.usuario_actual.get("tipo") == "docente":
            tk.Label(win, text=f"Docente activo: {self.usuario_actual['nombre']} (ID: {self.usuario_actual['id']})")\
                .grid(row=0, column=0, columnspan=3, padx=8, pady=(12, 6), sticky="w")

            tk.Label(win, text="ID del usuario a eliminar:").grid(row=1, column=0, padx=8, pady=8, sticky="e")
            entry_target = tk.Entry(win)
            entry_target.grid(row=1, column=1, padx=8, pady=8, sticky="w")

            frame_tabla = ttk.Frame(win)
            frame_tabla.grid(row=2, column=0, columnspan=3, padx=10, pady=8, sticky="nsew")
            frame_tabla.rowconfigure(0, weight=1)
            frame_tabla.columnconfigure(0, weight=1)

            cols = ("ID", "Nombre", "Tipo")
            tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=10)
            for c in cols:
                tabla.heading(c, text=c)
                tabla.column(c, width=180 if c != "Tipo" else 100, anchor="center")
            tabla.grid(row=0, column=0, sticky="nsew")

            vsb = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
            tabla.configure(yscrollcommand=vsb.set)
            vsb.grid(row=0, column=1, sticky="ns")

            def on_dclick_user(_e):
                sel = tabla.selection()
                if sel:
                    values = tabla.item(sel[0], "values")
                    entry_target.delete(0, tk.END)
                    entry_target.insert(0, values[0])

            tabla.bind("<Double-1>", on_dclick_user)

            cargar_tabla(tabla)

            def _eliminar_u():
                target_id = entry_target.get().strip()
                if not target_id:
                    messagebox.showerror("Error", "Ingresá el ID del usuario a eliminar.")
                    return
                if target_id == self.usuario_actual["id"]:
                    messagebox.showwarning("Aviso", "No podés eliminar tu propio usuario mientras estás logueado.")
                    return
                ok = eliminar_usuario(target_id)
                if ok:
                    messagebox.showinfo("Éxito", f"Se eliminó el usuario ID {target_id}.")
                    cargar_tabla(tabla)
                    entry_target.delete(0, tk.END)
                else:
                    messagebox.showwarning(
                        "No eliminado",
                        "No se pudo eliminar.\n"
                        "Posibles causas:\n"
                        "• El usuario no existe.\n"
                        "• Tiene préstamos activos o historial asociado."
                    )

            ttk.Button(win, text="Eliminar Usuario", command=_eliminar_u).grid(row=1, column=2, padx=8, pady=8, sticky="w")

        else:
            tk.Label(win, text="ID Docente:").grid(row=0, column=0, padx=8, pady=(12, 6), sticky="e")
            entry_doc = tk.Entry(win)
            entry_doc.grid(row=0, column=1, padx=8, pady=(12, 6), sticky="w")

            tk.Label(win, text="ID del usuario a eliminar:").grid(row=1, column=0, padx=8, pady=8, sticky="e")
            entry_target = tk.Entry(win)
            entry_target.grid(row=1, column=1, padx=8, pady=8, sticky="w")

            frame_tabla = ttk.Frame(win)
            frame_tabla.grid(row=2, column=0, columnspan=3, padx=10, pady=8, sticky="nsew")
            frame_tabla.rowconfigure(0, weight=1)
            frame_tabla.columnconfigure(0, weight=1)

            cols = ("ID", "Nombre", "Tipo")
            tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=10)
            for c in cols:
                tabla.heading(c, text=c)
                tabla.column(c, width=180 if c != "Tipo" else 100, anchor="center")
            tabla.grid(row=0, column=0, sticky="nsew")

            vsb = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
            tabla.configure(yscrollcommand=vsb.set)
            vsb.grid(row=0, column=1, sticky="ns")

            def on_dclick_user(_e):
                sel = tabla.selection()
                if sel:
                    values = tabla.item(sel[0], "values")
                    entry_target.delete(0, tk.END)
                    entry_target.insert(0, values[0])

            tabla.bind("<Double-1>", on_dclick_user)

            cargar_tabla(tabla)

            def _eliminar_u():
                docente_id = entry_doc.get().strip()
                target_id = entry_target.get().strip()
                if not docente_id or not target_id:
                    messagebox.showerror("Error", "Completá todos los campos.")
                    return
                if not es_docente(docente_id):
                    messagebox.showerror("Permisos", "El ID ingresado no corresponde a un docente.")
                    return
                ok = eliminar_usuario(target_id)
                if ok:
                    messagebox.showinfo("Éxito", f"Se eliminó el usuario ID {target_id}.")
                    cargar_tabla(tabla)
                    entry_target.delete(0, tk.END)
                else:
                    messagebox.showwarning(
                        "No eliminado",
                        "No se pudo eliminar.\n"
                        "Posibles causas:\n"
                        "• El usuario no existe.\n"
                        "• Tiene préstamos activos o historial asociado."
                    )

            ttk.Button(win, text="Eliminar Usuario", command=_eliminar_u).grid(row=1, column=2, padx=8, pady=8, sticky="w")

    # -------- Eliminar PRÉSTAMO (docente) por (Usuario ID + ISBN) --------
    def abrir_eliminar_prestamo(self):
        win = tk.Toplevel(self.root)
        win.title("Eliminar Préstamo (solo docente)")
        win.geometry("1000x500")

        # ---------- Fila de inputs ----------
        inputs = ttk.Frame(win, padding=(8, 8))
        inputs.grid(row=0, column=0, sticky="we")
        for c in range(5):
            inputs.columnconfigure(c, weight=0)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(1, weight=1)

        row_top = 0
        if self.usuario_actual and self.usuario_actual.get("tipo") == "docente":
            ttk.Label(inputs, text=f"Docente activo: {self.usuario_actual['nombre']} (ID: {self.usuario_actual['id']})")\
                .grid(row=row_top, column=0, columnspan=5, sticky="w", pady=(0, 6))
        else:
            ttk.Label(inputs, text="ID Docente:").grid(row=row_top, column=0, sticky="e", padx=(0,6))
            entry_doc = ttk.Entry(inputs, width=18)
            entry_doc.grid(row=row_top, column=1, sticky="w", padx=(0,12))

        row_top += 1
        ttk.Label(inputs, text="Usuario ID:").grid(row=row_top, column=0, sticky="e", padx=(0,6))
        entry_uid = ttk.Entry(inputs, width=22)
        entry_uid.grid(row=row_top, column=1, sticky="w", padx=(0,12))

        ttk.Label(inputs, text="ISBN:").grid(row=row_top, column=2, sticky="e", padx=(0,6))
        entry_isbn = ttk.Entry(inputs, width=22)
        entry_isbn.grid(row=row_top, column=3, sticky="w", padx=(0,12))

        btn_eliminar = ttk.Button(inputs, text="Eliminar Préstamo")
        btn_eliminar.grid(row=row_top, column=4, sticky="w")

        # ---------- Tabla de préstamos ----------
        frame_tabla = ttk.Frame(win, padding=(8, 0))
        frame_tabla.grid(row=1, column=0, sticky="nsew")
        frame_tabla.rowconfigure(0, weight=1)
        frame_tabla.columnconfigure(0, weight=1)

        cols = ("ID", "ISBN", "Título", "UsuarioID", "Usuario", "Tipo", "Fecha préstamo", "Fecha devolución")
        tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=14)
        for c in cols:
            tabla.heading(c, text=c)
        ancho = {
            "ID": 60, "ISBN": 120, "Título": 240, "UsuarioID": 100, "Usuario": 160,
            "Tipo": 80, "Fecha préstamo": 160, "Fecha devolución": 160
        }
        for c in cols:
            tabla.column(c, width=ancho[c], anchor="center" if c in ("ID", "UsuarioID", "Tipo") else "w")
        tabla.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        def cargar_tabla():
            tabla.delete(*tabla.get_children())
            prestamos = obtener_prestamos()
            for p in prestamos:
                tabla.insert("", "end", values=(
                    p["id"], p["isbn"], p["titulo"], p.get("usuario_id", ""), p["usuario"], p["tipo"],
                    p["fecha_prestamo"], p["fecha_devolucion"] if p["fecha_devolucion"] else "—"
                ))
        cargar_tabla()

        def on_dclick_prestamo(_event):
            sel = tabla.selection()
            if not sel:
                return
            v = tabla.item(sel[0], "values")
            entry_uid.delete(0, tk.END)
            entry_uid.insert(0, v[3])  # UsuarioID
            entry_isbn.delete(0, tk.END)
            entry_isbn.insert(0, v[1])  # ISBN
        tabla.bind("<Double-1>", on_dclick_prestamo)

        def _eliminar_p():
            usuario_id = entry_uid.get().strip()
            isbn = entry_isbn.get().strip()
            if not usuario_id or not isbn:
                messagebox.showerror("Error", "Ingresá Usuario ID e ISBN.")
                return
            if not (self.usuario_actual and self.usuario_actual.get("tipo") == "docente"):
                docente_id = entry_doc.get().strip() if 'entry_doc' in locals() else ""
                if not docente_id:
                    messagebox.showerror("Error", "Ingresá el ID Docente.")
                    return
                if not es_docente(docente_id):
                    messagebox.showerror("Permisos", "El ID ingresado no corresponde a un docente.")
                    return
            ok = eliminar_prestamo_por_usuario_isbn(usuario_id, isbn)
            if ok:
                messagebox.showinfo("Éxito", f"Se eliminó el préstamo ACTIVO de Usuario '{usuario_id}' con ISBN {isbn}.")
                cargar_tabla()
                entry_uid.delete(0, tk.END)
                entry_isbn.delete(0, tk.END)
                self.actualizar_tabla()
            else:
                messagebox.showwarning(
                    "No eliminado",
                    "No se encontró un préstamo ACTIVO con ese Usuario ID y ese ISBN.\n"
                    "Verificá que el préstamo no esté ya devuelto o que los datos coincidan."
                )

        btn_eliminar.configure(command=_eliminar_p)

    # -------- Eliminar HISTORIAL de devoluciones (docente) --------
    def abrir_eliminar_historial(self):
        docente_ok = False
        if self.usuario_actual and self.usuario_actual.get("tipo") == "docente":
            docente_ok = True
        else:
            top = tk.Toplevel(self.root)
            top.title("Confirmación docente")
            tk.Label(top, text="ID Docente:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
            entry_doc = tk.Entry(top)
            entry_doc.grid(row=0, column=1, padx=10, pady=10)
            def _check():
                did = entry_doc.get().strip()
                if not did:
                    messagebox.showerror("Error", "Ingresá el ID Docente.")
                    return
                if not es_docente(did):
                    messagebox.showerror("Permisos", "El ID ingresado no corresponde a un docente.")
                    return
                nonlocal docente_ok
                docente_ok = True
                top.destroy()
            tk.Button(top, text="Continuar", command=_check).grid(row=1, column=0, columnspan=2, pady=(0,10))
            top.grab_set()
            top.wait_window()

        if not docente_ok:
            return

        if not messagebox.askyesno(
            "Eliminar historial",
            "Se eliminarán TODOS los préstamos con fecha de devolución (historial).\n"
            "Esta acción no se puede deshacer.\n\n¿Continuar?"
        ):
            return

        try:
            borrados = eliminar_historial_devoluciones()
            messagebox.showinfo("Listo", f"Se eliminaron {borrados} préstamos del historial.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el historial.\n{e}")
            return

        self.actualizar_tabla()

    # -------- Gráfico: libros por género --------
    def mostrar_grafico_libros_por_genero(self):
        """Muestra un gráfico de barras con la cantidad de libros por género."""
        libros = obtener_libros()
        if not libros:
            messagebox.showinfo("Sin datos", "No hay libros registrados en la base de datos.")
            return

        # Contar libros por género
        generos = {}
        for l in libros:
            genero = l["genero"] if l["genero"] else "Sin género"
            generos[genero] = generos.get(genero, 0) + 1

        # Gráfico (sin estilos específicos para cumplir buenas prácticas)
        plt.figure(figsize=(6, 4))
        plt.bar(generos.keys(), generos.values())
        plt.title("Cantidad de libros por género")
        plt.xlabel("Género")
        plt.ylabel("Cantidad de libros")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        plt.show()

    # -------- Utilidad --------
    def actualizar_tabla(self):
        for item in self.tabla_libros.get_children():
            self.tabla_libros.delete(item)

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
