# Use the lightweight Python 3.12 image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies:
# - wget for HEALTHCHECK
# - build-essential, libpq-dev for Python packages with native extensions (if needed)
# Clean up apt cache to reduce image size
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file to leverage Docker layer caching
COPY app/requirements.txt .

# Upgrade pip and install Python dependencies without cache
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app/ .

# Create a non-root user 'appuser' with home directory set to /app
RUN adduser --disabled-password --gecos "" --home /app appuser

# Ensure 'appuser' owns the application directory
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the application port
EXPOSE 8080

# Define a HEALTHCHECK to monitor application status
HEALTHCHECK --interval=30s --timeout=5s \
  CMD wget --spider http://localhost:8080/health || exit 1

# Start the application using Gunicorn with 2 workers and a 120s timeout
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8080", \
     "--timeout", "120", \
     "--workers", "2", \
     "main:app"]
