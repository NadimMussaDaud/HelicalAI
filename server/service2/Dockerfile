FROM python:3.11-slim

# Install minimal system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install only required Python packages
RUN pip install \
    fastapi==0.109.1 \
    uvicorn==0.27.0 \
    pydantic==2.6.1

COPY . .

EXPOSE 8002
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8002"]
