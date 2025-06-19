FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python packages directly
RUN pip install \
    fastapi==0.109.1 \
    uvicorn==0.27.0 \
    pandas==2.1.4

COPY . .

EXPOSE 8001
CMD ["uvicorn", "service1:app", "--host", "0.0.0.0", "--port", "8001"]