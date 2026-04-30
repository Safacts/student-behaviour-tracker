# Utility Functions

This directory contains utility functions and helpers for the application.

## Files

- **monitoring.py** - Application monitoring
  - Prometheus metrics initialization
  - API request tracking
  - Performance metrics
  - Application info metrics

## Features

- **Metrics Tracking**: Track API requests, duration, and active users
- **Prometheus Integration**: Export metrics in Prometheus format
- **Performance Monitoring**: Monitor application performance
- **Health Metrics**: Track application health status

## Usage

```python
from src.utils.monitoring import initialize_metrics, api_requests_total

# Initialize metrics
initialize_metrics()

# Track API request
api_requests_total.labels(method="GET", endpoint="/api/students").inc()
```
