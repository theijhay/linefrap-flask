#!/bin/bash

echo "🚀 Starting LineFRAP Deployment..."

# Stop previous containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build new image
echo "🏗️ Building Docker images..."
docker-compose build

# Start container
echo "🚀 Starting Docker containers..."
docker-compose up -d

# Check status
echo "📊 Checking container status..."
docker ps

echo "✅ Deployment complete. App should be live at http://localhost:5000"
