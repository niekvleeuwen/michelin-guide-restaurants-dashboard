FROM python:3.15-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=0 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project \
 && find /opt/venv -type d \( -name tests -o -name test -o -name __pycache__ \) -prune -exec rm -rf {} + \
 && find /opt/venv -name '*.pyc' -delete


FROM python:3.15-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN addgroup --system dashgroup && adduser --system --ingroup dashgroup dashuser

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=dashuser:dashgroup dashboard ./dashboard
RUN mkdir cache && chown dashuser:dashgroup cache

USER dashuser

EXPOSE 8050

CMD ["gunicorn", "--preload", "--bind", "0.0.0.0:8050", "--workers", "4", "--threads", "2", "dashboard.main:server"]
