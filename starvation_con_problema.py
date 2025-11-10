import threading
import time
import queue
from datetime import datetime
from collections import deque
import random

class Tarea:
    def __init__(self, id, prioridad, tiempo_creacion):
        self.id = id
        self.prioridad = prioridad  # 'A' (Alta), 'M' (Media), 'B' (Baja)
        self.tiempo_creacion = tiempo_creacion
        self.tiempo_procesamiento = {'A': 0.05, 'M': 0.1, 'B': 0.15}[prioridad]  # 500ms, 1000ms, 1500ms - MÁS LENTO
        
    def __str__(self):
        return f"Tarea[{self.id}]-{self.prioridad}"

class ColaPrioridades:
    def __init__(self, capacidad_maxima=20):
        self.capacidad_maxima = capacidad_maxima
        self.cola_alta = deque()      # Prioridad A
        self.cola_media = deque()     # Prioridad M  
        self.cola_baja = deque()      # Prioridad B
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)
        
    def put(self, tarea):
        with self.lock:
            while self.size() >= self.capacidad_maxima:
                self.not_full.wait()
            
            # Agregar según prioridad
            if tarea.prioridad == 'A':
                self.cola_alta.append(tarea)
            elif tarea.prioridad == 'M':
                self.cola_media.append(tarea)
            else:
                self.cola_baja.append(tarea)
            
            self.not_empty.notify()
    
    def get(self):
        """VERSIÓN CON STARVATION: Siempre prioriza A y M sobre B"""
        with self.lock:
            while self.size() == 0:
                self.not_empty.wait()
            
            # POLÍTICA QUE CAUSA STARVATION: Siempre tomar A primero, luego M, nunca B si hay A o M
            if self.cola_alta:
                tarea = self.cola_alta.popleft()
            elif self.cola_media:
                tarea = self.cola_media.popleft()
            elif self.cola_baja:
                tarea = self.cola_baja.popleft()
            else:
                return None
                
            self.not_full.notify()
            return tarea
    
    def size(self):
        return len(self.cola_alta) + len(self.cola_media) + len(self.cola_baja)
    
    def get_estado(self):
        """Retorna el estado actual de las colas"""
        return {
            'A': len(self.cola_alta),
            'M': len(self.cola_media), 
            'B': len(self.cola_baja),
            'total': self.size()
        }

def timestamp():
    """Genera timestamp formateado"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def mostrar_estado_screenshot(titulo, cola, stats, tiempo_seg, extra_info=""):
    """Muestra información formateada para captura de screenshots"""
    print("\n" + "="*80)
    print(f"MOMENTO PARA SCREENSHOT: {titulo}")
    print(f"TIMESTAMP: {timestamp()}")
    print(f"TIEMPO TRANSCURRIDO: {tiempo_seg} segundos")
    print("="*80)
    
    estado = cola.get_estado()
    print("ESTADO DE LA COLA:")
    print(f"    Tareas A en cola: {estado['A']}")
    print(f"    Tareas M en cola: {estado['M']}")
    print(f"    Tareas B en cola: {estado['B']}")
    print(f"    Total en cola: {estado['total']}")
    
    print("\nTAREAS PROCESADAS:")
    print(f"    Tareas A procesadas: {stats['A_procesadas']}")
    print(f"    Tareas M procesadas: {stats['M_procesadas']}")
    print(f"    Tareas B procesadas: {stats['B_procesadas']}")
    print(f"    Tareas B en espera: {estado['B']}")
    
    if extra_info:
        print(f"\nINFORMACION ADICIONAL:")
        print(f"    {extra_info}")
    
    print("="*80)
    print("CAPTURAR SCREENSHOT AQUI")
    print("="*80)

class Producer(threading.Thread):
    def __init__(self, cola, producer_id, secuencia_tareas):
        super().__init__(name=f"Producer-{producer_id}")
        self.cola = cola
        self.producer_id = producer_id
        self.secuencia_tareas = secuencia_tareas
        self.tarea_counter = 0
        
    def run(self):
        print(f"[{self.name}] [{timestamp()}] Iniciado")
        
        # Generar SOLO las tareas específicas del documento (30 total)
        for prioridad in self.secuencia_tareas:
            self.tarea_counter += 1
            tarea_id = f"{self.producer_id}-{self.tarea_counter}"
            tarea = Tarea(tarea_id, prioridad, time.time())
            
            print(f"[{self.name}] [{timestamp()}] Produciendo {tarea}")
            self.cola.put(tarea)
            
            # Pausa entre producciones para simular llegada realista
            time.sleep(0.2)
        
        print(f"[{self.name}] [{timestamp()}] Finalizado - {len(self.secuencia_tareas)} tareas producidas")

class Consumer(threading.Thread):
    def __init__(self, cola, consumer_id, stats, tiempo_limite=10):
        super().__init__(name=f"Consumer-{consumer_id}")
        self.cola = cola
        self.consumer_id = consumer_id
        self.stats = stats
        self.tiempo_limite = tiempo_limite
        self.running = True
        
    def run(self):
        print(f"[{self.name}] [{timestamp()}] Iniciado")
        tiempo_inicio = time.time()
        
        while self.running and (time.time() - tiempo_inicio) < self.tiempo_limite:
            try:
                tarea = self.cola.get()
                if tarea is None:
                    continue
                    
                tiempo_espera = time.time() - tarea.tiempo_creacion
                print(f"[{self.name}] [{timestamp()}] Procesando {tarea} (espera: {tiempo_espera:.3f}s)")
                
                # Simular procesamiento
                time.sleep(tarea.tiempo_procesamiento)
                
                # Actualizar estadísticas
                with self.stats['lock']:
                    key = f"{tarea.prioridad}_procesadas"
                    self.stats[key] += 1
                    if tarea.prioridad == 'B':
                        self.stats['tiempo_espera_B'].append(tiempo_espera)
                
                print(f"[{self.name}] [{timestamp()}] Completado {tarea}")
                
            except Exception as e:
                print(f"[{self.name}] Error: {e}")
                time.sleep(0.1)
        
        self.running = False
        print(f"[{self.name}] [{timestamp()}] Finalizado por timeout ({self.tiempo_limite}s)")

def main():
    print("=== SIMULACION DE STARVATION - SISTEMA DE PRIORIDADES DE TAREAS ===")
    print("VERSIÓN CON STARVATION: Siempre se priorizan tareas A y M")
    
    # Crear cola compartida
    cola = ColaPrioridades(capacidad_maxima=20)
    
    # Estadísticas compartidas
    stats = {
        'A_procesadas': 0,
        'M_procesadas': 0,
        'B_procesadas': 0,
        'tiempo_espera_B': [],
        'lock': threading.Lock()
    }
    
    # Screenshot 1: Estado inicial
    mostrar_estado_screenshot(
        "ESTADO INICIAL DEL SISTEMA", 
        cola, 
        stats, 
        0,
        "Sistema iniciado - 3 productores (30 tareas específicas) y 2 consumidores - DISEÑADO PARA STARVATION"
    )
    
    # Secuencia específica de 30 tareas según el documento
    secuencias = [
        ['B','B','M','B','B','B','A','M','B','B'],      # Tareas 1-10
        ['M','B','B','B','A','B','M','B','B','B'],      # Tareas 11-20  
        ['B','B','B','M','A','B','B','M','B','B']       # Tareas 21-30
    ]
    
    print(f"\n=== PREDICCION DE STARVATION ===")
    print("MOMENTO ESPERADO DE STARVATION:")
    print("- Las tareas B comenzarán a acumularse inmediatamente")
    print("- A medida que lleguen más tareas A y M, las B nunca serán procesadas")
    print("- Después de 10 segundos, múltiples tareas B quedarán sin procesar")
    
    tiempo_inicio = time.time()
    
    # Crear y iniciar productores - SOLO 3 productores para las 30 tareas específicas
    producers = []
    for i in range(3):  # CORREGIDO: Solo 3 productores para 30 tareas exactas
        secuencia = secuencias[i]
        producer = Producer(cola, i+1, secuencia)
        producers.append(producer)
        producer.start()
    
    # Crear y iniciar consumidores - REDUCIDO A 2 para crear cuello de botella
    consumers = []
    for i in range(2):  # CORREGIDO: Solo 2 consumidores en lugar de 3
        consumer = Consumer(cola, i+1, stats, tiempo_limite=10)
        consumers.append(consumer)
        consumer.start()
    
    # Monitoreo temporal cada 2 segundos
    tiempos_monitoreo = [2, 4, 6, 8, 10]
    
    for tiempo_objetivo in tiempos_monitoreo:
        # Esperar hasta el tiempo objetivo
        while (time.time() - tiempo_inicio) < tiempo_objetivo:
            time.sleep(0.1)
        
        tiempo_actual = int(time.time() - tiempo_inicio)
        extra_info = f"Monitoreo programado a los {tiempo_objetivo} segundos"
        
        if tiempo_objetivo == 10:
            extra_info += " - *** EVIDENCIA DE STARVATION ***"
        
        mostrar_estado_screenshot(
            f"MONITOREO A LOS {tiempo_objetivo} SEGUNDOS",
            cola,
            stats,
            tiempo_actual,
            extra_info
        )
    
    # Finalizar productores
    for producer in producers:
        producer.join()
    
    # Detener consumidores después de 10 segundos
    time.sleep(max(0, 10 - (time.time() - tiempo_inicio)))
    for consumer in consumers:
        consumer.running = False
        consumer.join()
    
    # Resultados finales
    tiempo_total = time.time() - tiempo_inicio
    estado_final = cola.get_estado()
    
    print(f"\n=== RESULTADOS FINALES ===")
    print(f"TIMESTAMP FIN: {timestamp()}")
    print(f"Tiempo total de ejecución: {tiempo_total:.2f} segundos")
    
    print(f"\n=== TABLA DE MONITOREO TEMPORAL ===")
    print("| Tiempo (seg) | Tareas A Procesadas | Tareas M Procesadas | Tareas B Procesadas | Tareas B en Espera |")
    print("|--------------|--------------------|--------------------|--------------------|--------------------|")
    print(f"| Final        | {stats['A_procesadas']:18} | {stats['M_procesadas']:18} | {stats['B_procesadas']:18} | {estado_final['B']:18} |")
    
    print(f"\n=== EVIDENCIA DE STARVATION ===")
    print(f"Tareas B sin procesar después de 10 segundos: {estado_final['B']}")
    print(f"Total de tareas B procesadas: {stats['B_procesadas']}")
    
    if stats['tiempo_espera_B']:
        tiempo_max_espera = max(stats['tiempo_espera_B'])
        tiempo_promedio_espera = sum(stats['tiempo_espera_B']) / len(stats['tiempo_espera_B'])
        print(f"Tiempo de espera máximo para tareas B: {tiempo_max_espera:.3f} segundos")
        print(f"Tiempo de espera promedio para tareas B: {tiempo_promedio_espera:.3f} segundos")
    else:
        print("Tiempo de espera máximo para tareas B: No aplicable (ninguna procesada)")
    
    print(f"\n=== ANÁLISIS DEL STARVATION ===")
    print("CAUSA DEL STARVATION:")
    print("- La política 'siempre priorizar A y M' impide que las tareas B sean procesadas")
    print("- Las tareas B se acumulan indefinidamente mientras haya tareas A o M")
    print("- No existe mecanismo de aging o time-slice para garantizar progreso de B")
    
    print(f"\n=== SECUENCIA ESPECÍFICA QUE CAUSA STARVATION ===")
    print("1. Llegan tareas B y se encolan")
    print("2. Llegan tareas A/M que tienen mayor prioridad")
    print("3. Consumidores siempre toman A/M, dejando B esperando")
    print("4. STARVATION: Las tareas B nunca obtienen CPU")

if __name__ == "__main__":
    main()