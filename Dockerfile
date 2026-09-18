FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies required by PaddleOCR and OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port (Railway uses the PORT environment variable)
EXPOSE 8000

# Command to run the FastAPI application
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
