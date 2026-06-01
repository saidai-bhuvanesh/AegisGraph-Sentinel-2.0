# ============================================================================
# Stage 1: Build dependencies
# ============================================================================
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================================================
# Stage 2: Final runtime image
# ============================================================================
FROM python:3.11-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH \
    ENV=prod

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python dependencies from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application source code
COPY src/ /app/src/

# Create a non-root system user and adjust permissions
RUN useradd -u 10001 -U -d /app -s /bin/false appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health/ || exit 1

CMD ["python", "-m", "uvicorn", "src.api.app_factory:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]
