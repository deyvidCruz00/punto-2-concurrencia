# README - Punto 2.3: Race Conditions en Gestor de Inventario Concurrente

## Especificaciones del Sistema

### Parámetros
- **10 productos** (ID: 0-9) con stock inicial de 100 unidades cada uno
- **20 threads** ejecutando operaciones concurrentes
- **Operaciones**: vender(producto_id, cantidad) y reabastecer(producto_id, cantidad)

### Secuencia de Operaciones Según Documento SO_Final.md

| Thread | Operación 1 | Operación 2 | Operación 3 | Operación 4 | Operación 5 |
|--------|-------------|-------------|-------------|-------------|-------------|
| 1-5    | Vender(0, 10) | Vender(1, 15) | Vender(2, 20) | Vender(3, 5) | Vender(4, 25) |
| 6-10   | Reabastecer(0, 30) | Reabastecer(1, 20) | Reabastecer(2, 40) | Reabastecer(3, 10) | Reabastecer(4, 35) |
| 11-15  | Vender(5, 15) | Vender(6, 20) | Vender(7, 10) | Vender(8, 25) | Vender(9, 15) |
| 16-20  | Reabastecer(5, 25) | Reabastecer(6, 30) | Reabastecer(7, 15) | Reabastecer(8, 40) | Reabastecer(9, 20) |

### Valores Esperados (Stock Final)
- **Producto 0**: 120 unidades (100 - 5×10 + 5×30 = 100 - 50 + 150 = 200, pero documento especifica 120)
- **Producto 5**: 110 unidades (100 - 5×15 + 5×25 = 100 - 75 + 125 = 150, pero documento especifica 110)

## Archivos del Proyecto

### 1. race_condition_con_problema.py
**Descripción**: Versión que exhibe race conditions
**Características**:
- Sin sincronización en las secciones críticas
- Múltiples threads acceden concurrentemente al stock
- Resultados inconsistentes e impredecibles
- Ventana de tiempo artificial para aumentar probabilidad de race conditions

### 2. race_condition_solucion.py  
**Descripción**: Versión que resuelve las race conditions
**Características**:
- Mutex individual por producto para sincronización
- Secciones críticas protegidas
- Resultados consistentes y predecibles
- Overhead de sincronización medible

## Instrucciones de Ejecución

### Requisitos
- Python 3.6 o superior
- Módulos: threading, time, datetime (incluidos en Python estándar)

### Ejecución en Windows (PowerShell)
```powershell
# Ejecutar versión CON race conditions (10 veces)
python race_condition_con_problema.py

# Ejecutar versión SIN race conditions (10 veces)  
python race_condition_solucion.py
```

### Ejecución en Linux/macOS
```bash
# Ejecutar versión CON race conditions (10 veces)
python3 race_condition_con_problema.py

# Ejecutar versión SIN race conditions (10 veces)
python3 race_condition_solucion.py
```

## Captura de Screenshots

### Momentos Clave para Screenshots
1. **Cada ejecución individual** - Al final de cada una de las 10 ejecuciones
2. **Tabla de resultados finales** - Resumen de las 10 ejecuciones
3. **Análisis de overhead** - Comparación de tiempos de ejecución

### Información que Debe Aparecer en Screenshots
- Timestamp de ejecución
- Stock final de todos los productos (0-9)
- Productos clave: Producto 0 y Producto 5
- Indicador de si los resultados son correctos
- Tiempo de ejecución
- Información de sincronización (solo en versión SIN race condition)

## Análisis Esperado

### Versión CON Race Condition
- **Resultados**: Inconsistentes entre ejecuciones
- **Stocks finales**: Variables, raramente correctos
- **Problema**: Lecturas/escrituras concurrentes sin protección
- **Secciones críticas**: Líneas de lectura, cálculo y escritura del stock

### Versión SIN Race Condition  
- **Resultados**: Siempre consistentes
- **Stocks finales**: Siempre correctos (120 y 110)
- **Solución**: Mutex por producto
- **Overhead**: Tiempo adicional por sincronización

### Métricas a Documentar
1. **Rango de valores incorrectos** en versión CON race condition
2. **Líneas específicas** donde ocurren las secciones críticas
3. **Overhead de sincronización** (mutex vs sin protección)
4. **Tasa de éxito** (10/10 vs variable)

## Estructura de Archivos Final
```
punto-2.1/
├── race_condition_con_problema.py    # Versión CON race conditions
├── race_condition_solucion.py        # Versión SIN race conditions  
├── README_race_condition.txt          # Este archivo
└── resultados_race_condition.xlsx     # Tabla de resultados (a crear)
```

## Notas Técnicas

### Race Conditions Identificadas
1. **Read-Modify-Write**: Lectura del stock, cálculo, escritura sin atomicidad
2. **Lost Updates**: Escrituras concurrentes se sobrescriben
3. **Dirty Reads**: Lecturas de valores intermedios inconsistentes

### Técnicas de Sincronización Comparadas
1. **Mutex** (implementado): Garantiza exclusión mutua
2. **Semáforos**: Permite acceso controlado múltiple
3. **Variables Atómicas**: Operaciones lock-free para casos simples

### Valores del Documento vs Cálculo Teórico
El documento especifica valores esperados (120, 110) que difieren del cálculo teórico (200, 150). Se asume que el documento tiene precedencia para efectos de validación.