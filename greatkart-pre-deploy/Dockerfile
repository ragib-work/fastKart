# Set the Python version (Change if needed)
ARG PYTHON_VERSION=3.7.4
FROM python:${PYTHON_VERSION}

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies (Postgres, Pillow, CairoSVG, GCC, tzdata)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    libcairo2 \
    gcc \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip & install essential tools
RUN pip install --upgrade pip setuptools wheel

# Set working directory
WORKDIR /code

# Copy dependencies first (for caching efficiency)
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Copy the project files
COPY ./greatkart-pre-deploy /code

# Set Django environment variables
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

ARG DJANGO_DEBUG=0
ENV DJANGO_DEBUG=${DJANGO_DEBUG}

# Collect static files (Now runs at runtime instead of build-time)
RUN python manage.py vendor_pull
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
