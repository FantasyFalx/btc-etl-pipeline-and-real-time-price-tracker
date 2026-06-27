# Build from the src/ directory:
# GCS base for python dataflow flex templates.
FROM gcr.io/dataflow-templates-base/python312-template-launcher-base

ARG WORKDIR=/dataflow/template
WORKDIR ${WORKDIR}

# Pipeline files
COPY btc_streaming_etl/dataflow/requirements.txt ./requirements.txt
COPY btc_streaming_etl/dataflow/pipeline.py ./btc_streaming_etl/dataflow/pipeline.py
COPY btc_streaming_etl/dataflow/__init__.py ./btc_streaming_etl/dataflow/__init__.py
COPY btc_streaming_etl/dataflow/configs/configs.py ./btc_streaming_etl/dataflow/configs/configs.py
COPY btc_streaming_etl/dataflow/configs/__init__.py ./btc_streaming_etl/dataflow/configs/__init__.py

# Environment variables for the flex template
ENV PYTHONPATH=${WORKDIR}
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="btc_streaming_etl/dataflow/pipeline.py"
ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="requirements.txt"
