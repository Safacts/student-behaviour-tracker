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
    TOOL_SCHEMA,
    generate_llm_agent_report,
    export_student_data_to_csv,
    export_class_data_to_csv,
    generate_student_chart_data,
    generate_class_chart_data,
    generate_report_summary_text,
    generate_parent_email,
    generate_staff_notification,
    create_intervention_task,
    create_monitoring_task,
    update_task_status,
    get_assigned_tasks,
    get_student_tasks,
    get_overdue_tasks,
    generate_pdf_report_content,
    generate_meeting_agenda,
    predict_student_performance,
    detect_anomalies,
    validate_student_data,
    clean_student_data,
    generate_calendar_event,
    generate_recurring_schedule
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
    """Behavior Analysis Agent - Deep behavioral pattern analysis with LLM report"""
    try:
        analysis = analyze_student_behavior(student_id)
        llm_report = generate_llm_agent_report("behavior", analysis)
        
        return {
            "agent": "Behavior Analysis Agent",
            "student_id": student_id,
            "analysis": analysis,
            "llm_report": llm_report,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Behavior analysis failed: {str(e)}")

@app.get("/api/agents/learning-path/{student_id}")
def learning_path_agent(student_id: str):
    """Learning Path Agent - Creates personalized learning paths with LLM report"""
    try:
        learning_path = create_learning_path(student_id)
        llm_report = generate_llm_agent_report("learning_path", learning_path)
        
        return {
            "agent": "Learning Path Agent",
            "student_id": student_id,
            "learning_path": learning_path,
            "llm_report": llm_report,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Learning path creation failed: {str(e)}")

@app.get("/api/agents/intervention/{student_id}")
def intervention_agent(student_id: str):
    """Intervention Agent - Recommends targeted interventions with LLM report"""
    try:
        intervention = suggest_intervention(student_id)
        llm_report = generate_llm_agent_report("intervention", intervention)
        
        return {
            "agent": "Intervention Agent",
            "student_id": student_id,
            "intervention": intervention,
            "llm_report": llm_report,
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

# Export and Visualization Endpoints

@app.get("/api/export/student/{student_id}/csv")
def export_student_csv(student_id: str):
    """Export student data to CSV"""
    try:
        csv_result = export_student_data_to_csv(student_id)
        return csv_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV export failed: {str(e)}")

@app.get("/api/export/class/csv")
def export_class_csv():
    """Export all class data to CSV"""
    try:
        csv_result = export_class_data_to_csv()
        return csv_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV export failed: {str(e)}")

@app.get("/api/charts/student/{student_id}")
def get_student_chart(student_id: str, chart_type: str = "performance"):
    """Get student chart data"""
    try:
        chart_data = generate_student_chart_data(student_id, chart_type)
        return chart_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chart generation failed: {str(e)}")

@app.get("/api/charts/class")
def get_class_chart(chart_type: str = "comparison"):
    """Get class chart data"""
    try:
        chart_data = generate_class_chart_data(chart_type)
        return chart_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chart generation failed: {str(e)}")

@app.get("/api/report/summary/{student_id}")
def get_report_summary(student_id: str):
    """Get comprehensive text report summary"""
    try:
        summary = generate_report_summary_text(student_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

# Communication Endpoints

@app.get("/api/communication/parent-email/{student_id}")
def get_parent_email(student_id: str, email_type: str = "report"):
    """Generate email content for parent communication"""
    try:
        email_content = generate_parent_email(student_id, email_type)
        return email_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email generation failed: {str(e)}")

@app.get("/api/communication/staff-notification/{student_id}")
def get_staff_notification(student_id: str, notification_type: str = "intervention"):
    """Generate notification content for staff/teachers"""
    try:
        notification = generate_staff_notification(student_id, notification_type)
        return notification
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Notification generation failed: {str(e)}")

# Task Management Endpoints

@app.post("/api/tasks/intervention")
def create_intervention_task_endpoint(student_id: str, assigned_to: str, due_date: str = None):
    """Create intervention task"""
    try:
        task = create_intervention_task(student_id, assigned_to, due_date)
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task creation failed: {str(e)}")

@app.post("/api/tasks/monitoring")
def create_monitoring_task_endpoint(student_id: str, assigned_to: str, monitoring_period_days: int = 30):
    """Create monitoring task"""
    try:
        task = create_monitoring_task(student_id, assigned_to, monitoring_period_days)
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task creation failed: {str(e)}")

@app.put("/api/tasks/{task_id}/status")
def update_task_status_endpoint(task_id: str, status: str, notes: str = None):
    """Update task status"""
    try:
        updated_task = update_task_status(task_id, status, notes)
        return updated_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task update failed: {str(e)}")

@app.get("/api/tasks/assigned/{assigned_to}")
def get_assigned_tasks_endpoint(assigned_to: str):
    """Get tasks assigned to a person"""
    try:
        tasks = get_assigned_tasks(assigned_to)
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get assigned tasks: {str(e)}")

@app.get("/api/tasks/student/{student_id}")
def get_student_tasks_endpoint(student_id: str):
    """Get tasks for a student"""
    try:
        tasks = get_student_tasks(student_id)
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get student tasks: {str(e)}")

@app.get("/api/tasks/overdue")
def get_overdue_tasks_endpoint():
    """Get overdue tasks"""
    try:
        tasks = get_overdue_tasks()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get overdue tasks: {str(e)}")

# Document Generation Endpoints

@app.get("/api/documents/pdf-report/{student_id}")
def get_pdf_report_content(student_id: str):
    """Generate PDF report content"""
    try:
        pdf_content = generate_pdf_report_content(student_id)
        return pdf_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF report generation failed: {str(e)}")

@app.get("/api/documents/meeting-agenda/{student_id}")
def get_meeting_agenda(student_id: str, meeting_type: str = "parent_teacher"):
    """Generate meeting agenda"""
    try:
        agenda = generate_meeting_agenda(student_id, meeting_type)
        return agenda
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Meeting agenda generation failed: {str(e)}")

# Advanced Analytics Endpoints

@app.get("/api/analytics/predict/{student_id}")
def get_performance_prediction(student_id: str, days_ahead: int = 30):
    """Predict student performance"""
    try:
        prediction = predict_student_performance(student_id, days_ahead)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/api/analytics/anomalies/{student_id}")
def get_anomalies(student_id: str, threshold_std: float = 2.0):
    """Detect anomalies in student data"""
    try:
        anomalies = detect_anomalies(student_id, threshold_std)
        return anomalies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anomaly detection failed: {str(e)}")

# Data Quality Endpoints

@app.get("/api/data-quality/validate/{student_id}")
def validate_data(student_id: str):
    """Validate student data quality"""
    try:
        validation = validate_student_data(student_id)
        return validation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data validation failed: {str(e)}")

@app.get("/api/data-quality/clean/{student_id}")
def clean_data(student_id: str):
    """Clean student data"""
    try:
        cleaning = clean_student_data(student_id)
        return cleaning
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data cleaning failed: {str(e)}")

# Calendar Integration Endpoints

@app.get("/api/calendar/event/{student_id}")
def get_calendar_event(student_id: str, event_type: str = "parent_meeting"):
    """Generate calendar event"""
    try:
        event = generate_calendar_event(student_id, event_type)
        return event
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calendar event generation failed: {str(e)}")

@app.get("/api/calendar/schedule/{student_id}")
def get_recurring_schedule(student_id: str, frequency: str = "weekly"):
    """Generate recurring schedule"""
    try:
        schedule = generate_recurring_schedule(student_id, frequency)
        return schedule
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Schedule generation failed: {str(e)}")

@app.get("/api/agents/comprehensive/{student_id}")
def comprehensive_agent(student_id: str):
    """Comprehensive Agent - Runs all agents with LLM reports and combines results"""
    try:
        # Get analysis from all agents
        behavior_analysis = analyze_student_behavior(student_id)
        learning_path = create_learning_path(student_id)
        intervention = suggest_intervention(student_id)
        
        # Generate LLM reports for each agent
        behavior_llm_report = generate_llm_agent_report("behavior", behavior_analysis)
        learning_llm_report = generate_llm_agent_report("learning_path", learning_path)
        intervention_llm_report = generate_llm_agent_report("intervention", intervention)
        
        # Generate summary
        behavioral_tag = behavior_analysis.get("behavioral_tag", "Unknown")
        avg_marks = behavior_analysis.get("avg_marks", 0)
        
        # Determine overall risk level
        if behavioral_tag == "High Flight Risk":
            overall_risk = "Critical"
            success_prob = 0.4
        elif behavioral_tag == "Concept Comprehension Issue":
            overall_risk = "High"
            success_prob = 0.6
        else:
            overall_risk = "Low"
            success_prob = 0.8
        
        # Generate recommended actions
        if overall_risk == "Critical":
            recommended_actions = [
                "Immediate intervention required",
                "Daily monitoring needed",
                "Parent meeting scheduled"
            ]
        elif overall_risk == "High":
            recommended_actions = [
                "Weekly check-ins",
                "Additional support resources",
                "Progress tracking"
            ]
        else:
            recommended_actions = [
                "Continue current approach",
                "Monitor for changes",
                "Provide enrichment opportunities"
            ]
        
        return {
            "agent": "Comprehensive Agent",
            "student_id": student_id,
            "comprehensive_analysis": {
                "behavior_analysis": behavior_analysis,
                "learning_path": learning_path,
                "intervention_plan": intervention
            },
            "llm_reports": {
                "behavior_analysis_report": behavior_llm_report,
                "learning_path_report": learning_llm_report,
                "intervention_report": intervention_llm_report
            },
            "summary": {
                "overall_risk_level": overall_risk,
                "success_probability": success_prob,
                "recommended_actions": recommended_actions
            },
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comprehensive analysis failed: {str(e)}")

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
