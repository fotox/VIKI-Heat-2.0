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
- [API Overview](#api-overview)
- [Configuration](#configuration)
- [Getting Started (Local Development)](#getting-started-local-development)
- [Docker](#docker)
- [Swagger / API Docs](#swagger--api-docs)
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
src/
  .env
  app.py
  config.py
  extensions.py
  memory.json
  requirements.txt
  swagger_config.yml
  api/
    api/
      auth/
      dashboard/
      settings/
  database/
    resources/
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

## API Overview

- **Auth** (`/api/auth`):
  - `/login` (POST),
  - `/register` (POST),
  - `/profile` (GET/PUT),
  - `/profile/photo` (GET),
  - `/reset-password` (POST)
- **Dashboard** (`/api/dashboard`):
  - `/modules` (GET/POST/DELETE),
  - `/modules/reorder` (POST)
- **Modules** (`/api/dashboard`):
  - `/energy_data` (GET),
  - `/energy_price` (GET),
  - `/heat_pipes` (GET),
  - `/heat_pipe/<id>` (GET/PUT),
  - `/heating_mode` (GET/PUT),
  - `/inverter_data` (GET),
  - `/heating_tank_temp` (GET),
  - `/buffer_tank_temp` (GET)
- **Settings** (`/api/settings`):
  - category,
  - energy,
  - heating,
  - location,
  - manufacturer,
  - photovoltaic,
  - sensors,
  - tanks,
  - weather

> Full, interactive documentation is available via **Swagger UI** (see below). Some endpoint docs are still being completed.

---

## Configuration

Create a `.env` file (or use the provided example) in the project root:

```env
SECRET_KEY=dev-secret
JWT_SECRET_KEY=super-secret
MASTER_RESET_KEY=viki-masterkey
DATABASE_URL=postgresql://viki:viki-secret@viki-data:5432/viki
```

- `DATABASE_URL` points to a **PostgreSQL** instance. Postgres itself is documented in the main [README.md](../../README.md).
- JWTs are stored in **cookies** (`JWT_TOKEN_LOCATION = ["cookies"]`), CSRF protection is currently **disabled** for JWT cookies.
- CORS is enabled (see `app.py` for policy).
- Default port: **5000**.

---

## Getting Started (Local Development)

### Prerequisites
- Python **3.11**
- PostgreSQL (connection available via `DATABASE_URL`)
- Virtual environment tool (`venv`)

### 1) Create & activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2) Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Configure environment
Create `.env` as shown above and ensure your Postgres is reachable.

### 4) Initialize database (optional seeds)
The directory `database\resources` contains CSV files that import the manufacturer data and categories initially. If
the manufacturer database is expanded, please remember to also expand the CSV file `manufacturer.csv` with this data
in order to continuously expand the cross-manufacturer functionality.

Users and their roles are initially loaded at startup by calling the file `database\init_db.py`.

### 5) Run the server
```bash
python app.py
# or explicitly with Socket.IO and no reloader:
# python -c "import app as a; a.socketio.run(a.create_app(), host='0.0.0.0', port=5000, debug=True, use_reloader=False)"
```
Server starts on **http://localhost:5000**.

---

## Docker

### Build the image
```bash
docker build -t viki-heat-backend:latest .
```

### Run with Docker only (Postgres external)
Assuming your Postgres is reachable (see `DATABASE_URL`), start the API:
```bash
docker run -d --name viki-heat-backend -p 5000:5000 \
  --env-file .env \
  viki-heat-backend:latest
```

### Run in a Docker network (with the frontend)
```bash
docker network create viki-net || true

# Start Postgres separately, or use your existing DB container (name: viki-data)
# docker run -d --name viki-data --network viki-net -e POSTGRES_DB=viki -e POSTGRES_USER=viki -e POSTGRES_PASSWORD=viki-secret postgres:16

# Start backend on the same network
docker run -d --name viki-heat-backend --network viki-net -p 5000:5000 \
  --env-file .env \
  viki-heat-backend:latest
```

When running together with the frontend, the frontend proxies `/api` to `http://viki-backend:5000`.
Make sure the backend container is named **`viki-heat-backend`** or create an alias **`viki-backend`** on the network:
```bash
docker network connect viki-net viki-heat-backend --alias viki-backend
```

---

## Swagger / API Docs

- **Swagger UI** (Flasgger) is available at: `http://localhost:5000/docs`
- Base config: `swagger_config.yml`

Example UI (will be added to repo at `../../documentation/swagger_ui.jpg`):

- ![](../../documentation/swagger_ui.jpg)

> Endpoint docstrings are partially present and will be completed over time.

---

## Contributing

Contributions are welcome! Suggested workflow:

1. Fork & create a feature branch:
   ```bash
   git checkout -b feat/your-topic
   ```
2. Setup environment & run locally:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```
3. Open a Pull Request and document changes (especially API docs/Swagger and DB migrations if any).

_Tests_: There are **no tests yet**. PRs adding unit/integration tests are very welcome.

---

## License

This project is licensed under the **MIT License** (same as the frontend).
See [LICENSE](../../LICENSE) for details.
