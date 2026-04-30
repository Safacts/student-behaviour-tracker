# Student Behavior Analytics Platform

Production-grade student behavior analytics platform with agentic AI capabilities, workflow automation, and role-based conversational AI for educational institutions.

## Overview

This platform provides comprehensive student behavior analysis, personalized learning recommendations, intervention strategies, and workflow automation using advanced AI agents. It features a modern web interface, conversational AI chat, API builder for custom queries, and n8n-like workflow automation.

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
- **Role-Based Chat**: Conversational AI tailored to user roles (developer, student, faculty, parent, principal)

### Workflow Automation
- **Visual Workflow Builder**: n8n-like drag-and-drop workflow creation
- **Workflow Engine**: Execute multi-step automation workflows
- **Node Types**: Data Query, AI Processing, Email Send, Condition, Loop
- **Workflow Templates**: Pre-built workflows for common tasks

### API Builder
- **Dynamic Query Builder**: Create custom API endpoints without coding
- **AI-Powered Query Building**: Natural language to SQL conversion
- **Query Persistence**: Save and reuse query configurations
- **API Generation**: Generate REST endpoints from queries

### Enterprise Features
- **Production-Grade Architecture**: Modular, scalable design
- **Comprehensive API**: RESTful APIs with authentication
- **Health Monitoring**: Microservice health checks and debugging
- **Container Ready**: Docker support with production configurations

## Project Structure

```
student_behavior_analysis/
├── main.py                 # Application entry point
├── src/                    # Source code
│   ├── agents/            # AI agent implementations
│   ├── api/               # FastAPI application and endpoints
│   ├── core/              # Core utilities (auth, cache, logger, validators)
│   ├── models/            # Data models and task management
│   ├── services/          # Business logic services
│   └── utils/             # Utility functions
├── templates/             # HTML templates for web UI
├── static/                # Static assets
├── tests/                 # Test files
├── docs/                  # Documentation
├── scripts/               # Utility and deployment scripts
├── config/                # Configuration files
├── logs/                  # Log files
├── behavior.db            # SQLite database
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md             # This file
```

## Quick Start

### Prerequisites
- Python 3.11+
- SQLite (included) or PostgreSQL (production)
- API keys for AI features (Groq, OpenAI, Gemini)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd student_behavior_analysis
```

2. **Setup environment**
```bash
# Copy environment configuration
cp config/.env.example .env

# Update with your configuration
# Set GROQ_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY
# Set SMTP credentials for email features
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Start the application**
```bash
python main.py
```

5. **Access the application**
- Main UI: http://localhost:8000
- Dashboard: http://localhost:8000/dashboard
- Chat: http://localhost:8000/chat
- API Builder: http://localhost:8000/api-builder
- Agents: http://localhost:8000/agents
- Monitor: http://localhost:8000/monitor

## API Documentation

### Base URL
- Development: `http://localhost:8000`

### Authentication
API endpoints require authentication tokens. Generate a token:

```bash
curl "http://localhost:8000/api/auth/token?user_id=your_user_id"
```

Use the token in the Authorization header:
```
Authorization: Bearer <token>
```

### Key Endpoints

#### Student Analysis
```bash
GET /api/students                    # List all students
GET /api/report/{student_id}         # Get student analysis report
GET /api/activity-logs              # Get all activity logs
```

#### Chat & AI
```bash
POST /api/chat                       # Conversational AI chat
POST /api/query/ai-build             # AI-powered query building
```

#### API Builder
```bash
GET /api/query/tables               # Get available database tables
GET /api/query/config/list          # List saved query configurations
POST /api/query/config/save         # Save query configuration
GET /api/query/config/execute/{name} # Execute saved configuration
```

#### Task Management
```bash
GET /api/v2/tasks/create/intervention  # Create intervention task
GET /api/v2/tasks/create/monitoring    # Create monitoring task
GET /api/v2/tasks/complete/{task_id}   # Complete task
GET /api/v2/tasks/assigned/{assigned_to} # Get tasks for user
```

#### Workflow Automation
```bash
POST /api/workflows                 # Create workflow
GET /api/workflows                  # List workflows
GET /api/workflows/{id}             # Get workflow details
POST /api/workflows/{id}/execute    # Execute workflow
DELETE /api/workflows/{id}          # Delete workflow
```

#### Health Monitoring
```bash
GET /api/health                     # Basic health check
GET /api/health/detailed            # Comprehensive health check
GET /api/health/debug               # Debug report with recommendations
```

## Architecture

### Layered Architecture
```
UI Layer (templates/)
    ↓
API Layer (src/api/)
    ↓
Service Layer (src/services/)
    ↓
Core Layer (src/core/)
    ↓
Model Layer (src/models/)
```

### Core Components
- **API Layer**: FastAPI with comprehensive error handling
- **Agent Layer**: AI agents for behavior analysis and recommendations
- **Service Layer**: Business logic (analyzer, LLM, workflow engine)
- **Core Layer**: Authentication, caching, logging, validation
- **Model Layer**: Data models and task management

## Configuration

### Environment Variables

Copy `config/.env.example` to `.env` and configure:

```bash
# AI API Keys
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# SMTP Configuration (for email sending)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

## Deployment

### Development
```bash
python main.py
```

### Production with Docker
```bash
# Build and run
docker-compose -f scripts/docker-compose.yml up -d
```

### Production Script
```bash
# Windows
scripts\deploy.bat

# Linux/Mac
bash scripts/deploy.sh
```

## Monitoring

### Health Checks
- **Basic**: `/api/health` - Service status
- **Detailed**: `/api/health/detailed` - Comprehensive system health
- **Debug**: `/api/health/debug` - Debug report with recommendations

### Metrics
- **Prometheus**: `/metrics` - Application metrics
- **Custom Metrics**: Request count, processing time, error rates

## Documentation

- **Project Structure**: See individual README files in each directory
- **API Documentation**: See `docs/` directory
- **Development Guides**: See `docs/` directory
- **User Guides**: See `docs/USER_GUIDE.md`

## Contributing

See `docs/OWNERSHIP_GUIDE.md` for contribution guidelines.

## License

This project is licensed under the MIT License.
