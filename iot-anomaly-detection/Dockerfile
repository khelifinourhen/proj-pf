FROM python:3.11-slim

WORKDIR /app

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api/
COPY model/ ./model/

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "5000", "--log-level", "info"]
