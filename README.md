# Student Behavior Analytics Microservice

Production-grade student behavior analytics microservice with agentic AI capabilities for educational institutions.

## Overview

This microservice provides comprehensive student behavior analysis, personalized learning recommendations, and intervention strategies using advanced AI agents. It's designed as a flexible, independent service that can be easily integrated into any existing educational system.

## Features

### Core Analytics
- **Behavior Pattern Recognition**: AI-powered analysis of student learning patterns
- **Performance Tracking**: Comprehensive academic performance metrics
- **Trend Analysis**: Identify learning trends and predict outcomes
- **Risk Assessment**: Early detection of at-risk students

### Agentic AI Capabilities
- **Behavior Analysis Agent**: Analyzes behavioral patterns and identifies risks
- **Learning Path Agent**: Generates personalized learning recommendations
- **Intervention Agent**: Provides actionable intervention strategies
- **Agent Orchestration**: Pipeline execution for comprehensive analysis

### Enterprise Features
- **Production-Grade Architecture**: Scalable microservice design
- **Comprehensive API**: RESTful APIs with OpenAPI documentation
- **Real-time Processing**: Async support for high-performance analytics
- **Monitoring & Logging**: Structured logging with correlation IDs
- **Container Ready**: Docker support with production configurations

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (production) or SQLite (development)
- Redis (optional, for caching)
- Google AI API key (for AI features)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd student_behavior_analysis
```

2. **Setup environment**
```bash
# Copy environment configuration
cp .env.example .env

# Update with your configuration
# Set GOOGLE_API_KEY for AI features
# Set DATABASE_URL for your database
```

3. **Install dependencies**
```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install -r requirements.txt
```

4. **Start the service**
```bash
# Auto-detect environment and start
./scripts/start.sh start

# Or force development mode
./scripts/start.sh dev

# Or force production mode
./scripts/start.sh prod
```

5. **Verify installation**
```bash
curl http://localhost:8000/health/live
```

### Docker Deployment

```bash
# Build and run with Docker Compose
cd docker
docker-compose up -d

# Check health
curl http://localhost:8000/health/live
```

## API Documentation

### Base URL
- Development: `http://localhost:8000`
- Production: `http://your-domain.com`

### Authentication
This microservice is designed to be authentication-agnostic. Client systems should handle authentication at their end.

### Key Endpoints

#### Health Checks
```bash
GET /health/live          # Liveness probe
GET /health/ready         # Readiness probe
GET /health/              # Comprehensive health check
```

#### Analytics
```bash
GET /api/v1/analytics/students/{student_id}/summary
GET /api/v1/analytics/students/{student_id}/activity
GET /api/v1/analytics/students/{student_id}/trends
GET /api/v1/analytics/class/{class_name}/summary
POST /api/v1/analytics/batch-analysis
```

#### AI Agents
```bash
POST /api/v1/agents/analyze                    # Single agent analysis
POST /api/v1/agents/analyze-batch              # Batch analysis
POST /api/v1/agents/pipeline                   # Agent pipeline
GET  /api/v1/agents/available                 # Available agents
POST /api/v1/agents/learning-path              # Learning path generation
POST /api/v1/agents/intervention               # Intervention suggestions
```

#### Student Management
```bash
POST /api/v1/students/activity                 # Add activity data
POST /api/v1/students/activity/batch           # Batch activity upload
GET  /api/v1/students/list                     # List students
GET  /api/v1/students/{student_id}             # Student details
DELETE /api/v1/students/{student_id}           # Delete student data
```

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs` (development only)
- OpenAPI Spec: `http://localhost:8000/openapi.json`

## Architecture

### Microservice Design
```
student-behavior-analytics/
```

### Core Components
- **API Layer**: FastAPI with comprehensive error handling
- **Analytics Engine**: Data processing and aggregation
- **AI Agents**: LangChain-based agentic AI framework
- **Database Layer**: SQLAlchemy with async support
- **Configuration**: Environment-based configuration management
- **Logging**: Structured logging with correlation tracking

### Data Flow
1. **Data Ingestion**: Student activity data via REST APIs
2. **Processing**: Real-time analytics and trend analysis
3. **AI Analysis**: Agent-based behavioral insights
4. **Response**: Structured JSON responses with metadata

## Configuration

### Environment Variables

#### Core Settings
```bash
ENVIRONMENT=development|production
DEBUG=true|false
SECRET_KEY=your-secret-key
```

#### Database
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
SQLITE_URL=sqlite:///./data/student_behavior.db
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

#### AI/ML
```bash
GOOGLE_API_KEY=your-google-api-key
GEMINI_MODEL=gemini-2.5-flash
AGENT_TIMEOUT=300
BEHAVIOR_ANALYSIS_THRESHOLD=0.7
```

#### API Settings
```bash
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
RATE_LIMIT_REQUESTS=100
CORS_ORIGINS=["*"]
```

#### Monitoring
```bash
ENABLE_METRICS=true
LOG_LEVEL=INFO
LOG_FORMAT=json|console
```

## AI Agents

### Behavior Analysis Agent
Analyzes student behavior patterns and identifies risks.

**Request:**
```json
{
  "agent_type": "behavior_analysis",
  "student_id": "S001",
  "parameters": {}
}
```

**Response:**
```json
{
  "behavioral_analysis": {
    "behavioral_tag": "On Track",
    "confidence_score": 0.85,
    "risk_factors": [],
    "strengths": ["Excellent focus", "Consistent study habits"],
    "recommendations": ["Maintain current patterns"]
  }
}
```

### Learning Path Agent
Generates personalized learning recommendations.

**Request:**
```json
{
  "agent_type": "learning_path",
  "student_id": "S001",
  "parameters": {
    "subject_focus": "math",
    "difficulty_level": "intermediate"
  }
}
```

### Intervention Agent
Provides intervention strategies for at-risk students.

**Request:**
```json
{
  "agent_type": "intervention",
  "student_id": "S001",
  "parameters": {
    "intervention_type": "academic",
    "urgency_level": "medium"
  }
}
```

## Integration Guide

### Client Integration

#### 1. Direct API Integration
```python
import requests

# Get student summary
response = requests.get(
    "http://your-service/api/v1/analytics/students/S001/summary"
)
data = response.json()

# Run behavior analysis
response = requests.post(
    "http://your-service/api/v1/agents/analyze",
    json={
        "agent_type": "behavior_analysis",
        "student_id": "S001"
    }
)
```

#### 2. Batch Processing
```python
# Process multiple students
response = requests.post(
    "http://your-service/api/v1/analytics/batch-analysis",
    json={
        "student_ids": ["S001", "S002", "S003"],
        "analysis_type": "comprehensive",
        "days": 30
    }
)
```

#### 3. Agent Pipeline
```python
# Run comprehensive analysis pipeline
response = requests.post(
    "http://your-service/api/v1/agents/pipeline",
    json={
        "student_id": "S001",
        "agent_types": ["behavior_analysis", "learning_path", "intervention"]
    }
)
```

### Data Format

#### Student Activity Data
```json
{
  "student_id": "S001",
  "student_name": "John Doe",
  "log_date": "2024-01-15",
  "subject_category": "math",
  "lesson_name": "Algebra Basics",
  "quiz_score": "85%",
  "time_spent_minutes": 45,
  "distraction_score": 2.5,
  "marks_achieved_percent": 85.0
}
```

#### Batch Upload
```json
{
  "activities": [
    {
      "student_id": "S001",
      "log_date": "2024-01-15",
      "subject_category": "math",
      "lesson_name": "Algebra Basics",
      "quiz_score": "85%",
      "time_spent_minutes": 45
    },
    {
      "student_id": "S002",
      "log_date": "2024-01-15",
      "subject_category": "science",
      "lesson_name": "Physics Fundamentals",
      "quiz_score": "78%",
      "time_spent_minutes": 38
    }
  ]
}
```

## Deployment

### Development
```bash
# Start development server
./scripts/start.sh dev

# Or with Poetry
poetry run uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```

### Production with Docker
```bash
# Build and deploy
docker-compose -f docker/docker-compose.yml up -d

# Scale the service
docker-compose -f docker/docker-compose.yml up -d --scale student-behavior-analytics=3
```

### Kubernetes
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment
kubectl get pods -n student-behavior-analytics
```

## Monitoring

### Health Checks
- **Liveness**: `/health/live` - Service is running
- **Readiness**: `/health/ready` - Service is ready to accept requests
- **Comprehensive**: `/health` - Full system health including database

### Metrics
- **Prometheus**: `/metrics` - Application metrics
- **Custom Metrics**: Request count, processing time, error rates
- **Agent Metrics**: Agent execution time, confidence scores

### Logging
- **Structured JSON**: Production-ready structured logs
- **Correlation IDs**: Request tracking across services
- **Performance Logging**: Operation timing and success rates

## Security

### Best Practices
- **Environment Variables**: Sensitive data in environment variables
- **No Authentication**: Client-side authentication handling
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Protection**: SQLAlchemy parameterized queries
- **Rate Limiting**: Configurable request rate limits

### Recommendations
- Use HTTPS in production
- Implement authentication at the gateway level
- Regular security updates for dependencies
- Monitor for unusual activity patterns

## Performance

### Optimization Features
- **Async Processing**: Non-blocking I/O operations
- **Connection Pooling**: Database connection management
- **Caching**: Redis-based caching for frequent queries
- **Batch Processing**: Efficient bulk operations

### Benchmarks
- **Response Time**: < 500ms for analytics queries
- **Throughput**: 1000+ requests/minute per instance
- **Memory Usage**: < 512MB per instance
- **CPU Usage**: < 50% under normal load

## Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check environment
./scripts/start.sh check

# Verify dependencies
poetry install

# Check port availability
netstat -tulpn | grep :8000
```

#### Database Connection Issues
```bash
# Check database URL
echo $DATABASE_URL

# Test connection
python -c "from src.core.database import db_manager; db_manager.health_check()"
```

#### AI Features Not Working
```bash
# Check API key
echo $GOOGLE_API_KEY

# Test AI service
curl -X POST http://localhost:8000/api/v1/agents/analyze \
  -H "Content-Type: application/json" \
  -d '{"agent_type":"behavior_analysis","student_id":"test"}'
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
export DEBUG=true

# Start with verbose output
./scripts/start.sh dev
```

## Contributing

### Development Setup
1. Clone repository
2. Install development dependencies: `poetry install --with dev`
3. Setup pre-commit hooks: `pre-commit install`
4. Run tests: `pytest`

### Code Style
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_analytics.py::test_student_summary
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation at `/docs`

## Changelog

### v1.0.0
- Initial production release
- Agentic AI framework
- Comprehensive analytics
- Production-grade architecture
- Docker deployment support
- Full API documentation
