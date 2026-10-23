
FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Collect Django static files during build
RUN DJANGO_SECRET_KEY=build-only-placeholder DJANGO_DEBUG=True python manage.py collectstatic --noinput

# Create a non-root user
RUN groupadd --system django && \
    useradd --system --gid django --home-dir /app django && \
    chown -R django:django /app

# Run application as non-root
USER django

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
