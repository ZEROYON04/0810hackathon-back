FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Installing separately from its dependencies allows optimal layer caching
COPY  /app /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /

ENTRYPOINT []


EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# 例: Gunicornと連携する場合 (本番環境推奨)
# CMD ["gunicorn", "main:app", "--workers", "4", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]