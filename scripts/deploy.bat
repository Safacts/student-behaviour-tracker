@echo off
REM Production deployment script for Student Behavior Analytics (Windows)

echo Starting deployment of Student Behavior Analytics...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

REM Create necessary directories
if not exist logs mkdir logs
if not exist ssl mkdir ssl

REM Copy production environment file if it doesn't exist
if not exist .env.production (
    echo Creating .env.production file...
    copy .env.production .env.production
    echo Please update .env.production with your configuration before running this script again.
    exit /b 1
)

REM Build Docker images
echo Building Docker images...
docker-compose build

REM Stop existing containers
echo Stopping existing containers...
docker-compose down

REM Start services
echo Starting services...
docker-compose up -d

REM Wait for services to be healthy
echo Waiting for services to be healthy...
timeout /t 10 /nobreak >nul

REM Check health
echo Checking service health...
curl -f http://localhost:8000/api/health
if %errorlevel% neq 0 (
    echo Health check failed. Please check the logs.
    docker-compose logs
    exit /b 1
)

echo Deployment completed successfully!
echo Service is running at http://localhost:8000
echo View logs with: docker-compose logs -f
