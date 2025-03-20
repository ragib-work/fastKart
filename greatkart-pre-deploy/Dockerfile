# Set Python version
ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    tzdata \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv

# Use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and wheel
RUN pip install --upgrade pip setuptools wheel

# Set working directory
WORKDIR /code

# Copy dependencies first for caching efficiency
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy project files
COPY ./greatkart-pre-deploy /code

# Set Django environment variables
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

ARG DJANGO_DEBUG=0
ENV DJANGO_DEBUG=${DJANGO_DEBUG}

# Run static file collection (if needed)
RUN python manage.py collectstatic --noinput || echo "Skipping collectstatic"

# Django project settings
ARG PROJ_NAME="greatkart"

# Create a script to run Django at runtime
RUN printf "#!/bin/bash\n" > ./paracord_runner.sh && \
    printf "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./paracord_runner.sh && \
    printf "python manage.py migrate --no-input\n" >> ./paracord_runner.sh && \
    printf "gunicorn ${PROJ_NAME}.wsgi:application --bind \"0.0.0.0:\$RUN_PORT\"\n" >> ./paracord_runner.sh

# Make the script executable
RUN chmod +x paracord_runner.sh

# Clean up cache to reduce image size
RUN apt-get autoremove -y && apt-get clean

# Run Django when the container starts
CMD ["./paracord_runner.sh"]
