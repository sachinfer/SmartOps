FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y supervisor

COPY . ./dashboard/
WORKDIR /app/dashboard

COPY supervisord.conf ./

EXPOSE 8501
EXPOSE 8000

CMD ["/usr/bin/supervisord", "-c", "/app/dashboard/supervisord.conf"] 