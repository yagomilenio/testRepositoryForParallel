# INICIO RÁPIDO
## 1. Instalación
```bash
make install
```
## 2. Prueba Básica
```bash
make test
```
## 3. Ejecutar con índices específicos
```bash
make run START=0 END=4
```
## 4. Ejecución Paralela (ejemplo con 4 procesos)
### Opción A: Script automático
```bash
bash run_parallel.sh
```
### Opción B: Manual
```bash
make run START=0 END=4 &
make run START=5 END=9 &
make run START=10 END=14 &
make run START=15 END=19 &
wait
```
## 5. Ver resultados
```bash
ls -lh outputs/
cat outputs/results_0_2.json
```
## 6. Limpiar outputs
```bash
make clean
```
---
## Estructura de Archivos
- **config.json**: Configuración (carpetas inputs/outputs)
- **inputs/ranges.txt**: Rangos de números a procesar (cada línea = 1 trabajo)
- **outputs/**: Resultados parciales en formato JSON
- **Makefile**: Comandos de automatización
- **calculate.py**: Script principal de cálculo
## Personalizar Rangos
Edita `inputs/ranges.txt` para cambiar los rangos a procesar.
Cada línea representa un trabajo independiente que puede ejecutarse en paralelo.
Formato: `inicio,fin`
Ejemplo:
```
1,100000
100001,200000
200001,300000
```
Los índices (START y END) hacen referencia al número de línea (empezando en 0).