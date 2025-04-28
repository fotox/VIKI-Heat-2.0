# --- Stage 1: Build ---
FROM node:18-slim AS builder

WORKDIR /app

# Nur Manifest-Dateien kopieren für besseren Cache
COPY package.json package-lock.json ./

# DevDependencies & ProdDependencies installieren
RUN npm ci

# gesamten Quellcode kopieren
COPY . .

# Produktion-Build erzeugen
RUN npm run build


# --- Stage 2: Production Image ---
FROM nginx:alpine AS production

# standardmäßiges nginx-HTML-Verzeichnis leeren (optional)
RUN rm -rf /usr/share/nginx/html/*

# fertige Assets aus dem Builder kopieren
COPY --from=builder /app/dist /usr/share/nginx/html

# Wenn Du eine eigene Nginx-Config brauchst, kopiere sie hierhin:
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Port 80 exposed (optional, da Nginx standardmäßig 80 nutzt)
EXPOSE 80

# Nginx im Vordergrund starten
CMD ["nginx", "-g", "daemon off;"]
