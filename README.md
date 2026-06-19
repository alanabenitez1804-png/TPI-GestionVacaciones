# Sistema de Gestión de Vacaciones — TechSolutions S.A.

Trabajo Práctico Integrador — Organización Empresarial  
UTN Tecnicatura Universitaria en Programación (TUP) a Distancia

## Descripción
Simulación de un chatbot de consola que automatiza el proceso de 
solicitud de vacaciones mediante una máquina de estados, 
siguiendo el modelo de procesos BPMN 2.0.

## Archivos
| Archivo | Descripción |
|---|---|
| `chatbot.py` | Bot principal con la máquina de estados |
| `crear_base_datos.py` | Genera los archivos CSV de datos |
| `empleados.csv` | Base de datos de empleados (se genera automáticamente) |
| `solicitudes.csv` | Registro de solicitudes (se genera automáticamente) |

## Requisitos
- Python 3.x
- Módulo `csv` (incluido en Python, no requiere instalación)

## Cómo ejecutar

**Paso 1 — Generar la base de datos**  
Ejecutar una sola vez antes de usar el chatbot:
Esto crea dos archivos CSV en la misma carpeta:
- `empleados.csv` → contiene los datos de los empleados
- `solicitudes.csv` → empieza vacío y se llena con cada solicitud

**Paso 2 — Ejecutar el chatbot**

**Paso 3 — Seguir el flujo**  
El bot guía al usuario paso a paso:
- Ingresar número de legajo
- Ingresar fecha de inicio de vacaciones
- Ingresar cantidad de días solicitados
- Si tiene saldo: el Jefe de Área aprueba o rechaza
- El resultado queda registrado automáticamente en `solicitudes.csv`

## Empleados de prueba
| Legajo | Nombre | Área | Días disponibles |
|---|---|---|---|
| 1001 | Juan Pérez | Desarrollo | 15 |
| 1002 | María García | Soporte | 10 |
| 1003 | Carlos López | Administración | 20 |
| 1004 | Ana Martínez | RRHH | 12 |
| 1005 | Luis Fernández | Desarrollo | 0 |

## Tecnologías utilizadas
- Lenguaje: Python 3
- Persistencia: archivos CSV
- Metodología de modelado: BPMN 2.0
- Herramienta de modelado: diagrams.net (draw.io)

**Paso 2 — Ejecutar el chatbot**
