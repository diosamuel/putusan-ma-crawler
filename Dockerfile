# Base image with Python
FROM python:3.10

# Set environment variables
ENV AIRFLOW_HOME=/usr/local/airflow
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libpq-dev \
    gcc \
    curl \
    git \
    nano \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean

# Create working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt && pip install "apache-airflow[celery]==3.0.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.0.3/constraints-3.10.txt"

# Expose port if needed (for API)
EXPOSE 8000

# Default command (overridden by docker-compose)
CMD ["bash"]
