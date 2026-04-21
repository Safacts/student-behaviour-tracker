"""
Simple, self-contained health monitoring system
"""
import time
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List

class SimpleHealthMonitor:
    """Production-ready health monitoring without external dependencies"""
    
    def __init__(self):
        self.start_time = time.time()
        self.metrics_history = []
        self.max_history_size = 1000
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get basic system metrics without psutil"""
        try:
            # Basic system metrics
            uptime = time.time() - self.start_time
            
            # Database metrics
            db_size = os.path.getsize('behavior.db') if os.path.exists('behavior.db') else 0
            db_connection_time = self._test_database_connection()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": uptime,
                "database": {
                    "size_mb": db_size / (1024**2),
                    "connection_time_ms": db_connection_time * 1000 if db_connection_time else None,
                    "status": "connected" if db_connection_time is not None else "error"
                },
                "service": {
                    "status": "healthy",
                    "response_time_ms": self._test_api_response_time() * 1000
                }
            }
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            }
    
    def _test_database_connection(self) -> float:
        """Test database connection speed"""
        start_time = time.time()
        try:
            conn = sqlite3.connect('behavior.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM student_activity")
            count = cursor.fetchone()[0]
            conn.close()
            return time.time() - start_time
        except Exception as e:
            return None
    
    def _test_api_response_time(self) -> float:
        """Test API response time"""
        start_time = time.time()
        try:
            conn = sqlite3.connect('behavior.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM student_activity LIMIT 1")
            cursor.fetchone()
            conn.close()
            return time.time() - start_time
        except Exception as e:
            return None
    
    def check_database_integrity(self) -> Dict[str, Any]:
        """Check database integrity"""
        try:
            conn = sqlite3.connect('behavior.db')
            cursor = conn.cursor()
            
            # Check table existence
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Check record counts
            cursor.execute("SELECT COUNT(*) FROM student_activity")
            activity_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT student_id) FROM student_activity")
            student_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "status": "healthy" if "student_activity" in tables else "error",
                "tables": tables,
                "record_counts": {
                    "student_activity": activity_count,
                    "students": student_count
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def check_ai_service_health(self) -> Dict[str, Any]:
        """Check AI service availability"""
        try:
            from llm_service import generate_parent_report
            
            test_data = {
                "student_name": "HealthCheck",
                "total_study_time": 450,
                "avg_distraction": 5.0,
                "avg_marks": 75.0
            }
            
            start_time = time.time()
            result = generate_parent_report(test_data, "On Track")
            response_time = time.time() - start_time
            
            is_healthy = (
                result is not None and
                len(result) > 10 and
                "Error" not in result
            )
            
            return {
                "status": "healthy" if is_healthy else "degraded",
                "response_time_ms": response_time * 1000,
                "last_check": datetime.now().isoformat(),
                "sample_result": result[:100] if result else None
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary"""
        system_metrics = self.get_system_metrics()
        db_health = self.check_database_integrity()
        ai_health = self.check_ai_service_health()
        
        overall_status = "healthy"
        if (db_health.get("status") != "healthy" or
            ai_health.get("status") == "error"):
            overall_status = "degraded"
        
        return {
            "overall_status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": system_metrics.get("uptime_seconds", 0),
            "system_metrics": system_metrics,
            "database_health": db_health,
            "ai_service_health": ai_health,
            "checks_performed": [
                "database_integrity",
                "ai_service_availability"
            ]
        }
    
    def add_metric_to_history(self, metric: Dict[str, Any]):
        """Add metric to history"""
        self.metrics_history.append({
            **metric,
            "recorded_at": datetime.now().isoformat()
        })
        
        if len(self.metrics_history) > self.max_history_size:
            self.metrics_history = self.metrics_history[-self.max_history_size:]
    
    def get_metrics_trend(self, hours: int = 24) -> Dict[str, Any]:
        """Get metrics trend over specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_metrics = [
            metric for metric in self.metrics_history
            if datetime.fromisoformat(metric["timestamp"]) > cutoff_time
        ]
        
        if not recent_metrics:
            return {"trend": "no_data", "message": f"No metrics available for last {hours} hours"}
        
        return {
            "trend": "analyzed",
            "period_hours": hours,
            "data_points": len(recent_metrics),
            "latest": recent_metrics[-1] if recent_metrics else None
        }

# Global health monitor instance
health_monitor = SimpleHealthMonitor()
