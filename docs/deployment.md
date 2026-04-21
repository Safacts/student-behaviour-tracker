# Deployment Guide

This guide covers various deployment options for the Student Behavior Analytics microservice.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Development Deployment](#development-deployment)
- [Production Deployment](#production-deployment)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## Prerequisites

### System Requirements
- **CPU**: Minimum 2 cores, Recommended 4+ cores
- **Memory**: Minimum 4GB RAM, Recommended 8GB+ RAM
- **Storage**: Minimum 20GB, Recommended 100GB+
- **Network**: Stable internet connection for AI services

### Software Requirements
- Python 3.11+ or Docker 20.10+
- PostgreSQL 15+ (production) or SQLite (development)
- Redis 7+ (optional, for caching)
- Google AI API key (for AI features)

## Environment Setup

### 1. Clone Repository
```bash
git clone https://github.com/Safacts/student-behaviour-tracker.git
cd student-behaviour-tracker
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**Required Environment Variables:**
```bash
# Core Settings
ENVIRONMENT=production
SECRET_KEY=your-secure-secret-key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/student_behavior

# AI Services
GOOGLE_API_KEY=your-google-api-key

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
```

### 3. Install Dependencies
```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install -r requirements.txt
```

## Development Deployment

### Quick Start
```bash
# Start development server
./scripts/start.sh dev

# Or using Poetry directly
poetry run uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```

### Hybrid Mode (Legacy + Production)
```bash
# Start with legacy compatibility
python main_production.py

# Access endpoints:
# Legacy: http://localhost:8000/api/students
# Production: http://localhost:8000/api/v2/analytics
```

### Development Features
- Auto-reload on code changes
- Debug logging enabled
- SQLite database by default
- CORS enabled for all origins
- API documentation at `/docs`

## Production Deployment

### 1. Production Server Setup
```bash
# Install system dependencies
sudo apt update
sudo apt install python3.11 python3.11-venv postgresql-15 redis-server

# Create application user
sudo useradd -m -s /bin/bash student-analytics
sudo su - student-analytics
```

### 2. Database Setup
```bash
# Switch to postgres user
sudo su - postgres

# Create database and user
createdb student_behavior
psql -c "CREATE USER student_user WITH PASSWORD 'secure_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE student_behavior TO student_user;"

# Import schema
psql -d student_behavior -f docker/init-db.sql
```

### 3. Application Setup
```bash
# Clone and setup application
git clone https://github.com/Safacts/student-behaviour-tracker.git
cd student-behaviour-tracker

# Install dependencies
poetry install --only main

# Setup environment
cp .env.example .env
# Edit .env with production values
```

### 4. Systemd Service
```bash
# Create service file
sudo tee /etc/systemd/system/student-analytics.service << EOF
[Unit]
Description=Student Behavior Analytics API
After=network.target postgresql.service redis.service

[Service]
Type=exec
User=student-analytics
Group=student-analytics
WorkingDirectory=/home/student-analytics/student-behaviour-tracker
Environment=PATH=/home/student-analytics/.local/bin
ExecStart=/home/student-analytics/.local/bin/poetry run uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable student-analytics
sudo systemctl start student-analytics
```

### 5. Nginx Reverse Proxy
```bash
# Install Nginx
sudo apt install nginx

# Create configuration
sudo tee /etc/nginx/sites-available/student-analytics << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/student-analytics /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Docker Deployment

### 1. Using Docker Compose (Recommended)
```bash
# Navigate to project directory
cd student-behaviour-tracker

# Start all services
cd docker
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f student-behavior-analytics
```

### 2. Custom Docker Configuration
```bash
# Build image
docker build -f docker/Dockerfile -t student-behavior-analytics .

# Run container
docker run -d \
  --name student-analytics \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e GOOGLE_API_KEY=your-api-key \
  -v $(pwd)/data:/app/data \
  student-behavior-analytics
```

### 3. Production Docker Compose
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/student_behavior
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: student_behavior
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

## Kubernetes Deployment

### 1. Namespace and ConfigMap
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: student-analytics
---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: student-analytics
data:
  ENVIRONMENT: "production"
  API_HOST: "0.0.0.0"
  API_PORT: "8000"
  LOG_LEVEL: "INFO"
```

### 2. Secret Management
```yaml
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: student-analytics
type: Opaque
data:
  DATABASE_URL: <base64-encoded-url>
  GOOGLE_API_KEY: <base64-encoded-key>
  SECRET_KEY: <base64-encoded-secret>
```

### 3. Deployment
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: student-analytics
  namespace: student-analytics
spec:
  replicas: 3
  selector:
    matchLabels:
      app: student-analytics
  template:
    metadata:
      labels:
        app: student-analytics
    spec:
      containers:
      - name: app
        image: your-registry/student-behavior-analytics:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### 4. Service and Ingress
```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: student-analytics-service
  namespace: student-analytics
spec:
  selector:
    app: student-analytics
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
---
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: student-analytics-ingress
  namespace: student-analytics
spec:
  rules:
  - host: analytics.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: student-analytics-service
            port:
              number: 80
```

### 5. Deploy to Kubernetes
```bash
# Apply all configurations
kubectl apply -f k8s/

# Check deployment
kubectl get pods -n student-analytics

# Check service
kubectl get svc -n student-analytics

# View logs
kubectl logs -f deployment/student-analytics -n student-analytics
```

## Cloud Deployment

### AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-west-2.amazonaws.com

docker build -f docker/Dockerfile -t student-behavior-analytics .
docker tag student-behavior-analytics:latest <account-id>.dkr.ecr.us-west-2.amazonaws.com/student-behavior-analytics:latest
docker push <account-id>.dkr.ecr.us-west-2.amazonaws.com/student-behavior-analytics:latest

# Deploy using ECS task definition
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json
aws ecs update-service --cluster student-analytics --service student-analytics --task-definition student-analytics:1
```

### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/your-project/student-behavior-analytics

# Deploy to Cloud Run
gcloud run deploy student-analytics \
  --image gcr.io/your-project/student-behavior-analytics \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=your-db-url,GOOGLE_API_KEY=your-api-key
```

### Azure Container Instances
```bash
# Create resource group
az group create --name student-analytics --location eastus

# Deploy container
az container create \
  --resource-group student-analytics \
  --name student-analytics \
  --image your-registry/student-behavior-analytics:latest \
  --cpu 1 \
  --memory 2 \
  --ports 8000 \
  --environment-variables DATABASE_URL=your-db-url GOOGLE_API_KEY=your-api-key
```

## Monitoring and Maintenance

### Health Checks
```bash
# Application health
curl http://localhost:8000/health/live

# Database health
curl http://localhost:8000/health/ready

# Full system health
curl http://localhost:8000/health/
```

### Log Management
```bash
# View application logs
docker-compose logs -f student-behavior-analytics

# System logs (systemd)
sudo journalctl -u student-analytics -f

# Kubernetes logs
kubectl logs -f deployment/student-analytics -n student-analytics
```

### Performance Monitoring
```bash
# Application metrics
curl http://localhost:8000/metrics

# Resource usage
docker stats
# or
kubectl top pods -n student-analytics
```

### Backup and Recovery
```bash
# Database backup
pg_dump student_behavior > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf app_backup_$(date +%Y%m%d).tar.gz data/ logs/

# Restore database
psql student_behavior < backup_20240115.sql
```

### Scaling
```bash
# Docker Compose scaling
docker-compose up -d --scale student-behavior-analytics=3

# Kubernetes scaling
kubectl scale deployment student-analytics --replicas=5 -n student-analytics

# Manual scaling (systemd)
# Edit service file and update workers count
sudo systemctl edit student-analytics
```

### Updates and Maintenance
```bash
# Update application
git pull origin main
poetry install
sudo systemctl restart student-analytics

# Rolling update (Kubernetes)
kubectl set image deployment/student-analytics app=your-registry/student-behavior-analytics:v2 -n student-analytics

# Blue-green deployment
# Deploy to staging first, then switch traffic
```

## Troubleshooting

### Common Issues
1. **Database Connection Failed**
   - Check DATABASE_URL format
   - Verify database is running
   - Check network connectivity

2. **AI Services Not Working**
   - Verify GOOGLE_API_KEY is valid
   - Check internet connectivity
   - Review API quota limits

3. **High Memory Usage**
   - Reduce API workers count
   - Enable caching
   - Optimize database queries

4. **Slow Response Times**
   - Add Redis caching
   - Optimize database indexes
   - Scale horizontally

### Debug Commands
```bash
# Check application status
systemctl status student-analytics

# Test database connection
python -c "from src.core.database import db_manager; print(db_manager.health_check())"

# Check logs
tail -f /var/log/student-analytics/app.log

# Performance test
locust --headless --users 50 --run-time 60s --host http://localhost:8000
```

## Security Considerations

### Production Security
- Use HTTPS in production
- Implement rate limiting
- Regular security updates
- Monitor for unusual activity
- Backup data regularly

### Network Security
- Firewall configuration
- VPN access for admin
- Network segmentation
- DDoS protection

### Data Security
- Encrypt sensitive data
- Regular backups
- Access control
- Audit logging

This deployment guide covers the most common deployment scenarios. Choose the one that best fits your infrastructure and requirements.
