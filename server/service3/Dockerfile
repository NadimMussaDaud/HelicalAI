FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
RUN pip install \
    fastapi==0.109.1 \
    uvicorn==0.27.0 \
    pandas==2.1.4 \
    scikit-learn==1.3.2 \
    pydantic==2.6.1

COPY . .

EXPOSE 8006
CMD ["uvicorn", "TranscriptFormer:app", "--host", "0.0.0.0", "--port", "8006"]