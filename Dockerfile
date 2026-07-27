# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN groupadd --system fanpesa \
    && useradd --system --gid fanpesa --home /app --shell /usr/sbin/nologin fanpesa \
    && mkdir -p /app/logs \
    && chown -R fanpesa:fanpesa /app

USER fanpesa

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
