FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# App code
COPY . .

# Collect static
RUN python manage.py collectstatic --noinput 2>/dev/null || true

# Non-root user
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 8000

CMD ["gunicorn", "medicore.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
