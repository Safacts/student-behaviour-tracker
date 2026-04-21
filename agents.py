"""
Agentic AI Tools for Student Behavior Analytics
These tools can be called by AI agents to perform actions
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from analyzer import analyze_student
from llm_service import generate_parent_report

# ============================================
# TOOL 1: Student Data Retrieval Tools
# ============================================

def get_student_info(student_id: str) -> Dict[str, Any]:
    """
    Get basic student information
    
    Args:
        student_id: Student identifier (e.g., "S001")
    
    Returns:
        Student information dictionary
    """
    conn = sqlite3.connect('behavior.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT student_id, student_name 
        FROM student_activity 
        WHERE student_id = ?
    """, (student_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return {"error": "Student not found"}
    
    return {
        "student_id": result[0],
        "student_name": result[1]
    }

def get_all_students() -> List[Dict[str, Any]]:
    """
    Get list of all students
    
    Returns:
        List of student dictionaries
    """
    conn = sqlite3.connect('behavior.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT student_id, student_name 
        FROM student_activity
    """)
    
    students = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    conn.close()
    
    return students

def get_student_activity_logs(student_id: str, days: int = 7) -> List[Dict[str, Any]]:
    """
    Get student activity logs for specified time period
    
    Args:
        student_id: Student identifier
        days: Number of days to look back (default: 7)
    
    Returns:
        List of activity log dictionaries
    """
    conn = sqlite3.connect('behavior.db')
    cursor = conn.cursor()
    
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    cursor.execute("""
        SELECT id, student_id, student_name, date, time_spent_mins, 
               distraction_score, marks_achieved_percent
        FROM student_activity
        WHERE student_id = ? AND date >= ?
        ORDER BY date DESC
    """, (student_id, cutoff_date))
    
    columns = [column[0] for column in cursor.description]
    logs = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    
    return logs

# ============================================
# TOOL 2: Analysis Tools
# ============================================

def analyze_student_behavior(student_id: str) -> Dict[str, Any]:
    """
    Perform comprehensive behavioral analysis of a student
    
    Args:
        student_id: Student identifier
    
    Returns:
        Analysis results with behavioral tag and metrics
    """
    analysis = analyze_student(student_id)
    
    if not analysis:
        return {"error": "Student not found or no data available"}
    
    # Add additional analysis
    conn = sqlite3.connect('behavior.db')
    cursor = conn.cursor()
    
    # Get recent trends
    cursor.execute("""
        SELECT date, time_spent_mins, distraction_score, marks_achieved_percent
        FROM student_activity
        WHERE student_id = ?
        ORDER BY date DESC
        LIMIT 10
    """, (student_id,))
    
    recent_activities = cursor.fetchall()
    conn.close()
    
    # Calculate trends
    if len(recent_activities) >= 2:
        latest_marks = recent_activities[0][3]
        previous_marks = recent_activities[-1][3]
        marks_trend = latest_marks - previous_marks
    else:
        marks_trend = 0
    
    analysis["marks_trend"] = round(marks_trend, 2)
    analysis["recent_activities_count"] = len(recent_activities)
    
    return analysis

def get_class_overview() -> Dict[str, Any]:
    """
    Get overview of entire class performance
    
    Returns:
        Class-wide statistics and metrics
    """
    conn = sqlite3.connect('behavior.db')
    cursor = conn.cursor()
    
    # Get all students
    cursor.execute("SELECT DISTINCT student_id FROM student_activity")
    student_ids = [row[0] for row in cursor.fetchall()]
    
    # Analyze each student
    analyses = []
    for student_id in student_ids:
        analysis = analyze_student(student_id)
        if analysis:
            analyses.append(analysis)
    
    conn.close()
    
    if not analyses:
        return {"error": "No student data available"}
    
    # Calculate class statistics
    avg_marks = sum(a['avg_marks'] for a in analyses) / len(analyses)
    avg_distraction = sum(a['avg_distraction'] for a in analyses) / len(analyses)
    
    # Count by behavioral tag
    tag_counts = {}
    for analysis in analyses:
        tag = analysis['behavioral_tag']
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    return {
        "total_students": len(analyses),
        "average_marks": round(avg_marks, 2),
        "average_distraction": round(avg_distraction, 2),
        "behavioral_tag_distribution": tag_counts,
        "students_at_risk": tag_counts.get("High Flight Risk", 0),
        "students_on_track": tag_counts.get("On Track", 0),
        "students_with_comprehension_issues": tag_counts.get("Concept Comprehension Issue", 0)
    }

# ============================================
# TOOL 3: AI Report Generation Tools
# ============================================

def generate_ai_recommendation(student_id: str) -> Dict[str, Any]:
    """
    Generate AI-powered recommendation for a student
    
    Args:
        student_id: Student identifier
    
    Returns:
        AI recommendation with analysis
    """
    analysis = analyze_student(student_id)
    
    if not analysis:
        return {"error": "Student not found"}
    
    # Get student name
    conn = sqlite3.connect('behavior.db')
    cursor = conn.cursor()
    cursor.execute("SELECT student_name FROM student_activity WHERE student_id = ? LIMIT 1", (student_id,))
    name_row = cursor.fetchone()
    conn.close()
    
    student_name = name_row[0] if name_row else "Unknown"
    analysis["student_name"] = student_name
    
    # Generate AI report
    ai_report = generate_parent_report(analysis, analysis["behavioral_tag"])
    
    return {
        "student_id": student_id,
        "student_name": student_name,
        "analysis": analysis,
        "ai_recommendation": ai_report
    }

# ============================================
# TOOL 4: Intervention Planning Tools
# ============================================

def identify_at_risk_students(threshold_marks: float = 50.0, 
                              threshold_distraction: float = 6.0) -> List[Dict[str, Any]]:
    """
    Identify students who need intervention
    
    Args:
        threshold_marks: Marks threshold (default: 50.0)
        threshold_distraction: Distraction threshold (default: 6.0)
    
    Returns:
        List of at-risk students with their data
    """
    conn = sqlite3.connect('behavior.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT student_id, student_name
        FROM student_activity
    """)
    
    at_risk_students = []
    
    for row in cursor.fetchall():
        student_id, student_name = row
        analysis = analyze_student(student_id)
        
        if analysis and (analysis['avg_marks'] < threshold_marks or 
                       analysis['avg_distraction'] > threshold_distraction):
            at_risk_students.append({
                "student_id": student_id,
                "student_name": student_name,
                "avg_marks": analysis['avg_marks'],
                "avg_distraction": analysis['avg_distraction'],
                "behavioral_tag": analysis['behavioral_tag']
            })
    
    conn.close()
    
    # Sort by urgency (lowest marks first)
    at_risk_students.sort(key=lambda x: x['avg_marks'])
    
    return at_risk_students

def suggest_intervention(student_id: str) -> Dict[str, Any]:
    """
    Suggest specific intervention for a student
    
    Args:
        student_id: Student identifier
    
    Returns:
        Intervention suggestions with action plan
    """
    analysis = analyze_student(student_id)
    
    if not analysis:
        return {"error": "Student not found"}
    
    behavioral_tag = analysis['behavioral_tag']
    avg_marks = analysis['avg_marks']
    avg_distraction = analysis['avg_distraction']
    
    # Generate intervention suggestions based on behavioral tag
    if behavioral_tag == "High Flight Risk":
        intervention = {
            "urgency": "HIGH",
            "intervention_type": "Immediate Support",
            "actions": [
                "Schedule immediate parent-teacher meeting",
                "Implement daily check-in system",
                "Reduce distractions in study environment",
                "Consider peer tutoring program",
                "Set short-term achievable goals"
            ],
            "timeline": "Within 1 week",
            "success_metrics": [
                "Increase average marks by 10% within 2 weeks",
                "Reduce distraction score by 2 points",
                "Improve daily study time consistency"
            ]
        }
    elif behavioral_tag == "Concept Comprehension Issue":
        intervention = {
            "urgency": "MEDIUM",
            "intervention_type": "Learning Support",
            "actions": [
                "Identify specific knowledge gaps",
                "Provide alternative learning materials",
                "Use visual aids and interactive content",
                "Arrange subject-specific tutoring",
                "Implement spaced repetition practice"
            ],
            "timeline": "Within 2 weeks",
            "success_metrics": [
                "Increase average marks by 15% within 3 weeks",
                "Maintain low distraction levels",
                "Complete concept mastery tests"
            ]
        }
    else:  # On Track
        intervention = {
            "urgency": "LOW",
            "intervention_type": "Enhancement",
            "actions": [
                "Introduce advanced challenges",
                "Provide enrichment activities",
                "Encourage peer mentoring",
                "Set stretch goals",
                "Explore advanced topics"
            ],
            "timeline": "Ongoing",
            "success_metrics": [
                "Maintain or improve current performance",
                "Take on leadership roles",
                "Complete advanced projects"
            ]
        }
    
    # Add student-specific data
    intervention["student_id"] = student_id
    intervention["current_status"] = {
        "avg_marks": avg_marks,
        "avg_distraction": avg_distraction,
        "behavioral_tag": behavioral_tag
    }
    
    return intervention

# ============================================
# TOOL 5: Learning Path Tools
# ============================================

def create_learning_path(student_id: str) -> Dict[str, Any]:
    """
    Create personalized learning path for a student
    
    Args:
        student_id: Student identifier
    
    Returns:
        Learning path with milestones and resources
    """
    analysis = analyze_student(student_id)
    
    if not analysis:
        return {"error": "Student not found"}
    
    behavioral_tag = analysis['behavioral_tag']
    avg_marks = analysis['avg_marks']
    
    # Create learning path based on current level
    if behavioral_tag == "High Flight Risk":
        learning_path = {
            "level": "Foundation Building",
            "duration": "4-6 weeks",
            "milestones": [
                {
                    "week": 1,
                    "focus": "Study Habits & Routine",
                    "objectives": [
                        "Establish consistent study schedule",
                        "Create distraction-free study environment",
                        "Set daily study time goals"
                    ],
                    "resources": ["Study planner template", "Focus techniques guide"]
                },
                {
                    "week": 2,
                    "focus": "Basic Concept Review",
                    "objectives": [
                        "Review fundamental concepts",
                        "Complete practice exercises",
                        "Identify knowledge gaps"
                    ],
                    "resources": ["Concept review videos", "Practice worksheets"]
                },
                {
                    "week": 3,
                    "focus": "Skill Building",
                    "objectives": [
                        "Practice problem-solving",
                        "Build confidence in weak areas",
                        "Track progress daily"
                    ],
                    "resources": ["Interactive exercises", "Progress tracking tools"]
                },
                {
                    "week": 4,
                    "focus": "Assessment & Adjustment",
                    "objectives": [
                        "Complete assessment tests",
                        "Review progress",
                        "Adjust learning strategy"
                    ],
                    "resources": ["Assessment tools", "Progress reports"]
                }
            ]
        }
    elif behavioral_tag == "Concept Comprehension Issue":
        learning_path = {
            "level": "Concept Mastery",
            "duration": "3-4 weeks",
            "milestones": [
                {
                    "week": 1,
                    "focus": "Diagnosis",
                    "objectives": [
                        "Identify specific comprehension gaps",
                        "Assess learning style",
                        "Choose appropriate materials"
                    ],
                    "resources": ["Learning style assessment", "Diagnostic tests"]
                },
                {
                    "week": 2,
                    "focus": "Alternative Approaches",
                    "objectives": [
                        "Try different teaching methods",
                        "Use visual and interactive materials",
                        "Practice with real-world examples"
                    ],
                    "resources": ["Visual learning tools", "Real-world examples"]
                },
                {
                    "week": 3,
                    "focus": "Reinforcement",
                    "objectives": [
                        "Practice with varied problems",
                        "Teach concepts to others",
                        "Apply concepts in projects"
                    ],
                    "resources": ["Practice problems", "Project ideas"]
                }
            ]
        }
    else:  # On Track
        learning_path = {
            "level": "Advanced & Enrichment",
            "duration": "Ongoing",
            "milestones": [
                {
                    "week": 1,
                    "focus": "Challenge Introduction",
                    "objectives": [
                        "Introduce advanced concepts",
                        "Set stretch goals",
                        "Begin enrichment projects"
                    ],
                    "resources": ["Advanced materials", "Project templates"]
                },
                {
                    "week": 2,
                    "focus": "Deep Dive",
                    "objectives": [
                        "Explore advanced topics",
                        "Work on complex problems",
                        "Develop expertise areas"
                    ],
                    "resources": ["Expert resources", "Complex problem sets"]
                },
                {
                    "week": 3,
                    "focus": "Leadership & Mentoring",
                    "objectives": [
                        "Mentor other students",
                        "Lead group projects",
                        "Share knowledge"
                    ],
                    "resources": ["Leadership guides", "Mentoring materials"]
                }
            ]
        }
    
    learning_path["student_id"] = student_id
    learning_path["starting_point"] = {
        "avg_marks": avg_marks,
        "behavioral_tag": behavioral_tag
    }
    
    return learning_path

# ============================================
# TOOL 6: Data Management Tools
# ============================================

def add_student_activity(student_id: str, student_name: str, date: str,
                        time_spent_mins: int, distraction_score: float,
                        marks_achieved_percent: float) -> Dict[str, Any]:
    """
    Add new student activity record
    
    Args:
        student_id: Student identifier
        student_name: Student full name
        date: Activity date (YYYY-MM-DD format)
        time_spent_mins: Time spent in minutes
        distraction_score: Distraction score (0-10)
        marks_achieved_percent: Marks percentage (0-100)
    
    Returns:
        Success/error message
    """
    try:
        conn = sqlite3.connect('behavior.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO student_activity 
            (student_id, student_name, date, time_spent_mins, distraction_score, marks_achieved_percent)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, student_name, date, time_spent_mins, distraction_score, marks_achieved_percent))
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Activity record added successfully",
            "student_id": student_id,
            "date": date
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_student_summary(student_id: str) -> Dict[str, Any]:
    """
    Get comprehensive summary of student data
    
    Args:
        student_id: Student identifier
    
    Returns:
        Complete student summary
    """
    # Get basic info
    info = get_student_info(student_id)
    if "error" in info:
        return info
    
    # Get analysis
    analysis = analyze_student_behavior(student_id)
    
    # Get recent activities
    activities = get_student_activity_logs(student_id, days=7)
    
    # Get AI recommendation
    recommendation = generate_ai_recommendation(student_id)
    
    # Get intervention suggestion
    intervention = suggest_intervention(student_id)
    
    # Get learning path
    learning_path = create_learning_path(student_id)
    
    return {
        "student_info": info,
        "analysis": analysis,
        "recent_activities": activities,
        "ai_recommendation": recommendation,
        "intervention_suggestion": intervention,
        "learning_path": learning_path
    }

# ============================================
# TOOL SCHEMA FOR AGENTIC AI
# ============================================

TOOL_SCHEMA = {
    "student_data_tools": [
        {
            "name": "get_student_info",
            "description": "Get basic student information",
            "parameters": {
                "student_id": {"type": "string", "required": True}
            }
        },
        {
            "name": "get_all_students",
            "description": "Get list of all students",
            "parameters": {}
        },
        {
            "name": "get_student_activity_logs",
            "description": "Get student activity logs",
            "parameters": {
                "student_id": {"type": "string", "required": True},
                "days": {"type": "integer", "required": False, "default": 7}
            }
        }
    ],
    "analysis_tools": [
        {
            "name": "analyze_student_behavior",
            "description": "Perform comprehensive behavioral analysis",
            "parameters": {
                "student_id": {"type": "string", "required": True}
            }
        },
        {
            "name": "get_class_overview",
            "description": "Get class-wide statistics",
            "parameters": {}
        }
    ],
    "ai_tools": [
        {
            "name": "generate_ai_recommendation",
            "description": "Generate AI-powered recommendation",
            "parameters": {
                "student_id": {"type": "string", "required": True}
            }
        }
    ],
    "intervention_tools": [
        {
            "name": "identify_at_risk_students",
            "description": "Identify students needing intervention",
            "parameters": {
                "threshold_marks": {"type": "float", "required": False, "default": 50.0},
                "threshold_distraction": {"type": "float", "required": False, "default": 6.0}
            }
        },
        {
            "name": "suggest_intervention",
            "description": "Suggest specific intervention for student",
            "parameters": {
                "student_id": {"type": "string", "required": True}
            }
        }
    ],
    "learning_path_tools": [
        {
            "name": "create_learning_path",
            "description": "Create personalized learning path",
            "parameters": {
                "student_id": {"type": "string", "required": True}
            }
        }
    ],
    "data_management_tools": [
        {
            "name": "add_student_activity",
            "description": "Add new student activity record",
            "parameters": {
                "student_id": {"type": "string", "required": True},
                "student_name": {"type": "string", "required": True},
                "date": {"type": "string", "required": True},
                "time_spent_mins": {"type": "integer", "required": True},
                "distraction_score": {"type": "float", "required": True},
                "marks_achieved_percent": {"type": "float", "required": True}
            }
        },
        {
            "name": "get_student_summary",
            "description": "Get comprehensive student summary",
            "parameters": {
                "student_id": {"type": "string", "required": True}
            }
        }
    ]
}

if __name__ == "__main__":
    # Test the tools
    print("Testing Agentic AI Tools...")
    print("\n1. Get Student Info:")
    print(get_student_info("S001"))
    
    print("\n2. Analyze Student Behavior:")
    print(analyze_student_behavior("S001"))
    
    print("\n3. Get Class Overview:")
    print(get_class_overview())
    
    print("\n4. Identify At-Risk Students:")
    print(identify_at_risk_students())
    
    print("\n5. Suggest Intervention:")
    print(suggest_intervention("S001"))
    
    print("\n6. Create Learning Path:")
    print(create_learning_path("S001"))
    
    print("\n7. Get Student Summary:")
    print(get_student_summary("S001"))
