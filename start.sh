#!/bin/bash

# Tornar script seguro
set -e

echo "Construindo e rodando o container Docker..."

# Construir e iniciar os containers em modo detach
docker-compose up --build -d

echo "Aplicação rodando em http://localhost:5000"
echo "Para parar os containers: docker-compose down"
