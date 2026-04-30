# Data Models

This directory contains data models and task management logic.

## Files

- **task_manager.py** - Task management system
  - Intervention task creation and management
  - Monitoring task creation and management
  - Task status updates
  - Task assignment and tracking
  - Database-backed task persistence

## Features

- **Task Types**: Intervention tasks, monitoring tasks
- **Task Status**: pending, in_progress, completed, overdue
- **Priority Levels**: low, medium, high, critical
- **Assignment**: Assign tasks to users
- **Persistence**: SQLite database storage
- **Validation**: Input validation for task creation

## Usage

```python
from src.models.task_manager import task_manager

# Create intervention task
task = task_manager.create_intervention_task(
    student_id="S001",
    priority="high",
    assigned_to="teacher_123"
)

# Get assigned tasks
tasks = task_manager.get_assigned_tasks("teacher_123")

# Update task status
result = task_manager.update_task_status(
    task_id="TASK_001",
    status="completed",
    notes="Student showed improvement",
    completed_by="teacher_123"
)
```
