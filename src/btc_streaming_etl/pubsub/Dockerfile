FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
COPY btc_streaming_etl ./btc_streaming_etl

RUN uv sync --frozen --no-dev

ENV PYTHONPATH=/app

CMD ["uv", "run", "python", "-m", "btc_streaming_etl.pubsub.message_controller"]
