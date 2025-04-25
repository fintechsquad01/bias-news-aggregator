###########################
# 1. Build stage
###########################
FROM python:3.11-slim AS builder
WORKDIR /opt/build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY backend/requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

###########################
# 2. Runtime stage
###########################
FROM python:3.11-slim AS runtime
WORKDIR /app

# Create non-root user
RUN addgroup --system app && adduser --system --group app
USER app

# Copy installed deps from builder
COPY --from=builder /install /usr/local

# Copy source
COPY backend /app

EXPOSE 8000
ENTRYPOINT ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--access-logfile", "-"]
