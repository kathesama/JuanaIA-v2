FROM python:3.11-slim

WORKDIR /app

COPY api-gateway/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY api-gateway /app/api-gateway
COPY common /app/common
COPY orchestrator /app/orchestrator

ENV PYTHONPATH=/app/api-gateway:/app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
