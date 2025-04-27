# function/frontend/Dockerfile

# 1. Abhängigkeiten installieren
FROM node:18-slim AS deps
WORKDIR /app
# Nur package.json & package-lock kopieren für deterministische install
COPY package.json package-lock.json ./
# CI-Install für exakte Reproduzierbarkeit
RUN npm ci

# 2. Quellcode kopieren und (Dev-)Server starten
FROM node:18-slim AS dev
WORKDIR /app
# node_modules aus deps übernehmen
COPY --from=deps /app/node_modules ./node_modules
# Restlichen Code kopieren (inkl. index.html, src/, components/ui/)
COPY . .
# Dev-Server starten
CMD ["npm", "run", "dev"]
