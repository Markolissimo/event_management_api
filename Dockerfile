FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -u 1000 -m celeryuser

RUN mkdir -p /var/lib/celery/beat && \
    chown -R celeryuser:celeryuser /var/lib/celery

COPY requirements.txt .
RUN pip install "setuptools<58.0.0"
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R celeryuser:celeryuser /app

USER celeryuser

CMD ["gunicorn", "event_management.wsgi:application", "--bind", "0.0.0.0:8000"] 