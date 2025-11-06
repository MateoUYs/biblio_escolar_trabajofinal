import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import messagebox
from data.base_datos import obtener_usuario

class FormLoginDocente:
    """
    Ventana de login mínima por ID.
    Si el usuario existe y es 'docente', ejecuta on_login(usuario_dict) y cierra.
    """
    def __init__(self, root, on_login):
        self.root = root
        self.on_login = on_login

        self.root.title("Iniciar sesión (Docente)")
        self.root.geometry("320x150")

        tk.Label(root, text="ID de usuario:").grid(row=0, column=0, padx=8, pady=(12, 6), sticky="e")
        self.entry_id = tk.Entry(root)
        self.entry_id.grid(row=0, column=1, padx=8, pady=(12, 6))

        tk.Button(root, text="Ingresar", command=self._login).grid(row=1, column=0, columnspan=2, pady=12)

    def _login(self):
        user_id = self.entry_id.get().strip()
        if not user_id:
            messagebox.showerror("Error", "Ingresá tu ID de usuario.")
            return

        usuario = obtener_usuario(user_id)
        if not usuario:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return

        if usuario["tipo"] != "docente":
            messagebox.showerror("Permisos", "Solo pueden iniciar sesión los docentes.")
            return

        # OK
        self.on_login(usuario)   # Notificamos a la ventana princ
        messagebox.showinfo("Sesión iniciada", f"Bienvenido/a {usuario['nombre']} (Docente).")
        self.root.destroy()
        
