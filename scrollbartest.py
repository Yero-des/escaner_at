import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("400x300")

frame_tabla = ttk.Frame(root)
frame_tabla.pack(fill="both", expand=True, padx=8, pady=8)

# Scrollbar vertical
scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")

# Treeview
tree = ttk.Treeview(
    frame_tabla,
    columns=("Nombre", "Acciones"),
    show="headings",
    yscrollcommand=scroll_y.set
)
tree.heading("Nombre", text="Nombre")
tree.heading("Acciones", text="Acciones")
tree.column("Nombre", width=220, anchor="w")
tree.column("Acciones", width=100, anchor="center")

# Vincular scrollbar
scroll_y.config(command=tree.yview)

# Empaquetar
tree.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

# Insertar datos de prueba (muchos para que aparezca scroll)
for i in range(30):
    tree.insert("", "end", values=(f"Opción {i+1}", "Eliminar"))

# --- Ocultar scrollbar si no es necesario ---
def actualizar_scrollbar():
    if tree.yview() == (0.0, 1.0):  # Todo visible
        scroll_y.pack_forget()
    else:
        scroll_y.pack(side="right", fill="y")

# Revisar cuando cambia el contenido
tree.bind("<Configure>", lambda e: actualizar_scrollbar())
tree.bind("<<TreeviewSelect>>", lambda e: actualizar_scrollbar())

root.mainloop()
