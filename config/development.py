"""
Development environment configuration.
"""
from ..core.config import Settings

class DevelopmentSettings(Settings):
    """Development-specific settings."""
    
    environment: str = "development"
    debug: bool = True
    
    # Database - use SQLite for development
    database_url: str = "sqlite:///./data/student_behavior.db"
    
    # Redis - optional for development
    redis_url: str = "redis://localhost:6379/0"
    enable_caching: bool = False
    
    # API settings
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    api_workers: int = 1
    
    # Logging
    log_level: str = "DEBUG"
    log_format: str = "console"
    log_file: str = None
    
    # AI/ML
    langchain_verbose: bool = True
    langchain_debug: bool = True
    
    # CORS - allow all origins in development
    cors_origins: list = ["*"]
    cors_methods: list = ["*"]
    cors_headers: list = ["*"]
    
    # Rate limiting - more permissive in development
    rate_limit_requests: int = 1000
    rate_limit_window: int = 60
    
    # Monitoring - disabled in development
    enable_metrics: bool = False
    enable_tracing: bool = False
