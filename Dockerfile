FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY fisens_dashboard.py .
COPY templates/ ./templates/

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=fisens_dashboard.py
ENV PYTHONUNBUFFERED=1

# Run the Flask application
CMD ["python", "fisens_dashboard.py"]