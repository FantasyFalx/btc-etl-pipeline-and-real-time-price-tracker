# -----------------------------------------------------------------------------
# Dataflow flex template image — Pub/Sub to BigQuery streaming pipeline.
#
# Build from src/:
#   docker build -f btc_streaming_etl/dataflow/Dockerfile -t btc-dataflow-pipeline .
# -----------------------------------------------------------------------------

FROM gcr.io/dataflow-templates-base/python312-template-launcher-base

ARG TEMPLATE_DIR=/dataflow/template
WORKDIR ${TEMPLATE_DIR}

# Pipeline source and dependencies
COPY btc_streaming_etl/dataflow/ ./btc_streaming_etl/dataflow/

ENV PYTHONPATH=${TEMPLATE_DIR} \
    FLEX_TEMPLATE_PYTHON_PY_FILE=btc_streaming_etl/dataflow/pipeline.py \
    FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE=requirements.txt
