# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libudev-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY serial-web-interface.py .
COPY templates/index.html templates/

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["python", "serial-web-interface.py"]