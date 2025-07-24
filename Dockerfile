# Use official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies for Scrapy and ClickHouse
RUN apt-get update && \
    apt-get install -y gcc build-essential libxml2-dev libxslt1-dev libffi-dev libssl-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose port if you want to use Scrapyd or a web UI (optional)
# EXPOSE 6800

# Default command (can be overridden)
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["get-latest-putusan"]  # default command