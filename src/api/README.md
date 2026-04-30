# API Layer

This directory contains the FastAPI application and REST API endpoints.

## Files

- **main.py** - Main FastAPI application with all API endpoints
  - Student analysis endpoints
  - Chat and conversational AI endpoints
  - API Builder endpoints
  - Task management endpoints
  - Workflow automation endpoints
  - Health check endpoints
  - Static file serving

## API Endpoints

### Student Analysis
- `GET /api/students` - List all students
- `GET /api/report/{student_id}` - Get student analysis report
- `GET /api/activity-logs` - Get all activity logs

### Chat & AI
- `POST /api/chat` - Conversational AI chat endpoint
- `POST /api/query/ai-build` - AI-powered query building

### API Builder
- `GET /api/query/tables` - Get available database tables
- `GET /api/query/config/list` - List saved query configurations
- `POST /api/query/config/save` - Save query configuration
- `GET /api/query/config/execute/{name}` - Execute saved configuration

### Task Management
- `GET /api/v2/tasks/create/intervention` - Create intervention task
- `GET /api/v2/tasks/create/monitoring` - Create monitoring task
- `GET /api/v2/tasks/complete/{task_id}` - Complete task
- `GET /api/v2/tasks/assigned/{assigned_to}` - Get tasks for user

### Workflow Automation
- `POST /api/workflows` - Create workflow
- `GET /api/workflows` - List workflows
- `GET /api/workflows/{id}` - Get workflow details
- `POST /api/workflows/{id}/execute` - Execute workflow
- `DELETE /api/workflows/{id}` - Delete workflow

### Health Monitoring
- `GET /api/health` - Basic health check
- `GET /api/health/detailed` - Comprehensive health check
- `GET /api/health/debug` - Debug report with recommendations

## Usage

Run the API server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```
