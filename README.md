# INSTRUCCIONES DE COMPILACIÓN Y EJECUCIÓN
## Problemas de Concurrencia y Sincronización

## REQUISITOS DEL SISTEMA
**Lenguaje:** Python 3.8 o superior  
**Sistema Operativo:** Windows 10/11, Linux, macOS  
**Librerías requeridas:** threading (estándar de Python)

### VERIFICACIÓN DE PYTHON
Abrir terminal y ejecutar: `python --version`  
Debe mostrar: Python 3.x.x (donde x >= 8)

## PUNTO 2.1: DEADLOCK - SISTEMA DE TRANSFERENCIAS BANCARIAS

### VERSIÓN CON DEADLOCK
**Archivo:** deadlock_con_problema.py  
**Ejecución:** `python deadlock_con_problema.py`  
**Resultado esperado:** Sistema se bloquea (deadlock), Threads quedan esperando indefinidamente, Presionar Ctrl+C para terminar

### VERSIÓN SIN DEADLOCK
**Archivo:** deadlock_solucion.py  
**Ejecución:** `python deadlock_solucion.py`  
**Resultado esperado:** 30 transferencias completadas exitosamente, Saldos finales correctos, Sin bloqueos

## PUNTO 2.2: STARVATION - SISTEMA DE PRIORIDADES DE TAREAS

### VERSIÓN CON STARVATION
**Archivo:** starvation_con_problema.py  
**Ejecución:** `python starvation_con_problema.py`  
**Duración:** 10 segundos  
**Resultado esperado:** Tareas tipo B no se procesan, 15-20 tareas B quedan sin procesar, Screenshots automáticos a los 2, 4, 6, 8, 10 segundos

### VERSIÓN SIN STARVATION
**Archivo:** starvation_solucion.py  
**Ejecución:** `python starvation_solucion.py`  
**Duración:** 10 segundos  
**Resultado esperado:** Todas las tareas se procesan eventualmente, Mecanismo de aging visible, Tareas B progresan gradualmente

## PUNTO 2.3: RACE CONDITION - GESTOR DE INVENTARIO CONCURRENTE

### VERSIÓN CON RACE CONDITION
**Archivo:** race_condition_con_problema.py  
**Ejecución:** `python race_condition_con_problema.py`  
**Resultado esperado:** Stock final inconsistente (varía en cada ejecución), Valores incorrectos para Producto 0 y Producto 5, Ejecutar 10 veces para documentar variaciones

### VERSIÓN SIN RACE CONDITION
**Archivo:** race_condition_solucion.py  
**Ejecución:** `python race_condition_solucion.py`  
**Resultado esperado:** Stock final consistente (siempre igual), Producto 0: 120 unidades, Producto 5: 110 unidades, Resultados idénticos en 10 ejecuciones

## EJECUCIÓN DE PRUEBAS AUTOMATIZADAS

### SCRIPT DE PRUEBAS RACE CONDITION
**Archivo:** ejecutar_pruebas_race_condition.py  
**Ejecución:** `python ejecutar_pruebas_race_condition.py`  
**Descripción:** Ejecuta automáticamente 10 veces cada versión (con y sin race condition) y genera tabla comparativa de resultados.

## ESTRUCTURA DE ARCHIVOS
├── deadlock_con_problema.py
├── deadlock_solucion.py
├── starvation_con_problema.py
├── starvation_solucion.py
├── race_condition_con_problema.py
├── race_condition_solucion.py
├── ejecutar_pruebas_race_condition.py
├── README_compilacion.txt
├── README_deadlock.md
├── README_starvation.md
└── README_race_condition.txt
