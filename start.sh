#!/bin/bash
# Start script for Linux/Mac

echo "Starting Zammad Hacka Application..."
echo

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "Virtual environment not found. Please run installation first."
    echo "Run: npm run install:backend"
    exit 1
fi

# Start backend in background
echo "Starting backend..."
cd backend
source venv/bin/activate
python run.py &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 3

# Start frontend in background
echo "Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo
echo "Both services are starting..."
echo "Backend: http://localhost:8000 (PID: $BACKEND_PID)"
echo "Frontend: http://localhost:5173 (PID: $FRONTEND_PID)"
echo
echo "Press Ctrl+C to stop both services"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait

