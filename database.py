from queue import Queue
import sqlite3
from logger import log_info, log_error

DB_FILE = "contactos.db"
POOL_SIZE = 3

class ConnectionPool:
    def __init__(self, database, pool_size):
        self.pool = Queue(maxsize=pool_size)
        for _ in range(pool_size):
            conexion = sqlite3.connect(database, check_same_thread=False)
            self.pool.put(conexion)

    def get_conexion(self):
        return self.pool.get()

    def devolver_conexion(self, conexion):
        self.pool.put(conexion)

pool = ConnectionPool(DB_FILE, POOL_SIZE)

def conectar():
    return pool.get_conexion()

def desconectar(conexion):
    pool.devolver_conexion(conexion)

def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            email TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL,
            stock INTEGER,
            categoria_id INTEGER,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """)
    conexion.commit()
    desconectar(conexion)
    log_info("Tablas verificadas/creadas.")

# ── CONTACTOS ──────────────────────────────────────────

def crear_contacto(nombre, telefono, email):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO contactos (nombre, telefono, email) VALUES (?, ?, ?)",
                       (nombre, telefono, email))
        conexion.commit()
        desconectar(conexion)
        log_info(f"Contacto creado: {nombre} | {telefono} | {email}")
        print("Contacto guardado correctamente.")
    except Exception as e:
        log_error(f"Error al crear contacto: {e}")
        print(f"Error: {e}")

def ver_contactos():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM contactos")
        contactos = cursor.fetchall()
        desconectar(conexion)
        if not contactos:
            print("No hay contactos registrados.")
            return
        print("\n" + "-" * 50)
        for c in contactos:
            print(f"ID: {c[0]} | Nombre: {c[1]} | Tel: {c[2]} | Email: {c[3]}")
        print("-" * 50)
        log_info("Se consultaron todos los contactos.")
    except Exception as e:
        log_error(f"Error al ver contactos: {e}")
        print(f"Error: {e}")

def actualizar_contacto(id, nombre, telefono, email):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("UPDATE contactos SET nombre=?, telefono=?, email=? WHERE id=?",
                       (nombre, telefono, email, id))
        conexion.commit()
        desconectar(conexion)
        log_info(f"Contacto ID {id} actualizado.")
        print("Contacto actualizado correctamente.")
    except Exception as e:
        log_error(f"Error al actualizar contacto: {e}")
        print(f"Error: {e}")

def eliminar_contacto(id):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM contactos WHERE id=?", (id,))
        conexion.commit()
        desconectar(conexion)
        log_info(f"Contacto ID {id} eliminado.")
        print("Contacto eliminado correctamente.")
    except Exception as e:
        log_error(f"Error al eliminar contacto: {e}")
        print(f"Error: {e}")

def truncar_contactos():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM contactos")
        conexion.commit()
        desconectar(conexion)
        log_info("Tabla contactos truncada.")
        print("Tabla contactos vaciada.")
    except Exception as e:
        log_error(f"Error al truncar contactos: {e}")
        print(f"Error: {e}")

# ── CATEGORIAS ─────────────────────────────────────────

def crear_categoria(nombre):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
        conexion.commit()
        desconectar(conexion)
        log_info(f"Categoría creada: {nombre}")
        print("Categoría guardada correctamente.")
    except Exception as e:
        log_error(f"Error al crear categoría: {e}")
        print(f"Error: {e}")

def ver_categorias():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM categorias")
        categorias = cursor.fetchall()
        desconectar(conexion)
        if not categorias:
            print("No hay categorías registradas.")
            return
        print("\n" + "-" * 30)
        for c in categorias:
            print(f"ID: {c[0]} | Nombre: {c[1]}")
        print("-" * 30)
        log_info("Se consultaron todas las categorías.")
    except Exception as e:
        log_error(f"Error al ver categorías: {e}")
        print(f"Error: {e}")

def eliminar_categoria(id):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM categorias WHERE id=?", (id,))
        conexion.commit()
        desconectar(conexion)
        log_info(f"Categoría ID {id} eliminada.")
        print("Categoría eliminada correctamente.")
    except Exception as e:
        log_error(f"Error al eliminar categoría: {e}")
        print(f"Error: {e}")

def truncar_categorias():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM categorias")
        conexion.commit()
        desconectar(conexion)
        log_info("Tabla categorias truncada.")
        print("Tabla categorias vaciada.")
    except Exception as e:
        log_error(f"Error al truncar categorias: {e}")
        print(f"Error: {e}")

# ── PRODUCTOS ──────────────────────────────────────────

def crear_producto(nombre, precio, stock, categoria_id):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio, stock, categoria_id) VALUES (?, ?, ?, ?)",
                       (nombre, precio, stock, categoria_id))
        conexion.commit()
        desconectar(conexion)
        log_info(f"Producto creado: {nombre} | Precio: {precio} | Stock: {stock}")
        print("Producto guardado correctamente.")
    except Exception as e:
        log_error(f"Error al crear producto: {e}")
        print(f"Error: {e}")

def ver_productos():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.id, p.nombre, p.precio, p.stock, c.nombre
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
        """)
        productos = cursor.fetchall()
        desconectar(conexion)
        if not productos:
            print("No hay productos registrados.")
            return
        print("\n" + "-" * 60)
        for p in productos:
            print(f"ID: {p[0]} | {p[1]} | Precio: {p[2]} | Stock: {p[3]} | Cat: {p[4]}")
        print("-" * 60)
        log_info("Se consultaron todos los productos.")
    except Exception as e:
        log_error(f"Error al ver productos: {e}")
        print(f"Error: {e}")

def actualizar_producto(id, nombre, precio, stock, categoria_id):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("UPDATE productos SET nombre=?, precio=?, stock=?, categoria_id=? WHERE id=?",
                       (nombre, precio, stock, categoria_id, id))
        conexion.commit()
        desconectar(conexion)
        log_info(f"Producto ID {id} actualizado.")
        print("Producto actualizado correctamente.")
    except Exception as e:
        log_error(f"Error al actualizar producto: {e}")
        print(f"Error: {e}")

def eliminar_producto(id):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id=?", (id,))
        conexion.commit()
        desconectar(conexion)
        log_info(f"Producto ID {id} eliminado.")
        print("Producto eliminado correctamente.")
    except Exception as e:
        log_error(f"Error al eliminar producto: {e}")
        print(f"Error: {e}")

def truncar_productos():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos")
        conexion.commit()
        desconectar(conexion)
        log_info("Tabla productos truncada.")
        print("Tabla productos vaciada.")
    except Exception as e:
        log_error(f"Error al truncar productos: {e}")
        print(f"Error: {e}")