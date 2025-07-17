FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./dashboard/
WORKDIR /app/dashboard

EXPOSE 8501

# To run the event API (for dev):
# CMD ["uvicorn", "event_api:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"] 