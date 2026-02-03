#!/bin/bash

# Script de ejemplo para ejecutar el cálculo en paralelo
# Divide el trabajo en 4 procesos paralelos

echo "==================================================="
echo "  Ejecución Paralela - Calculadora de Primos"
echo "==================================================="
echo ""
echo "Iniciando 4 procesos paralelos..."
echo ""

# Ejecutar 4 trabajos en paralelo
make run START_INDEX=0 END_INDEX=4 &
PID1=$!
echo "Proceso 1 iniciado (PID: $PID1) - Rangos 0-4"

make run START_INDEX=5 END_INDEX=9 &
PID2=$!
echo "Proceso 2 iniciado (PID: $PID2) - Rangos 5-9"

make run START_INDEX=10 END_INDEX=14 &
PID3=$!
echo "Proceso 3 iniciado (PID: $PID3) - Rangos 10-14"

make run START_INDEX=15 END_INDEX=19 &
PID4=$!
echo "Proceso 4 iniciado (PID: $PID4) - Rangos 15-19"

echo ""
echo "Esperando a que todos los procesos terminen..."

# Esperar a que todos terminen
wait $PID1
wait $PID2
wait $PID3
wait $PID4

echo ""
echo "==================================================="
echo "  ✓ Todos los procesos completados"
echo "==================================================="
echo ""
echo "Revisa la carpeta 'outputs/' para ver los resultados:"
ls -lh outputs/
