#!/usr/bin/env python3
"""
Script de Prueba - Punto 2.3 Race Conditions
Ejecuta ambas versiones del gestor de inventario para comparación
"""

import subprocess
import sys
import time
from datetime import datetime

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ejecutar_version(archivo, descripcion, num_ejecuciones=3):
    """Ejecuta una versión específica del programa"""
    print(f"\n{'='*80}")
    print(f"EJECUTANDO: {descripcion}")
    print(f"ARCHIVO: {archivo}")
    print(f"TIMESTAMP: {timestamp()}")
    print(f"{'='*80}")
    
    for i in range(1, num_ejecuciones + 1):
        print(f"\n{'-'*60}")
        print(f"EJECUCIÓN {i}/{num_ejecuciones} - {descripcion}")
        print(f"{'-'*60}")
        
        try:
            # Ejecutar el archivo Python
            resultado = subprocess.run([sys.executable, archivo], 
                                     capture_output=True, 
                                     text=True, 
                                     timeout=120)
            
            if resultado.returncode == 0:
                print("✓ EJECUCIÓN EXITOSA")
                # Mostrar solo las últimas líneas del output para no saturar
                lineas = resultado.stdout.split('\n')
                lineas_importantes = [l for l in lineas if 'RESULTADO' in l or 'Stock' in l or 'TABLA' in l]
                
                if lineas_importantes:
                    print("RESULTADOS CLAVE:")
                    for linea in lineas_importantes[-10:]:  # Últimas 10 líneas importantes
                        print(f"  {linea}")
                else:
                    # Si no hay líneas importantes, mostrar las últimas líneas generales
                    print("SALIDA FINAL:")
                    for linea in lineas[-5:]:
                        if linea.strip():
                            print(f"  {linea}")
            else:
                print("✗ ERROR EN EJECUCIÓN")
                print(f"Código de salida: {resultado.returncode}")
                print(f"Error: {resultado.stderr}")
                
        except subprocess.TimeoutExpired:
            print("✗ TIMEOUT - La ejecución tardó más de 2 minutos")
        except Exception as e:
            print(f"✗ EXCEPCIÓN: {e}")
        
        if i < num_ejecuciones:
            print(f"\nEsperando 2 segundos antes de la siguiente ejecución...")
            time.sleep(2)

def main():
    print("="*80)
    print("SCRIPT DE PRUEBA - PUNTO 2.3 RACE CONDITIONS")
    print("Gestor de Inventario Concurrente")
    print(f"Inicio: {timestamp()}")
    print("="*80)
    
    print("\nEste script ejecutará ambas versiones del programa:")
    print("1. Versión CON race conditions (resultados inconsistentes)")
    print("2. Versión SIN race conditions (resultados consistentes)")
    print("\nCada versión se ejecutará 3 veces para demostración.")
    
    # Verificar que los archivos existan
    archivos = [
        ("race_condition_con_problema.py", "Versión CON Race Conditions"),
        ("race_condition_solucion.py", "Versión SIN Race Conditions")
    ]
    
    for archivo, descripcion in archivos:
        try:
            with open(archivo, 'r') as f:
                print(f"✓ {archivo} encontrado")
        except FileNotFoundError:
            print(f"✗ ERROR: {archivo} no encontrado")
            print(f"Asegúrate de que todos los archivos estén en el directorio actual")
            return 1
    
    print(f"\n🚀 Iniciando ejecuciones...")
    
    # Ejecutar versión CON race conditions
    ejecutar_version("race_condition_con_problema.py", 
                     "Versión CON Race Conditions", 
                     num_ejecuciones=3)
    
    print(f"\n⏳ Pausa de 5 segundos entre versiones...")
    time.sleep(5)
    
    # Ejecutar versión SIN race conditions  
    ejecutar_version("race_condition_solucion.py", 
                     "Versión SIN Race Conditions", 
                     num_ejecuciones=3)
    
    print(f"\n{'='*80}")
    print("RESUMEN DE PRUEBAS COMPLETADO")
    print(f"Fin: {timestamp()}")
    print("="*80)
    
    print("\n📋 CONCLUSIONES ESPERADAS:")
    print("• Versión CON race conditions: Stocks finales variables e inconsistentes")
    print("• Versión SIN race conditions: Stocks finales siempre correctos (120, 110)")
    print("• Overhead de sincronización: Tiempo ligeramente mayor en versión segura")
    
    print("\n📸 PARA DOCUMENTACIÓN:")
    print("• Capturar screenshots de los resultados finales de cada ejecución")
    print("• Documentar la tabla de 10 ejecuciones para cada versión")
    print("• Comparar tiempos de ejecución entre ambas versiones")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())