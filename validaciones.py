import re

def validar_nombre(nombre):
    if not nombre.strip():
        print("   El nombre no puede estar vacío.")
        return False
    if len(nombre) < 2:
        print("   El nombre debe tener al menos 2 caracteres.")
        return False
    return True

def validar_telefono(telefono):
    if not telefono.strip():
        return True  # El teléfono es opcional
    if not telefono.replace("+", "").replace("-", "").isdigit():
        print("   El teléfono solo puede contener números, + y -")
        return False
    return True

def validar_email(email):
    if not email.strip():
        return True  # El email es opcional
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(patron, email):
        print("   El email no tiene un formato válido.")
        return False
    return True

def validar_precio(precio):
    try:
        valor = float(precio)
        if valor < 0:
            print("   El precio no puede ser negativo.")
            return False
        return True
    except ValueError:
        print("   El precio debe ser un número.")
        return False

def validar_stock(stock):
    try:
        valor = int(stock)
        if valor < 0:
            print("   El stock no puede ser negativo.")
            return False
        return True
    except ValueError:
        print("   El stock debe ser un número entero.")
        return False