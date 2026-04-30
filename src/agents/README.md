# AI Agents

This directory contains AI agent implementations for student behavior analysis and automation.

## Files

- **agents.py** - Core agent tools and functions for student analysis
  - Student data retrieval tools
  - Behavior analysis tools
  - Learning path generation
  - Intervention suggestions
  - Task management tools
  - Report generation tools

- **agent_orchestrator.py** - Agent orchestration and routing
  - IntentParser - Parses natural language queries
  - ToolRegistry - Registry of available agent tools
  - ConversationalRouter - Routes queries to appropriate tools
  - Role-based response generation

## Features

- **Behavior Analysis**: Analyze student behavior patterns and identify risks
- **Learning Paths**: Generate personalized learning paths for students
- **Interventions**: Suggest intervention strategies for at-risk students
- **Task Management**: Create and manage intervention/monitoring tasks
- **Report Generation**: Generate AI-powered reports using LLM
- **Conversational AI**: Natural language interface for querying student data

## Usage

```python
from src.agents.agents import analyze_student_behavior, create_learning_path
from src.agents.agent_orchestrator import ConversationalRouter

# Analyze student behavior
result = analyze_student_behavior("S001")

# Create learning path
path = create_learning_path("S001")

# Use conversational router
router = ConversationalRouter(tool_registry, intent_parser)
response = router.process_query("Analyze student S001")
```
