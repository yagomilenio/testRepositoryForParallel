#!/usr/bin/env python3
"""
Calculadora de números primos paralelizable.
Utiliza la Criba de Eratóstenes para encontrar primos en un rango.
Paralelizada con ProcessPoolExecutor para usar todos los cores disponibles.
"""
import json
import sys
import os
import time
import math
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed



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


def sieve_of_eratosthenes(start, end):
    """
    Implementación de la Criba de Eratóstenes para un rango específico.
    Args:
        start: número inicial del rango
        end: número final del rango
    Returns:
        lista de números primos en el rango
    """
    if end < 2:
        return []
    start = max(2, start)

    size = end - start + 1
    is_prime = [True] * size

    sqrt_end = int(math.sqrt(end)) + 1
    base_primes = simple_sieve(sqrt_end)

    for prime in base_primes:
        first_multiple = ((start + prime - 1) // prime) * prime
        if first_multiple == prime:
            first_multiple += prime
        for j in range(first_multiple, end + 1, prime):
            is_prime[j - start] = False

    primes = [start + i for i in range(size) if is_prime[i]]
    return primes


def _worker(args):
    """Función worker que ejecuta la criba en un sub-rango. Se ejecuta en un proceso separado."""
    start, end = args
    t0 = time.time()
    primes = sieve_of_eratosthenes(start, end)
    elapsed = time.time() - t0
    return start, end, primes, elapsed


def split_range(start, end, n_chunks):
    """Divide [start, end] en n_chunks sub-rangos aproximadamente iguales."""
    total = end - start + 1
    chunk_size = math.ceil(total / n_chunks)
    chunks = []
    s = start
    while s <= end:
        e = min(s + chunk_size - 1, end)
        chunks.append((s, e))
        s = e + 1
    return chunks


def process_input_range(start, end, output_dir):
    """
    Procesa el rango [start, end] distribuyendo el trabajo entre todos los CPUs disponibles.
    """
    n_workers = os.cpu_count() or 1
    chunks = split_range(start, end, n_workers)

    print(f"Usando {n_workers} workers para {len(chunks)} sub-rangos\n")

    all_primes = []
    total_start = time.time()

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = {executor.submit(_worker, chunk): chunk for chunk in chunks}
        for future in as_completed(futures):
            s, e, primes, elapsed = future.result()
            print(f"  [{s:,} - {e:,}] → {len(primes):,} primos en {elapsed:.2f}s")
            all_primes.extend(primes)

    total_elapsed = time.time() - total_start

    # Ordenar (as_completed no garantiza orden)
    all_primes.sort()

    results = {
        'range': [start, end],
        'primes_count': len(all_primes),
        'primes': all_primes,
        'computation_time': total_elapsed,
        'workers_used': n_workers,
    }

    output_file = Path(output_dir) / f"results_{start}_{end}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*60}")
    print(f"RESUMEN:")
    print(f"Rango procesado: {start:,} a {end:,}")
    print(f"Workers usados: {n_workers}")
    print(f"Total de primos encontrados: {len(all_primes):,}")
    print(f"Tiempo total: {total_elapsed:.2f}s")
    print(f"Resultados guardados en: {output_file}")
    print(f"{'='*60}")


def main():
    if len(sys.argv) != 3:
        print("Uso: python calculate.py <start> <end>")
        print("Ejemplo: python calculate.py 0 1000000")
        sys.exit(1)

    start = int(sys.argv[1])
    end = int(sys.argv[2])

    output_dir = "outputs"

    print(f"Procesando rango {start:,} a {end:,}\n")
    process_input_range(start, end, output_dir)


if __name__ == "__main__":
    main()
