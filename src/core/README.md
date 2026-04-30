# Core Utilities

This directory contains core utility modules used across the application.

## Files

- **auth.py** - Authentication and authorization
  - Token generation and validation
  - User authentication
  - JWT token management

- **cache.py** - Caching layer
  - In-memory caching
  - Cache expiration
  - Performance optimization

- **logger.py** - Logging configuration
  - Structured logging setup
  - Log file management
  - Error tracking

- **rate_limiter.py** - Rate limiting
  - API rate limiting
  - Request throttling
  - Abuse prevention

- **validators.py** - Input validation
  - Student ID validation
  - Data validation
  - Request validation

- **websocket_manager.py** - WebSocket management
  - Real-time communication
  - Connection management
  - Event broadcasting

## Usage

```python
from src.core.auth import auth
from src.core.validators import moderate_validator
from src.core.rate_limiter import rate_limiter

# Validate student ID
valid, error = moderate_validator.validate_student_id("S001")

# Check rate limit
if not rate_limiter.is_allowed("user_123"):
    raise HTTPException(429, "Rate limit exceeded")
```
