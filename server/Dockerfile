FROM python:3.11-slim

# 1. Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev git && \
    rm -rf /var/lib/apt/lists/*

# 2. Set up directory structure
WORKDIR /app
RUN mkdir -p /app/data  # For file uploads

# 3. Install Python dependencies (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy app code
COPY . .

EXPOSE 8000
CMD ["uvicorn", "server.server:app", "--host", "0.0.0.0", "--port", "8000"]