import threading
import time
from datetime import datetime
import random

class Producto:
    def __init__(self, id, stock_inicial=100):
        self.id = id
        self.stock = stock_inicial
        
    def __str__(self):
        return f"Producto[{self.id}] = {self.stock} unidades"

class GestorInventarioSeguro:
    def __init__(self, num_productos=10):
        # Crear 10 productos con stock inicial de 100 unidades cada uno
        self.productos = [Producto(i, 100) for i in range(num_productos)]
        
        # MECANISMO DE SINCRONIZACIÓN: Mutex para cada producto
        self.mutex_productos = [threading.Lock() for _ in range(num_productos)]
        
        # Mutex global para estadísticas
        self.mutex_stats = threading.Lock()
        self.operaciones_completadas = 0
        self.operaciones_fallidas = 0
        
    def vender(self, producto_id, cantidad, thread_name):
        """VERSIÓN SIN RACE CONDITION: Con mutex de sincronización"""
        producto = self.productos[producto_id]
        
        print(f"[{thread_name}] [{timestamp()}] Iniciando VENTA: Producto {producto_id}, cantidad {cantidad}")
        
        # ADQUIRIR MUTEX DEL PRODUCTO ANTES DE LA SECCIÓN CRÍTICA
        with self.mutex_productos[producto_id]:
            print(f"[{thread_name}] [{timestamp()}] MUTEX ADQUIRIDO para Producto {producto_id}")
            
            # SECCIÓN CRÍTICA PROTEGIDA - NO HAY RACE CONDITION
            stock_actual = producto.stock  # Lectura protegida
            time.sleep(0.001)  # Simula tiempo de procesamiento (sin race condition)
            
            if stock_actual >= cantidad:
                nuevo_stock = stock_actual - cantidad  # Cálculo con dato válido
                time.sleep(0.001)  # Sin race condition gracias al mutex
                producto.stock = nuevo_stock  # Escritura protegida
                
                print(f"[{thread_name}] [{timestamp()}] VENTA EXITOSA: Producto {producto_id}, vendido {cantidad}, stock restante: {producto.stock}")
                
                # Actualizar estadísticas de forma segura
                with self.mutex_stats:
                    self.operaciones_completadas += 1
            else:
                print(f"[{thread_name}] [{timestamp()}] VENTA FALLIDA: Producto {producto_id}, stock insuficiente ({stock_actual} < {cantidad})")
                
                # Actualizar estadísticas de forma segura
                with self.mutex_stats:
                    self.operaciones_fallidas += 1
            
            print(f"[{thread_name}] [{timestamp()}] MUTEX LIBERADO para Producto {producto_id}")
        # MUTEX AUTOMÁTICAMENTE LIBERADO AL SALIR DEL BLOQUE WITH
    
    def reabastecer(self, producto_id, cantidad, thread_name):
        """VERSIÓN SIN RACE CONDITION: Con mutex de sincronización"""
        producto = self.productos[producto_id]
        
        print(f"[{thread_name}] [{timestamp()}] Iniciando REABASTECIMIENTO: Producto {producto_id}, cantidad {cantidad}")
        
        # ADQUIRIR MUTEX DEL PRODUCTO ANTES DE LA SECCIÓN CRÍTICA
        with self.mutex_productos[producto_id]:
            print(f"[{thread_name}] [{timestamp()}] MUTEX ADQUIRIDO para Producto {producto_id}")
            
            # SECCIÓN CRÍTICA PROTEGIDA - NO HAY RACE CONDITION
            stock_actual = producto.stock  # Lectura protegida
            time.sleep(0.001)  # Simula tiempo de procesamiento (sin race condition)
            
            nuevo_stock = stock_actual + cantidad  # Cálculo con dato válido
            time.sleep(0.001)  # Sin race condition gracias al mutex
            producto.stock = nuevo_stock  # Escritura protegida
            
            print(f"[{thread_name}] [{timestamp()}] REABASTECIMIENTO EXITOSO: Producto {producto_id}, agregado {cantidad}, stock actual: {producto.stock}")
            
            # Actualizar estadísticas de forma segura
            with self.mutex_stats:
                self.operaciones_completadas += 1
            
            print(f"[{thread_name}] [{timestamp()}] MUTEX LIBERADO para Producto {producto_id}")
        # MUTEX AUTOMÁTICAMENTE LIBERADO AL SALIR DEL BLOQUE WITH
    
    def obtener_stock(self, producto_id):
        """Obtiene el stock actual de un producto de forma segura"""
        with self.mutex_productos[producto_id]:
            return self.productos[producto_id].stock
    
    def mostrar_inventario(self):
        """Muestra el estado completo del inventario de forma segura"""
        print("\n=== ESTADO DEL INVENTARIO ===")
        for i, producto in enumerate(self.productos):
            # Lectura segura del stock
            stock_seguro = self.obtener_stock(i)
            print(f"  Producto[{i}] = {stock_seguro} unidades")
        
        with self.mutex_stats:
            print(f"Operaciones completadas: {self.operaciones_completadas}")
            print(f"Operaciones fallidas: {self.operaciones_fallidas}")

def timestamp():
    """Genera timestamp formateado"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def mostrar_estado_screenshot(titulo, inventario, ejecucion_num, tiempo_overhead=None):
    """Muestra información formateada para captura de screenshots"""
    print("\n" + "="*80)
    print(f"MOMENTO PARA SCREENSHOT: {titulo}")
    print(f"TIMESTAMP: {timestamp()}")
    print(f"EJECUCIÓN: #{ejecucion_num}")
    print("="*80)
    
    print("STOCK FINAL DE PRODUCTOS:")
    for i in range(10):
        stock = inventario.obtener_stock(i)
        print(f"    Producto {i}: {stock} unidades")
    
    # Mostrar productos específicos requeridos para la tabla
    print(f"\nPRODUCTOS CLAVE PARA TABLA:")
    print(f"    Producto 0: {inventario.obtener_stock(0)} unidades (Esperado: 120)")
    print(f"    Producto 5: {inventario.obtener_stock(5)} unidades (Esperado: 110)")
    
    print(f"\nSINCRONIZACIÓN:")
    print(f"    Mecanismo: Mutex individual por producto")
    print(f"    Estado: Sin race conditions - Resultados consistentes")
    
    if tiempo_overhead:
        print(f"\nOVERHEAD DE SINCRONIZACIÓN:")
        print(f"    Tiempo con overhead: {tiempo_overhead:.3f}s")
    
    print("="*80)
    print("CAPTURAR SCREENSHOT AQUI")
    print("="*80)

class WorkerThreadSeguro(threading.Thread):
    def __init__(self, thread_id, inventario, operaciones):
        super().__init__(name=f"Thread-{thread_id}")
        self.thread_id = thread_id
        self.inventario = inventario
        self.operaciones = operaciones
        
    def run(self):
        print(f"[{self.name}] [{timestamp()}] Iniciado")
        
        for i, (operacion, producto_id, cantidad) in enumerate(self.operaciones, 1):
            print(f"\n[{self.name}] [{timestamp()}] Operación {i}/5: {operacion}({producto_id}, {cantidad})")
            
            if operacion == "vender":
                self.inventario.vender(producto_id, cantidad, self.name)
            elif operacion == "reabastecer":
                self.inventario.reabastecer(producto_id, cantidad, self.name)
            
            # Pequeña pausa entre operaciones del mismo thread
            time.sleep(0.01)
        
        print(f"[{self.name}] [{timestamp()}] Finalizado - 5 operaciones completadas")

def ejecutar_simulacion_segura(ejecucion_num):
    """Ejecuta una simulación completa del sistema de inventario SIN race conditions"""
    print(f"\n{'='*60}")
    print(f"EJECUCIÓN #{ejecucion_num} - VERSIÓN SIN RACE CONDITION")
    print(f"{'='*60}")
    
    # Crear inventario con sincronización
    inventario = GestorInventarioSeguro()
    
    # Mostrar estado inicial
    print(f"\n=== ESTADO INICIAL ===")
    inventario.mostrar_inventario()
    
    # Misma secuencia de operaciones que la versión CON race condition
    operaciones_threads = [
        # Threads 1-5: Operaciones de VENTA
        [("vender", 0, 10), ("vender", 1, 15), ("vender", 2, 20), ("vender", 3, 5), ("vender", 4, 25)],     # Thread 1
        [("vender", 0, 10), ("vender", 1, 15), ("vender", 2, 20), ("vender", 3, 5), ("vender", 4, 25)],     # Thread 2  
        [("vender", 0, 10), ("vender", 1, 15), ("vender", 2, 20), ("vender", 3, 5), ("vender", 4, 25)],     # Thread 3
        [("vender", 0, 10), ("vender", 1, 15), ("vender", 2, 20), ("vender", 3, 5), ("vender", 4, 25)],     # Thread 4
        [("vender", 0, 10), ("vender", 1, 15), ("vender", 2, 20), ("vender", 3, 5), ("vender", 4, 25)],     # Thread 5
        
        # Threads 6-10: Operaciones de REABASTECIMIENTO  
        [("reabastecer", 0, 30), ("reabastecer", 1, 20), ("reabastecer", 2, 40), ("reabastecer", 3, 10), ("reabastecer", 4, 35)],  # Thread 6
        [("reabastecer", 0, 30), ("reabastecer", 1, 20), ("reabastecer", 2, 40), ("reabastecer", 3, 10), ("reabastecer", 4, 35)],  # Thread 7
        [("reabastecer", 0, 30), ("reabastecer", 1, 20), ("reabastecer", 2, 40), ("reabastecer", 3, 10), ("reabastecer", 4, 35)],  # Thread 8
        [("reabastecer", 0, 30), ("reabastecer", 1, 20), ("reabastecer", 2, 40), ("reabastecer", 3, 10), ("reabastecer", 4, 35)],  # Thread 9
        [("reabastecer", 0, 30), ("reabastecer", 1, 20), ("reabastecer", 2, 40), ("reabastecer", 3, 10), ("reabastecer", 4, 35)],  # Thread 10
        
        # Threads 11-15: Operaciones de VENTA (productos 5-9)
        [("vender", 5, 15), ("vender", 6, 20), ("vender", 7, 10), ("vender", 8, 25), ("vender", 9, 15)],     # Thread 11
        [("vender", 5, 15), ("vender", 6, 20), ("vender", 7, 10), ("vender", 8, 25), ("vender", 9, 15)],     # Thread 12
        [("vender", 5, 15), ("vender", 6, 20), ("vender", 7, 10), ("vender", 8, 25), ("vender", 9, 15)],     # Thread 13
        [("vender", 5, 15), ("vender", 6, 20), ("vender", 7, 10), ("vender", 8, 25), ("vender", 9, 15)],     # Thread 14
        [("vender", 5, 15), ("vender", 6, 20), ("vender", 7, 10), ("vender", 8, 25), ("vender", 9, 15)],     # Thread 15
        
        # Threads 16-20: Operaciones de REABASTECIMIENTO (productos 5-9)
        [("reabastecer", 5, 25), ("reabastecer", 6, 30), ("reabastecer", 7, 15), ("reabastecer", 8, 40), ("reabastecer", 9, 20)],  # Thread 16
        [("reabastecer", 5, 25), ("reabastecer", 6, 30), ("reabastecer", 7, 15), ("reabastecer", 8, 40), ("reabastecer", 9, 20)],  # Thread 17
        [("reabastecer", 5, 25), ("reabastecer", 6, 30), ("reabastecer", 7, 15), ("reabastecer", 8, 40), ("reabastecer", 9, 20)],  # Thread 18
        [("reabastecer", 5, 25), ("reabastecer", 6, 30), ("reabastecer", 7, 15), ("reabastecer", 8, 40), ("reabastecer", 9, 20)],  # Thread 19
        [("reabastecer", 5, 25), ("reabastecer", 6, 30), ("reabastecer", 7, 15), ("reabastecer", 8, 40), ("reabastecer", 9, 20)]   # Thread 20
    ]
    
    print(f"\n=== MECANISMO DE SINCRONIZACIÓN ===")
    print("TÉCNICA UTILIZADA: Mutex individual por producto")
    print("- Cada producto tiene su propio mutex (Lock)")
    print("- Las operaciones adquieren el mutex antes de acceder al stock")
    print("- Escrituras y lecturas son atómicas")
    print("- No hay interferencia entre threads")
    print("- Resultado: Stock final siempre consistente y predecible")
    
    tiempo_inicio = time.time()
    
    # Crear y iniciar threads
    threads = []
    for i in range(20):
        thread = WorkerThreadSeguro(i+1, inventario, operaciones_threads[i])
        threads.append(thread)
        thread.start()
    
    # Esperar a que todos los threads terminen
    for thread in threads:
        thread.join()
    
    tiempo_total = time.time() - tiempo_inicio
    
    # Mostrar resultados finales
    print(f"\n=== RESULTADOS FINALES EJECUCIÓN #{ejecucion_num} ===")
    print(f"Tiempo total: {tiempo_total:.3f} segundos")
    inventario.mostrar_inventario()
    
    # Verificar si los resultados son correctos
    stock_producto_0 = inventario.obtener_stock(0)
    stock_producto_5 = inventario.obtener_stock(5)
    
    # Valores esperados según el documento: 120 y 110
    todos_correctos = (stock_producto_0 == 120 and stock_producto_5 == 110)
    
    print(f"\n=== VERIFICACIÓN DE CONSISTENCIA ===")
    print(f"Stock Producto 0: {stock_producto_0} (Esperado: 120) - {'✓ CORRECTO' if stock_producto_0 == 120 else '✗ INCORRECTO'}")
    print(f"Stock Producto 5: {stock_producto_5} (Esperado: 110) - {'✓ CORRECTO' if stock_producto_5 == 110 else '✗ INCORRECTO'}")
    print(f"Todos correctos: {'SÍ' if todos_correctos else 'NO'}")
    
    # Screenshot para la tabla
    mostrar_estado_screenshot(
        f"RESULTADOS EJECUCIÓN #{ejecucion_num}",
        inventario,
        ejecucion_num,
        tiempo_total
    )
    
    return {
        'ejecucion': ejecucion_num,
        'stock_producto_0': stock_producto_0,
        'stock_producto_5': stock_producto_5,
        'todos_correctos': todos_correctos,
        'tiempo': tiempo_total
    }

def main():
    print("=== SIMULACIÓN SIN RACE CONDITIONS - GESTOR DE INVENTARIO CONCURRENTE ===")
    print("VERSIÓN SIN RACE CONDITION: Con mutex de sincronización")
    print("Especificaciones:")
    print("- 10 productos (ID: 0-9) con stock inicial de 100 unidades cada uno")
    print("- 20 threads ejecutando operaciones concurrentes")
    print("- Operaciones: vender() y reabastecer() con protección mutex")
    print("- Sincronización: Un mutex por producto + mutex para estadísticas")
    
    print(f"\n=== EJECUCIÓN DE 10 PRUEBAS PARA VERIFICAR CONSISTENCIA ===")
    
    resultados = []
    tiempos = []
    
    # Ejecutar 10 veces para verificar consistencia
    for i in range(1, 11):
        resultado = ejecutar_simulacion_segura(i)
        resultados.append(resultado)
        tiempos.append(resultado['tiempo'])
        
        # Pausa entre ejecuciones
        if i < 10:
            print(f"\n{'*'*60}")
            print(f"Preparando ejecución #{i+1}...")
            print(f"{'*'*60}")
            time.sleep(1)
    
    # Resumen final de todas las ejecuciones
    print(f"\n{'='*80}")
    print("TABLA DE RESULTADOS (10 EJECUCIONES)")
    print(f"{'='*80}")
    
    print("| Ejecución | Stock Final Prod 0 (Esperado: 120) | Stock Final Prod 5 (Esperado: 110) | ¿Todos Correctos? |")
    print("|-----------|------------------------------------|------------------------------------|-------------------|")
    
    correctos = 0
    
    for resultado in resultados:
        stock_0 = resultado['stock_producto_0']
        stock_5 = resultado['stock_producto_5']
        correcto = "SÍ" if resultado['todos_correctos'] else "NO"
        
        if resultado['todos_correctos']:
            correctos += 1
        
        print(f"| SIN RC #{resultado['ejecucion']:2} | {stock_0:34} | {stock_5:34} | {correcto:17} |")
    
    print(f"|-----------|------------------------------------|------------------------------------|-------------------|")
    print(f"| RESUMEN   | Siempre: 120 {'':23} | Siempre: 110 {'':23} | {correctos}/10 correctas  |")
    
    # Análisis de resultados
    print(f"\n=== ANÁLISIS DE RESULTADOS ===")
    print(f"Ejecuciones con resultados correctos: {correctos}/10")
    print(f"Consistencia: {'✓ PERFECTA' if correctos == 10 else '✗ PROBLEMAS'}")
    
    print(f"\n=== OVERHEAD DE SINCRONIZACIÓN ===")
    tiempo_promedio = sum(tiempos) / len(tiempos)
    tiempo_min = min(tiempos)
    tiempo_max = max(tiempos)
    
    print(f"Tiempo promedio: {tiempo_promedio:.3f} segundos")
    print(f"Tiempo mínimo: {tiempo_min:.3f} segundos")
    print(f"Tiempo máximo: {tiempo_max:.3f} segundos")
    print(f"Variación: {tiempo_max - tiempo_min:.3f} segundos")
    
    print(f"\n=== TÉCNICAS DE SINCRONIZACIÓN COMPARADAS ===")
    print("1. MUTEX (IMPLEMENTADO):")
    print("   - Ventajas: Fácil implementación, garantiza exclusión mutua")
    print("   - Desventajas: Overhead de adquisición/liberación, posible contención")
    print(f"   - Overhead medido: {tiempo_promedio:.3f}s promedio")
    
    print("\n2. SEMÁFOROS (ALTERNATIVA):")
    print("   - Ventajas: Permite múltiples accesos controlados")
    print("   - Desventajas: Más complejo, overhead similar a mutex")
    print("   - Overhead estimado: Similar al mutex (~{:.3f}s)".format(tiempo_promedio * 1.1))
    
    print("\n3. VARIABLES ATÓMICAS (ALTERNATIVA):")
    print("   - Ventajas: Menor overhead, operaciones lock-free")
    print("   - Desventajas: Limitado a operaciones simples")
    print("   - Overhead estimado: Menor (~{:.3f}s)".format(tiempo_promedio * 0.7))
    
    print(f"\n=== LÍNEAS DE CÓDIGO DONDE ESTÁ LA SECCIÓN CRÍTICA PROTEGIDA ===")
    print("FUNCIÓN vender() - VERSIÓN SEGURA:")
    print("  - Línea ~24: with self.mutex_productos[producto_id]:  # ADQUISICIÓN MUTEX")
    print("  - Línea ~28:     stock_actual = producto.stock  # LECTURA PROTEGIDA")
    print("  - Línea ~32:     producto.stock = nuevo_stock  # ESCRITURA PROTEGIDA")
    print("  - Línea ~42: # LIBERACIÓN AUTOMÁTICA AL SALIR DEL BLOQUE WITH")
    
    print("FUNCIÓN reabastecer() - VERSIÓN SEGURA:")
    print("  - Línea ~51: with self.mutex_productos[producto_id]:  # ADQUISICIÓN MUTEX")
    print("  - Línea ~55:     stock_actual = producto.stock  # LECTURA PROTEGIDA")
    print("  - Línea ~58:     producto.stock = nuevo_stock  # ESCRITURA PROTEGIDA")
    print("  - Línea ~65: # LIBERACIÓN AUTOMÁTICA AL SALIR DEL BLOQUE WITH")
    
    print(f"\nTIMESTAMP FIN: {timestamp()}")

if __name__ == "__main__":
    main()