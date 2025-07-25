# Dockerfile para paquita-api
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn pyairtable python-dotenv transformers torch==2.7.1 -f https://download.pytorch.org/whl/torch_stable.html

EXPOSE 8002

CMD ["uvicorn", "api_dashboard_cors_fixed:app", "--host", "0.0.0.0", "--port", "8002"]
