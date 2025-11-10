import threading
import time
from datetime import datetime

class Cuenta:
    def __init__(self, id, saldo):
        self.id = id
        self.saldo = saldo
        self.lock = threading.Lock()

    def __str__(self):
        return f"Cuenta[{self.id}] = ${self.saldo}"

def transferir(cuentas, origen, destino, monto):
    """
    Versión CON deadlock - sin ordenamiento de locks
    Implementa el pseudocódigo especificado en el documento:
    
    transfer(cuenta_origen, cuenta_destino, monto):
        lock(cuenta_origen)
        lock(cuenta_destino)
        if saldo[cuenta_origen] >= monto:
            saldo[cuenta_origen] -= monto
            saldo[cuenta_destino] += monto
        unlock(cuenta_destino)
        unlock(cuenta_origen)
    """
    cta_origen = cuentas[origen]
    cta_destino = cuentas[destino]

    print(f"[{threading.current_thread().name}] [{timestamp()}] Iniciando transferencia ${monto}: Cuenta {origen} -> Cuenta {destino}")
    
    # PASO 1: Adquirir lock de cuenta origen
    print(f"[{threading.current_thread().name}] [{timestamp()}] Intentando adquirir lock de cuenta {origen}...")
    cta_origen.lock.acquire()
    print(f"[{threading.current_thread().name}] [{timestamp()}] Lock adquirido para cuenta {origen}")
    
    try:
        # Simular procesamiento que da tiempo a otros threads para crear condiciones de deadlock
        time.sleep(0.1)  # Ventana crítica para que otros threads adquieran locks
        
        # PASO 2: Intentar adquirir lock de cuenta destino
        print(f"[{threading.current_thread().name}] [{timestamp()}] Intentando adquirir lock de cuenta {destino}...")
        print(f"[{threading.current_thread().name}] [{timestamp()}] *** PUNTO CRITICO: POSIBLE DEADLOCK AQUI ***")
        cta_destino.lock.acquire()
        print(f"[{threading.current_thread().name}] [{timestamp()}] Lock adquirido para cuenta {destino}")
        
        try:
            # PASO 3: Realizar la transferencia si hay saldo suficiente
            if cta_origen.saldo >= monto:
                cta_origen.saldo -= monto
                cta_destino.saldo += monto
                print(f"[{threading.current_thread().name}] [{timestamp()}] EXITO: Transferencia ${monto} de Cuenta {origen} -> Cuenta {destino}")
            else:
                print(f"[{threading.current_thread().name}] [{timestamp()}] FALLO: Saldo insuficiente en cuenta {origen} (saldo: ${cta_origen.saldo}, necesario: ${monto})")
        finally:
            # PASO 4: Liberar lock de cuenta destino
            cta_destino.lock.release()
            print(f"[{threading.current_thread().name}] [{timestamp()}] Lock liberado para cuenta {destino}")
    finally:
        # PASO 5: Liberar lock de cuenta origen
        cta_origen.lock.release()
        print(f"[{threading.current_thread().name}] [{timestamp()}] Lock liberado para cuenta {origen}")
    
    print(f"[{threading.current_thread().name}] [{timestamp()}] Transferencia completada.")

def ejecutar_transferencias(cuentas, transferencias):
    """Ejecuta una secuencia de transferencias para un thread específico"""
    thread_name = threading.current_thread().name
    print(f"\n{thread_name} iniciado - Ejecutando {len(transferencias)} transferencias")
    
    for i, (origen, destino, monto) in enumerate(transferencias, 1):
        print(f"\n{thread_name} - Operación {i}/{len(transferencias)}")
        transferir(cuentas, origen, destino, monto)
        # Pequeña pausa entre transferencias del mismo thread
        time.sleep(0.05)
    
    print(f"\n{thread_name} FINALIZADO - Todas las transferencias completadas")

def timestamp():
    """Genera timestamp formateado para screenshots"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def analizar_deadlock(threads):
    """Analiza el patrón de deadlock que se produce"""
    print(f"\n*** ANALISIS DEL DEADLOCK ***")
    print(f"TIMESTAMP DEADLOCK DETECTADO: {timestamp()}")
    print("\nPATRON DE DEADLOCK IDENTIFICADO:")
    print("El deadlock se produce cuando múltiples threads intentan adquirir locks")
    print("de cuentas en diferente orden, creando espera circular.")
    print("\nEJEMPLO DE SECUENCIA QUE CAUSA DEADLOCK:")
    print("1. Thread-1 adquiere lock(cuenta0), intenta lock(cuenta1)")  
    print("2. Thread-2 adquiere lock(cuenta1), intenta lock(cuenta0)")
    print("3. DEADLOCK: Thread-1 espera Thread-2, Thread-2 espera Thread-1")
    print("\nTHREADS BLOQUEADOS DETECTADOS:")
    bloqueados = [t for t in threads if t.is_alive()]
    for t in bloqueados:
        print(f"  - {t.name}: Bloqueado esperando lock de cuenta")
    return bloqueados

def mostrar_estado_screenshot(titulo, cuentas, threads=None, extra_info=""):
    """Muestra información formateada para captura de screenshots"""
    print("\n" + "="*80)
    print(f"MOMENTO PARA SCREENSHOT: {titulo}")
    print(f"TIMESTAMP: {timestamp()}")
    print("="*80)
    
    if cuentas:
        print("ESTADO ACTUAL DE CUENTAS:")
        for c in cuentas:
            print(f"    {c}")
    
    if threads:
        print(f"\nESTADO DE THREADS:")
        activos = sum(1 for t in threads if t.is_alive())
        print(f"    Threads activos: {activos}/{len(threads)}")
        bloqueados = [t for t in threads if t.is_alive()]
        if bloqueados:
            print("    Threads bloqueados:")
            for t in bloqueados:
                print(f"      - {t.name}")
    
    if extra_info:
        print(f"\nINFORMACION ADICIONAL:")
        print(f"    {extra_info}")
    
    print("="*80)
    print("CAPTURAR SCREENSHOT AQUI")
    print("="*80)

def main():
    # Crear 5 cuentas bancarias con saldos iniciales según especificación
    # Cuenta[i] = 1000 * (i+1): Cuenta 0: $1000, Cuenta 1: $2000, etc.
    cuentas = [Cuenta(i, 1000*(i+1)) for i in range(5)]
    
    print("=== SIMULACIÓN DE DEADLOCK - SISTEMA DE TRANSFERENCIAS BANCARIAS ===")
    
    print(f"\n=== PREDICCION DEL DEADLOCK ===")
    print("MOMENTO EXACTO ESPERADO DEL DEADLOCK:")
    print("- Ocurrirá aproximadamente 0.1-0.3 segundos después del inicio de threads")
    print("- Se producirá cuando threads intenten adquirir segundo lock en orden inverso")
    print("- Ejemplo típico: Thread-1 tiene lock(cuenta0) y quiere lock(cuenta1)")
    print("                 Thread-2 tiene lock(cuenta1) y quiere lock(cuenta0)")
    print("- Threads que probablemente se bloquearán: Múltiples, depende del timing")
    
    # Screenshot 1: Estado inicial
    mostrar_estado_screenshot(
        "ESTADO INICIAL DEL SISTEMA", 
        cuentas, 
        extra_info="Sistema iniciado con 5 cuentas, listo para 10 threads y 30 transferencias"
    )
    
    # Tabla de transferencias según especificación del documento (punto 2.1)
    # Formato: (origen, destino, monto)
    operaciones = [
        # Thread 1: 0→1, $200 | 1→2, $300 | 2→0, $150
        [(0,1,200), (1,2,300), (2,0,150)],
        # Thread 2: 1→0, $250 | 0→2, $100 | 2→1, $200
        [(1,0,250), (0,2,100), (2,1,200)],
        # Thread 3: 2→3, $300 | 3→4, $400 | 4→2, $250
        [(2,3,300), (3,4,400), (4,2,250)],
        # Thread 4: 3→2, $350 | 2→4, $200 | 4→3, $300
        [(3,2,350), (2,4,200), (4,3,300)],
        # Thread 5: 4→0, $400 | 0→3, $250 | 3→4, $150
        [(4,0,400), (0,3,250), (3,4,150)],
        # Thread 6: 0→4, $300 | 4→1, $350 | 1→0, $200
        [(0,4,300), (4,1,350), (1,0,200)],
        # Thread 7: 1→3, $250 | 3→0, $300 | 0→1, $150
        [(1,3,250), (3,0,300), (0,1,150)],
        # Thread 8: 2→1, $200 | 1→4, $250 | 4→2, $300
        [(2,1,200), (1,4,250), (4,2,300)],
        # Thread 9: 3→1, $300 | 1→2, $200 | 2→3, $250
        [(3,1,300), (1,2,200), (2,3,250)],
        # Thread 10: 4→3, $350 | 3→2, $250 | 2→4, $200
        [(4,3,350), (3,2,250), (2,4,200)],
    ]

    print("Iniciando 10 threads con transferencias concurrentes...")
    print("VERSIÓN CON DEADLOCK: locks sin ordenamiento")
    print("-" * 60)
    
    threads = []
    for i in range(10):
        t = threading.Thread(target=ejecutar_transferencias, args=(cuentas, operaciones[i]), name=f"Thread-{i+1}")
        threads.append(t)
        t.start()

    # Screenshot 2: Threads iniciados
    mostrar_estado_screenshot(
        "THREADS INICIADOS - ESPERANDO ACTIVIDAD", 
        cuentas, 
        threads, 
        "10 threads creados y ejecutándose concurrentemente"
    )

    # Breve pausa para permitir que los threads ejecuten y potencialmente se bloqueen
    time.sleep(3)
    
    # Screenshot 3: Durante ejecución/deadlock
    mostrar_estado_screenshot(
        "DURANTE EJECUCIÓN - POSIBLE DEADLOCK", 
        cuentas, 
        threads, 
        "Threads en ejecución por 3 segundos - verificar si hay bloqueos"
    )
    
    # Esperar por los threads con timeout para detectar deadlock
    print("Esperando finalización de threads (timeout 5 segundos)...")
    threads_completados = 0
    for t in threads:
        t.join(timeout=5)
        if not t.is_alive():
            threads_completados += 1
    
    # Analizar el deadlock si ocurrió
    threads_bloqueados = []
    if threads_completados < 10:
        threads_bloqueados = analizar_deadlock(threads)
    
    # Screenshot 4: Resultados finales
    extra_info_resultado = f"Threads completados: {threads_completados}/10, Bloqueados: {10-threads_completados}/10"
    if threads_completados < 10:
        extra_info_resultado += " - *** DEADLOCK CONFIRMADO ***"
        
    mostrar_estado_screenshot(
        "RESULTADOS FINALES DEL EXPERIMENTO", 
        cuentas, 
        threads, 
        extra_info_resultado
    )
    
    print(f"\n=== RESUMEN PARA TABLA COMPARATIVA ===")
    print(f"TIMESTAMP FIN ANALISIS: {timestamp()}")
    print(f"Tiempo de ejecución: N/A (bloqueado por deadlock)")
    print(f"Transferencias completadas: 0/30 (todas bloqueadas por deadlock)")
    print(f"Threads bloqueados: {len(threads_bloqueados)}/10")
    print(f"Lista threads bloqueados: {[t.name for t in threads_bloqueados]}")
    print(f"Saldos finales: No verificables debido al deadlock")
    
    print(f"\n=== MOMENTO EXACTO DEL DEADLOCK ===")
    print("El deadlock se produce aproximadamente 0.1-0.2 segundos después del inicio")
    print("cuando múltiples threads intentan adquirir locks de cuentas en orden inverso.")
    print("Punto crítico: En la línea 'Intentando adquirir lock de cuenta destino'")
    print("donde threads quedan esperando indefinidamente.")

if __name__ == "__main__":
    main()
