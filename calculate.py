#!/usr/bin/env python3
"""
Calculadora de números primos paralelizable.
Utiliza la Criba de Eratóstenes para encontrar primos en un rango.
"""

import json
import sys
import os
import time
import math
from pathlib import Path


def load_config():
    """Carga la configuración desde config.json"""
    with open('config.json', 'r') as f:
        return json.load(f)


def sieve_of_eratosthenes(start, end):
    """
    Implementación de la Criba de Eratóstenes para un rango específico.
    Este es un algoritmo pesado computacionalmente para rangos grandes.
    
    Args:
        start: número inicial del rango
        end: número final del rango
    
    Returns:
        lista de números primos en el rango
    """
    if end < 2:
        return []
    
    # Ajustar el inicio para asegurar que empezamos desde al menos 2
    start = max(2, start)
    
    # Crear un array booleano para marcar números primos
    # Usamos un enfoque de ventana para rangos grandes
    size = end - start + 1
    is_prime = [True] * size
    
    # Necesitamos todos los primos hasta sqrt(end) para cribar
    sqrt_end = int(math.sqrt(end)) + 1
    base_primes = simple_sieve(sqrt_end)
    
    # Cribar el rango usando los primos base
    for prime in base_primes:
        # Encontrar el primer múltiplo de prime en nuestro rango
        first_multiple = ((start + prime - 1) // prime) * prime
        
        # Si el primer múltiplo es el primo mismo y está en nuestro rango, comenzar desde el siguiente
        if first_multiple == prime:
            first_multiple += prime
            
        # Marcar todos los múltiplos como no primos
        for j in range(first_multiple, end + 1, prime):
            is_prime[j - start] = False
    
    # Recolectar todos los números primos
    primes = [start + i for i in range(size) if is_prime[i]]
    
    return primes


def simple_sieve(n):
    """Criba simple para números pequeños (para obtener primos base)"""
    if n < 2:
        return []
    
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    
    return [i for i in range(n + 1) if is_prime[i]]


def process_input_range(input_file, start_idx, end_idx, output_dir):
    """
    Procesa un rango de inputs desde un archivo.
    
    Args:
        input_file: archivo con los rangos a procesar
        start_idx: índice inicial (inclusivo)
        end_idx: índice final (inclusivo)
        output_dir: directorio donde guardar los resultados
    """
    # Leer los rangos del archivo
    with open(input_file, 'r') as f:
        ranges = [line.strip().split(',') for line in f if line.strip()]
    
    # Procesar solo los rangos especificados
    results = {}
    total_primes = 0
    
    for idx in range(start_idx, min(end_idx + 1, len(ranges))):
        if idx >= len(ranges):
            break
            
        start, end = int(ranges[idx][0]), int(ranges[idx][1])
        
        print(f"Procesando rango {idx}: [{start}, {end}]")
        start_time = time.time()
        
        primes = sieve_of_eratosthenes(start, end)
        
        elapsed = time.time() - start_time
        print(f"  Encontrados {len(primes)} primos en {elapsed:.2f} segundos")
        
        results[idx] = {
            'range': [start, end],
            'primes_count': len(primes),
            'primes': primes,
            'computation_time': elapsed
        }
        total_primes += len(primes)
    
    # Guardar resultados
    output_file = Path(output_dir) / f"results_{start_idx}_{end_idx}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"RESUMEN:")
    print(f"Rangos procesados: {start_idx} a {min(end_idx, len(ranges)-1)}")
    print(f"Total de primos encontrados: {total_primes}")
    print(f"Resultados guardados en: {output_file}")
    print(f"{'='*60}")


def main():
    if len(sys.argv) != 3:
        print("Uso: python calculate.py <start_index> <end_index>")
        print("Ejemplo: python calculate.py 0 9")
        sys.exit(1)
    
    start_idx = int(sys.argv[1])
    end_idx = int(sys.argv[2])
    
    # Cargar configuración
    config = load_config()
    input_dir = config['input_dir']
    output_dir = config['output_dir']
    
    # Buscar archivo de entrada
    input_files = list(Path(input_dir).glob('*.txt'))
    
    if not input_files:
        print(f"Error: No se encontraron archivos de entrada en {input_dir}/")
        sys.exit(1)
    
    input_file = input_files[0]
    print(f"Usando archivo de entrada: {input_file}")
    print(f"Procesando índices {start_idx} a {end_idx}\n")
    
    # Procesar
    process_input_range(input_file, start_idx, end_idx, output_dir)


if __name__ == "__main__":
    main()
