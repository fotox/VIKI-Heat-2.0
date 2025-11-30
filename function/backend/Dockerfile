# =============================================================================
# Multi-Stage Dockerfile für VIKI-Heat Backend
# Stages: base -> development -> test -> production
# =============================================================================

# -----------------------------------------------------------------------------
# Base Stage - Gemeinsame Dependencies
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS base

# Metadata
LABEL maintainer="carsten_stephan@mail.de"
LABEL version="2.0"
LABEL description="VIKI-Heat Backend Service"

# System Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Setze Arbeitsverzeichnis
WORKDIR /app

# Python Umgebungsvariablen
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Kopiere Requirements
COPY requirements.txt .

# Installiere Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------------------
# Development Stage
# -----------------------------------------------------------------------------
FROM base AS development

# Installiere Development Tools
RUN pip install --no-cache-dir \
    debugpy \
    ipython \
    flask-debugtoolbar

# Installiere GPIO Mock für Entwicklung
COPY services/heating/GpioMock.py /usr/local/lib/python3.11/site-packages/

# Erstelle notwendige Verzeichnisse
RUN mkdir -p /app/logs /app/database/resources

# Kopiere Application Code
COPY . .

# Setze Timezone
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Exponiere Port
EXPOSE 5000 5678

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Start Command
CMD ["python", "app.py"]

# -----------------------------------------------------------------------------
# Test Stage
# -----------------------------------------------------------------------------
FROM base AS test

# Installiere Test Dependencies
RUN pip install --no-cache-dir \
    pytest \
    pytest-cov \
    pytest-flask \
    pytest-mock \
    httpx \
    faker

# Kopiere Application Code
COPY . .

# Erstelle Test-Verzeichnisse
RUN mkdir -p /app/test-results /app/htmlcov

# Exponiere Port
EXPOSE 5000

# Run Tests
CMD ["pytest", "-v", "--cov=.", "--cov-report=html", "--cov-report=term"]

# -----------------------------------------------------------------------------
# Production Stage
# -----------------------------------------------------------------------------
FROM base AS production

# Installiere nur Production Dependencies
RUN pip install --no-cache-dir \
    gunicorn \
    gevent

# Erstelle non-root User
RUN groupadd -r viki && \
    useradd -r -g viki -u 1001 viki && \
    mkdir -p /app/logs /app/database/resources && \
    chown -R viki:viki /app

# Kopiere nur notwendige Files (keine Tests, keine Dev-Files)
COPY --chown=viki:viki . .

# Setze Timezone
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Wechsle zu non-root User
USER viki

# Exponiere Port
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Start mit Gunicorn
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "4", \
     "--threads", "2", \
     "--worker-class", "gevent", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "app:create_app()"]
