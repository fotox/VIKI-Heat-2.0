# V.I.K.I - Heat - Backend
Backend service for **V.I.K.I - Heat** — provides REST endpoints for authentication, dashboard modules, and settings.
Built with **Flask**, served via **Flask-SocketIO**, documented with **Swagger (Flasgger)**, and uses **PostgreSQL** via SQLAlchemy.

> Status: **Open Source** project with basic functionalities under development and ready for further development.
> Tests are **not yet implemented**. API docs exist but some endpoints still require **docstring/Swagger** completion.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started (Local Development)](#getting-started-local-development)
  - [Step 1: Clone Repository](#step-1-clone-repository)
  - [Step 2: Start Database with Docker Compose](#step-2-start-database-with-docker-compose)
  - [Step 3: Setup Virtual Environment](#step-3-setup-virtual-environment)
  - [Step 4: Install Dependencies](#step-4-install-dependencies)
  - [Step 5: Configure Environment](#step-5-configure-environment)
  - [Step 6: Start the Backend](#step-6-start-the-backend)
- [Using the Makefile](#using-the-makefile)
- [Docker (Full Stack)](#docker-full-stack)
- [API Overview](#api-overview)
- [Swagger / API Docs](#swagger--api-docs)
- [Database Seeding](#database-seeding)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- JWT cookie-based authentication (login, profile, register, password reset)
- Dashboard and module endpoints for energy data, prices, heat pipes, heating modes, inverter, and tank temperatures
- Settings endpoints for energy, heating, location, manufacturer, photovoltaic, sensors, tanks, and weather
- Background scheduler (APScheduler) for periodic data pulls/control jobs
- Socket.IO server initialized for realtime (used by frontend proxy configuration)
- Structured logging service and data formatting utilities

---

## Tech Stack

- Python 3.11
- Flask 3 + Blueprints
- Flask-JWT-Extended (cookie-based JWT)
- Flask-SQLAlchemy + SQLAlchemy (PostgreSQL)
- Flask-CORS
- Flasgger (Swagger/OpenAPI UI at /docs)
- Flask-SocketIO
- APScheduler
- Requests, Pandas (data processing)
- Docker (python:3.11-slim)

---

## Project Structure

```
function/backend/
  .env
  app.py
  config.py
  extensions.py
  memory.json
  requirements.txt
  swagger_config.yml
  api/
    auth/
    dashboard/
    settings/
  database/
    init_db.py
    resources/
      manufacturer.csv
      category.csv
  logs/
  services/
    energy/
    heating/
    temperature/
  utils/
```

_Notable files:_
- `app.py` – Application factory, CORS, Swagger init, blueprints, Socket.IO run at `0.0.0.0:5000`
- `config.py` – Loads `.env`, JWT/secret keys, `DATABASE_URL`, cookie/JWT config
- `extensions.py` – SQLAlchemy, JWTManager, SocketIO instances
- `api/*` – Auth, Dashboard, Modules, Settings blueprints
- `database/*` – Models and seed scripts
- `services/*` – Energy/heating/temperature services, control integrations
- `swagger_config.yml` – Flasgger base configuration

---

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.11** ([Download](https://www.python.org/downloads/))
- **Docker & Docker Compose** ([Download](https://docs.docker.com/get-docker/))
- **Git** ([Download](https://git-scm.com/downloads))

---

## Getting Started (Local Development)

Follow these steps to run the backend locally on your machine:

### Step 1: Clone Repository

```bash
git clone https://github.com/fotox/VIKI-Heat-2.0.git
cd VIKI-Heat-2.0
```

### Step 2: Start Database with Docker Compose

The backend requires a PostgreSQL database. Start it using Docker Compose from the **root directory**:

```bash
# From the root directory of the project
docker-compose up -d db
```

This will:
- Start PostgreSQL on port `5432`
- Create a database named `viki`
- Username: `viki`
- Password: `viki-secret`

Verify the database is running:
```bash
docker ps | grep viki-db
```

### Step 3: Setup Virtual Environment

Navigate to the backend directory and create a virtual environment:

```bash
cd function/backend
```

**Option A: Using Makefile (Windows)**

If you're on Windows and have the Makefile setup:
```bash
# From root directory
make init_venv
```

**Option B: Manual Setup (All Platforms)**

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies

With the virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment

Create a `.env` file in the `function/backend/` directory:

```bash
# Copy from example or create new
touch .env
```

Add the following configuration to `.env`:

```env
SECRET_KEY=dev-secret
JWT_SECRET_KEY=super-secret
MASTER_RESET_KEY=viki-masterkey
DATABASE_URL=postgresql://viki:viki-secret@localhost:5432/viki
```

**Important Notes:**
- When running **locally** (not in Docker), use `localhost` as the database host
- When running **inside Docker**, the hostname is `db` (as configured in docker-compose.yml)

### Step 6: Start the Backend

Start the Flask application:

```bash
python app.py
```

The backend should now be running at: **http://localhost:5000**

You should see output similar to:
```
 * Running on http://0.0.0.0:5000
```

Test the API:
```bash
curl http://localhost:5000/
# Expected response: {"message": "VIKI Backend API läuft"}
```

---

## Using the Makefile

The root directory contains a `Makefile` with helpful commands for Windows development:

### Available Commands

```bash
# Initialize complete environment (venv + pre-commit)
make init

# Create only virtual environment
make init_venv

# Install/update dependencies
make update

# Run tests
make test

# Run tests with coverage
make test-cov

# Clean virtual environment
make clean

# Reinitialize everything
make re-init
```

### Example Workflow

```bash
# 1. Initialize project
make init

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Navigate to backend
cd function/backend

# 4. Start database
docker-compose up -d db

# 5. Run backend
python app.py
```

---

## Docker (Full Stack)

To run the entire stack (database + backend + frontend) with Docker:

### Build Backend Image

From the **backend directory**:
```bash
cd function/backend
docker build -t viki-heat_arm_backend:latest .
```

### Start Full Stack

From the **root directory**:
```bash
docker-compose up -d
```

This will start:
- **Database** (viki-db) on port `5432`
- **Backend** (viki-backend) on port `5000`
- **Frontend** (viki-frontend) on port `80`

Access the application:
- Frontend: http://localhost
- Backend API: http://localhost:5000
- Swagger Docs: http://localhost:5000/docs

### Stop Services

```bash
docker-compose down
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

---

## API Overview

- **Auth** (`/api/auth`):
  - `/login` (POST)
  - `/register` (POST)
  - `/profile` (GET/PUT)
  - `/profile/photo` (GET)
  - `/reset-password` (POST)

- **Dashboard** (`/api/dashboard`):
  - `/modules` (GET/POST/DELETE)
  - `/modules/reorder` (POST)

- **Modules** (`/api/modules`):
  - `/energy_data` (GET)
  - `/energy_price` (GET)
  - `/heat_pipes` (GET)
  - `/heat_pipe/<id>` (GET/PUT)
  - `/heating_mode` (GET/PUT)
  - `/inverter_data` (GET)
  - `/heating_tank_temp` (GET)
  - `/buffer_tank_temp` (GET)

- **Settings** (`/api/settings`):
  - `/category`, `/energy`, `/heating`, `/location`, `/manufacturer`
  - `/photovoltaic`, `/sensors`, `/tanks`, `/weather`

---

## Swagger / API Docs

Interactive API documentation is available via **Swagger UI**:

**URL:** http://localhost:5000/docs

The Swagger interface allows you to:
- View all available endpoints
- Test API calls directly from the browser
- See request/response schemas
- Understand authentication requirements

> Some endpoint docstrings are still being completed.

---

## Database Seeding

The application automatically seeds the database on startup with:

1. **User Roles** (Admin, User, etc.)
2. **Default Users**
3. **Categories**
4. **Manufacturers** (from `database/resources/manufacturer.csv`)
5. **Location data**

The seeding happens in `app.py` via `create_app()`:
```python
with app.app_context():
    db.create_all()
    seed_roles()
    seed_users()
    seed_category()
    seed_manufacturers()
    seed_location()
```

**To expand manufacturer data:**
1. Edit `database/resources/manufacturer.csv`
2. Restart the application
3. The new data will be imported automatically

---

## Troubleshooting

### Problem: "could not translate host name 'viki-data' to address"

**Cause:** The app is trying to connect to a Docker hostname, but you're running locally.

**Solution:** Check your `.env` file and ensure it uses `localhost`:
```env
DATABASE_URL=postgresql://viki:viki-secret@localhost:5432/viki
```

### Problem: Database connection refused

**Cause:** PostgreSQL is not running.

**Solution:**
```bash
# Start database
docker-compose up -d db

# Check if it's running
docker ps | grep viki-db

# Check logs
docker-compose logs db
```

### Problem: Port 5432 already in use

**Cause:** Another PostgreSQL instance is running.

**Solution:**
```bash
# Stop local PostgreSQL
# Windows: Services → PostgreSQL → Stop
# Linux: sudo systemctl stop postgresql

# Or change port in docker-compose.yml:
ports:
  - "5433:5432"  # Use different host port

# Then update .env:
DATABASE_URL=postgresql://viki:viki-secret@localhost:5433/viki
```

### Problem: ModuleNotFoundError

**Cause:** Dependencies not installed or wrong virtual environment.

**Solution:**
```bash
# Ensure virtual environment is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: Permission denied on GPIO devices

**Cause:** Running without proper permissions for hardware access.

**Solution:** This is expected when running locally without Raspberry Pi hardware. The GPIO functionality is only needed in production.

---

## Contributing

Contributions are welcome! Suggested workflow:

1. Fork & create a feature branch:
   ```bash
   git checkout -b feat/your-topic
   ```

2. Setup environment & run locally:
   ```bash
   # Initialize with Makefile
   make init

   # Or manually
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt

   # Start database
   docker-compose up -d db

   # Run backend
   cd function/backend
   python app.py
   ```

3. Make your changes and test thoroughly

4. Open a Pull Request and document changes (especially API docs/Swagger and DB migrations if any)

_Tests_: There are **no tests yet**. PRs adding unit/integration tests are very welcome.

---

## License

This project is licensed under the **MIT License**.
See [LICENSE](../../LICENSE) for details.
