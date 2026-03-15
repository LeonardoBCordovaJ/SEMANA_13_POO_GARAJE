# El Hangar - Sistema de Gestión de Garaje

**Autor:** Leonardo Benjamín Córdova Jaramillo  
**Universidad:** Universidad Estatal Amazónica - UEA  
**Materia:** Programación Orientada a Objetos (POO)  
**Semana:** 13  

## Descripción

Aplicación de escritorio desarrollada en Python utilizando **Tkinter** para la gestión de ingresos y salidas de vehículos en un garaje.  
El sistema aplica una arquitectura modular por capas (Modelos, Servicios, UI) y calcula automáticamente la tarifa basada en el tiempo de permanencia.

## Funcionalidades principales

- Registro de **entrada** de vehículos (placa, marca, propietario, hora de entrada).
- Registro de **salida** de vehículos a partir de la placa y la hora de salida.
- Cálculo automático del costo:
  - Tarifa de **$1.00** por cada bloque de **30 minutos**.
  - El cálculo se realiza al momento de registrar la salida.
- Edición de datos del vehículo (marca y propietario).
- Eliminación de registros.
- Limpieza rápida de los campos del formulario.
- Interfaz gráfica profesional con:
  - Encabezado tipo logo "**EL HANGAR**".
  - Formulario con **placeholders** que muestran ejemplos de cómo llenar la información.
  - Tabla (Treeview) con columnas: Placa, Marca, Propietario, Hora de Entrada, Hora de Salida y Costo.

## Arquitectura del proyecto

- `modelos/vehiculo.py`  
  Clase `Vehiculo` que representa a cada vehículo con atributos encapsulados (placa, marca, propietario, horas y costo).

- `servicios/garaje_servicio.py`  
  Lógica del negocio:
  - Registro de entrada.
  - Registro de salida con cálculo de tarifa.
  - Búsqueda, edición y eliminación de vehículos.
  - Gestión de la colección de vehículos en memoria.

- `ui/app_tkinter.py`  
  Interfaz gráfica con Tkinter:
  - Formularios, botones, validaciones y tabla de visualización.

- `main.py`  
  Punto de entrada de la aplicación.

## Requisitos

- Python 3.15
- Librería estándar Tkinter (incluida en Python para Windows)

## Ejecución

1. Clonar el repositorio.
2. (Opcional) Crear y activar un entorno virtual.
3. Ejecutar:

```bash
python garaje_app/main.py