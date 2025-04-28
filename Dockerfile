# Step 1: Build stage
FROM python:3.10-slim AS builder

WORKDIR /install

# Install OS libraries needed for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --prefix=/install/packages -r requirements.txt

# Runtime stage
FROM python:3.10-slim

WORKDIR /app

# Copy system libraries again (minimal base)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages
COPY --from=builder /install/packages /usr/local

# Copy application code
COPY . .

ENV PYTHONPATH=/usr/local:$PYTHONPATH
ENV FLASK_ENV=production
ENV UPLOAD_FOLDER=/app/uploads

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
