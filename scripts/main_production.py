"""
Production main application that bridges existing PoC with new microservice architecture.
"""
import os
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import sqlite3
import uvicorn

# Import existing components
from analyzer import analyze_student
from llm_service import generate_parent_report

# Import new production components
try:
    from src.core.config import settings
    from src.core.logging import setup_logging, get_logger
    from src.api.main import app as production_app
    PRODUCTION_MODE = True
except ImportError as e:
    print(f"Production components not available: {e}")
    PRODUCTION_MODE = False

# Setup logging if available
if PRODUCTION_MODE:
    setup_logging()
    logger = get_logger(__name__)
else:
    import logging
    logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Student Behavior Analysis - Hybrid Mode")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include production routes if available
if PRODUCTION_MODE:
    try:
        # Mount production app under /api/v2
        app.mount("/api/v2", production_app)
        logger.info("Production API mounted at /api/v2")
    except Exception as e:
        logger.error(f"Failed to mount production API: {e}")

# Legacy endpoints for backward compatibility
@app.get("/api/students")
def get_students():
    """Legacy endpoint - get students list."""
    try:
        conn = sqlite3.connect('behavior.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT student_id, student_name FROM student_activity")
        students = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        conn.close()
        return students
    except Exception as e:
        logger.error(f"Error getting students: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve students")

@app.get("/api/activity-logs")
def get_activity_logs():
    """Legacy endpoint - get activity logs."""
    try:
        conn = sqlite3.connect('behavior.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student_activity ORDER BY date DESC, id DESC")
        columns = [column[0] for column in cursor.description]
        logs = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return logs
    except Exception as e:
        logger.error(f"Error getting activity logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve activity logs")

@app.get("/api/report/{student_id}")
def get_report(student_id: str):
    """Legacy endpoint - get student report."""
    try:
        # Run Analysis
        analysis = analyze_student(student_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Get student name for the report
        conn = sqlite3.connect('behavior.db')
        cursor = conn.cursor()
        cursor.execute("SELECT student_name FROM student_activity WHERE student_id = ? LIMIT 1", (student_id,))
        name_row = cursor.fetchone()
        conn.close()
        
        student_name = name_row[0] if name_row else "Unknown"
        analysis["student_name"] = student_name

        # Call LLM for empathetic report
        ai_report = generate_parent_report(analysis, analysis["behavioral_tag"])
        
        return {
            "student_id": student_id,
            "student_name": student_name,
            "stats": {
                "total_time": analysis["total_study_time"],
                "avg_distraction": analysis["avg_distraction"],
                "avg_marks": analysis["avg_marks"]
            },
            "analysis": {
                "tag": analysis["behavioral_tag"]
            },
            "ai_recommendation": ai_report
        }
    except Exception as e:
        logger.error(f"Error generating report for {student_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate report")

# New hybrid endpoints
@app.get("/api/hybrid/summary")
def get_hybrid_summary():
    """Get summary of both legacy and production systems."""
    return {
        "legacy_available": True,
        "production_available": PRODUCTION_MODE,
        "endpoints": {
            "legacy": {
                "students": "/api/students",
                "activity_logs": "/api/activity-logs",
                "report": "/api/report/{student_id}"
            },
            "production": {
                "analytics": "/api/v2/analytics",
                "agents": "/api/v2/agents",
                "students": "/api/v2/students",
                "health": "/api/v2/health"
            } if PRODUCTION_MODE else None
        }
    }

# Serve the index.html
@app.get("/")
def read_root():
    """Serve the frontend dashboard."""
    return FileResponse("index.html")

# Health check
@app.get("/health")
def health_check():
    """Simple health check."""
    return {
        "status": "healthy",
        "mode": "hybrid",
        "production_available": PRODUCTION_MODE,
        "legacy_available": True
    }

if __name__ == "__main__":
    # Determine configuration
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info(f"Starting Student Behavior Analysis in hybrid mode")
    logger.info(f"Host: {host}, Port: {port}, Debug: {debug}")
    logger.info(f"Production mode: {PRODUCTION_MODE}")
    
    uvicorn.run(
        app, 
        host=host, 
        port=port, 
        reload=debug,
        log_level="debug" if debug else "info"
    )
