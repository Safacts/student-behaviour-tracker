"""
Simple, self-contained logging system for production-grade logging
"""
import logging
import sys
from datetime import datetime
from pathlib import Path
import json
from typing import Dict, Any, Optional

class SimpleLogger:
    """Production-ready logger without external dependencies"""
    
    def __init__(self, name: str, log_level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(
            log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        if extra:
            self.logger.info(f"{message} | {json.dumps(extra)}")
        else:
            self.logger.info(message)
    
    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        if extra:
            self.logger.warning(f"{message} | {json.dumps(extra)}")
        else:
            self.logger.warning(message)
    
    def error(self, message: str, extra: Optional[Dict[str, Any]] = None, exception: Optional[Exception] = None):
        if extra:
            error_data = {"error_details": extra}
            if exception:
                error_data["exception"] = str(exception)
            self.logger.error(f"{message} | {json.dumps(error_data)}")
        else:
            if exception:
                self.logger.error(f"{message} | Exception: {str(exception)}")
            else:
                self.logger.error(message)
    
    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        if extra:
            self.logger.debug(f"{message} | {json.dumps(extra)}")
        else:
            self.logger.debug(message)
    
    def api_request(self, method: str, endpoint: str, status_code: int = None, 
                   response_time: float = None, user_id: str = None, error: str = None):
        log_data = {
            "method": method,
            "endpoint": endpoint,
            "status_code": status_code,
            "response_time_ms": response_time * 1000 if response_time else None,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
        
        if error:
            log_data["error"] = error
            self.error(f"API Request Failed: {method} {endpoint}", log_data)
        else:
            self.info(f"API Request: {method} {endpoint}", log_data)
    
    def agent_execution(self, agent_name: str, student_id: str, execution_time: float = None,
                     success: bool = True, error: str = None):
        log_data = {
            "agent": agent_name,
            "student_id": student_id,
            "execution_time_ms": execution_time * 1000 if execution_time else None,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        
        if error:
            log_data["error"] = error
            self.error(f"Agent Execution Failed: {agent_name}", log_data)
        else:
            self.info(f"Agent Execution: {agent_name}", log_data)

# Initialize loggers
main_logger = SimpleLogger("main", "INFO")
api_logger = SimpleLogger("api", "INFO")
agent_logger = SimpleLogger("agents", "INFO")
db_logger = SimpleLogger("database", "INFO")
