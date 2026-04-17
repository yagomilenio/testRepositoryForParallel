# Calculadora de Números Primos en Paralelo

Este repositorio contiene una calculadora de números primos computacionalmente intensiva, diseñada para ser fácilmente paralelizable. Utiliza el algoritmo de la Criba de Eratóstenes segmentada, lo que lo convierte en un benchmark ideal para pruebas de procesamiento paralelo y distribuido.

El script principal, `calculate.py`, encuentra todos los números primos dentro de un rango numérico dado. La arquitectura está diseñada para permitir que múltiples instancias de este script se ejecuten concurrentemente sobre rangos distintos, habilitando un paralelismo simple de grano grueso.

## Estructura del Proyecto

```
.
├── Makefile          # Tareas de automatización (run, test, clean)
├── calculate.py      # El script principal de cálculo de primos
├── config.toml       # Archivo de configuración de la tarea
├── QUICKSTART.md     # Guía de inicio rápido
└── outputs/          # Directorio para los archivos de resultados generados
    └── (archivos generados)
```

## Cómo Funciona

El script `calculate.py` implementa el algoritmo de la **Criba de Eratóstenes**. Está optimizado para trabajar sobre segmentos específicos (p. ej., del 1 al 1.000.000).

- **Paralelismo Intra-script**: Para una sola ejecución, el script utiliza `concurrent.futures.ProcessPoolExecutor` de Python para distribuir el cálculo de un rango dado entre todos los núcleos de CPU disponibles.
- **Paralelismo Inter-script**: El uso previsto es ejecutar múltiples instancias del script con distintos rangos de forma simultánea. Esto permite dividir la carga de trabajo entre diferentes máquinas o procesos.

## Configuración

El proyecto requiere Python 3. Para preparar el entorno, simplemente ejecuta:

```bash
make setup
```

Este comando verificará que Python 3 está instalado y creará el directorio `outputs` necesario. No se requieren paquetes externos.

## Uso

### Ejecución Simple

Para calcular los primos de un rango numérico específico, usa el comando `make run` indicando los valores `START` y `END`.

```bash
# Ejemplo: Calcular primos del 1 al 1.000.000
make run START=1 END=1000000
```

Los resultados se guardarán en `outputs/results_1_1000000.json`.

### Ejecución en Paralelo

La característica principal de este repositorio es su capacidad de paralelizarse ejecutando múltiples trabajos. Aquí hay algunas formas de lograrlo:

#### 1. Múltiples Terminales

Puedes dividir la carga manualmente ejecutando distintos comandos en ventanas de terminal separadas.

**Terminal 1:**
```bash
make run START=1 END=1000000
```

**Terminal 2:**
```bash
make run START=1000001 END=2000000
```

**Terminal 3:**
```bash
make run START=2000001 END=3000000
```

#### 2. Jobs en Segundo Plano con Bash

Usa comandos de shell para ejecutar múltiples procesos en segundo plano y esperar a que todos terminen.

```bash
make run START=1 END=1000000 &
make run START=1000001 END=2000000 &
make run START=2000001 END=3000000 &
make run START=3000001 END=4000000 &
wait
echo "All processes completed."
```

#### 3. GNU Parallel

Si tienes `GNU Parallel` instalado, puedes distribuir fácilmente el trabajo entre múltiples núcleos con un solo comando.

```bash
# Este comando ejecuta 4 trabajos en paralelo, cada uno procesando un rango de 1 millón de números.
# Procesa números del 0 al 4 millones.
seq 0 1000000 3000000 | parallel -j4 'make run START={} END=$(({}+999999))'
```

## Comandos del Makefile

- `make setup`: Prepara el entorno.
- `make run START=<num> END=<num>`: Ejecuta el cálculo de primos para el rango especificado.
- `make test`: Ejecuta un caso de prueba pequeño y rápido (calcula primos del 0 al 2).
- `make clean`: Elimina todos los archivos generados del directorio `outputs`.
- `make parallel-example`: Muestra ejemplos de cómo ejecutar el script en paralelo.
- `make help`: Muestra un mensaje de ayuda con todos los targets disponibles.

## Formato de Salida

El script genera un archivo JSON por cada ejecución en el directorio `outputs/`, con el nombre `results_<START>_<END>.json`. El archivo contiene el rango procesado, el total de primos encontrados y una lista con los propios primos.

Ejemplo `outputs/results_0_4.json`:
```json
{
  "range": [
    0,
    4
  ],
  "primes_count": 2,
  "primes": [
    2,
    3
  ]
}
```
