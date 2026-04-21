from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import uvicorn
import time
import traceback
from typing import Dict, Any

from analyzer import analyze_student
from llm_service import generate_parent_report
from agents import (
    analyze_student_behavior,
    create_learning_path,
    suggest_intervention,
    identify_at_risk_students,
    get_class_overview,
    TOOL_SCHEMA
)

app = FastAPI(title="Student Behavior Analysis PoC")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/students")
def get_students():
    """Get all students"""
    try:
        conn = sqlite3.connect('behavior.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT student_id, student_name FROM student_activity")
        students = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        conn.close()
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve students")

@app.get("/api/activity-logs")
def get_activity_logs():
    """Get all activity logs"""
    try:
        conn = sqlite3.connect('behavior.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student_activity ORDER BY date DESC, id DESC")
        columns = [column[0] for column in cursor.description]
        logs = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve activity logs")

@app.get("/api/report/{student_id}")
def get_report(student_id: str):
    """Generate comprehensive student report"""
    try:
        analysis = analyze_student(student_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Student not found")
        
        conn = sqlite3.connect('behavior.db')
        cursor = conn.cursor()
        cursor.execute("SELECT student_name FROM student_activity WHERE student_id = ? LIMIT 1", (student_id,))
        name_row = cursor.fetchone()
        conn.close()
        
        student_name = name_row[0] if name_row else "Unknown"
        analysis["student_name"] = student_name

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
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

# Agent endpoints - now fully functional

@app.get("/api/agents")
def list_agents():
    """List all available agents"""
    return {
        "agents": [
            {
                "name": "Behavior Analysis Agent",
                "description": "Analyzes behavioral patterns and identifies at-risk students",
                "endpoint": "/api/agents/behavior/{student_id}",
                "capabilities": ["Behavior pattern analysis", "Risk factor identification", "Confidence scoring"]
            },
            {
                "name": "Learning Path Agent",
                "description": "Creates personalized learning paths and recommendations",
                "endpoint": "/api/agents/learning-path/{student_id}",
                "capabilities": ["Learning path creation", "Milestone generation", "Resource identification"]
            },
            {
                "name": "Intervention Agent",
                "description": "Recommends targeted interventions for at-risk students",
                "endpoint": "/api/agents/intervention/{student_id}",
                "capabilities": ["Intervention strategies", "Urgency assessment", "Success metrics definition"]
            }
        ]
    }

@app.get("/api/agents/behavior/{student_id}")
def behavior_analysis_agent(student_id: str):
    """Behavior Analysis Agent - Deep behavioral pattern analysis"""
    try:
        analysis = analyze_student_behavior(student_id)
        return {
            "agent": "Behavior Analysis Agent",
            "student_id": student_id,
            "analysis": analysis,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Behavior analysis failed: {str(e)}")

@app.get("/api/agents/learning-path/{student_id}")
def learning_path_agent(student_id: str):
    """Learning Path Agent - Creates personalized learning paths"""
    try:
        learning_path = create_learning_path(student_id)
        return {
            "agent": "Learning Path Agent",
            "student_id": student_id,
            "learning_path": learning_path,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Learning path creation failed: {str(e)}")

@app.get("/api/agents/intervention/{student_id}")
def intervention_agent(student_id: str):
    """Intervention Agent - Recommends targeted interventions"""
    try:
        intervention = suggest_intervention(student_id)
        return {
            "agent": "Intervention Agent",
            "student_id": student_id,
            "intervention": intervention,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Intervention suggestion failed: {str(e)}")

@app.get("/api/agents/class-overview")
def class_overview_agent():
    """Class Overview Agent - Provides class-wide analysis"""
    try:
        overview = get_class_overview()
        return {
            "agent": "Class Overview Agent",
            "overview": overview,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Class overview failed: {str(e)}")

@app.get("/api/agents/at-risk")
def at_risk_agent(threshold_marks: float = 50.0, threshold_distraction: float = 6.0):
    """At-Risk Students Agent - Identifies students needing intervention"""
    try:
        at_risk = identify_at_risk_students(threshold_marks, threshold_distraction)
        return {
            "agent": "At-Risk Students Agent",
            "thresholds": {
                "marks": threshold_marks,
                "distraction": threshold_distraction
            },
            "at_risk_students": at_risk,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"At-risk identification failed: {str(e)}")

@app.get("/api/agents/tools")
def get_agent_tools():
    """Get tool schema for agentic AI integration"""
    return TOOL_SCHEMA

# Serve the index.html
@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/dashboard")
def read_dashboard():
    return FileResponse("dashboard.html")

@app.get("/dashboard.html")
def read_dashboard_html():
    return FileResponse("dashboard.html")

@app.get("/monitor")
def read_monitor():
    return FileResponse("monitor.html")

@app.get("/monitor.html")
def read_monitor_html():
    return FileResponse("monitor.html")

@app.get("/agents")
def read_agents():
    return FileResponse("agents.html")

@app.get("/docs")
def read_docs():
    return FileResponse("docs.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
