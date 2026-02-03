# Calculadora de Números Primos - Paralelizable

Este proyecto implementa un algoritmo de cálculo pesado (Criba de Eratóstenes) diseñado para ser paralelizado. Es ideal para pruebas de paralelización y procesamiento distribuido.

## Estructura del Proyecto

```
prime-calculator/
├── config.json          # Configuración del proyecto
├── Makefile            # Automatización de tareas
├── calculate.py        # Script principal de cálculo
├── README.md           # Esta documentación
├── inputs/             # Archivos de entrada
│   └── ranges.txt      # Rangos de números para procesar
└── outputs/            # Resultados parciales (generados automáticamente)
    └── results_*.json  # Archivos de resultados por rango
```

## Configuración (config.json)

```json
{
  "input_dir": "inputs",       # Directorio de archivos de entrada
  "output_dir": "outputs",     # Directorio de salida
  "algorithm": "prime_sieve",  # Algoritmo utilizado
  "chunk_size": 1000000        # Tamaño de chunk por defecto
}
```

## Instalación

```bash
make install
```

Este comando:
- Verifica que Python 3 esté instalado
- Verifica la estructura de directorios
- Valida la configuración

## Uso

### Ejecución Básica

```bash
make run START_INDEX=0 END_INDEX=4
```

Esto procesará los rangos de la línea 0 a la 4 del archivo `inputs/ranges.txt`.

### Paralelización

#### Opción 1: Múltiples terminales

Terminal 1:
```bash
make run START_INDEX=0 END_INDEX=4
```

Terminal 2:
```bash
make run START_INDEX=5 END_INDEX=9
```

Terminal 3:
```bash
make run START_INDEX=10 END_INDEX=14
```

#### Opción 2: Background jobs en bash

```bash
make run START_INDEX=0 END_INDEX=4 &
make run START_INDEX=5 END_INDEX=9 &
make run START_INDEX=10 END_INDEX=14 &
make run START_INDEX=15 END_INDEX=19 &
wait
```

#### Opción 3: GNU Parallel (si está instalado)

```bash
seq 0 4 19 | parallel -j4 'make run START_INDEX={} END_INDEX=$$(({}+4))'
```

## Formato de Entrada

El archivo `inputs/ranges.txt` contiene rangos en formato CSV:

```
inicio,fin
1,100000
100001,200000
200001,300000
...
```

Cada línea representa un rango de números donde buscar primos.

## Formato de Salida

Los resultados se guardan en `outputs/results_<START>_<END>.json`:

```json
{
  "0": {
    "range": [1, 100000],
    "primes_count": 9592,
    "primes": [2, 3, 5, 7, 11, ...],
    "computation_time": 0.45
  },
  "1": {
    "range": [100001, 200000],
    "primes_count": 8392,
    "primes": [100003, 100019, ...],
    "computation_time": 0.52
  }
}
```

## Algoritmo

El proyecto utiliza la **Criba de Eratóstenes por segmentos**, que es:
- **Computacionalmente pesado**: Requiere cálculo intensivo para rangos grandes
- **Fácilmente paralelizable**: Cada rango es independiente
- **Eficiente**: O(n log log n) por segmento

## Comandos Adicionales

```bash
make help              # Muestra ayuda
make test              # Ejecuta una prueba rápida
make clean             # Limpia archivos de salida
make parallel-example  # Muestra ejemplos de paralelización
```

## Rendimiento

En un sistema moderno, cada rango de 100,000 números tarda aproximadamente:
- 0.1 - 0.5 segundos para rangos pequeños (< 1M)
- 0.5 - 2 segundos para rangos medios (1M - 10M)
- 2+ segundos para rangos grandes (> 10M)

La paralelización puede reducir el tiempo total significativamente según el número de núcleos disponibles.

## Personalización

Para cambiar los rangos a procesar, edita `inputs/ranges.txt`:

```bash
# Ejemplo: rangos más grandes para más carga
10000000,11000000
11000000,12000000
12000000,13000000
```

## Ejemplos de Uso

### Prueba rápida
```bash
make test
```

### Procesar todo en serie
```bash
make run START_INDEX=0 END_INDEX=19
```

### Dividir en 4 partes paralelas
```bash
make run START_INDEX=0 END_INDEX=4 &
make run START_INDEX=5 END_INDEX=9 &
make run START_INDEX=10 END_INDEX=14 &
make run START_INDEX=15 END_INDEX=19 &
wait
echo "Todos los procesos completados"
```

## Licencia

MIT
