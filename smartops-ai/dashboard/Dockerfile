FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY dash_app.py .
COPY event_api.py .
COPY log_deployment_event.py .

# Copy pages directory (Plotly-Dash modules)
COPY pages/ ./pages/

# Create data directory
RUN mkdir -p /app/data

# Create data directory (data files will be mounted at runtime)
RUN mkdir -p /app/data
# Ensure data directory has proper permissions
RUN chmod 755 /app/data

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/ || exit 1

# Run the application
CMD ["python", "dash_app.py"]
