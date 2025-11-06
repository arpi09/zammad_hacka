# Zammad Hacka

A web application for visualizing Zammad ticket data with Python backend and React frontend.

## Quick Commands

```bash
# Install all dependencies
npm install                    # Root dependencies
npm run install:all           # Backend + Frontend dependencies

# Start application
npm start                     # Start both (requires venv activation)
# OR
start.bat                     # Windows - handles venv automatically
./start.sh                    # Linux/Mac - handles venv automatically

# Run tests
npm run test:all              # All tests
npm run test:backend          # Backend tests only
npm run test:frontend         # Frontend tests only
```

## Project Structure

```
zammad_hacka/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration and utilities
│   │   ├── domain/         # Domain models
│   │   ├── repositories/   # Data access layer
│   │   ├── services/       # Business logic layer
│   │   └── main.py         # Application entry point
│   ├── tests/
│   │   ├── unit/           # Unit tests
│   │   └── integration/   # Integration tests
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend Docker configuration
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service layer
│   │   ├── config/         # Configuration
│   │   └── test/           # Test setup
│   ├── package.json        # Node dependencies
│   └── Dockerfile          # Frontend Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── package.json            # Root package.json with start scripts
└── README.md               # This file
```

## Architecture Principles

This project follows **SOLID principles**:

- **Single Responsibility**: Each class/component has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Interfaces can be substituted with implementations
- **Interface Segregation**: Clients depend only on interfaces they use
- **Dependency Inversion**: Depend on abstractions, not concretions

## Technology Stack

### Backend

- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation
- **Pytest**: Testing framework
- **HTTPX**: Async HTTP client

### Frontend

- **React 18**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool
- **React Query**: Data fetching and caching
- **Recharts**: Data visualization
- **Vitest**: Testing framework

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+ and npm
- (Optional) Docker and Docker Compose

### Installation

1. **Install root-level dependencies** (for running both services):

```bash
npm install
```

2. **Install backend dependencies**:

```bash
npm run install:backend
```

Or manually:

```bash
cd backend
python -m venv venv
# Activate virtual environment:
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

3. **Install frontend dependencies**:

```bash
npm run install:frontend
```

Or manually:

```bash
cd frontend
npm install
```

4. **Configure environment variables**:

   **Backend** - Create `backend/.env`:

   ```bash
   cd backend
   # Windows: copy .env.example .env
   # Linux/Mac: cp .env.example .env
   ```

   Then edit `backend/.env` with your Zammad API credentials:

   ```
   ZAMMAD_API_URL=http://your-zammad-instance.com
   ZAMMAD_API_TOKEN=your_api_token_here
   BACKEND_HOST=0.0.0.0
   BACKEND_PORT=8000
   BACKEND_DEBUG=True
   CORS_ORIGINS=http://localhost:3000,http://localhost:5173
   ```

   **Frontend** - Create `frontend/.env`:

   ```bash
   cd frontend
   # Windows: copy .env.example .env
   # Linux/Mac: cp .env.example .env
   ```

   Then edit `frontend/.env`:

   ```
   VITE_API_BASE_URL=http://localhost:8000
   ```

### Start the Application

**Important:** Before starting, make sure the backend virtual environment is activated:

```bash
# Windows
cd backend
venv\Scripts\activate
cd ..

# Linux/Mac
cd backend
source venv/bin/activate
cd ..
```

**Start both backend and frontend with one command:**

Using npm (requires venv to be activated first):

```bash
npm start
```

Or use the platform-specific scripts:

- **Windows**: `start.bat` (double-click or run from command line)
- **Linux/Mac**: `./start.sh` (make executable first: `chmod +x start.sh`)

This will start:

- Backend API at `http://localhost:8000`
- Frontend app at `http://localhost:5173`

You can also start them separately:

```bash
npm run start:backend   # Backend only (venv must be activated)
npm run start:frontend   # Frontend only
```

## Detailed Setup Instructions

### Backend Setup (Manual)

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create and configure `.env` file (see Quick Start section above)

6. Run the backend:

```bash
python run.py
# Or: uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

### Frontend Setup (Manual)

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Create and configure `.env` file (see Quick Start section above)

4. Run the frontend:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Docker Setup

1. Create `.env` files for both backend and frontend (see above)

2. Run with Docker Compose:

```bash
docker-compose up --build
```

This will start both backend and frontend services.

## Testing

### Run All Tests

Run all tests (backend and frontend):

```bash
npm run test:all
```

### Backend Tests

Run all backend tests:

```bash
npm run test:backend
```

Or manually:

```bash
cd backend
pytest tests/unit -v          # Unit tests only
pytest tests/integration -v   # Integration tests only
pytest --cov=app --cov-report=html  # All tests with coverage
```

### Frontend Tests

Run all frontend tests:

```bash
npm run test:frontend
```

Or manually:

```bash
cd frontend
npm test                # Run tests
npm run test:ui         # Run tests with UI
npm run test:coverage   # Run tests with coverage
```

## API Endpoints

### Tickets

- `GET /api/v1/tickets` - Get all tickets
- `GET /api/v1/tickets/{id}` - Get ticket by ID

### Statistics

- `GET /api/v1/statistics/tickets` - Get ticket statistics

### Organizations

- `GET /api/v1/organizations` - Get all organizations

### Users

- `GET /api/v1/users` - Get all users

## Development Guidelines

### Code Style

**Backend:**

- Use `black` for code formatting: `black app/`
- Use `isort` for import sorting: `isort app/`
- Use `flake8` for linting: `flake8 app/`

**Frontend:**

- Use ESLint for linting: `npm run lint`
- Follow TypeScript strict mode

### Git Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Write tests for new features
4. Ensure all tests pass
5. Commit with descriptive messages
6. Push and create a pull request

### Adding New Features

1. **Backend**: Follow the layered architecture:

   - Add domain models in `app/domain/`
   - Add repository interfaces and implementations in `app/repositories/`
   - Add business logic in `app/services/`
   - Add API endpoints in `app/api/v1/endpoints/`

2. **Frontend**: Follow component structure:
   - Add services in `src/services/`
   - Add components in `src/components/`
   - Add pages in `src/pages/`

## Contributing

This is a collaborative project. When working on features:

1. Communicate with team members
2. Follow SOLID principles
3. Write tests for new code
4. Update documentation as needed
5. Keep commits atomic and descriptive

## License

[Add your license here]
