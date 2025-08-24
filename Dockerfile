FROM python:3.13-slim

# Add image metadata to match docker-compose.yml
LABEL org.opencontainers.image.title="pr-semgrep-scanner"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.description="PR Semgrep Scanner using Portia SDK Python"
LABEL org.opencontainers.image.authors="AlapMistry"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create directory for plan storage
RUN mkdir -p demo_runs && chmod 777 demo_runs

# Set default environment variables
# These will be overridden by values from .env file when using docker-compose
ENV PORT=4000
ENV PYTHONUNBUFFERED=1

# Expose the port (should match PORT environment variable)
EXPOSE 4000

# Run the application
CMD ["python", "start_server.py"]
