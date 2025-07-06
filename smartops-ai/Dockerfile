# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# Add timeout + retries for pip
RUN pip install --default-timeout=100 --retries=10 --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
