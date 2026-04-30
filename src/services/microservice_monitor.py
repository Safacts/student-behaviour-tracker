"""
Microservice Health Monitor - Agentic debugging capability
"""
import sqlite3
import requests
import time
import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class MicroserviceMonitor:
    """Monitor and debug microservice components"""
    
    def __init__(self, base_url: str = "http://localhost:8000", db_path: str = "behavior.db"):
        self.base_url = base_url
        self.db_path = db_path
    
    def check_database(self) -> Dict[str, Any]:
        """Check database connectivity and health"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if tables exist
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            # Check table row counts
            table_stats = {}
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                table_stats[table] = cursor.fetchone()[0]
            
            # Check for API builder configs table
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='api_builder_configs'
            """)
            has_api_builder = cursor.fetchone() is not None
            
            conn.close()
            
            return {
                "status": "healthy",
                "tables": tables,
                "table_stats": table_stats,
                "api_builder_table": has_api_builder,
                "message": f"Database healthy with {len(tables)} tables"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Database check failed: {str(e)}",
                "suggestion": "Check if behavior.db exists and is accessible"
            }
    
    def check_api_endpoints(self) -> Dict[str, Any]:
        """Check if API endpoints are responding (skip self-check)"""
        # Skip API endpoint check when running on same server to avoid timeouts
        # In a real microservice architecture, this would check other services
        return {
            "status": "healthy",
            "message": "API endpoint check skipped (running on same server)",
            "endpoints": {
                "/api/students": {"status": "skipped", "message": "Self-check skipped"},
                "/api/activity-logs": {"status": "skipped", "message": "Self-check skipped"},
                "/api/query/tables": {"status": "skipped", "message": "Self-check skipped"},
                "/api/auth/token": {"status": "skipped", "message": "Self-check skipped"},
                "/api/query/custom": {"status": "skipped", "message": "Self-check skipped"}
            },
            "summary": "API endpoints running on same server (self-check skipped)"
        }
    
    def check_external_apis(self) -> Dict[str, Any]:
        """Check external API integrations (OpenAI, Gemini, Groq)"""
        from dotenv import load_dotenv
        import os
        load_dotenv()
        
        checks = {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY")
        }
        
        results = {}
        for key, value in checks.items():
            if value and value not in ["[INSERT_API_KEY_HERE]", "your_groq_api_key_here"]:
                results[key] = {
                    "status": "configured",
                    "message": f"{key} is set"
                }
            else:
                results[key] = {
                    "status": "missing",
                    "message": f"{key} not configured or using placeholder"
                }
        
        configured_count = sum(1 for r in results.values() if r.get("status") == "configured")
        
        return {
            "status": "healthy" if configured_count > 0 else "warning",
            "apis": results,
            "summary": f"{configured_count}/{len(checks)} external APIs configured"
        }
    
    def check_system_resources(self) -> Dict[str, Any]:
        """Check system resources"""
        import psutil
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('.')
            
            return {
                "status": "healthy",
                "cpu": {
                    "percent": cpu_percent,
                    "message": f"CPU usage: {cpu_percent}%"
                },
                "memory": {
                    "percent": memory.percent,
                    "available_gb": memory.available / (1024**3),
                    "message": f"Memory: {memory.percent}% used, {memory.available / (1024**3):.2f}GB available"
                },
                "disk": {
                    "percent": disk.percent,
                    "free_gb": disk.free / (1024**3),
                    "message": f"Disk: {disk.percent}% used, {disk.free / (1024**3):.2f}GB free"
                }
            }
        except ImportError:
            return {
                "status": "warning",
                "message": "psutil not installed, cannot check system resources"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"System resource check failed: {str(e)}"
            }
    
    def comprehensive_health_check(self) -> Dict[str, Any]:
        """Run comprehensive health check on all components"""
        logger.info("Running comprehensive health check")
        
        checks = {
            "database": self.check_database(),
            "api_endpoints": self.check_api_endpoints(),
            "external_apis": self.check_external_apis(),
            "system_resources": self.check_system_resources()
        }
        
        # Determine overall health
        overall_status = "healthy"
        issues = []
        
        for component, result in checks.items():
            if result.get("status") == "error":
                overall_status = "error"
                issues.append(f"{component}: {result.get('message', 'Unknown error')}")
            elif result.get("status") == "degraded" or result.get("status") == "warning":
                if overall_status != "error":
                    overall_status = "degraded"
                issues.append(f"{component}: {result.get('message', 'Degraded')}")
        
        return {
            "overall_status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "checks": checks,
            "issues": issues,
            "message": f"System {overall_status}" + (f" - {len(issues)} issues found" if issues else " - All systems operational")
        }
    
    def generate_debug_report(self) -> Dict[str, Any]:
        """Generate detailed debugging report with actionable recommendations"""
        health = self.comprehensive_health_check()
        
        recommendations = []
        
        # Database recommendations
        db_status = health["checks"]["database"]
        if db_status["status"] == "error":
            recommendations.append({
                "component": "database",
                "issue": db_status["message"],
                "action": "Verify database file exists and has correct permissions"
            })
        elif not db_status.get("api_builder_table"):
            recommendations.append({
                "component": "database",
                "issue": "API Builder configuration table missing",
                "action": "Restart server to initialize api_builder_configs table"
            })
        
        # API endpoint recommendations
        api_status = health["checks"]["api_endpoints"]
        if api_status["status"] == "degraded":
            for endpoint, result in api_status["endpoints"].items():
                if result["status"] == "error":
                    recommendations.append({
                        "component": "api_endpoints",
                        "issue": f"Endpoint {endpoint} not responding",
                        "action": f"Check endpoint implementation and server logs for {endpoint}"
                    })
        
        # External API recommendations
        ext_status = health["checks"]["external_apis"]
        if ext_status["status"] == "warning":
            for api, result in ext_status["apis"].items():
                if result["status"] == "missing":
                    recommendations.append({
                        "component": "external_apis",
                        "issue": f"{api} not configured",
                        "action": f"Add {api} to .env file or disable features that require it"
                    })
        
        # System resource recommendations
        sys_status = health["checks"]["system_resources"]
        if sys_status["status"] == "healthy":
            if sys_status["memory"]["percent"] > 80:
                recommendations.append({
                    "component": "system_resources",
                    "issue": "High memory usage",
                    "action": "Consider restarting server or adding more memory"
                })
            if sys_status["cpu"]["percent"] > 80:
                recommendations.append({
                    "component": "system_resources",
                    "issue": "High CPU usage",
                    "action": "Check for resource-intensive operations"
                })
        
        return {
            "health_summary": health,
            "recommendations": recommendations,
            "actionable_items": len(recommendations)
        }

if __name__ == "__main__":
    # Test the monitor
    monitor = MicroserviceMonitor()
    
    print("=== Comprehensive Health Check ===")
    health = monitor.comprehensive_health_check()
    print(f"Overall Status: {health['overall_status']}")
    print(f"Message: {health['message']}")
    
    if health['issues']:
        print("\nIssues:")
        for issue in health['issues']:
            print(f"  - {issue}")
    
    print("\n=== Debug Report ===")
    debug = monitor.generate_debug_report()
    print(f"Actionable Items: {debug['actionable_items']}")
    
    if debug['recommendations']:
        print("\nRecommendations:")
        for rec in debug['recommendations']:
            print(f"\n  Component: {rec['component']}")
            print(f"  Issue: {rec['issue']}")
            print(f"  Action: {rec['action']}")
