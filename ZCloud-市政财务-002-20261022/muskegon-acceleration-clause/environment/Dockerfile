# Reuses the locally cached pinned SDK image; no downloads or installation.
FROM office-demo-sdk:0.1.7 AS offline
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY input_files/ /app/input_files/
RUN python3 -c "import openpyxl; print(openpyxl.__version__)" \
    && chmod -R a-w /app/input_files \
    && mkdir -p /app/output /logs/verifier


FROM offline AS judge
