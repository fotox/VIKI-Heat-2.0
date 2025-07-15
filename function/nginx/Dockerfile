# Stage 1: Frontend bauen
FROM node:18-slim AS builder
WORKDIR /app

COPY function/frontend/package.json function/frontend/package-lock.json ./
RUN npm ci

COPY function/frontend ./
RUN npm run build

# Stage 2: Nginx mit statischen Assets
FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/dist /usr/share/nginx/html
COPY function/nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
