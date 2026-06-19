# crear_base_datos.py
# TechSolutions S.A. - Sistema de Gestión de Vacaciones
# Genera los archivos CSV que simulan la base de datos

import csv

def crear_empleados():
    """Crea el archivo CSV con los datos de los empleados."""

    encabezados = ["Legajo", "Nombre", "Area", "Dias_Disponibles"]

    datos = [
        {"Legajo": 1001, "Nombre": "Juan Pérez",     "Area": "Desarrollo",     "Dias_Disponibles": 15},
        {"Legajo": 1002, "Nombre": "María García",   "Area": "Soporte",        "Dias_Disponibles": 10},
        {"Legajo": 1003, "Nombre": "Carlos López",   "Area": "Administración", "Dias_Disponibles": 20},
        {"Legajo": 1004, "Nombre": "Ana Martínez",   "Area": "RRHH",           "Dias_Disponibles": 12},
        {"Legajo": 1005, "Nombre": "Luis Fernández", "Area": "Desarrollo",     "Dias_Disponibles":  0},
    ]

    try:
        with open("empleados.csv", "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=encabezados)
            escritor.writeheader()
            escritor.writerows(datos)
        print(" Archivo creado: empleados.csv (5 empleados)")
    except PermissionError:
        print(" Error: asegurate de que empleados.csv no esté abierto en otro programa.")

def crear_solicitudes():
    """Crea el archivo CSV vacío para registrar solicitudes."""

    encabezados = ["ID", "Legajo", "Nombre", "Fecha_Inicio",
                   "Dias_Solicitados", "Estado"]

    try:
        with open("solicitudes.csv", "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=encabezados)
            escritor.writeheader()
        print("Archivo creado: solicitudes.csv (listo para registrar)")
    except PermissionError:
        print("Error: asegurate de que solicitudes.csv no esté abierto en otro programa.")


crear_empleados()
crear_solicitudes()
print("\nBase de datos lista. Ejecute: python chatbot.py")
