# -----------------------------------------------------------------------------
# Pub/Sub messenger image — streams BTC prices from YFinance to GCP Pub/Sub.
#
# Build from src/:
#   docker build -f btc_streaming_etl/pubsub/Dockerfile -t btc-pubsub-messenger .
# -----------------------------------------------------------------------------

FROM python:3.12-slim

ARG APP_DIR=/app
WORKDIR ${APP_DIR}

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install dependencies (cached when only application code changes)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application source
COPY btc_streaming_etl ./btc_streaming_etl

ENV PYTHONPATH=${APP_DIR}

CMD ["uv", "run", "python", "-m", "btc_streaming_etl.pubsub.message_controller"]
