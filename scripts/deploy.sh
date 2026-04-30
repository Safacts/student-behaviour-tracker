#!/bin/bash

# Production deployment script for Student Behavior Analytics

set -e

echo "Starting deployment of Student Behavior Analytics..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
mkdir -p logs ssl

# Copy production environment file if it doesn't exist
if [ ! -f .env.production ]; then
    echo "Creating .env.production file..."
    cp .env.production .env.production
    echo "Please update .env.production with your configuration before running this script again."
    exit 1
fi

# Build Docker images
echo "Building Docker images..."
docker-compose build

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down

# Start services
echo "Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo "Waiting for services to be healthy..."
sleep 10

# Check health
echo "Checking service health..."
curl -f http://localhost:8000/api/health || {
    echo "Health check failed. Please check the logs."
    docker-compose logs
    exit 1
}

echo "Deployment completed successfully!"
echo "Service is running at http://localhost:8000"
echo "View logs with: docker-compose logs -f"
