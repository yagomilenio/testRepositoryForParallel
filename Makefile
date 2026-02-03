.PHONY: install run clean help

# Variables
PYTHON := python3
SCRIPT := calculate.py
START_INDEX ?= 0
END_INDEX ?= 0

help:
	@echo "==================================================="
	@echo "  Calculadora de Números Primos - Paralelizable"
	@echo "==================================================="
	@echo ""
	@echo "Targets disponibles:"
	@echo "  make install              - Instala dependencias necesarias"
	@echo "  make run START_INDEX=N END_INDEX=M - Ejecuta el cálculo para rangos N a M"
	@echo "  make clean                - Limpia los archivos de salida"
	@echo "  make test                 - Ejecuta una prueba rápida"
	@echo "  make parallel-example     - Ejemplo de ejecución paralela"
	@echo ""
	@echo "Ejemplos:"
	@echo "  make run START_INDEX=0 END_INDEX=4"
	@echo "  make run START_INDEX=5 END_INDEX=9"
	@echo ""

install:
	@echo "Instalando dependencias..."
	@which $(PYTHON) > /dev/null || (echo "Error: Python 3 no está instalado" && exit 1)
	@echo "✓ Python 3 está instalado"
	@echo "✓ No se requieren paquetes adicionales para este proyecto"
	@echo "✓ Verificando estructura de directorios..."
	@mkdir -p inputs outputs
	@test -f config.json || (echo "Error: config.json no encontrado" && exit 1)
	@echo "✓ Configuración verificada"
	@echo ""
	@echo "Instalación completada exitosamente!"
	@echo "Usa 'make run START_INDEX=0 END_INDEX=4' para ejecutar el programa"

run:
	@if [ -z "$(START_INDEX)" ] || [ -z "$(END_INDEX)" ]; then \
		echo "Error: Debes especificar START_INDEX y END_INDEX"; \
		echo "Ejemplo: make run START_INDEX=0 END_INDEX=4"; \
		exit 1; \
	fi
	@echo "Ejecutando cálculo de primos..."
	@echo "Rango de índices: $(START_INDEX) a $(END_INDEX)"
	@$(PYTHON) $(SCRIPT) $(START_INDEX) $(END_INDEX)

clean:
	@echo "Limpiando archivos de salida..."
	@rm -f outputs/*.json
	@echo "✓ Archivos de salida eliminados"

test:
	@echo "Ejecutando prueba rápida (índices 0-2)..."
	@$(PYTHON) $(SCRIPT) 0 2
	@echo ""
	@echo "✓ Prueba completada. Revisa outputs/ para ver los resultados"

parallel-example:
	@echo "==================================================="
	@echo "  Ejemplo de Ejecución Paralela"
	@echo "==================================================="
	@echo ""
	@echo "Para ejecutar en paralelo, abre múltiples terminales y ejecuta:"
	@echo ""
	@echo "Terminal 1: make run START_INDEX=0 END_INDEX=4"
	@echo "Terminal 2: make run START_INDEX=5 END_INDEX=9"
	@echo "Terminal 3: make run START_INDEX=10 END_INDEX=14"
	@echo "Terminal 4: make run START_INDEX=15 END_INDEX=19"
	@echo ""
	@echo "O usando GNU Parallel (si está instalado):"
	@echo "  seq 0 4 19 | parallel -j4 'make run START_INDEX={} END_INDEX=$$(({}+4))'"
	@echo ""
	@echo "O usando background jobs:"
	@echo "  make run START_INDEX=0 END_INDEX=4 &"
	@echo "  make run START_INDEX=5 END_INDEX=9 &"
	@echo "  make run START_INDEX=10 END_INDEX=14 &"
	@echo "  make run START_INDEX=15 END_INDEX=19 &"
	@echo "  wait"
	@echo ""
