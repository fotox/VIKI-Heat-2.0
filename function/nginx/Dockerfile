# Stage 1: Frontend bauen
FROM node:18-slim AS builder
WORKDIR /app

# Nur package.json & lockfile kopieren
COPY function/frontend/package.json function/frontend/package-lock.json ./
RUN npm ci

# Restliches Frontend kopieren & bauen
COPY function/frontend ./
RUN npm run build

# Stage 2: Nginx mit statischen Assets
FROM nginx:alpine
# Altes HTML-Verzeichnis leeren
RUN rm -rf /usr/share/nginx/html/*
# Assets aus dem Builder-Stage übernehmen
COPY --from=builder /app/dist /usr/share/nginx/html
# Deine Config in nginx.conf einbinden
COPY function/nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
