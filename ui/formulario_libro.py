import tkinter as tk
from tkinter import messagebox
from data.base_datos import agregar_usuario

class FormularioUsuario:
    def __init__(self, root):
        self.root = root
        self.root.title("Agregar Usuario")
        self.root.geometry("300x200")

        tk.Label(root, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(root)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Tipo:").grid(row=2, column=0, padx=5, pady=5)
        self.var_tipo = tk.StringVar(value="alumno")
        tk.OptionMenu(root, self.var_tipo, "alumno", "docente").grid(row=2, column=1, padx=5, pady=5)

        tk.Button(root, text="Agregar", command=self.agregar).grid(row=3, column=0, columnspan=2, pady=10)

    def agregar(self):
        id_usuario = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        tipo = self.var_tipo.get().strip()

        if not id_usuario or not nombre:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        agregar_usuario(id_usuario, nombre, tipo)
        messagebox.showinfo("Éxito", f"Usuario {nombre} agregado correctamente")
        self.root.destroy()
