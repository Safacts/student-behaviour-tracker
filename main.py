from fastapi import FastAPI, HTTPException, Header, Request, Response, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
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
    generate_recurring_schedule,
    generate_iit_prep_report,
    analyze_topic_performance,
    analyze_chapter_performance,
    assign_teacher_to_student,
    get_teacher_responsibilities,
    generate_teacher_report
)
from task_manager import task_manager, teacher_assignment_manager
from validators import moderate_validator
from auth import auth
from rate_limiter import rate_limiter
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Authentication dependency
async def verify_auth_token(authorization: str = Header(None), request: Request = None) -> Optional[str]:
    """Verify authentication token from Authorization header"""
    # Rate limiting check
    if request:
        client_ip = request.client.host if request.client else "unknown"
        allowed, rate_info = rate_limiter.is_allowed(client_ip)
        if not allowed:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            raise HTTPException(status_code=429, detail=rate_info)
    
    if not authorization:
        logger.warning("Missing authorization header")
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    if not authorization.startswith("Bearer "):
        logger.warning("Invalid authorization format")
        raise HTTPException(status_code=401, detail="Invalid authorization format. Use: Bearer <token>")
    
    token = authorization.split(" ")[1]
    user_info = auth.validate_token(token)
    
    if not user_info:
        logger.warning(f"Invalid or expired token: {token[:10]}...")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user_info["user_id"]

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

# IIT Prep Endpoints

@app.get("/api/iit-prep/report/{student_id}")
def get_iit_prep_report(student_id: str):
    """Generate IIT preparation report"""
    try:
        report = generate_iit_prep_report(student_id)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"IIT prep report generation failed: {str(e)}")

# Topic/Chapter Analysis Endpoints

@app.get("/api/analysis/topic/{student_id}")
def get_topic_analysis(student_id: str):
    """Analyze student performance by topic"""
    try:
        analysis = analyze_topic_performance(student_id)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Topic analysis failed: {str(e)}")

@app.get("/api/analysis/chapter/{student_id}")
def get_chapter_analysis(student_id: str):
    """Analyze student performance by chapter"""
    try:
        analysis = analyze_chapter_performance(student_id)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chapter analysis failed: {str(e)}")

# PDF Download Endpoints

@app.get("/api/download/pdf/{student_id}")
def download_pdf_report(student_id: str):
    """Generate and download PDF report"""
    try:
        from datetime import datetime
        import os
        
        # Get report content
        report_content = generate_pdf_report_content(student_id)
        
        if "error" in report_content:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Create PDF
        filename = f"report_{student_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        filepath = os.path.join(os.getcwd(), filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add title
        title = Paragraph(f"Student Report - {student_id}", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Add content sections
        for section_name, section_data in report_content.get('pdf_content', {}).items():
            if isinstance(section_data, dict):
                section_title = Paragraph(section_name.replace('_', ' ').title(), styles['Heading2'])
                story.append(section_title)
                
                for key, value in section_data.items():
                    text = Paragraph(f"{key}: {value}", styles['Normal'])
                    story.append(text)
                story.append(Spacer(1, 12))
        
        doc.build(story)
        
        # Return file
        return FileResponse(filepath, filename=filename, media_type='application/pdf')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

# Teacher Responsibility Endpoints

@app.get("/api/teacher/assign")
def assign_teacher(student_id: str, teacher_id: str, subject: str):
    """Assign teacher to student for a specific subject"""
    try:
        assignment = assign_teacher_to_student(student_id, teacher_id, subject)
        return assignment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Teacher assignment failed: {str(e)}")

@app.get("/api/teacher/responsibilities/{teacher_id}")
def get_teacher_resp(teacher_id: str):
    """Get all responsibilities for a teacher"""
    try:
        responsibilities = get_teacher_responsibilities(teacher_id)
        return responsibilities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get responsibilities: {str(e)}")

@app.get("/api/teacher/report/{teacher_id}")
def get_teacher_report(teacher_id: str):
    """Generate comprehensive teacher report"""
    try:
        report = generate_teacher_report(teacher_id)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Teacher report generation failed: {str(e)}")

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

# V2 Database-backed Task Management Endpoints

@app.get("/api/v2/tasks/create/intervention")
async def create_intervention_v2(student_id: str, priority: str = "medium", assigned_to: str = None, current_user: str = Depends(verify_auth_token), request: Request = None):
    """Create an intervention task (database-backed)"""
    try:
        logger.info(f"User {current_user} creating intervention task for student {student_id}")
        # Validate inputs
        valid, error = moderate_validator.validate_student_id(student_id)
        if not valid:
            logger.warning(f"Invalid student ID: {student_id} - {error}")
            raise HTTPException(status_code=400, detail=f"Invalid student ID: {error}")
        
        if priority not in ["low", "medium", "high", "critical"]:
            logger.warning(f"Invalid priority: {priority}")
            raise HTTPException(status_code=400, detail="Invalid priority. Must be: low, medium, high, or critical")
        
        task = task_manager.create_intervention_task(student_id, priority, assigned_to=assigned_to)
        
        # Handle database errors
        if "error" in task:
            logger.error(f"Database error: {task['error']}")
            if "already exists" in task.get("error", "").lower():
                raise HTTPException(status_code=409, detail=task["error"])
            raise HTTPException(status_code=500, detail=task["error"])
        
        logger.info(f"Successfully created intervention task {task.get('task_id')}")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Task creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Task creation failed: {str(e)}")

@app.get("/api/v2/tasks/create/monitoring")
async def create_monitoring_v2(student_id: str, assigned_to: str, monitoring_period_days: int = 30, current_user: str = Depends(verify_auth_token), request: Request = None):
    """Create a monitoring task (database-backed)"""
    try:
        logger.info(f"User {current_user} creating monitoring task for student {student_id}")
        # Validate inputs
        valid, error = moderate_validator.validate_student_id(student_id)
        if not valid:
            logger.warning(f"Invalid student ID: {student_id} - {error}")
            raise HTTPException(status_code=400, detail=f"Invalid student ID: {error}")
        
        if not assigned_to:
            logger.warning("assigned_to parameter is required")
            raise HTTPException(status_code=400, detail="assigned_to parameter is required")
        
        if monitoring_period_days < 1 or monitoring_period_days > 365:
            logger.warning(f"Invalid monitoring period: {monitoring_period_days}")
            raise HTTPException(status_code=400, detail="Monitoring period must be between 1 and 365 days")
        
        task = task_manager.create_monitoring_task(student_id, assigned_to, monitoring_period_days)
        
        # Handle database errors
        if "error" in task:
            logger.error(f"Database error: {task['error']}")
            if "already exists" in task.get("error", "").lower():
                raise HTTPException(status_code=409, detail=task["error"])
            raise HTTPException(status_code=500, detail=task["error"])
        
        logger.info(f"Successfully created monitoring task {task.get('task_id')}")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Task creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Task creation failed: {str(e)}")

@app.get("/api/v2/tasks/complete/{task_id}")
async def complete_task_v2(task_id: str, completed_by: str, notes: str = None, current_user: str = Depends(verify_auth_token), request: Request = None):
    """Mark a task as completed (database-backed)"""
    try:
        logger.info(f"User {current_user} marking task {task_id} as completed by {completed_by}")
        
        if not task_id:
            logger.warning("Task ID is required")
            raise HTTPException(status_code=400, detail="Task ID is required")
        
        if not completed_by:
            logger.warning("completed_by parameter is required")
            raise HTTPException(status_code=400, detail="completed_by parameter is required")
        
        result = task_manager.update_task_status(task_id, "completed", notes, completed_by)
        
        # Handle database errors
        if "error" in result:
            logger.error(f"Database error: {result['error']}")
            if "not found" in result.get("error", "").lower():
                raise HTTPException(status_code=404, detail=result["error"])
            raise HTTPException(status_code=500, detail=result["error"])
        
        logger.info(f"Successfully completed task {task_id}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Task completion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Task completion failed: {str(e)}")

@app.get("/api/v2/tasks/assigned/{assigned_to}")
async def get_tasks_for_user_v2(assigned_to: str, current_user: str = Depends(verify_auth_token), request: Request = None):
    """Get all tasks assigned to a user (database-backed)"""
    try:
        logger.info(f"User {current_user} getting tasks assigned to {assigned_to}")
        
        if not assigned_to:
            logger.warning("assigned_to parameter is required")
            raise HTTPException(status_code=400, detail="assigned_to parameter is required")
        
        tasks = task_manager.get_assigned_tasks(assigned_to)
        
        # Handle database errors
        if "error" in tasks:
            logger.error(f"Database error: {tasks['error']}")
            raise HTTPException(status_code=500, detail=tasks["error"])
        
        logger.info(f"Found {tasks.get('task_count', 0)} tasks")
        return tasks
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get tasks: {str(e)}")

@app.get("/api/v2/tasks/student/{student_id}")
async def get_tasks_for_student_v2(student_id: str, current_user: str = Depends(verify_auth_token), request: Request = None):
    """Get all tasks for a student (database-backed)"""
    try:
        logger.info(f"User {current_user} getting tasks for student {student_id}")
        
        if not student_id:
            logger.warning("Student ID is required")
            raise HTTPException(status_code=400, detail="Student ID is required")
        
        valid, error = moderate_validator.validate_student_id(student_id)
        if not valid:
            logger.warning(f"Invalid student ID: {student_id} - {error}")
            raise HTTPException(status_code=400, detail=f"Invalid student ID: {error}")
        
        tasks = task_manager.get_student_tasks(student_id)
        
        # Handle database errors
        if "error" in tasks:
            logger.error(f"Database error: {tasks['error']}")
            raise HTTPException(status_code=500, detail=tasks["error"])
        
        logger.info(f"Found {tasks.get('task_count', 0)} tasks")
        return tasks
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get student tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get student tasks: {str(e)}")

@app.get("/api/v2/tasks/overdue")
async def get_overdue_tasks_list_v2(current_user: str = Depends(verify_auth_token), request: Request = None):
    """Get all overdue tasks (database-backed)"""
    try:
        logger.info(f"User {current_user} getting overdue tasks")
        tasks = task_manager.get_overdue_tasks()
        
        # Handle database errors
        if "error" in tasks:
            logger.error(f"Database error: {tasks['error']}")
            raise HTTPException(status_code=500, detail=tasks["error"])
        
        logger.info(f"Found {tasks.get('total_overdue', 0)} overdue tasks")
        return tasks
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get overdue tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get overdue tasks: {str(e)}")

# V2 Teacher Assignment Endpoints

@app.get("/api/v2/teacher/assign")
async def assign_teacher_v2(student_id: str, teacher_id: str, subject: str, assigned_by: str = "system", current_user: str = Depends(verify_auth_token), request: Request = None):
    """Assign teacher to student (database-backed)"""
    try:
        logger.info(f"User {current_user} assigning teacher {teacher_id} to student {student_id} for {subject}")
        # Validate inputs
        valid, error = moderate_validator.validate_student_id(student_id)
        if not valid:
            logger.warning(f"Invalid student ID: {student_id} - {error}")
            raise HTTPException(status_code=400, detail=f"Invalid student ID: {error}")
        
        if not teacher_id:
            logger.warning("Teacher ID is required")
            raise HTTPException(status_code=400, detail="Teacher ID is required")
        
        if not subject:
            logger.warning("Subject is required")
            raise HTTPException(status_code=400, detail="Subject is required")
        
        assignment = teacher_assignment_manager.assign_teacher_to_student(student_id, teacher_id, subject, assigned_by)
        
        # Handle database errors
        if "error" in assignment:
            logger.error(f"Database error: {assignment['error']}")
            if "already exists" in assignment.get("error", "").lower():
                raise HTTPException(status_code=409, detail=assignment["error"])
            raise HTTPException(status_code=500, detail=assignment["error"])
        
        logger.info(f"Successfully assigned teacher {teacher_id} to student {student_id}")
        return assignment
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Teacher assignment failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Teacher assignment failed: {str(e)}")

@app.get("/api/v2/teacher/responsibilities/{teacher_id}")
async def get_teacher_resp_v2(teacher_id: str, current_user: str = Depends(verify_auth_token), request: Request = None):
    """Get all responsibilities for a teacher (database-backed)"""
    try:
        logger.info(f"User {current_user} getting responsibilities for teacher {teacher_id}")
        
        if not teacher_id:
            logger.warning("Teacher ID is required")
            raise HTTPException(status_code=400, detail="Teacher ID is required")
        
        responsibilities = teacher_assignment_manager.get_teacher_responsibilities(teacher_id)
        
        # Handle database errors
        if "error" in responsibilities:
            logger.error(f"Database error: {responsibilities['error']}")
            raise HTTPException(status_code=500, detail=responsibilities["error"])
        
        logger.info(f"Found {responsibilities.get('total_responsibilities', 0)} responsibilities")
        return responsibilities
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get responsibilities: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get responsibilities: {str(e)}")

# Authentication Endpoints

@app.get("/api/auth/token")
def generate_token(user_id: str):
    """Generate an authentication token for testing (in production, use proper login)"""
    try:
        logger.info(f"Generating token for user {user_id}")
        token = auth.generate_token(user_id)
        return {
            "success": True,
            "user_id": user_id,
            "token": token,
            "message": "Use this token in Authorization header as: Bearer <token>"
        }
    except Exception as e:
        logger.error(f"Token generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Token generation failed: {str(e)}")

@app.get("/api/auth/stats")
def get_auth_stats():
    """Get authentication system statistics"""
    try:
        stats = auth.get_user_stats()
        return stats
    except Exception as e:
        logger.error(f"Failed to get auth stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get auth stats: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
