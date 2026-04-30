# Source Code

This directory contains all the application source code organized into modular subdirectories.

## Directory Structure

- **agents/** - AI agent implementations for student behavior analysis
- **api/** - FastAPI application and REST API endpoints
- **core/** - Core utilities (authentication, caching, logging, validation)
- **models/** - Data models and task management
- **services/** - Business logic services (analyzer, LLM, query builder, workflow)
- **utils/** - Utility functions and helpers

## Architecture

The application follows a layered architecture:

```
API Layer (src/api/)
    ↓
Service Layer (src/services/)
    ↓
Core Layer (src/core/)
    ↓
Model Layer (src/models/)
```

## Usage

Import modules using the `src` package:

```python
from src.services.analyzer import analyze_student
from src.agents.agents import analyze_student_behavior
from src.api.main import app
```
