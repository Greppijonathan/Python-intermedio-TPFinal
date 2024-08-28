import sqlite3
import re


class MiBaseDatos:
    def __init__(self, db_name="mibase.db"):
        self.db_name = db_name

    def conexion(self):
        return sqlite3.connect(self.db_name)

    def crear_tabla(self):
        con = self.conexion()
        cursor = con.cursor()
        sql = """CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    material TEXT NOT NULL,
                    cantidad REAL,
                    color TEXT NOT NULL,
                    precio REAL,
                    fecha_ingreso TEXT,
                    descripcion TEXT
                )"""
        cursor.execute(sql)
        con.commit()
        con.close()

    def alta(self, material, cantidad, color, precio, fecha_ingreso, descripcion, tree):
        patron = "^[A-Za-záéíóú]*$"  # regex para el campo material
        if re.match(patron, material):
            con = self.conexion()
            cursor = con.cursor()
            data = (material, cantidad, color, precio, fecha_ingreso, descripcion)
            sql = """INSERT INTO productos (material, cantidad, color, precio, fecha_ingreso, descripcion)
                     VALUES (?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, data)
            con.commit()
            con.close()
            self.actualizar_treeview(tree)
        else:
            print("Error en campo material")

    def consultar(self):
        con = self.conexion()
        cursor = con.cursor()
        sql = "SELECT * FROM productos"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        for fila in resultado:
            print(fila)
        con.close()
        return resultado

    def borrar(self, tree):
        valor = tree.selection()
        item = tree.item(valor)
        mi_id = item['text']

        con = self.conexion()
        cursor = con.cursor()
        data = (mi_id,)
        sql = "DELETE FROM productos WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()
        con.close()
        tree.delete(valor)

    def actualizar_treeview(self, mitreview):
        records = mitreview.get_children()
        for element in records:
            mitreview.delete(element)

        sql = "SELECT * FROM productos ORDER BY id ASC"
        con = self.conexion()
        cursor = con.cursor()
        datos = cursor.execute(sql)
        resultado = datos.fetchall()
        con.close()

        for fila in resultado:
            mitreview.insert("", "end", text=fila[0], values=(
                fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]
            ))

    def modificar(self, id_producto, material, cantidad, color, precio, fecha_ingreso, descripcion):
        con = self.conexion()
        cursor = con.cursor()
        data = (material, cantidad, color, precio, fecha_ingreso, descripcion, id_producto)
        sql = """UPDATE productos
                 SET material = ?, cantidad = ?, color = ?, precio = ?, fecha_ingreso = ?, descripcion = ?
                 WHERE id = ?"""
        cursor.execute(sql, data)
        con.commit()
        con.close()


# Uso de la clase Database
db = MiBaseDatos()

try:
    db.crear_tabla()
except Exception as e:
    print(f"Hay un error: {e}")
