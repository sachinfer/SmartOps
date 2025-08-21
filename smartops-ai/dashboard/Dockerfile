# 🚀 OPTIMIZED: Multi-stage build with better caching
FROM python:3.9-slim as base

# Install system dependencies in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    supervisor \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code and configuration
COPY . ./dashboard/
COPY supervisord.conf ./

# Set working directory to dashboard
WORKDIR /app/dashboard

# Expose ports
EXPOSE 8501
EXPOSE 8000

# Use supervisord for process management
CMD ["/usr/bin/supervisord", "-c", "/app/dashboard/supervisord.conf"] 