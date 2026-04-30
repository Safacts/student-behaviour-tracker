# Business Services

This directory contains business logic services that handle core application functionality.

## Files

- **analyzer.py** - Student behavior analysis
  - Analyze student activity data
  - Calculate behavioral metrics
  - Generate behavioral tags
  - Identify patterns and trends

- **llm_service.py** - LLM integration service
  - Parent report generation using AI
  - Natural language query processing
  - Groq API integration
  - OpenAI API integration
  - Gemini API integration
  - Fallback mechanisms for rate limits

- **query_builder.py** - API Builder service
  - Dynamic query configuration
  - Query execution
  - Configuration persistence
  - SQL query generation

- **workflow_engine.py** - Workflow automation engine
  - Workflow execution orchestration
  - Node execution management
  - State management
  - Workflow persistence
  - Topological sorting for dependencies

- **workflow_nodes.py** - Workflow node implementations
  - DataQueryNode - Database query execution
  - AIProcessNode - AI data processing
  - EmailSendNode - Email sending via SMTP
  - ConditionNode - Conditional branching
  - LoopNode - Data iteration

- **microservice_monitor.py** - Health monitoring service
  - Database connectivity checks
  - API endpoint monitoring
  - External API health checks
  - System resource monitoring
  - Debug report generation

## Usage

```python
from src.services.analyzer import analyze_student
from src.services.llm_service import generate_parent_report
from src.services.workflow_engine import WorkflowEngine

# Analyze student
analysis = analyze_student("S001")

# Generate AI report
report = generate_parent_report(student_data, "High Flight Risk")

# Execute workflow
engine = WorkflowEngine()
result = engine.execute_workflow(workflow_id)
```
