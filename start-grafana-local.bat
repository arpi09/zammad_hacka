@echo off
REM Start local Grafana for development/testing
echo Starting Local Grafana for Development...
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Start backend and Grafana
echo Starting backend and local Grafana...
docker-compose -f docker-compose.local.yml up -d backend grafana-local

echo.
echo Services started!
echo.
echo Backend API: http://localhost:8000
echo Local Grafana: http://localhost:3001
echo   - Username: admin
echo   - Password: admin
echo.
echo To view logs: docker-compose -f docker-compose.local.yml logs -f
echo To stop: docker-compose -f docker-compose.local.yml down
echo.
pause

