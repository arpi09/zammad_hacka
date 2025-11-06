#!/bin/bash
# Start local Grafana for development/testing

echo "Starting Local Grafana for Development..."
echo

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker first."
    exit 1
fi

# Start backend and Grafana
echo "Starting backend and local Grafana..."
docker-compose -f docker-compose.local.yml up -d backend grafana-local

echo
echo "Services started!"
echo
echo "Backend API: http://localhost:8000"
echo "Local Grafana: http://localhost:3001"
echo "  - Username: admin"
echo "  - Password: admin"
echo
echo "To view logs: docker-compose -f docker-compose.local.yml logs -f"
echo "To stop: docker-compose -f docker-compose.local.yml down"

