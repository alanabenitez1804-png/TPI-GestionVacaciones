
# TechSolutions S.A. - Chatbot de Gestión de Vacaciones
# Simulación de proceso administrativo con máquina de estados
# Trabajo Práctico Integrador - Organización Empresarial - UTN TUP

import csv

# ARCHIVOS DE LA BASE DE DATOS

ARCHIVO_EMPLEADOS   = "empleados.csv"
ARCHIVO_SOLICITUDES = "solicitudes.csv"

# MÁQUINA DE ESTADOS
# Define todos los estados posibles del proceso

ESTADO_ESPERANDO_LEGAJO  = "ESPERANDO_LEGAJO"
ESTADO_ESPERANDO_FECHA   = "ESPERANDO_FECHA_INICIO"
ESTADO_ESPERANDO_DIAS    = "ESPERANDO_DIAS"
ESTADO_ESPERANDO_JEFE    = "ESPERANDO_DECISION_JEFE"
ESTADO_FIN               = "FIN"


# FUNCIONES DE BASE DE DATOS


def buscar_empleado(legajo):
    """
    Busca un empleado en empleados.csv por su número de legajo.
    Retorna un diccionario con sus datos o None si no existe.
    """
    try:
        with open(ARCHIVO_EMPLEADOS, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                if fila["Legajo"] == str(legajo):
                    return {
                        "legajo":           fila["Legajo"],
                        "nombre":           fila["Nombre"],
                        "area":             fila["Area"],
                        "dias_disponibles": int(fila["Dias_Disponibles"])
                    }
    except FileNotFoundError:
        print(" Error: no se encontró 'empleados.csv'.")
        print("  Ejecute primero: python crear_base_datos.py")
    return None

def registrar_solicitud(legajo, nombre, fecha_inicio, dias, estado_solicitud):
    """
    Registra una solicitud en solicitudes.csv.
    Estado posible: APROBADA | RECHAZADA-SinSaldo | RECHAZADA-Jefe
    """
    encabezados = ["ID", "Legajo", "Nombre", "Fecha_Inicio",
                   "Dias_Solicitados", "Estado"]
    try:
        with open(ARCHIVO_SOLICITUDES, "r", encoding="utf-8") as archivo:
            filas = list(csv.DictReader(archivo))
        nuevo_id = len(filas) + 1

        nueva_solicitud = {
            "ID":               nuevo_id,
            "Legajo":           legajo,
            "Nombre":           nombre,
            "Fecha_Inicio":     fecha_inicio,
            "Dias_Solicitados": dias,
            "Estado":           estado_solicitud
        }

        with open(ARCHIVO_SOLICITUDES, "a", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=encabezados)
            escritor.writerow(nueva_solicitud)

    except FileNotFoundError:
        print("✗ Error: no se encontró 'solicitudes.csv'.")

def actualizar_dias_empleado(legajo, dias_usados):
    """
    Descuenta los días aprobados del saldo del empleado en empleados.csv.
    """
    try:
        with open(ARCHIVO_EMPLEADOS, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            filas = list(lector)
            encabezados = lector.fieldnames

        for fila in filas:
            if fila["Legajo"] == str(legajo):
                fila["Dias_Disponibles"] = int(fila["Dias_Disponibles"]) - dias_usados

        with open(ARCHIVO_EMPLEADOS, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=encabezados)
            escritor.writeheader()
            escritor.writerows(filas)

    except FileNotFoundError:
        print("✗ Error: no se encontró 'empleados.csv'.")

# FUNCIONES DE INTERFAZ

def separador():
    print("─" * 52)

def encabezado():
    print("═" * 52)
    print("   TECHSOLUTIONS S.A.")
    print("   Sistema de Gestión de Solicitudes de Vacaciones")
    print("═" * 52)
    print(" Escriba 'salir' en cualquier momento para cancelar.")
    separador()

# LÓGICA PRINCIPAL DEL BOT (MÁQUINA DE ESTADOS)


def ejecutar_bot():
    # Variables de sesión
    estado          = ESTADO_ESPERANDO_LEGAJO
    empleado_actual = None
    fecha_inicio    = None
    dias_solicitados = 0

    encabezado()
    print("Ingrese su número de legajo:")

    # ── CICLO PRINCIPAL ──────────────────────────────
    while estado != ESTADO_FIN:

        try:
            entrada = input("> ").strip()
        except KeyboardInterrupt:
            print("\n\nSesión interrumpida.")
            break

        if entrada.lower() == "salir":
            print("\nSesión cancelada. Hasta luego.")
            break

        # ── ESTADO 1: VALIDAR LEGAJO ─────────────────
        if estado == ESTADO_ESPERANDO_LEGAJO:

            if not entrada.isdigit():
                print("⚠  El legajo debe contener solo números. Intente nuevamente:")
                continue

            empleado_actual = buscar_empleado(entrada)

            if not empleado_actual:
                print("⚠  No existe ningún empleado con ese legajo. Intente nuevamente:")
                continue

            separador()
            print(f"✓ Bienvenido/a, {empleado_actual['nombre']}")
            print(f"  Área:             {empleado_actual['area']}")
            print(f"  Días disponibles: {empleado_actual['dias_disponibles']}")
            separador()
            print("Ingrese la fecha de inicio de sus vacaciones (DD/MM/AAAA):")
            estado = ESTADO_ESPERANDO_FECHA

        # ── ESTADO 2: FECHA DE INICIO ────────────────
        elif estado == ESTADO_ESPERANDO_FECHA:

            # Validación básica: formato DD/MM/AAAA
            partes = entrada.split("/")
            if len(partes) != 3 or not all(p.isdigit() for p in partes):
                print("Formato incorrecto. Use DD/MM/AAAA (ej: 15/07/2025):")
                continue

            fecha_inicio = entrada
            print("¿Cuántos días de vacaciones solicita?")
            estado = ESTADO_ESPERANDO_DIAS

        # ── ESTADO 3: DÍAS SOLICITADOS + GATEWAY 1 ───
        elif estado == ESTADO_ESPERANDO_DIAS:

            if not entrada.isdigit() or int(entrada) <= 0:
                print("Ingrese un número de días válido (mayor a cero):")
                continue

            dias_solicitados = int(entrada)

            separador()
            print(f"  Fecha de inicio:    {fecha_inicio}")
            print(f"  Días solicitados:   {dias_solicitados}")
            print(f"  Días disponibles:   {empleado_actual['dias_disponibles']}")
            separador()

            # ── GATEWAY 1: ¿Tiene días disponibles? ──
            if dias_solicitados > empleado_actual["dias_disponibles"]:
                print("✗ SOLICITUD RECHAZADA")
                print("  Motivo: no cuenta con suficientes días de vacaciones.")
                registrar_solicitud(
                    empleado_actual["legajo"], empleado_actual["nombre"],
                    fecha_inicio, dias_solicitados, "RECHAZADA-SinSaldo"
                )
                estado = ESTADO_FIN

            else:
                print("✓ Saldo verificado. Enviando solicitud al Jefe de Área...")
                separador()
                print("[SIMULACIÓN - Jefe de Área]")
                print(f"Solicitud de {empleado_actual['nombre']} ({dias_solicitados} días).")
                print("¿El momento es conveniente para el área? (si / no):")
                estado = ESTADO_ESPERANDO_JEFE

        # ── ESTADO 4: DECISIÓN DEL JEFE + GATEWAY 2 ─
        elif estado == ESTADO_ESPERANDO_JEFE:

            if entrada.lower() not in ["si", "sí", "no"]:
                print(" Respuesta inválida. Ingrese 'si' o 'no':")
                continue

            separador()

            if entrada.lower() == "no":
                print("✗ SOLICITUD RECHAZADA")
                print("  Motivo: el Jefe de Área indicó que el momento no es conveniente.")
                registrar_solicitud(
                    empleado_actual["legajo"], empleado_actual["nombre"],
                    fecha_inicio, dias_solicitados, "RECHAZADA-Jefe"
                )

            else:
                actualizar_dias_empleado(empleado_actual["legajo"], dias_solicitados)
                registrar_solicitud(
                    empleado_actual["legajo"], empleado_actual["nombre"],
                    fecha_inicio, dias_solicitados, "APROBADA"
                )
                dias_restantes = empleado_actual["dias_disponibles"] - dias_solicitados
                print("✓ SOLICITUD APROBADA")
                print(f"  Fecha de inicio: {fecha_inicio}")
                print(f"  Días usados:     {dias_solicitados}")
                print(f"  Días restantes:  {dias_restantes}")
                print("  [RR.HH. notificado automáticamente]")

            estado = ESTADO_FIN

    
    separador()
    print("  Gracias por usar el sistema de TechSolutions S.A.")
    print("═" * 52)


# PUNTO DE ENTRADA

ejecutar_bot()
