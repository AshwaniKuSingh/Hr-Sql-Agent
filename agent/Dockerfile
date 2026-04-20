# Stage 1 - builder
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Stage 2 - runtime
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY schema.py .
COPY agent.py .

ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=password123
ENV POSTGRES_DB=hrdb
ENV OLLAMA_HOST=http://ollama:11434
ENV OLLAMA_MODEL=llama3.2

CMD ["python", "agent.py"]