import json
import os
from datetime import datetime
from database import conectar, desconectar
from logger import log_info, log_error

def generar_backup():
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM contactos")
        contactos = [{"id": c[0], "nombre": c[1], "telefono": c[2], "email": c[3]} for c in cursor.fetchall()]

        cursor.execute("SELECT * FROM categorias")
        categorias = [{"id": c[0], "nombre": c[1]} for c in cursor.fetchall()]

        cursor.execute("SELECT * FROM productos")
        productos = [{"id": p[0], "nombre": p[1], "precio": p[2], "stock": p[3], "categoria_id": p[4]} for p in cursor.fetchall()]

        desconectar(conexion)

        datos = {
            "contactos": contactos,
            "categorias": categorias,
            "productos": productos
        }

        nombre_archivo = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)

        log_info(f"Backup generado: {nombre_archivo}")
        print(f"Backup guardado como: {nombre_archivo}")

    except Exception as e:
        log_error(f"Error al generar backup: {e}")
        print(f"Error: {e}")

def restaurar_backup(nombre_archivo):
    try:
        if not os.path.exists(nombre_archivo):
            print("El archivo no existe.")
            return

        with open(nombre_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM productos")
        cursor.execute("DELETE FROM categorias")
        cursor.execute("DELETE FROM contactos")

        for c in datos.get("contactos", []):
            cursor.execute("INSERT INTO contactos (id, nombre, telefono, email) VALUES (?, ?, ?, ?)",
                           (c["id"], c["nombre"], c["telefono"], c["email"]))

        for c in datos.get("categorias", []):
            cursor.execute("INSERT INTO categorias (id, nombre) VALUES (?, ?)",
                           (c["id"], c["nombre"]))

        for p in datos.get("productos", []):
            cursor.execute("INSERT INTO productos (id, nombre, precio, stock, categoria_id) VALUES (?, ?, ?, ?, ?)",
                           (p["id"], p["nombre"], p["precio"], p["stock"], p["categoria_id"]))

        conexion.commit()
        desconectar(conexion)

        log_info(f"Backup restaurado desde: {nombre_archivo}")
        print(f"Datos restaurados correctamente desde {nombre_archivo}")

    except Exception as e:
        log_error(f"Error al restaurar backup: {e}")
        print(f"Error: {e}")