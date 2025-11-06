@echo off
REM Start script for Windows
echo Starting Zammad Hacka Application...
echo.

REM Check if virtual environment exists
if not exist "backend\venv" (
    echo Virtual environment not found. Please run installation first.
    echo Run: npm run install:backend
    pause
    exit /b 1
)

REM Activate virtual environment and start backend
echo Starting backend...
start "Backend" cmd /k "cd backend && venv\Scripts\activate && python run.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo Starting frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Both services are starting in separate windows.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
pause

