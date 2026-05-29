from database import (crear_tabla,
                      crear_contacto, ver_contactos, actualizar_contacto, eliminar_contacto, truncar_contactos,
                      crear_categoria, ver_categorias, eliminar_categoria, truncar_categorias,
                      crear_producto, ver_productos, actualizar_producto, eliminar_producto, truncar_productos)
from backup import generar_backup, restaurar_backup
from logger import ver_historial
from validaciones import validar_nombre, validar_telefono, validar_email, validar_precio, validar_stock

def mostrar_menu():
    print("\n" + "=" * 45)
    print("         SISTEMA DE GESTIÓN")
    print("=" * 45)
    print("  --- CONTACTOS ---")
    print("  1. Crear contacto")
    print("  2. Ver contactos")
    print("  3. Actualizar contacto")
    print("  4. Eliminar contacto")
    print("  5. Truncar contactos")
    print("  --- CATEGORIAS ---")
    print("  6. Crear categoría")
    print("  7. Ver categorías")
    print("  8. Eliminar categoría")
    print("  9. Truncar categorías")
    print("  --- PRODUCTOS ---")
    print("  10. Crear producto")
    print("  11. Ver productos")
    print("  12. Actualizar producto")
    print("  13. Eliminar producto")
    print("  14. Truncar productos")
    print("  --- SISTEMA ---")
    print("  15. Ver historial de acciones")
    print("  16. Generar backup (.json)")
    print("  17. Restaurar backup")
    print("  0.  Salir")
    print("=" * 45)

def main():
    crear_tabla()

    while True:
        mostrar_menu()
        opcion = input("  Elige una opción: ")

        # ── CONTACTOS ──────────────────────────────
        if opcion == "1":
            nombre = input("  Nombre: ")
            if not validar_nombre(nombre): continue
            telefono = input("  Teléfono: ")
            if not validar_telefono(telefono): continue
            email = input("  Email: ")
            if not validar_email(email): continue
            crear_contacto(nombre, telefono, email)

        elif opcion == "2":
            ver_contactos()

        elif opcion == "3":
            ver_contactos()
            id = int(input("  ID a actualizar: "))
            nombre = input("  Nuevo nombre: ")
            if not validar_nombre(nombre): continue
            telefono = input("  Nuevo teléfono: ")
            if not validar_telefono(telefono): continue
            email = input("  Nuevo email: ")
            if not validar_email(email): continue
            actualizar_contacto(id, nombre, telefono, email)

        elif opcion == "4":
            ver_contactos()
            id = int(input("  ID a eliminar: "))
            eliminar_contacto(id)

        elif opcion == "5":
            confirm = input("  ¿Seguro que quieres vaciar todos los contactos? (s/n): ")
            if confirm.lower() == "s":
                truncar_contactos()

        # ── CATEGORIAS ─────────────────────────────
        elif opcion == "6":
            nombre = input("  Nombre de la categoría: ")
            if not validar_nombre(nombre): continue
            crear_categoria(nombre)

        elif opcion == "7":
            ver_categorias()

        elif opcion == "8":
            ver_categorias()
            id = int(input("  ID a eliminar: "))
            eliminar_categoria(id)

        elif opcion == "9":
            confirm = input("  ¿Seguro que quieres vaciar todas las categorías? (s/n): ")
            if confirm.lower() == "s":
                truncar_categorias()

        # ── PRODUCTOS ──────────────────────────────
        elif opcion == "10":
            nombre = input("  Nombre del producto: ")
            if not validar_nombre(nombre): continue
            precio = input("  Precio: ")
            if not validar_precio(precio): continue
            stock = input("  Stock: ")
            if not validar_stock(stock): continue
            ver_categorias()
            categoria_id = int(input("  ID de categoría: "))
            crear_producto(nombre, float(precio), int(stock), categoria_id)

        elif opcion == "11":
            ver_productos()

        elif opcion == "12":
            ver_productos()
            id = int(input("  ID a actualizar: "))
            nombre = input("  Nuevo nombre: ")
            if not validar_nombre(nombre): continue
            precio = input("  Nuevo precio: ")
            if not validar_precio(precio): continue
            stock = input("  Nuevo stock: ")
            if not validar_stock(stock): continue
            ver_categorias()
            categoria_id = int(input("  Nueva categoría ID: "))
            actualizar_producto(id, nombre, float(precio), int(stock), categoria_id)

        elif opcion == "13":
            ver_productos()
            id = int(input("  ID a eliminar: "))
            eliminar_producto(id)

        elif opcion == "14":
            confirm = input("  ¿Seguro que quieres vaciar todos los productos? (s/n): ")
            if confirm.lower() == "s":
                truncar_productos()

        # ── SISTEMA ────────────────────────────────
        elif opcion == "15":
            ver_historial()

        elif opcion == "16":
            generar_backup()

        elif opcion == "17":
            archivo = input("  Nombre del archivo backup: ")
            restaurar_backup(archivo)

        elif opcion == "0":
            print("  Hasta luego 👋")
            break

        else:
            print("  Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()