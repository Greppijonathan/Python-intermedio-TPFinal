import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from modelo import MiBaseDatos


class VistaControlador:
    def __init__(self, root):
        self.root = root
        self.root.title("Modulo intermedio")

        self.titulo = tk.Label(
            root, text="Control materiales 3D", bg="DarkOrchid3", fg="thistle1", height=1, width=60
        )
        self.titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=tk.W + tk.E)

        labels = ["Material", "Cantidad", "Color", "Precio", "Fecha de ingreso", "Descripcion"]
        for i, text in enumerate(labels):
            tk.Label(root, text=text).grid(row=i + 1, column=0, sticky=tk.W)

        # Estas variables se definen para tomar los datos de entrada
        self.material_val = tk.StringVar()
        self.cantidad_val = tk.DoubleVar()
        self.color_val = tk.StringVar()
        self.precio_val = tk.DoubleVar()
        self.fecha_val = tk.StringVar()
        self.descripcion_val = tk.StringVar()
        w_ancho = 20

        entradas = [
            self.material_val, self.cantidad_val, self.color_val,
            self.precio_val, self.fecha_val, self.descripcion_val
        ]
        for i, var in enumerate(entradas):
            tk.Entry(root, textvariable=var, width=w_ancho).grid(row=i + 1, column=1)

        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")
        self.tree.column("#0", width=90, minwidth=50, anchor=tk.W)
        self.tree.column("col1", width=200, minwidth=80)
        self.tree.column("col2", width=200, minwidth=80)
        self.tree.column("col3", width=200, minwidth=80)
        self.tree.column("col4", width=200, minwidth=80)
        self.tree.column("col5", width=200, minwidth=80)
        self.tree.column("col6", width=200, minwidth=80)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Material")
        self.tree.heading("col2", text="Cantidad")
        self.tree.heading("col3", text="Color")
        self.tree.heading("col4", text="Precio")
        self.tree.heading("col5", text="Fecha Ingreso")
        self.tree.heading("col6", text="Descripcion")
        self.tree.grid(row=11, column=0, columnspan=4)

        # Crear una instancia de la clase Database
        self.db = MiBaseDatos()

        self.boton_alta = tk.Button(
            root,
            text="Alta",
            width=20,
            command=lambda: self.db.alta(
                self.material_val.get(),
                self.cantidad_val.get(),
                self.color_val.get(),
                self.precio_val.get(),
                self.fecha_val.get(),
                self.descripcion_val.get(),
                self.tree,
            ),
        )
        self.boton_alta.grid(row=7, column=1)

        self.boton_consulta = tk.Button(root, text="Consultar", width=20, command=lambda: self.db.consultar())
        self.boton_consulta.grid(row=8, column=1)

        self.boton_borrar = tk.Button(root, text="Borrar", width=20, command=lambda: self.db.borrar(self.tree))
        self.boton_borrar.grid(row=9, column=1)

        self.boton_modificar = tk.Button(
            root,
            text="Modificar",
            width=20,
            command=lambda: self.modificar_producto()
        )
        self.boton_modificar.grid(row=10, column=1)

    def modificar_producto(self):
        selected_item = self.tree.selection()[0]
        item = self.tree.item(selected_item)
        mi_id = item['text']

        self.db.modificar(
            mi_id,
            self.material_val.get(),
            self.cantidad_val.get(),
            self.color_val.get(),
            self.precio_val.get(),
            self.fecha_val.get(),
            self.descripcion_val.get()
        )
        self.db.actualizar_treeview(self.tree)


if __name__ == "__main__":
    root = tk.Tk()
    app = VistaControlador(root)
    root.mainloop()
