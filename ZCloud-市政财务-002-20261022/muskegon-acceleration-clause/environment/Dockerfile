# Self-contained image for solving and verification; every layer comes from public package sources.
FROM python:3.12-slim-bookworm
ARG DEBIAN_MIRROR=http://deb.debian.org
ENV DEBIAN_FRONTEND=noninteractive PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN sed -i "s|http://deb.debian.org|${DEBIAN_MIRROR}|g" /etc/apt/sources.list.d/debian.sources \
    && apt-get update && apt-get install -y --no-install-recommends \
       bash ca-certificates nodejs npm poppler-utils libreoffice-calc-nogui fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*
# Judge component pinned to the version in the delivery template.
RUN npm install -g @anthropic-ai/claude-code@2.1.114
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /app
COPY input_files/ /app/input_files/
RUN chmod -R a-w /app/input_files && mkdir -p /app/output /logs/verifier
