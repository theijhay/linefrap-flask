# Build dependencies separately
FROM python:3.10-slim AS builder

WORKDIR /install

# Install pip dependencies first
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --prefix=/install/packages -r requirements.txt

# Final runtime image
FROM python:3.10-slim

WORKDIR /app

# Copy installed Python packages
COPY --from=builder /install/packages /usr/local

# Copy only app code (small)
COPY . .

ENV PYTHONPATH=/usr/local:$PYTHONPATH
ENV FLASK_ENV=production
ENV UPLOAD_FOLDER=/app/uploads

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
