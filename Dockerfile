# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Install system dependencies (needed for compiling certain ML libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a data directory for the SQLite database
RUN mkdir -p /app/data

# Copy the application code
COPY ./app ./app
COPY ./alembic.ini .
COPY ./models ./models

# Expose port
EXPOSE 8000

# Run FastAPI using uvicorn
# Using a script or direct command to apply migrations before starting could be done,
# but for simplicity, we'll start the server directly. In production, consider a start.sh script.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
