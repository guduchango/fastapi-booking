#!/bin/bash

# Colores para la salida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Iniciando tests de performance...${NC}"

# Verificar que los servicios estén corriendo
if ! docker-compose ps | grep -q "reservation-api"; then
    echo -e "${YELLOW}Iniciando servicios...${NC}"
    docker-compose up -d
    sleep 10  # Esperar a que los servicios estén listos
fi

# Iniciar Locust en modo master
echo -e "${GREEN}Iniciando Locust...${NC}"
echo -e "${YELLOW}Abre http://localhost:8089 en tu navegador para ver los resultados${NC}"

# Iniciar Locust master y worker
docker-compose up -d locust locust-worker

# Mostrar logs de Locust
docker-compose logs -f locust

# Para detener los tests, presiona Ctrl+C
# Los servicios se pueden detener con: docker-compose down 