# Zammad Hacka

A web application for visualizing Zammad ticket data with Python backend, React frontend, and Grafana integration.

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
├── grafana/                # Grafana configuration
│   ├── provisioning/      # Grafana datasource and dashboard provisioning
│   └── dashboards/        # Grafana dashboard JSON files
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

- **React 18**: UI library (optional - can use Grafana instead)
- **TypeScript**: Type safety
- **Vite**: Build tool
- **React Query**: Data fetching and caching
- **Recharts**: Data visualization
- **Vitest**: Testing framework

### Visualization

- **Grafana**: Professional data visualization and monitoring (recommended)
- **React Frontend**: Custom UI solution (kept as backup option)

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
- Frontend app at `http://localhost:5173` (if using React frontend)
- Grafana at `http://localhost:3001` (if using Docker Compose)

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

### Grafana Setup

Grafana is included as the recommended visualization solution. The backend includes Grafana-compatible endpoints.

**Current Setup: On-Premises Grafana (Docker)**

The current configuration is set up for **on-premises Grafana** running in Docker. The backend API endpoints are generic and will also work with **Grafana Cloud** if you make your backend API publicly accessible.

**Using Docker Compose (On-Premises - Recommended):**

1. Start all services including Grafana:

```bash
docker-compose up --build
```

2. Access Grafana at `http://localhost:3001`

   - Default username: `admin`
   - Default password: `admin`
   - Change these in production!

3. The Zammad API datasource is automatically configured
4. Example dashboards are available in the Grafana UI

**Manual Grafana Setup:**

1. Install Grafana following [official documentation](https://grafana.com/docs/grafana/latest/setup-grafana/installation/)

2. Install the Simple JSON Datasource plugin:

   ```bash
   grafana-cli plugins install grafana-simple-json-datasource
   ```

   Then restart Grafana.

3. Add the backend as a data source:

   - Go to Configuration → Data Sources
   - Click "Add data source"
   - Select "Simple JSON"
   - Configure:
     - Name: "Zammad API"
     - URL: `http://localhost:8000/api/v1/grafana`
     - Access: Server (default)
   - Click "Save & Test"

4. Available Grafana endpoints:
   - `/api/v1/grafana/query` - Main query endpoint (supports multiple targets)
   - `/api/v1/grafana/search` - Returns available metrics
   - `/api/v1/grafana/annotations` - For dashboard annotations
   - `/api/v1/grafana/tickets/timeseries` - Time-series data for tickets
   - `/api/v1/grafana/tickets/by-state` - Tickets grouped by state
   - `/api/v1/grafana/tickets/by-priority` - Tickets grouped by priority

**Grafana vs React Frontend:**

- **Grafana (Recommended)**: Professional dashboards, better for monitoring, alerting, and time-series analysis
- **React Frontend**: Custom UI, more flexibility for specific use cases, kept as backup option

You can use either or both - they both connect to the same backend API.

**Using Grafana Cloud:**

If you prefer to use Grafana Cloud instead of on-premises:

1. Deploy your backend API to a publicly accessible URL (e.g., AWS, Azure, Heroku, etc.)
2. In Grafana Cloud, go to Configuration → Data Sources
3. Install the "Simple JSON Datasource" plugin (if not already available)
4. Add a new datasource:
   - Type: Simple JSON
   - Name: "Zammad API"
   - URL: `https://your-backend-api.com/api/v1/grafana` (your public backend URL)
   - Access: Server
5. The same endpoints will work - just use your public backend URL instead of `http://backend:8000`

**Note:** The backend API endpoints are designed to work with both on-premises Grafana and Grafana Cloud. The only difference is the URL you use when configuring the datasource.

**Local Development/Testing with Grafana:**

If you have Grafana on a Windows server but want to test your code locally, you can run a local Grafana instance:

**Option 1: Using Docker (Recommended for Local Testing)**

1. Start local Grafana and backend:

   ```bash
   # Windows
   start-grafana-local.bat

   # Linux/Mac
   chmod +x start-grafana-local.sh
   ./start-grafana-local.sh
   ```

   Or manually:

   ```bash
   docker-compose -f docker-compose.local.yml up -d
   ```

2. Access local Grafana at `http://localhost:3001`

   - Username: `admin`
   - Password: `admin`

3. The datasource is automatically configured to point to your local backend at `http://localhost:8000`

4. Test your code changes locally before deploying to the Windows server

5. Stop local services:
   ```bash
   docker-compose -f docker-compose.local.yml down
   ```

**Option 2: Manual Local Grafana Installation**

1. Install Grafana locally following [official documentation](https://grafana.com/docs/grafana/latest/setup-grafana/installation/)

2. Install Simple JSON Datasource plugin:

   ```bash
   grafana-cli plugins install grafana-simple-json-datasource
   ```

3. Start your local backend:

   ```bash
   cd backend
   venv\Scripts\activate  # Windows
   python run.py
   ```

4. In local Grafana, add datasource:
   - URL: `http://localhost:8000/api/v1/grafana`
   - This connects to your local backend for testing

**Development Workflow:**

1. **Local Development**: Use local Grafana (`docker-compose.local.yml`) to test your backend code changes
2. **Production/Windows Server**: Deploy tested code and connect Windows server Grafana to your deployed backend

This allows you to develop and test locally without affecting your production Grafana on the Windows server.

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
