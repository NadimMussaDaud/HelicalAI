# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the frontend code into the container
COPY . .

# Install dependencies (NiceGUI + HTTP client)
RUN pip install nicegui httpx pandas matplotlib seaborn requests base64 io os

# Expose port 8080 (NiceGUI default)
EXPOSE 8080

# Command to run the app
CMD ["python", "app.py"]