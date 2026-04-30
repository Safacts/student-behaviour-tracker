"""Monitoring utilities"""
from prometheus_client import Counter, Histogram, Gauge, Info

# Initialize metrics
api_requests_total = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint'])
api_request_duration = Histogram('api_request_duration_seconds', 'API request duration')
active_users = Gauge('active_users', 'Number of active users')
app_info = Info('app_info', 'Application information')

def initialize_metrics():
    """Initialize application metrics"""
    app_info.info({
        'version': '2.0.0',
        'name': 'student-behavior-analytics'
    })
