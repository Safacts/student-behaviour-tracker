"""
Monitoring and Metrics Collection
Provides Prometheus metrics for monitoring the application
"""

from prometheus_client import Counter, Histogram, Gauge, Info
import time
from functools import wraps

# Request metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Agent metrics
agent_calls_total = Counter(
    'agent_calls_total',
    'Total agent tool calls',
    ['tool_name', 'status']
)

agent_call_duration = Histogram(
    'agent_call_duration_seconds',
    'Agent tool call duration in seconds',
    ['tool_name']
)

# Authentication metrics
auth_attempts_total = Counter(
    'auth_attempts_total',
    'Total authentication attempts',
    ['method', 'status']
)

active_sessions = Gauge(
    'active_sessions',
    'Number of active sessions'
)

# Database metrics
db_queries_total = Counter(
    'db_queries_total',
    'Total database queries',
    ['operation', 'table']
)

db_query_duration = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['operation', 'table']
)

# Application metrics
app_info = Info('app_info', 'Application information')

def track_request_duration(func):
    """Decorator to track HTTP request duration"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            http_requests_total.labels(
                method='POST',
                endpoint='/api/chat',
                status='success'
            ).inc()
            return result
        except Exception as e:
            http_requests_total.labels(
                method='POST',
                endpoint='/api/chat',
                status='error'
            ).inc()
            raise
        finally:
            duration = time.time() - start_time
            http_request_duration.labels(
                method='POST',
                endpoint='/api/chat'
            ).observe(duration)
    return wrapper

def track_agent_call(tool_name: str):
    """Decorator to track agent tool calls"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                agent_calls_total.labels(
                    tool_name=tool_name,
                    status='success'
                ).inc()
                return result
            except Exception as e:
                agent_calls_total.labels(
                    tool_name=tool_name,
                    status='error'
                ).inc()
                raise
            finally:
                duration = time.time() - start_time
                agent_call_duration.labels(tool_name=tool_name).observe(duration)
        return wrapper
    return decorator

def initialize_metrics():
    """Initialize application metrics"""
    app_info.info({
        'version': '1.0.0',
        'name': 'student-behavior-analysis'
    })
