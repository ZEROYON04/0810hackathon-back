# Lightweight multi-stage build for container optimization
# Stage 1: Build dependencies using uv
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY uv.lock pyproject.toml ./
RUN uv sync --locked --no-install-project --no-dev

COPY app /app
RUN uv sync --locked --no-dev

# Stage 2: Lightweight runtime using Alpine Linux (45MB vs 1GB base)
FROM python:3.13-alpine AS runtime

WORKDIR /

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy the application code
COPY app /app


# Set up environment to use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]