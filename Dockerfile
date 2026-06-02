FROM python:3.12-slim AS deps

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim

RUN useradd -m -u 1000 appuser

WORKDIR /app

COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin/uvicorn /usr/local/bin/uvicorn

COPY --chown=appuser:appuser . .

RUN mkdir -p uploads && chown appuser:appuser uploads

USER appuser

EXPOSE 8000

CMD uvicorn backend.main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000} \
    --loop uvloop \
    --http httptools \
    --timeout-keep-alive 65 \
    --proxy-headers \
    --forwarded-allow-ips "*"
