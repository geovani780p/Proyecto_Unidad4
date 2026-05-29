import logging 
import os

LOG_FILE = 'app.log'

logger = logging.getLogger("CRUD_APP")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def log_info(mensaje):
    logger.info(mensaje)

def log_error(mensaje):
    logger.error(mensaje)

def ver_historial(ultimas_n=20):
    if not os.path.exists(LOG_FILE):
        print("No hay historial todavia.")
        return
    
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    print(f"\n Ultimas {ultimas_n} acciones:")
    print("-" * 60)
    for linea in lineas[-ultimas_n:]:
        print(linea.rstrip())
    print("-" * 60)


