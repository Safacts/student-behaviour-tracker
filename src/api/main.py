from fastapi import FastAPI, HTTPException, Header, Request, Response, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import os
import pathlib

class ChatRequest(BaseModel):
    query: str
    use_llm: bool = True
    role: str = "student"

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import uvicorn
import time
import traceback
from typing import Dict, Any, Optional

from src.services.analyzer import analyze_student
from src.services.llm_service import generate_parent_report, generate_query_from_natural_language
from src.services.microservice_monitor import MicroserviceMonitor
from src.services.workflow_engine import WorkflowEngine
from src.agents.agents import (
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
from src.models.task_manager import task_manager, teacher_assignment_manager
from src.core.validators import moderate_validator
from src.core.auth import auth
from src.core.rate_limiter import rate_limiter
from src.agents.agent_orchestrator import conversational_router
from src.services.query_builder import QueryBuilderService
from src.utils.monitoring import initialize_metrics, app_info
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
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

# Mount static files directory
static_dir = pathlib.Path(__file__).parent.parent.parent / "static"
if not static_dir.exists():
    static_dir = pathlib.Path.cwd() / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Initialize QueryBuilderService
query_builder = QueryBuilderService()

# Initialize MicroserviceMonitor
microservice_monitor = MicroserviceMonitor()

# Initialize WorkflowEngine
workflow_engine = WorkflowEngine()

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
        logger.error(f"Failed to retrieve students: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve students: {str(e)}")

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
        logger.error(f"Failed to retrieve activity logs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@app.get("/api/report/weekly")
def weekly_report(start_date: str, end_date: str, student_id: Optional[str] = None):
    """Generate weekly report with flexible date range"""
    try:
        logger.info(f"Generating weekly report from {start_date} to {end_date}, student: {student_id}")
        
        conn = sqlite3.connect('behavior.db')
        cursor = conn.cursor()
        
        if student_id:
            cursor.execute("""
                SELECT student_id, student_name, subject, 
                       SUM(time_spent_mins) as total_time,
                       AVG(marks_achieved_percent) as avg_marks,
                       AVG(distraction_score) as avg_distraction,
                       COUNT(*) as activity_count
                FROM student_activity 
                WHERE date BETWEEN ? AND ? AND student_id = ?
                GROUP BY student_id, subject
                ORDER BY student_id, subject
            """, (start_date, end_date, student_id))
        else:
            cursor.execute("""
                SELECT student_id, student_name, subject,
                       SUM(time_spent_mins) as total_time,
                       AVG(marks_achieved_percent) as avg_marks,
                       AVG(distraction_score) as avg_distraction,
                       COUNT(*) as activity_count
                FROM student_activity 
                WHERE date BETWEEN ? AND ?
                GROUP BY student_id, subject
                ORDER BY student_id, subject
            """, (start_date, end_date))
        
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        
        return {
            "report_type": "weekly",
            "date_range": {"start": start_date, "end": end_date},
            "student_filter": student_id,
            "data": results
        }
    except sqlite3.Error as e:
        logger.error(f"Database error in weekly report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error in weekly report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate weekly report: {str(e)}")

@app.get("/api/report/daily")
def daily_report(date: str, student_id: Optional[str] = None):
    """Generate daily report for specific date"""
    try:
        logger.info(f"Generating daily report for {date}, student: {student_id}")
        
        conn = sqlite3.connect('behavior.db')
        cursor = conn.cursor()
        
        if student_id:
            cursor.execute("""
                SELECT student_id, student_name, activity_type, subject, topic,
                       time_spent_mins, marks_achieved_percent, distraction_score
                FROM student_activity 
                WHERE date = ? AND student_id = ?
                ORDER BY subject, activity_type
            """, (date, student_id))
        else:
            cursor.execute("""
                SELECT student_id, student_name, activity_type, subject, topic,
                       time_spent_mins, marks_achieved_percent, distraction_score
                FROM student_activity 
                WHERE date = ?
                ORDER BY student_id, subject, activity_type
            """, (date,))
        
        columns = [column[0] for column in cursor.description]
        activities = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        
        # Calculate summary
        if activities:
            total_time = sum(a['time_spent_mins'] for a in activities)
            avg_marks = sum(a['marks_achieved_percent'] for a in activities if a['marks_achieved_percent']) / len([a for a in activities if a['marks_achieved_percent']])
            avg_distraction = sum(a['distraction_score'] for a in activities) / len(activities)
        else:
            total_time = 0
            avg_marks = 0
            avg_distraction = 0
        
        return {
            "report_type": "daily",
            "date": date,
            "student_filter": student_id,
            "summary": {
                "total_activities": len(activities),
                "total_time_minutes": total_time,
                "avg_marks_percent": round(avg_marks, 2),
                "avg_distraction_score": round(avg_distraction, 2)
            },
            "activities": activities
        }
    except sqlite3.Error as e:
        logger.error(f"Database error in daily report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error in daily report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate daily report: {str(e)}")

@app.get("/api/report/{student_id}")
def get_report(student_id: str):
    """Generate comprehensive student report"""
    try:
        logger.info(f"Generating report for student {student_id}")
        analysis = analyze_student(student_id)
        if not analysis:
            logger.warning(f"Student {student_id} not found in analysis")
            raise HTTPException(status_code=404, detail="Student not found")
        
        conn = sqlite3.connect('behavior.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student_activity WHERE student_id = ? ORDER BY date DESC", (student_id,))
        columns = [column[0] for column in cursor.description]
        activities = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        
        return {
            "student_id": student_id,
            "analysis": analysis,
            "activities": activities
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

# API Builder endpoints
@app.post("/api/query/custom")
async def custom_query(config: Dict[str, Any], current_user: str = Depends(verify_auth_token)):
    """Execute custom query built via API Builder"""
    try:
        logger.info(f"User {current_user} executing custom query")
        
        results = query_builder.execute_query(config)
        
        return {
            "success": True,
            "data": results,
            "count": len(results)
        }
    except ValueError as e:
        logger.warning(f"Invalid query configuration: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid query configuration: {str(e)}")
    except Exception as e:
        logger.error(f"Custom query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")

@app.get("/api/query/tables")
async def get_allowed_tables(current_user: str = Depends(verify_auth_token)):
    """Get list of allowed tables and their columns for API Builder UI"""
    try:
        return query_builder.ALLOWED_TABLES
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tables: {str(e)}")

@app.post("/api/query/config/save")
async def save_config(request: Dict[str, Any], current_user: str = Depends(verify_auth_token)):
    """Save API Builder configuration"""
    try:
        name = request.get('name')
        config = request.get('config')
        description = request.get('description')
        
        if not name or not config:
            raise HTTPException(status_code=400, detail="name and config are required")
        
        result = query_builder.save_config(name, config, description, created_by=current_user)
        
        if not result.get('success'):
            raise HTTPException(status_code=400, detail=result.get('error'))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to save config: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save config: {str(e)}")

@app.get("/api/query/config/load/{name}")
async def load_config(name: str, current_user: str = Depends(verify_auth_token)):
    """Load API Builder configuration"""
    try:
        result = query_builder.load_config(name)
        
        if not result.get('success'):
            raise HTTPException(status_code=404, detail=result.get('error'))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to load config: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to load config: {str(e)}")

@app.get("/api/query/config/list")
async def list_configs(current_user: str = Depends(verify_auth_token)):
    """List all API Builder configurations"""
    try:
        result = query_builder.list_configs()
        
        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to list configs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list configs: {str(e)}")

@app.delete("/api/query/config/delete/{name}")
async def delete_config(name: str, current_user: str = Depends(verify_auth_token)):
    """Delete API Builder configuration"""
    try:
        result = query_builder.delete_config(name)
        
        if not result.get('success'):
            raise HTTPException(status_code=404, detail=result.get('error'))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete config: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete config: {str(e)}")

# Health Check Endpoints
@app.get("/api/health")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy", "service": "student-behavior-analytics"}

@app.get("/api/health/detailed")
async def detailed_health_check():
    """Comprehensive health check for all system components"""
    try:
        health_report = microservice_monitor.comprehensive_health_check()
        return health_report
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/api/health/debug")
async def debug_report():
    """Generate detailed debugging report with actionable recommendations"""
    try:
        debug_report = microservice_monitor.generate_debug_report()
        return debug_report
    except Exception as e:
        logger.error(f"Debug report generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Debug report generation failed: {str(e)}")

# Workflow Automation Endpoints
@app.post("/api/workflows")
async def create_workflow(request: Dict[str, Any], current_user: str = Depends(verify_auth_token)):
    """Create a new workflow"""
    try:
        from src.services.workflow_engine import Workflow, Node, Edge
        import uuid
        
        workflow_id = str(uuid.uuid4())
        name = request.get("name")
        description = request.get("description", "")
        nodes_data = request.get("nodes", [])
        edges_data = request.get("edges", [])
        
        if not name:
            raise HTTPException(status_code=400, detail="Workflow name is required")
        
        nodes = [
            Node(
                id=n["id"],
                type=n["type"],
                config=n.get("config", {})
            )
            for n in nodes_data
        ]
        
        edges = [
            Edge(
                source=e["source"],
                target=e["target"],
                condition=e.get("condition")
            )
            for e in edges_data
        ]
        
        workflow = Workflow(
            id=workflow_id,
            name=name,
            description=description,
            nodes=nodes,
            edges=edges
        )
        
        workflow_engine.save_workflow(workflow)
        
        logger.info(f"User {current_user} created workflow: {name}")
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "name": name,
            "description": description
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create workflow: {str(e)}")

@app.get("/api/workflows")
async def list_workflows(current_user: str = Depends(verify_auth_token)):
    """List all workflows"""
    try:
        workflows = workflow_engine.list_workflows()
        return {"success": True, "workflows": workflows}
    except Exception as e:
        logger.error(f"Failed to list workflows: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list workflows: {str(e)}")

@app.get("/api/workflows/{workflow_id}")
async def get_workflow(workflow_id: str, current_user: str = Depends(verify_auth_token)):
    """Get a specific workflow"""
    try:
        workflow = workflow_engine.load_workflow(workflow_id)
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        return {
            "success": True,
            "workflow": {
                "id": workflow.id,
                "name": workflow.name,
                "description": workflow.description,
                "nodes": [
                    {
                        "id": n.id,
                        "type": n.type,
                        "config": n.config,
                        "status": n.status.value
                    }
                    for n in workflow.nodes
                ],
                "edges": [
                    {
                        "source": e.source,
                        "target": e.target,
                        "condition": e.condition
                    }
                    for e in workflow.edges
                ]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get workflow: {str(e)}")

@app.post("/api/workflows/{workflow_id}/execute")
async def execute_workflow(workflow_id: str, current_user: str = Depends(verify_auth_token)):
    """Execute a workflow"""
    try:
        result = workflow_engine.execute_workflow(workflow_id)
        
        logger.info(f"User {current_user} executed workflow: {workflow_id}")
        
        return result
    except Exception as e:
        logger.error(f"Failed to execute workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to execute workflow: {str(e)}")

@app.delete("/api/workflows/{workflow_id}")
async def delete_workflow(workflow_id: str, current_user: str = Depends(verify_auth_token)):
    """Delete a workflow"""
    try:
        conn = sqlite3.connect("behavior.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM workflows WHERE id = ?", (workflow_id,))
        conn.commit()
        conn.close()
        
        logger.info(f"User {current_user} deleted workflow: {workflow_id}")
        
        return {"success": True, "message": f"Workflow {workflow_id} deleted"}
    except Exception as e:
        logger.error(f"Failed to delete workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete workflow: {str(e)}")

@app.get("/api/query/config/execute/{name}")
async def execute_saved_config(name: str, current_user: str = Depends(verify_auth_token)):
    """Execute a saved configuration as a dynamic endpoint"""
    try:
        # Load the configuration
        config_result = query_builder.load_config(name)
        
        if not config_result.get('success'):
            raise HTTPException(status_code=404, detail=config_result.get('error'))
        
        config = config_result.get('config')
        
        # Execute the query
        results = query_builder.execute_query(config)
        
        logger.info(f"User {current_user} executed saved config: {name}")
        
        return {
            "success": True,
            "config_name": name,
            "data": results,
            "count": len(results)
        }
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Invalid saved config: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid saved config: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to execute saved config: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to execute saved config: {str(e)}")

@app.post("/api/query/ai-build")
async def ai_build_query(request: Dict[str, str], current_user: str = Depends(verify_auth_token)):
    """Use AI to generate query configuration from natural language"""
    try:
        natural_query = request.get('query')
        
        if not natural_query:
            raise HTTPException(status_code=400, detail="query is required")
        
        logger.info(f"User {current_user} requesting AI query build: {natural_query}")
        
        # Generate query configuration using Groq
        result = generate_query_from_natural_language(natural_query)
        
        if 'error' in result:
            logger.error(f"AI query build failed: {result['error']}")
            raise HTTPException(status_code=500, detail=result['error'])
        
        logger.info(f"AI generated query config for: {natural_query}")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI query build failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI query build failed: {str(e)}")

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
# Initialize metrics
initialize_metrics()

@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
def root():
    return FileResponse("templates/index.html")

@app.get("/dashboard")
def read_dashboard():
    return FileResponse("templates/dashboard.html")

@app.get("/dashboard.html")
def read_dashboard_html():
    return FileResponse("templates/dashboard.html")

@app.get("/monitor")
def read_monitor():
    return FileResponse("templates/monitor.html")

@app.get("/monitor.html")
def read_monitor_html():
    return FileResponse("templates/monitor.html")

@app.get("/chat")
def serve_chat():
    return FileResponse("templates/chat.html")

@app.get("/chat.html")
def serve_chat_html():
    return FileResponse("templates/chat.html")

@app.get("/api-builder")
def serve_api_builder():
    return FileResponse("templates/api-builder.html")

@app.get("/api-builder.html")
def read_api_builder_html():
    return FileResponse("templates/api-builder.html")

@app.get("/agents")
def read_agents():
    return FileResponse("templates/agents.html")

@app.get("/docs")
def read_docs():
    return FileResponse("templates/docs.html")

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

@app.post("/api/auth/login")
def login_endpoint(username: str, password: str):
    """Login with username and password"""
    try:
        logger.info(f"Login attempt for user: {username}")
        result = auth.login(username, password)
        
        if result["success"]:
            logger.info(f"Login successful for user: {username}")
        else:
            logger.warning(f"Login failed for user: {username} - {result['message']}")
        
        return result
    except Exception as e:
        logger.error(f"Login endpoint failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.post("/api/auth/register")
def register_endpoint(username: str, password: str, role: str, name: str, email: str):
    """Register a new user"""
    try:
        logger.info(f"Registration attempt for user: {username}")
        result = auth.register_user(username, password, role, name, email)
        
        if result["success"]:
            logger.info(f"Registration successful for user: {username}")
        else:
            logger.warning(f"Registration failed for user: {username} - {result['message']}")
        
        return result
    except Exception as e:
        logger.error(f"Registration endpoint failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/api/auth/logout")
def logout_endpoint(token: str):
    """Logout user by revoking token"""
    try:
        logger.info("Logout attempt")
        result = auth.logout(token)
        
        if result["success"]:
            logger.info("Logout successful")
        else:
            logger.warning(f"Logout failed - {result['message']}")
        
        return result
    except Exception as e:
        logger.error(f"Logout endpoint failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")

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

# Conversational API Endpoint

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest, current_user: str = Depends(verify_auth_token), request_obj: Request = None):
    """Conversational API endpoint for natural language interaction with agents"""
    try:
        logger.info(f"User {current_user} (role: {request.role}) sent query: {request.query}")
        
        if not request.query:
            logger.warning("Query is required")
            raise HTTPException(status_code=400, detail="Query is required")
        
        # Process the query through the conversational router with role parameter
        result = conversational_router.process_query(request.query, request.use_llm, request.role)
        
        logger.info(f"Query processed successfully, tool used: {result.get('tool_used', 'none')}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat endpoint failed: {str(e)}")

if __name__ == "__main__":
    import ssl
    import os
    
    # SSL Configuration
    ssl_keyfile = None
    ssl_certfile = None
    
    if os.getenv("ENABLE_SSL", "false").lower() == "true":
        cert_file = os.getenv("SSL_CERT_FILE", "cert.pem")
        key_file = os.getenv("SSL_KEY_FILE", "key.pem")
        
        if os.path.exists(cert_file) and os.path.exists(key_file):
            ssl_certfile = cert_file
            ssl_keyfile = key_file
            logger.info("SSL enabled - server will run on HTTPS")
        else:
            logger.warning(f"SSL certificates not found at {cert_file} and {key_file}. Running on HTTP.")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        ssl_keyfile=ssl_keyfile,
        ssl_certfile=ssl_certfile
    )
