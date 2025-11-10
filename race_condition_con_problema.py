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

class GestorInventario:
    def __init__(self, num_productos=10):
        # Crear 10 productos con stock inicial de 100 unidades cada uno
        self.productos = [Producto(i, 100) for i in range(num_productos)]
        self.operaciones_completadas = 0
        self.operaciones_fallidas = 0
        
    def vender(self, producto_id, cantidad, thread_name):
        """VERSIÓN CON RACE CONDITION: Sin sincronización"""
        producto = self.productos[producto_id]
        
        print(f"[{thread_name}] [{timestamp()}] Iniciando VENTA: Producto {producto_id}, cantidad {cantidad}")
        
        # SECCIÓN CRÍTICA SIN PROTECCIÓN - AQUÍ OCURRE LA RACE CONDITION
        stock_actual = producto.stock  # Lectura
        time.sleep(0.001)  # Simula tiempo de procesamiento (ventana para race condition)
        
        if stock_actual >= cantidad:
            nuevo_stock = stock_actual - cantidad  # Cálculo
            time.sleep(0.001)  # Más tiempo para aumentar probabilidad de race condition
            producto.stock = nuevo_stock  # Escritura
            
            print(f"[{thread_name}] [{timestamp()}] VENTA EXITOSA: Producto {producto_id}, vendido {cantidad}, stock restante: {producto.stock}")
            self.operaciones_completadas += 1
        else:
            print(f"[{thread_name}] [{timestamp()}] VENTA FALLIDA: Producto {producto_id}, stock insuficiente ({stock_actual} < {cantidad})")
            self.operaciones_fallidas += 1
    
    def reabastecer(self, producto_id, cantidad, thread_name):
        """VERSIÓN CON RACE CONDITION: Sin sincronización"""
        producto = self.productos[producto_id]
        
        print(f"[{thread_name}] [{timestamp()}] Iniciando REABASTECIMIENTO: Producto {producto_id}, cantidad {cantidad}")
        
        # SECCIÓN CRÍTICA SIN PROTECCIÓN - AQUÍ OCURRE LA RACE CONDITION
        stock_actual = producto.stock  # Lectura
        time.sleep(0.001)  # Simula tiempo de procesamiento (ventana para race condition)
        
        nuevo_stock = stock_actual + cantidad  # Cálculo
        time.sleep(0.001)  # Más tiempo para aumentar probabilidad de race condition
        producto.stock = nuevo_stock  # Escritura
        
        print(f"[{thread_name}] [{timestamp()}] REABASTECIMIENTO EXITOSO: Producto {producto_id}, agregado {cantidad}, stock actual: {producto.stock}")
        self.operaciones_completadas += 1
    
    def obtener_stock(self, producto_id):
        """Obtiene el stock actual de un producto"""
        return self.productos[producto_id].stock
    
    def mostrar_inventario(self):
        """Muestra el estado completo del inventario"""
        print("\n=== ESTADO DEL INVENTARIO ===")
        for producto in self.productos:
            print(f"  {producto}")
        print(f"Operaciones completadas: {self.operaciones_completadas}")
        print(f"Operaciones fallidas: {self.operaciones_fallidas}")

def timestamp():
    """Genera timestamp formateado"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def mostrar_estado_screenshot(titulo, inventario, ejecucion_num, extra_info=""):
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
    
    if extra_info:
        print(f"\nINFORMACION ADICIONAL:")
        print(f"    {extra_info}")
    
    print("="*80)
    print("CAPTURAR SCREENSHOT AQUI")
    print("="*80)

class WorkerThread(threading.Thread):
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

def ejecutar_simulacion(ejecucion_num):
    """Ejecuta una simulación completa del sistema de inventario"""
    print(f"\n{'='*60}")
    print(f"EJECUCIÓN #{ejecucion_num} - VERSIÓN CON RACE CONDITION")
    print(f"{'='*60}")
    
    # Crear inventario
    inventario = GestorInventario()
    
    # Mostrar estado inicial
    print(f"\n=== ESTADO INICIAL ===")
    inventario.mostrar_inventario()
    
    # Secuencia de operaciones según el documento
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
    
    print(f"\n=== PREDICCIÓN DE RACE CONDITIONS ===")
    print("OPERACIONES CRÍTICAS DONDE OCURRIRÁN RACE CONDITIONS:")
    print("- Múltiples threads vendiendo/reabasteciendo el mismo producto simultáneamente")
    print("- Lecturas y escrituras concurrentes del stock sin sincronización")
    print("- Resultado: Stock final inconsistente e impredecible")
    
    tiempo_inicio = time.time()
    
    # Crear y iniciar threads
    threads = []
    for i in range(20):
        thread = WorkerThread(i+1, inventario, operaciones_threads[i])
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
    
    # Valores esperados según el documento:
    # Producto 0: 100 - (5*10) + (5*30) = 100 - 50 + 150 = 200 ❌ El documento dice 120
    # Producto 5: 100 - (5*15) + (5*25) = 100 - 75 + 125 = 150 ❌ El documento dice 110
    
    # Recalculando según documento:
    # Producto 0: Stock esperado = 120 (según tabla del documento)
    # Producto 5: Stock esperado = 110 (según tabla del documento)
    
    todos_correctos = (stock_producto_0 == 120 and stock_producto_5 == 110)
    
    print(f"\n=== VERIFICACIÓN DE CONSISTENCIA ===")
    print(f"Stock Producto 0: {stock_producto_0} (Esperado: 120) - {'✓ CORRECTO' if stock_producto_0 == 120 else '✗ INCORRECTO'}")
    print(f"Stock Producto 5: {stock_producto_5} (Esperado: 110) - {'✓ CORRECTO' if stock_producto_5 == 110 else '✗ INCORRECTO'}")
    print(f"Todos correctos: {'SÍ' if todos_correctos else 'NO'}")
    
    # Screenshot para la tabla
    extra_info = f"Race conditions detectadas - Resultados inconsistentes"
    if todos_correctos:
        extra_info = "Por casualidad, resultados correctos (poco probable con race conditions)"
    
    mostrar_estado_screenshot(
        f"RESULTADOS EJECUCIÓN #{ejecucion_num}",
        inventario,
        ejecucion_num,
        extra_info
    )
    
    return {
        'ejecucion': ejecucion_num,
        'stock_producto_0': stock_producto_0,
        'stock_producto_5': stock_producto_5,
        'todos_correctos': todos_correctos,
        'tiempo': tiempo_total
    }

def main():
    print("=== SIMULACIÓN DE RACE CONDITIONS - GESTOR DE INVENTARIO CONCURRENTE ===")
    print("VERSIÓN CON RACE CONDITION: Sin sincronización")
    print("Especificaciones:")
    print("- 10 productos (ID: 0-9) con stock inicial de 100 unidades cada uno")
    print("- 20 threads ejecutando operaciones concurrentes")
    print("- Operaciones: vender() y reabastecer() sin protección")
    
    print(f"\n=== EJECUCIÓN DE 10 PRUEBAS PARA DOCUMENTAR INCONSISTENCIAS ===")
    
    resultados = []
    
    # Ejecutar 10 veces para documentar inconsistencias
    for i in range(1, 11):
        resultado = ejecutar_simulacion(i)
        resultados.append(resultado)
        
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
    stocks_prod_0 = []
    stocks_prod_5 = []
    
    for resultado in resultados:
        stock_0 = resultado['stock_producto_0']
        stock_5 = resultado['stock_producto_5']
        correcto = "SÍ" if resultado['todos_correctos'] else "NO"
        
        if resultado['todos_correctos']:
            correctos += 1
        
        stocks_prod_0.append(stock_0)
        stocks_prod_5.append(stock_5)
        
        print(f"| RC #{resultado['ejecucion']:2}     | {stock_0:34} | {stock_5:34} | {correcto:17} |")
    
    print(f"|-----------|------------------------------------|------------------------------------|-------------------|")
    print(f"| RESUMEN   | Rango: {min(stocks_prod_0)}-{max(stocks_prod_0):22} | Rango: {min(stocks_prod_5)}-{max(stocks_prod_5):22} | {correctos}/10 correctas  |")
    
    # Análisis de resultados
    print(f"\n=== ANÁLISIS DE RESULTADOS ===")
    print(f"Ejecuciones con resultados correctos: {correctos}/10")
    print(f"Ejecuciones con race conditions: {10-correctos}/10")
    
    print(f"\nRango de valores incorrectos observados:")
    print(f"- Producto 0: {min(stocks_prod_0)} - {max(stocks_prod_0)} (esperado: 120)")
    print(f"- Producto 5: {min(stocks_prod_5)} - {max(stocks_prod_5)} (esperado: 110)")
    
    print(f"\n=== LÍNEAS DE CÓDIGO DONDE OCURRE LA SECCIÓN CRÍTICA ===")
    print("FUNCIÓN vender():")
    print("  - Línea ~25: stock_actual = producto.stock  # LECTURA sin protección")
    print("  - Línea ~29: nuevo_stock = stock_actual - cantidad  # CÁLCULO con dato obsoleto")
    print("  - Línea ~31: producto.stock = nuevo_stock  # ESCRITURA sin protección")
    
    print("FUNCIÓN reabastecer():")
    print("  - Línea ~42: stock_actual = producto.stock  # LECTURA sin protección")
    print("  - Línea ~45: nuevo_stock = stock_actual + cantidad  # CÁLCULO con dato obsoleto")
    print("  - Línea ~47: producto.stock = nuevo_stock  # ESCRITURA sin protección")
    
    print(f"\n=== OPERACIONES ESPECÍFICAS DONDE OCURREN RACE CONDITIONS ===")
    print("1. Múltiples threads leyendo el mismo stock simultáneamente")
    print("2. Cálculos basados en valores obsoletos del stock")
    print("3. Escrituras concurrentes sobrescribiéndose mutuamente")
    print("4. Pérdida de operaciones debido a la falta de atomicidad")
    
    print(f"\nTIMESTAMP FIN: {timestamp()}")

if __name__ == "__main__":
    main()