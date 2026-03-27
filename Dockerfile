FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
ARG VITE_API_BASE_URL=/api
ARG VITE_BUILD_BASE=/static/
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
ENV VITE_BUILD_BASE=${VITE_BUILD_BASE}
RUN npm run build

FROM python:3.12-slim AS backend
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SERVE_FRONTEND_FROM_DJANGO=true

WORKDIR /app/backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./
COPY --from=frontend-builder /app/frontend/dist /app/backend/frontend_dist
RUN chmod +x /app/backend/start.sh

EXPOSE 8000
CMD ["bash", "start.sh"]
