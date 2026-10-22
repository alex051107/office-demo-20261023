# The offline target reuses the existing pinned research image: no installation.
FROM excel-benchmark-runtime:20260912-arm64 AS offline
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY input_files/ /app/input_files/
RUN python3 -c "import openpyxl; print(openpyxl.__version__)" \
    && chmod -R a-w /app/input_files \
    && mkdir -p /app/output /logs/verifier

# Build this target only when preparing the later paid judge environment.
# It is deliberately separate from the zero-network offline acceptance.
FROM python:3.12-slim-bookworm AS judge
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends bash nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt \
    && npm install -g @anthropic-ai/claude-code@2.1.114
WORKDIR /app
COPY input_files/ /app/input_files/
RUN chmod -R a-w /app/input_files && mkdir -p /app/output /logs/verifier
