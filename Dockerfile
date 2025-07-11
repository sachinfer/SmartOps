FROM python:3.9-slim

WORKDIR /app

# ✅ Install curl for debugging
RUN apt-get update && apt-get install -y curl && apt-get clean

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 8081

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8081"]
