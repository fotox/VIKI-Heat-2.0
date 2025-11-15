# V.I.K.I - Heat - Frontend

A modern React + TypeScript frontend for visualizing and controlling home energy & heating data.
Built with **Vite**, **Tailwind CSS**, **Radix UI/shadcn**, and **Recharts**.
This part contains the **frontend** only — it consumes data from a separate backend service.

> Status: **Open Source** project with basic functionalities under development and ready for further
> development. Tests are **not yet implemented**.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started (Local Development)](#getting-started-local-development)
  - [Step 1: Clone Repository](#step-1-clone-repository)
  - [Step 2: Start Backend Services](#step-2-start-backend-services)
  - [Step 3: Install Frontend Dependencies](#step-3-install-frontend-dependencies)
  - [Step 4: Configure Backend Connection](#step-4-configure-backend-connection)
  - [Step 5: Start Development Server](#step-5-start-development-server)
- [Docker (Full Stack)](#docker-full-stack)
- [Configuration & Environment](#configuration--environment)
- [Available Scripts](#available-scripts)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Authentication UI** (login/register/profile) using cookie-based sessions and CSRF protection
- **Dashboard** with multiple modules:
  - Energy chart (consumption, production, pricing) using **Recharts**
  - Inverter charts (production, consumption, coverage, battery capacity)
  - Heating tank ring charts (buffer & heating tanks)
  - Phase switch panel for heat pipes & heating mode control
- **Settings** sections for energy, heating, location, manufacturer, photovoltaic, sensors, tanks, and weather
- **Responsive layout** with a collapsible sidebar and header navigation
- **UI primitives** built on **Radix UI** and **shadcn/ui** components
- **TypeScript-first** codebase with modular hooks and utilities

> All data is fetched from the backend via REST endpoints under `/api/*`.
> Real-time support (Socket.IO) is prepared in the configuration, but not used in the current code.

---

## Tech Stack

- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite 6
- **Styling**: Tailwind CSS, tailwind-merge, tailwindcss-animate
- **UI Library**: Radix UI + shadcn/ui (prebuilt components in `src/components/ui`)
- **Routing**: React Router v6
- **Charts**: Recharts
- **Icons**: lucide-react
- **HTTP**: built-in `fetch` with `credentials: "include"` for authenticated calls
- **Container**: Docker (multi-stage build) + Nginx for static serving & API proxy
- **Node/NPM**: Node 18

---

## Project Structure

```
function/frontend/
  src/
    App.tsx
    index.css
    main.tsx
    components/
      dashboard/
      layout/
      navigation/
      selectors/
      ui/
    hooks/
    routes/
      settings/
    utils/
  vite.config.ts
  nginx.conf
  Dockerfile
  package.json
  tailwind.config.js
  tsconfig.json
```

_Notable files:_
- `vite.config.ts` – Vite base config + dev proxy for `/api` and `/socket.io` to `http://viki-backend:5000`
- `nginx.conf` – Production Nginx config: serves SPA and proxies `/api` and `/socket.io` to the backend
- `Dockerfile` – Multi-stage build (Vite build → Nginx image)
- `src/components/ui/*` – shadcn/ui component set
- `src/routes/*` – pages (Dashboard, Analytics, Settings, Auth)

---

## Prerequisites

Before starting, ensure you have the following installed:

- **Node.js 18.x** ([Download](https://nodejs.org/))
- **npm** (comes with Node.js)
- **Docker & Docker Compose** ([Download](https://docs.docker.com/get-docker/)) - for backend services
- **Git** ([Download](https://git-scm.com/downloads))

---

## Getting Started (Local Development)

Follow these steps to run the frontend locally and connect it to the backend:

### Step 1: Clone Repository

```bash
git clone https://github.com/fotox/VIKI-Heat-2.0.git
cd VIKI-Heat-2.0
```

### Step 2: Start Backend Services

The frontend requires the backend API to be running. You have two options:

#### Option A: Start with Docker Compose (Recommended)

From the **root directory**, start the database and backend:

```bash
# Start database and backend
docker-compose up -d db backend
```

This starts:
- PostgreSQL database on `localhost:5432`
- Backend API on `localhost:5000`

Verify services are running:
```bash
docker ps
# Should show viki-db and viki-backend

# Test backend
curl http://localhost:5000/
# Expected: {"message": "VIKI Backend API läuft"}
```

#### Option B: Run Backend Locally

See the [Backend README](../backend/README.md) for instructions on running the backend locally with Python.

### Step 3: Install Frontend Dependencies

Navigate to the frontend directory and install dependencies:

```bash
cd function/frontend

# Install dependencies (uses package-lock.json for reproducible builds)
npm ci
```

**Note:** Use `npm ci` instead of `npm install` for consistent dependency versions.

### Step 4: Configure Backend Connection

The frontend needs to know where your backend is running. By default, it expects the backend at `http://viki-backend:5000`.

#### If Backend is Running via Docker Compose

**Option A: Add hosts entry (Recommended)**

Add the following line to your hosts file:

**Windows:** `C:\Windows\System32\drivers\etc\hosts`
**Linux/macOS:** `/etc/hosts`

```
127.0.0.1    viki-backend
```

**Windows PowerShell (as Administrator):**
```powershell
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "`n127.0.0.1    viki-backend"
```

**Linux/macOS:**
```bash
echo "127.0.0.1 viki-backend" | sudo tee -a /etc/hosts
```

#### If Backend is Running on Different Host/Port

Edit `vite.config.ts` and change the proxy target:

```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',  // Change this
        changeOrigin: true,
      },
      '/socket.io': {
        target: 'http://localhost:5000',  // Change this
        ws: true,
        changeOrigin: true,
      },
    },
  },
})
```

### Step 5: Start Development Server

Start the Vite development server:

```bash
npm run dev
```

The frontend will be available at: **http://localhost:5173**

You should see output like:
```
  VITE v6.3.3  ready in 523 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

Open your browser and navigate to http://localhost:5173

---

## Docker (Full Stack)

To run the complete application (database + backend + frontend) with Docker:

### Build Frontend Image

From the **frontend directory**:
```bash
cd function/frontend
docker build -t viki-heat_arm_frontend:latest .
```

### Start Full Stack

From the **root directory**:
```bash
docker-compose up -d
```

This starts:
- **Database** (viki-db) on port `5432`
- **Backend** (viki-backend) on port `5000`
- **Frontend** (viki-frontend) on port `80`

Access the application:
- **Frontend:** http://localhost
- **Backend API:** http://localhost:5000
- **Swagger Docs:** http://localhost:5000/docs

### Stop Services

```bash
docker-compose down
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f frontend
```

---

## Configuration & Environment

This frontend does **not** require `.env` variables by default.

### API Configuration

- **Development:** API requests are proxied through Vite dev server (configured in `vite.config.ts`)
  - `/api/*` → `http://viki-backend:5000`
  - `/socket.io` → `http://viki-backend:5000`

- **Production:** Nginx handles API proxying (configured in `nginx.conf`)
  - Serves static files from `/usr/share/nginx/html`
  - Proxies `/api/*` and `/socket.io` to backend

### Authentication

- Uses `credentials: "include"` for cookie-based authentication
- Expects `csrf_access_token` cookie from backend
- Adds `X-CSRF-TOKEN` header to authenticated requests

### Routing

- SPA routing with React Router
- Nginx fallback configuration: `try_files $uri /index.html;`
- All client-side routes are handled by React Router

---

## Available Scripts

### Development

```bash
# Start development server with hot reload
npm run dev

# Start on specific port
npm run dev -- --port 3000

# Expose to network
npm run dev -- --host
```

### Building

```bash
# Build production bundle
npm run build

# Output directory: ./dist
```

### Preview

```bash
# Preview production build locally
npm run preview

# Runs on http://localhost:4173
```

### Linting & Formatting

```bash
# Lint TypeScript files
npx tsc --noEmit

# Format with Prettier (if configured)
npx prettier --write "src/**/*.{ts,tsx,css}"
```

---

## Screenshots

Below are example views of the application:

- **Landing Page:**
  ![Landing Page](../../documentation/landing_page.jpg)

- **Login Page:**
  ![Login](../../documentation/login_page.jpg)

- **Settings:**
  ![Settings](../../documentation/settings-page.jpg)

- **Profile:**
  ![Profile](../../documentation/profile-page.jpg)

---

## Troubleshooting

### Problem: ERR_NAME_NOT_RESOLVED for viki-backend

**Cause:** The hostname `viki-backend` cannot be resolved by your system.

**Solution:**
1. Add hosts entry (see [Step 4](#step-4-configure-backend-connection))
2. OR change proxy target in `vite.config.ts` to `http://localhost:5000`

### Problem: Network Error / API calls fail

**Cause:** Backend is not running or not accessible.

**Solution:**
```bash
# Check if backend is running
curl http://localhost:5000/

# If using Docker:
docker ps | grep viki-backend
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

### Problem: Port 5173 already in use

**Cause:** Another Vite/dev server is running.

**Solution:**
```bash
# Use different port
npm run dev -- --port 3000

# Or kill the process using port 5173
# Windows:
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Linux/macOS:
lsof -ti:5173 | xargs kill -9
```

### Problem: White screen / blank page

**Cause:** Build issues or incorrect routing.

**Solution:**
```bash
# Clear Vite cache
rm -rf node_modules/.vite

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Restart dev server
npm run dev
```

### Problem: CORS errors

**Cause:** Backend CORS configuration.

**Solution:**
- Ensure backend has CORS enabled (it should be by default)
- Check `vite.config.ts` proxy configuration
- Verify `changeOrigin: true` is set in proxy config

### Problem: Authentication not working

**Cause:** Cookies not being sent/received.

**Solution:**
- Check that `credentials: "include"` is set in fetch calls
- Ensure backend and frontend are on same domain in production
- Check browser dev tools → Application → Cookies

### Problem: Module not found errors

**Cause:** Dependencies not installed correctly.

**Solution:**
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install

# Or use ci for reproducible builds
npm ci
```

---

## Contributing

Contributions are welcome! Suggested workflow:

1. Fork the repository & create a feature branch:
   ```bash
   git checkout -b feat/your-topic
   ```

2. Install dependencies & run the dev server:
   ```bash
   cd function/frontend
   npm ci
   npm run dev
   ```

3. Make your changes:
   - Keep components accessible (follow Radix UI patterns)
   - Use TypeScript for type safety
   - Follow existing code structure
   - Test thoroughly in development

4. Build to verify:
   ```bash
   npm run build
   npm run preview
   ```

5. Commit with clear messages and open a Pull Request

### Code Style Guidelines

- Use TypeScript for all new code
- Follow existing component patterns (shadcn/ui)
- Keep components small and focused
- Use Tailwind CSS for styling
- Ensure accessibility (ARIA labels, keyboard navigation)

---

## License

This project is licensed under the **MIT License**. See [LICENSE](../../LICENSE) for details.
