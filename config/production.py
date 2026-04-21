"""
Production environment configuration.
"""
from ..core.config import Settings

class ProductionSettings(Settings):
    """Production-specific settings."""
    
    environment: str = "production"
    debug: bool = False
    
    # Database - use PostgreSQL for production
    database_url: str = "postgresql://user:password@postgres:5432/student_behavior"
    
    # Redis - enabled for production
    redis_url: str = "redis://redis:6379/0"
    enable_caching: bool = True
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    log_file: str = "./logs/app.log"
    
    # AI/ML
    langchain_verbose: bool = False
    langchain_debug: bool = False
    
    # CORS - restrict origins in production
    cors_origins: list = ["https://client-domain.com"]
    cors_methods: list = ["GET", "POST", "PUT", "DELETE"]
    cors_headers: list = ["Content-Type", "Authorization", "X-Request-ID"]
    
    # Rate limiting - more restrictive in production
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    
    # Monitoring - enabled in production
    enable_metrics: bool = True
    enable_tracing: bool = True
    sampling_rate: float = 0.1
    
    # Security
    secret_key: str = "production-secret-key-change-this"
