.PHONY: setup run clean help
# Variables
PYTHON := python3
SCRIPT := calculate.py
START ?= 0
END ?= 0
help:
	@echo "==================================================="
	@echo "  Calculadora de Números Primos - Paralelizable"
	@echo "==================================================="
	@echo ""
	@echo "Targets disponibles:"
	@echo "  make setup              - Instala dependencias necesarias"
	@echo "  make run START=N END=M - Ejecuta el cálculo para rangos N a M"
	@echo "  make clean                - Limpia los archivos de salida"
	@echo "  make test                 - Ejecuta una prueba rápida"
	@echo "  make parallel-example     - Ejemplo de ejecución paralela"
	@echo ""
	@echo "Ejemplos:"
	@echo "  make run START=0 END=4"
	@echo "  make run START=5 END=9"
	@echo ""
setup:
	@echo "Instalando dependencias..."
	@which $(PYTHON) > /dev/null || (echo "Error: Python 3 no está instalado" && exit 1)
	@echo "✓ Python 3 está instalado"
	@echo "✓ No se requieren paquetes adicionales para este proyecto"
	@echo "✓ Verificando estructura de directorios..."
	@mkdir -p inputs outputs
	@test -f config.toml || (echo "Error: config.toml no encontrado" && exit 1)
	@echo "✓ Configuración verificada"
	@echo ""
	@echo "Instalación completada exitosamente!"
	@echo "Usa 'make run START=0 END=4' para ejecutar el programa"
run:
	@if [ -z "$(START)" ] || [ -z "$(END)" ]; then \
        echo "Error: Debes especificar START y END"; \
        echo "Ejemplo: make run START=0 END=4"; \
        exit 1; \
    fi
	@echo "Ejecutando cálculo de primos..."
	@echo "Rango de índices: $(START) a $(END)"
	@$(PYTHON) $(SCRIPT) $(START) $(END)
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
	@echo "Terminal 1: make run START=0 END=4"
	@echo "Terminal 2: make run START=5 END=9"
	@echo "Terminal 3: make run START=10 END=14"
	@echo "Terminal 4: make run START=15 END=19"
	@echo ""
	@echo "O usando GNU Parallel (si está instalado):"
	@echo "  seq 0 4 19 | parallel -j4 'make run START={} END=$$(({}+4))'"
	@echo ""
	@echo "O usando background jobs:"
	@echo "  make run START=0 END=4 &"
	@echo "  make run START=5 END=9 &"
	@echo "  make run START=10 END=14 &"
	@echo "  make run START=15 END=19 &"
	@echo "  wait"
	@echo ""
