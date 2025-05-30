# Use an official Python image as a base (minimal and secure)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GUNICORN_WORKERS=4 \
    GUNICORN_BIND=0.0.0.0:8050

# Create a non-root user to run the app
RUN addgroup --system dashgroup && adduser --system --ingroup dashgroup dashuser

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt .

# Install Python dependencies securely
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set permissions
RUN chown -R dashuser:dashgroup /app

# Switch to non-root user
USER dashuser

# Expose the port used by the Dash app
EXPOSE 8050

# Start the Gunicorn server with the Dash app
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "--workers", "4", "--threads", "2", "dashboard.main:server"]
