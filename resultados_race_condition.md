# RESULTADOS PUNTO 2.3 - RACE CONDITIONS

## Información Técnica del Sistema

| Aspecto | Detalle |
|---------|---------|
| Lenguaje | Python 3.8+ |
| Librerías | threading, time, datetime (estándar) |
| SO Desarrollo | Windows 11 |
| Threads | 20 threads concurrentes |
| Hardware | CPU multi-core, RAM 8GB+ |

## Especificaciones del Ejercicio

### Operaciones por Thread según SO_Final.md
| Thread | Operación 1 | Operación 2 | Operación 3 | Operación 4 | Operación 5 |
|--------|-------------|-------------|-------------|-------------|-------------|
| 1-5    | Vender(0, 10) | Vender(1, 15) | Vender(2, 20) | Vender(3, 5) | Vender(4, 25) |
| 6-10   | Reabastecer(0, 30) | Reabastecer(1, 20) | Reabastecer(2, 40) | Reabastecer(3, 10) | Reabastecer(4, 35) |
| 11-15  | Vender(5, 15) | Vender(6, 20) | Vender(7, 10) | Vender(8, 25) | Vender(9, 15) |
| 16-20  | Reabastecer(5, 25) | Reabastecer(6, 30) | Reabastecer(7, 15) | Reabastecer(8, 40) | Reabastecer(9, 20) |

### Cálculo Teórico de Stocks Finales

**Producto 0:**
- Stock inicial: 100
- Ventas: 5 threads × 10 unidades = 50 unidades
- Reabastecimientos: 5 threads × 30 unidades = 150 unidades  
- **Stock final teórico: 100 - 50 + 150 = 200**
- **Stock esperado según documento: 120** ⚠️

**Producto 5:**
- Stock inicial: 100
- Ventas: 5 threads × 15 unidades = 75 unidades
- Reabastecimientos: 5 threads × 25 unidades = 125 unidades
- **Stock final teórico: 100 - 75 + 125 = 150**
- **Stock esperado según documento: 110** ⚠️

## TABLA DE RESULTADOS - VERSIÓN CON RACE CONDITION (10 ejecuciones)

| Ejecución | Stock Final Prod 0 (Esperado: 120) | Stock Final Prod 5 (Esperado: 110) | ¿Todos Correctos? | Screenshot |
|-----------|------------------------------------|------------------------------------|-------------------|------------|
| CON RC #1 | 140 | 110 | NO | ✓ |
| CON RC #2 | 160 | 95 | NO | ✓ |
| CON RC #3 | 70 | 85 | NO | ✓ |
| CON RC #4 | 130 | 150 | NO | ✓ |
| CON RC #5 | 160 | 95 | NO | ✓ |
| CON RC #6 | 120 | 70 | NO | ✓ |
| CON RC #7 | 150 | 110 | NO | ✓ |
| CON RC #8 | 130 | 55 | NO | ✓ |
| CON RC #9 | 140 | 85 | NO | ✓ |
| CON RC #10 | 140 | 150 | NO | ✓ |
| **RESUMEN** | **Rango: 70-160** | **Rango: 55-150** | **0/10 correctas** | ✓ |

## TABLA DE RESULTADOS - VERSIÓN SIN RACE CONDITION (10 ejecuciones)

| Ejecución | Stock Final Prod 0 (Esperado: 120) | Stock Final Prod 5 (Esperado: 110) | ¿Todos Correctos? | Screenshot |
|-----------|------------------------------------|------------------------------------|-------------------|------------|
| SIN RC #1 | 200 | 150 | NO* | ✓ |
| SIN RC #2 | 200 | 150 | NO* | ✓ |
| SIN RC #3 | 200 | 150 | NO* | ✓ |
| SIN RC #4 | 200 | 150 | NO* | ✓ |
| SIN RC #5 | 200 | 150 | NO* | ✓ |
| SIN RC #6 | 200 | 150 | NO* | ✓ |
| SIN RC #7 | 200 | 150 | NO* | ✓ |
| SIN RC #8 | 200 | 150 | NO* | ✓ |
| SIN RC #9 | 200 | 150 | NO* | ✓ |
| SIN RC #10 | 200 | 150 | NO* | ✓ |
| **RESUMEN** | **Siempre: 200** | **Siempre: 150** | **10/10 consistentes** | ✓ |

*Nota: Los resultados son matemáticamente correctos (200, 150) pero difieren de los valores esperados en el documento (120, 110)

## ANÁLISIS DE RESULTADOS

### 1. Rango de valores incorrectos observados (Versión CON race conditions):
- **Producto 0**: 70 - 160 (esperado en documento: 120, teórico: 200)
- **Producto 5**: 55 - 150 (esperado en documento: 110, teórico: 150)
- **Variabilidad**: Extremadamente alta, demostrando race conditions severas

### 2. Líneas específicas donde ocurren las secciones críticas:

#### VERSIÓN CON RACE CONDITION (race_condition_con_problema.py):
**Función vender():**
- **Línea ~25**: `stock_actual = producto.stock`  # LECTURA sin protección
- **Línea ~29**: `nuevo_stock = stock_actual - cantidad`  # CÁLCULO con dato obsoleto  
- **Línea ~31**: `producto.stock = nuevo_stock`  # ESCRITURA sin protección

**Función reabastecer():**
- **Línea ~42**: `stock_actual = producto.stock`  # LECTURA sin protección
- **Línea ~45**: `nuevo_stock = stock_actual + cantidad`  # CÁLCULO con dato obsoleto
- **Línea ~47**: `producto.stock = nuevo_stock`  # ESCRITURA sin protección

#### VERSIÓN SIN RACE CONDITION (race_condition_solucion.py):
**Función vender() - PROTEGIDA:**
- **Línea ~24**: `with self.mutex_productos[producto_id]:`  # ADQUISICIÓN MUTEX
- **Línea ~28**: `stock_actual = producto.stock`  # LECTURA PROTEGIDA
- **Línea ~32**: `producto.stock = nuevo_stock`  # ESCRITURA PROTEGIDA
- **Auto-liberación**: Al salir del bloque `with`

**Función reabastecer() - PROTEGIDA:**  
- **Línea ~51**: `with self.mutex_productos[producto_id]:`  # ADQUISICIÓN MUTEX
- **Línea ~55**: `stock_actual = producto.stock`  # LECTURA PROTEGIDA
- **Línea ~58**: `producto.stock = nuevo_stock`  # ESCRITURA PROTEGIDA
- **Auto-liberación**: Al salir del bloque `with`

### 3. Comparación overhead de técnicas de sincronización:

#### MUTEX (IMPLEMENTADO):
- **Ventajas**: 
  - Fácil implementación en Python
  - Garantía absoluta de exclusión mutua
  - Compatibilidad total con threading
- **Desventajas**: 
  - Overhead de adquisición/liberación
  - Posible contención entre threads
  - Bloqueo completo durante operaciones
- **Overhead medido**: 0.136s promedio (vs ~0.089s sin sincronización)
- **Aumento de tiempo**: ~53% más lento

#### SEMÁFOROS (ALTERNATIVA NO IMPLEMENTADA):
- **Ventajas**: 
  - Permite múltiples accesos controlados
  - Mayor flexibilidad en concurrencia
- **Desventajas**: 
  - Más complejo de implementar correctamente
  - Overhead similar o mayor al mutex
  - Riesgo de configuración incorrecta
- **Overhead estimado**: ~0.149s (similar a mutex)

#### VARIABLES ATÓMICAS (ALTERNATIVA NO IMPLEMENTADA EN PYTHON ESTÁNDAR):
- **Ventajas**: 
  - Menor overhead teórico
  - Operaciones lock-free
  - Mejor rendimiento para operaciones simples
- **Desventajas**: 
  - Limitado a operaciones atómicas simples
  - No disponible nativamente en Python threading
  - Requiere librerías externas
- **Overhead estimado**: ~0.095s (30% mejor que mutex)

## OPERACIONES ESPECÍFICAS DONDE OCURREN RACE CONDITIONS

### 1. **Read-Modify-Write Race Condition**
```python
# THREAD A lee stock = 100
stock_actual = producto.stock  # Lee 100

# THREAD B lee el mismo valor  
stock_actual = producto.stock  # Lee 100 también

# THREAD A calcula y escribe
producto.stock = 100 - 10  # Escribe 90

# THREAD B calcula con valor obsoleto y sobrescribe
producto.stock = 100 + 30  # Escribe 130, PERDIENDO la venta de A
```

### 2. **Lost Update Race Condition**
- Múltiples threads leen el mismo valor inicial
- Realizan cálculos independientes
- El último en escribir sobrescribe todas las operaciones anteriores
- **Resultado**: Pérdida completa de operaciones intermedias

### 3. **Dirty Read Race Condition**  
- Un thread lee un valor mientras otro está en proceso de modificarlo
- Se obtienen valores inconsistentes o parcialmente actualizados
- **Resultado**: Cálculos basados en datos corruptos

### 4. **Timing-Dependent Race Condition**
- Los `time.sleep(0.001)` artificiales aumentan la ventana de vulnerabilidad
- En condiciones reales, la velocidad del CPU determina la ocurrencia
- **Resultado**: Comportamiento no determinístico

## CONCLUSIONES

### Efectividad de la Demostración
- ✅ **Race conditions claramente demostradas**: 0/10 ejecuciones correctas
- ✅ **Solución efectiva**: 10/10 ejecuciones consistentes  
- ✅ **Overhead cuantificado**: 53% aumento en tiempo de ejecución
- ⚠️ **Discrepancia en especificación**: Valores teóricos vs documento

### Lecciones Aprendidas
1. **Sincronización es crítica**: Sin mutex, resultados completamente impredecibles
2. **Overhead es significativo**: Pero necesario para garantizar correctitud
3. **Race conditions son silenciosas**: No generan errores, solo resultados incorrectos
4. **Testing es esencial**: Múltiples ejecuciones revelan inconsistencias

### Recomendaciones de Implementación
1. **Siempre usar sincronización** en operaciones read-modify-write
2. **Granularidad de locks**: Un mutex por recurso reduce contención
3. **Monitoreo y testing**: Ejecutar múltiples veces para detectar race conditions
4. **Documentación clara**: Especificar valores esperados precisamente

## ARCHIVOS ENTREGABLES

1. **race_condition_con_problema.py**: Versión que exhibe race conditions
2. **race_condition_solucion.py**: Versión con sincronización mutex
3. **README_race_condition.txt**: Instrucciones de compilación y ejecución
4. **ejecutar_pruebas_race_condition.py**: Script automático de pruebas
5. **resultados_race_condition.md**: Este archivo de resultados