"""
Agentic AI Tools for Student Behavior Analytics
These tools can be called by AI agents to perform actions
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from analyzer import analyze_student
from llm_service import generate_parent_report
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ============================================
# LLM-POWERED REPORT GENERATION
# ============================================

def generate_llm_agent_report(agent_type: str, analysis_data: Dict[str, Any]) -> str:
    """
    Generate natural language report using LLM based on agent analysis
    
    Args:
        agent_type: Type of agent (behavior, learning_path, intervention)
        analysis_data: Analysis data from the agent
    
    Returns:
        Natural language report from LLM
    """
    try:
        if GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here":
            client = Groq(api_key=GROQ_API_KEY)
            
            # Build prompt based on agent type
            if agent_type == "behavior":
                prompt = f"""
                You are an educational behavior analyst. Write a comprehensive behavioral analysis report based on this data:
                
                Student ID: {analysis_data.get('student_id', 'Unknown')}
                Total Study Time: {analysis_data.get('total_study_time', 0)} minutes
                Average Distraction: {analysis_data.get('avg_distraction', 0)}/10
                Average Marks: {analysis_data.get('avg_marks', 0)}%
                Behavioral Tag: {analysis_data.get('behavioral_tag', 'Unknown')}
                Marks Trend: {analysis_data.get('marks_trend', 0)}%
                Recent Activities: {analysis_data.get('recent_activities_count', 0)} sessions
                
                Write a 4-5 sentence analysis that explains:
                1. What the behavioral patterns indicate
                2. Key risk factors or strengths
                3. Specific observations from the data
                4. What this means for the student's progress
                5. Recommendations for next steps
                
                Be specific, professional, and actionable.
                """
            elif agent_type == "learning_path":
                level = analysis_data.get('level', 'Unknown')
                duration = analysis_data.get('duration', 'Unknown')
                milestones = analysis_data.get('milestones', [])
                
                prompt = f"""
                You are an educational curriculum designer. Write a comprehensive learning path report based on this data:
                
                Student ID: {analysis_data.get('student_id', 'Unknown')}
                Learning Level: {level}
                Duration: {duration}
                Starting Point: {analysis_data.get('starting_point', {})}
                
                Milestones: {milestones}
                
                Write a 4-5 sentence learning path summary that explains:
                1. Why this learning level was chosen
                2. What the student will focus on
                3. Key milestones and their importance
                4. How resources support the learning journey
                5. Expected outcomes and success indicators
                
                Be encouraging, structured, and clear about the learning journey.
                """
            elif agent_type == "intervention":
                urgency = analysis_data.get('urgency', 'Unknown')
                intervention_type = analysis_data.get('intervention_type', 'Unknown')
                timeline = analysis_data.get('timeline', 'Unknown')
                actions = analysis_data.get('actions', [])
                success_metrics = analysis_data.get('success_metrics', [])
                
                prompt = f"""
                You are an educational intervention specialist. Write a comprehensive intervention report based on this data:
                
                Student ID: {analysis_data.get('student_id', 'Unknown')}
                Urgency: {urgency}
                Intervention Type: {intervention_type}
                Timeline: {timeline}
                Current Status: {analysis_data.get('current_status', {})}
                
                Actions: {actions}
                Success Metrics: {success_metrics}
                
                Write a 4-5 sentence intervention summary that explains:
                1. Why this intervention is needed
                2. The specific approach and its rationale
                3. How the timeline ensures success
                4. What success looks like and how it will be measured
                5. Next steps for implementation
                
                Be urgent but supportive, specific, and actionable.
                """
            
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are an expert educational analyst and advisor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        else:
            return None
    except Exception as e:
        return None

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
# TOOL 7: Communication Tools
# ============================================

def generate_parent_email(student_id: str, email_type: str = "report") -> Dict[str, Any]:
    """
    Generate email content for parent communication
    
    Args:
        student_id: Student identifier
        email_type: Type of email (report, intervention, meeting_request, urgent_alert)
    
    Returns:
        Email content with subject, body, and metadata
    """
    try:
        analysis = analyze_student_behavior(student_id)
        
        if "error" in analysis:
            return {"error": "Student not found"}
        
        student_info = get_student_info(student_id)
        student_name = student_info.get("name", "Student")
        
        if email_type == "report":
            # Generate weekly/monthly report email
            subject = f"Student Progress Report - {student_name} ({student_id})"
            
            body = f"""
Dear Parent/Guardian,

This is an automated progress report for {student_name} ({student_id}).

PERFORMANCE SUMMARY
-------------------
Average Marks: {analysis.get('avg_marks', 0):.2f}%
Average Distraction Score: {analysis.get('avg_distraction', 0):.2f}/10
Total Study Time: {analysis.get('total_study_time', 0)} minutes
Behavioral Tag: {analysis.get('behavioral_tag', 'Unknown')}
Recent Activity Trend: {analysis.get('marks_trend', 0):.2f}%

KEY OBSERVATIONS
---------------
The student's current behavioral pattern indicates: {analysis.get('behavioral_tag', 'Unknown')}

RECOMMENDATIONS
---------------
Based on the analysis, we recommend:
1. Review study habits and routine
2. Monitor distraction levels during study time
3. Encourage consistent daily practice
4. Consider additional support if needed

NEXT STEPS
----------
Please review this report and contact us if you have any questions or concerns.
We can schedule a meeting to discuss specific strategies for improvement.

Best regards,
Student Behavior Analytics Team

---
This is an automated message. Please do not reply directly to this email.
"""
        
        elif email_type == "intervention":
            intervention = suggest_intervention(student_id)
            subject = f"URGENT: Intervention Plan Required - {student_name} ({student_id})"
            
            body = f"""
Dear Parent/Guardian,

URGENT ATTENTION REQUIRED

We have identified that {student_name} ({student_id}) requires immediate intervention support.

CURRENT STATUS
--------------
Urgency Level: {intervention.get('urgency', 'Unknown')}
Intervention Type: {intervention.get('intervention_type', 'Unknown')}
Timeline: {intervention.get('timeline', 'Unknown')}

INTERVENTION ACTIONS
--------------------
{chr(10).join([f"- {action}" for action in intervention.get('actions', [])])}

SUCCESS METRICS
---------------
{chr(10).join([f"- {metric}" for metric in intervention.get('success_metrics', [])])}

IMMEDIATE ACTION REQUIRED
--------------------------
Please contact us within 24 hours to discuss this intervention plan.
We need your support to implement these changes effectively.

This is a time-sensitive matter that requires immediate attention.

Best regards,
Student Behavior Analytics Team

---
This is an automated message. Please contact us directly to discuss.
"""
        
        elif email_type == "meeting_request":
            subject = f"Parent-Teacher Meeting Request - {student_name} ({student_id})"
            
            body = f"""
Dear Parent/Guardian,

We would like to schedule a meeting to discuss {student_name}'s progress.

MEETING PURPOSE
---------------
To discuss:
- Current academic performance
- Behavioral patterns and observations
- Strategies for improvement
- Support resources available

CURRENT STATUS
--------------
Average Marks: {analysis.get('avg_marks', 0):.2f}%
Behavioral Tag: {analysis.get('behavioral_tag', 'Unknown')}

SUGGESTED MEETING TIMES
----------------------
Please let us know your availability for a 30-minute meeting in the next week.
We are available:
- Monday to Friday: 9:00 AM - 5:00 PM
- Saturday: 10:00 AM - 2:00 PM

Please reply with your preferred time slots.

Best regards,
Student Behavior Analytics Team

---
This is an automated message. Please contact us to schedule.
"""
        
        elif email_type == "urgent_alert":
            subject = f"URGENT ALERT: {student_name} Needs Immediate Attention"
            
            body = f"""
URGENT ALERT - IMMEDIATE ATTENTION REQUIRED

Dear Parent/Guardian,

We have detected a significant decline in {student_name}'s performance that requires immediate attention.

ALERT DETAILS
------------
Student: {student_name} ({student_id})
Average Marks: {analysis.get('avg_marks', 0):.2f}%
Distraction Score: {analysis.get('avg_distraction', 0):.2f}/10
Behavioral Tag: {analysis.get('behavioral_tag', 'Unknown')}

CONCERNS
--------
- Performance has dropped significantly
- High distraction levels detected
- Risk of falling behind academically

IMMEDIATE ACTION NEEDED
----------------------
Please contact us TODAY to discuss emergency intervention measures.
We cannot delay - your child's academic progress is at risk.

Contact Information:
- Phone: [Your Phone Number]
- Email: [Your Email Address]

This is an urgent matter requiring immediate response.

Best regards,
Student Behavior Analytics Team

---
URGENT - Please respond immediately
"""
        
        else:
            return {"error": "Invalid email type"}
        
        return {
            "success": True,
            "student_id": student_id,
            "email_type": email_type,
            "subject": subject,
            "body": body.strip(),
            "to_email": f"parent_of_{student_id}@example.com",
            "from_email": "analytics@school.edu",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

def generate_staff_notification(student_id: str, notification_type: str = "intervention") -> Dict[str, Any]:
    """
    Generate notification content for staff/teachers
    
    Args:
        student_id: Student identifier
        notification_type: Type of notification (intervention, monitoring, followup, escalation)
    
    Returns:
        Notification content
    """
    try:
        analysis = analyze_student_behavior(student_id)
        
        if "error" in analysis:
            return {"error": "Student not found"}
        
        student_info = get_student_info(student_id)
        student_name = student_info.get("name", "Student")
        
        if notification_type == "intervention":
            intervention = suggest_intervention(student_id)
            subject = f"Intervention Required: {student_name} ({student_id})"
            
            message = f"""
INTERVENTION ALERT
-----------------
Student: {student_name} ({student_id})
Urgency: {intervention.get('urgency', 'Unknown')}
Timeline: {intervention.get('timeline', 'Unknown')}

Actions Required:
{chr(10).join([f"- {action}" for action in intervention.get('actions', [])])}

Please implement these actions and document progress.
"""
        
        elif notification_type == "monitoring":
            subject = f"Monitoring Required: {student_name} ({student_id})"
            
            message = f"""
MONITORING ALERT
---------------
Student: {student_name} ({student_id})
Behavioral Tag: {analysis.get('behavioral_tag', 'Unknown')}
Marks Trend: {analysis.get('marks_trend', 0):.2f}%

Please monitor this student closely and report any significant changes.
"""
        
        elif notification_type == "followup":
            subject = f"Follow-up Required: {student_name} ({student_id})"
            
            message = f"""
FOLLOW-UP REMINDER
----------------
Student: {student_name} ({student_id})

Previous intervention requires follow-up assessment.
Please review progress and determine if additional support is needed.
"""
        
        elif notification_type == "escalation":
            subject = f"ESCALATION: {student_name} ({student_id})"
            
            message = f"""
ESCALATION NOTICE
----------------
Student: {student_name} ({student_id})
Risk Level: {analysis.get('behavioral_tag', 'Unknown')}

This case requires escalation to senior staff or administration.
Current interventions are not showing desired results.
"""
        
        else:
            return {"error": "Invalid notification type"}
        
        return {
            "success": True,
            "student_id": student_id,
            "notification_type": notification_type,
            "subject": subject,
            "message": message.strip(),
            "priority": "high" if notification_type in ["intervention", "escalation"] else "medium",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

# ============================================
# TOOL 8: Task Management Tools
# ============================================

# In-memory task storage (in production, use a database)
_task_storage = {}

def create_intervention_task(student_id: str, assigned_to: str, due_date: str = None) -> Dict[str, Any]:
    """
    Create a task for intervention implementation
    
    Args:
        student_id: Student identifier
        assigned_to: Person assigned to the task
        due_date: Due date for task completion (ISO format)
    
    Returns:
        Task details
    """
    try:
        intervention = suggest_intervention(student_id)
        
        if "error" in intervention:
            return {"error": "Student not found"}
        
        task_id = f"task_{len(_task_storage) + 1}_{student_id}"
        
        # Calculate due date if not provided
        if not due_date:
            if intervention.get('urgency') == 'HIGH':
                due_date = (datetime.now() + timedelta(days=7)).isoformat()
            else:
                due_date = (datetime.now() + timedelta(days=14)).isoformat()
        
        task = {
            "task_id": task_id,
            "student_id": student_id,
            "task_type": "intervention",
            "assigned_to": assigned_to,
            "assigned_by": "system",
            "assigned_date": datetime.now().isoformat(),
            "due_date": due_date,
            "status": "pending",
            "priority": intervention.get('urgency', 'MEDIUM'),
            "actions": intervention.get('actions', []),
            "success_metrics": intervention.get('success_metrics', []),
            "notes": f"Implement intervention for student with {intervention.get('behavioral_tag', 'Unknown')} status"
        }
        
        _task_storage[task_id] = task
        
        return {
            "success": True,
            "task": task,
            "message": "Task created successfully"
        }
    except Exception as e:
        return {"error": str(e)}

def create_monitoring_task(student_id: str, assigned_to: str, monitoring_period_days: int = 30) -> Dict[str, Any]:
    """
    Create a task for ongoing student monitoring
    
    Args:
        student_id: Student identifier
        assigned_to: Person assigned to the task
        monitoring_period_days: Number of days to monitor
    
    Returns:
        Task details
    """
    try:
        analysis = analyze_student_behavior(student_id)
        
        if "error" in analysis:
            return {"error": "Student not found"}
        
        task_id = f"monitor_{len(_task_storage) + 1}_{student_id}"
        due_date = (datetime.now() + timedelta(days=monitoring_period_days)).isoformat()
        
        task = {
            "task_id": task_id,
            "student_id": student_id,
            "task_type": "monitoring",
            "assigned_to": assigned_to,
            "assigned_by": "system",
            "assigned_date": datetime.now().isoformat(),
            "due_date": due_date,
            "status": "pending",
            "priority": "medium",
            "monitoring_period_days": monitoring_period_days,
            "checkpoints": [
                {
                    "day": 7,
                    "action": "Initial check-in - assess early progress"
                },
                {
                    "day": 14,
                    "action": "Mid-period review - adjust if needed"
                },
                {
                    "day": monitoring_period_days,
                    "action": "Final assessment - determine next steps"
                }
            ],
            "notes": f"Monitor student with {analysis.get('behavioral_tag', 'Unknown')} status"
        }
        
        _task_storage[task_id] = task
        
        return {
            "success": True,
            "task": task,
            "message": "Monitoring task created successfully"
        }
    except Exception as e:
        return {"error": str(e)}

def update_task_status(task_id: str, status: str, notes: str = None) -> Dict[str, Any]:
    """
    Update task status and add notes
    
    Args:
        task_id: Task identifier
        status: New status (pending, in_progress, completed, blocked)
        notes: Optional notes about the update
    
    Returns:
        Updated task details
    """
    try:
        if task_id not in _task_storage:
            return {"error": "Task not found"}
        
        task = _task_storage[task_id]
        task['status'] = status
        task['last_updated'] = datetime.now().isoformat()
        
        if notes:
            if 'update_history' not in task:
                task['update_history'] = []
            task['update_history'].append({
                "timestamp": datetime.now().isoformat(),
                "status": status,
                "notes": notes
            })
            task['notes'] = notes
        
        _task_storage[task_id] = task
        
        return {
            "success": True,
            "task": task,
            "message": f"Task status updated to {status}"
        }
    except Exception as e:
        return {"error": str(e)}

def get_assigned_tasks(assigned_to: str) -> Dict[str, Any]:
    """
    Get all tasks assigned to a specific person
    
    Args:
        assigned_to: Person identifier
    
    Returns:
        List of assigned tasks
    """
    try:
        tasks = [task for task in _task_storage.values() if task.get('assigned_to') == assigned_to]
        
        # Sort by due date
        tasks.sort(key=lambda x: x.get('due_date', ''))
        
        return {
            "success": True,
            "assigned_to": assigned_to,
            "task_count": len(tasks),
            "tasks": tasks
        }
    except Exception as e:
        return {"error": str(e)}

def get_student_tasks(student_id: str) -> Dict[str, Any]:
    """
    Get all tasks for a specific student
    
    Args:
        student_id: Student identifier
    
    Returns:
        List of student tasks
    """
    try:
        tasks = [task for task in _task_storage.values() if task.get('student_id') == student_id]
        
        return {
            "success": True,
            "student_id": student_id,
            "task_count": len(tasks),
            "tasks": tasks
        }
    except Exception as e:
        return {"error": str(e)}

def get_overdue_tasks() -> Dict[str, Any]:
    """
    Get all overdue tasks
    
    Returns:
        List of overdue tasks
    """
    try:
        now = datetime.now()
        overdue_tasks = []
        
        for task in _task_storage.values():
            due_date = datetime.fromisoformat(task.get('due_date', ''))
            if due_date < now and task.get('status') not in ['completed', 'cancelled']:
                overdue_tasks.append(task)
        
        # Sort by how overdue they are
        overdue_tasks.sort(key=lambda x: datetime.fromisoformat(x['due_date']))
        
        return {
            "success": True,
            "overdue_count": len(overdue_tasks),
            "overdue_tasks": overdue_tasks
        }
    except Exception as e:
        return {"error": str(e)}

# ============================================
# TOOL 9: Document Generation Tools
# ============================================

def generate_pdf_report_content(student_id: str) -> Dict[str, Any]:
    """
    Generate content for PDF report (structured format)
    
    Args:
        student_id: Student identifier
    
    Returns:
        Structured content for PDF generation
    """
    try:
        # Get comprehensive data
        analysis = analyze_student_behavior(student_id)
        student_info = get_student_info(student_id)
        learning_path = create_learning_path(student_id)
        intervention = suggest_intervention(student_id)
        
        if "error" in analysis:
            return {"error": "Student not found"}
        
        # Generate LLM reports
        behavior_report = generate_llm_agent_report("behavior", analysis)
        learning_report = generate_llm_agent_report("learning_path", learning_path)
        intervention_report = generate_llm_agent_report("intervention", intervention)
        
        # Structure for PDF generation
        pdf_content = {
            "header": {
                "title": "Student Behavior Analysis Report",
                "student_id": student_id,
                "student_name": student_info.get("name", "Unknown"),
                "generated_date": datetime.now().strftime("%Y-%m-%d"),
                "school_name": "Your School Name"
            },
            "executive_summary": {
                "behavioral_tag": analysis.get("behavioral_tag", "Unknown"),
                "avg_marks": analysis.get("avg_marks", 0),
                "avg_distraction": analysis.get("avg_distraction", 0),
                "total_study_time": analysis.get("total_study_time", 0),
                "marks_trend": analysis.get("marks_trend", 0),
                "risk_level": "Critical" if analysis.get("behavioral_tag") == "High Flight Risk" else "High" if analysis.get("behavioral_tag") == "Concept Comprehension Issue" else "Low"
            },
            "behavioral_analysis": {
                "title": "Behavioral Analysis",
                "structured_data": analysis,
                "narrative": behavior_report or "Analysis not available"
            },
            "learning_path": {
                "title": "Personalized Learning Path",
                "structured_data": learning_path,
                "narrative": learning_report or "Learning path not available"
            },
            "intervention_plan": {
                "title": "Intervention Plan",
                "structured_data": intervention,
                "narrative": intervention_report or "Intervention plan not available"
            },
            "recommendations": {
                "title": "Key Recommendations",
                "items": [
                    "Implement suggested intervention strategies",
                    "Monitor progress regularly",
                    "Maintain communication with parents",
                    "Adjust learning path based on progress"
                ]
            },
            "footer": {
                "generated_by": "Student Behavior Analytics System",
                "contact_info": "analytics@school.edu",
                "disclaimer": "This report is generated automatically. Please verify all information before taking action."
            }
        }
        
        return {
            "success": True,
            "student_id": student_id,
            "pdf_content": pdf_content,
            "format": "structured_json"
        }
    except Exception as e:
        return {"error": str(e)}

def generate_meeting_agenda(student_id: str, meeting_type: str = "parent_teacher") -> Dict[str, Any]:
    """
    Generate agenda for parent-teacher or staff meeting
    
    Args:
        student_id: Student identifier
        meeting_type: Type of meeting (parent_teacher, staff_review, intervention_planning)
    
    Returns:
        Meeting agenda content
    """
    try:
        analysis = analyze_student_behavior(student_id)
        student_info = get_student_info(student_id)
        
        if "error" in analysis:
            return {"error": "Student not found"}
        
        if meeting_type == "parent_teacher":
            agenda = {
                "meeting_title": f"Parent-Teacher Meeting - {student_info.get('name', 'Student')}",
                "student_id": student_id,
                "duration": "30 minutes",
                "agenda_items": [
                    {
                        "item": 1,
                        "title": "Welcome and Introduction",
                        "duration": "5 minutes",
                        "description": "Introduce purpose of meeting and set expectations"
                    },
                    {
                        "item": 2,
                        "title": "Current Performance Review",
                        "duration": "10 minutes",
                        "description": f"Review current academic performance (Average: {analysis.get('avg_marks', 0):.2f}%, Behavioral Tag: {analysis.get('behavioral_tag', 'Unknown')})"
                    },
                    {
                        "item": 3,
                        "title": "Behavioral Patterns Discussion",
                        "duration": "10 minutes",
                        "description": f"Discuss behavioral patterns (Distraction: {analysis.get('avg_distraction', 0):.2f}/10, Study Time: {analysis.get('total_study_time', 0)} mins)"
                    },
                    {
                        "item": 4,
                        "title": "Action Plan and Next Steps",
                        "duration": "5 minutes",
                        "description": "Agree on action items and follow-up schedule"
                    }
                ],
                "prepared_by": "Student Behavior Analytics System",
                "preparation_notes": "Review student data and prepare specific examples before meeting"
            }
        
        elif meeting_type == "staff_review":
            intervention = suggest_intervention(student_id)
            agenda = {
                "meeting_title": f"Staff Review - {student_info.get('name', 'Student')}",
                "student_id": student_id,
                "duration": "20 minutes",
                "agenda_items": [
                    {
                        "item": 1,
                        "title": "Current Status Update",
                        "duration": "5 minutes",
                        "description": "Review current intervention status"
                    },
                    {
                        "item": 2,
                        "title": "Progress Assessment",
                        "duration": "10 minutes",
                        "description": f"Assess progress against success metrics (Urgency: {intervention.get('urgency', 'Unknown')})"
                    },
                    {
                        "item": 3,
                        "title": "Next Steps",
                        "duration": "5 minutes",
                        "description": "Determine if intervention needs adjustment or escalation"
                    }
                ],
                "prepared_by": "Student Behavior Analytics System"
            }
        
        elif meeting_type == "intervention_planning":
            agenda = {
                "meeting_title": f"Intervention Planning - {student_info.get('name', 'Student')}",
                "student_id": student_id,
                "duration": "45 minutes",
                "agenda_items": [
                    {
                        "item": 1,
                        "title": "Problem Identification",
                        "duration": "10 minutes",
                        "description": "Identify specific issues and root causes"
                    },
                    {
                        "item": 2,
                        "title": "Strategy Development",
                        "duration": "20 minutes",
                        "description": "Develop comprehensive intervention strategy"
                    },
                    {
                        "item": 3,
                        "title": "Resource Allocation",
                        "duration": "10 minutes",
                        "description": "Assign resources and responsibilities"
                    },
                    {
                        "item": 4,
                        "title": "Timeline and Metrics",
                        "duration": "5 minutes",
                        "description": "Set timeline and success metrics"
                    }
                ],
                "prepared_by": "Student Behavior Analytics System"
            }
        
        else:
            return {"error": "Invalid meeting type"}
        
        return {
            "success": True,
            "student_id": student_id,
            "meeting_type": meeting_type,
            "agenda": agenda
        }
    except Exception as e:
        return {"error": str(e)}

# ============================================
# TOOL 10: Advanced Analytics Tools
# ============================================

def predict_student_performance(student_id: str, days_ahead: int = 30) -> Dict[str, Any]:
    """
    Predict future student performance based on historical trends
    
    Args:
        student_id: Student identifier
        days_ahead: Number of days ahead to predict
    
    Returns:
        Performance predictions with confidence scores
    """
    try:
        activities = get_student_activity_logs(student_id, days=60)
        
        if not activities:
            return {"error": "Insufficient data for prediction"}
        
        # Calculate trends
        recent_activities = sorted(activities, key=lambda x: x['date'], reverse=True)[:30]
        marks_data = [a['marks_achieved_percent'] for a in recent_activities if a['marks_achieved_percent'] > 0]
        distraction_data = [a['distraction_score'] for a in recent_activities]
        
        if len(marks_data) < 5:
            return {"error": "Insufficient data points for prediction"}
        
        # Calculate simple linear trend
        marks_trend = (marks_data[-1] - marks_data[0]) / len(marks_data) if len(marks_data) > 0 else 0
        distraction_trend = (distraction_data[-1] - distraction_data[0]) / len(distraction_data) if len(distraction_data) > 0 else 0
        
        # Predict future values
        current_avg_marks = sum(marks_data) / len(marks_data)
        current_avg_distraction = sum(distraction_data) / len(distraction_data)
        
        predicted_marks = current_avg_marks + (marks_trend * days_ahead)
        predicted_distraction = current_avg_distraction + (distraction_trend * days_ahead)
        
        # Calculate confidence based on data consistency
        marks_variance = sum((x - current_avg_marks) ** 2 for x in marks_data) / len(marks_data)
        confidence = max(0, min(100, 100 - marks_variance))
        
        # Determine risk level
        if predicted_marks < 40 or predicted_distraction > 7:
            risk_level = "Critical"
        elif predicted_marks < 50 or predicted_distraction > 5:
            risk_level = "High"
        elif predicted_marks < 60 or predicted_distraction > 4:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        # Generate recommendations
        recommendations = []
        if marks_trend < -1:
            recommendations.append("Marks are declining - immediate intervention needed")
        elif marks_trend < 0:
            recommendations.append("Marks are slowly declining - monitor closely")
        
        if distraction_trend > 0.5:
            recommendations.append("Distraction is increasing - address study environment")
        
        if risk_level in ["Critical", "High"]:
            recommendations.append("Schedule parent meeting and implement intervention plan")
        
        return {
            "success": True,
            "student_id": student_id,
            "prediction_period_days": days_ahead,
            "current_performance": {
                "avg_marks": current_avg_marks,
                "avg_distraction": current_avg_distraction
            },
            "predicted_performance": {
                "avg_marks": max(0, min(100, predicted_marks)),
                "avg_distraction": max(0, min(10, predicted_distraction))
            },
            "trends": {
                "marks_trend": marks_trend,
                "distraction_trend": distraction_trend
            },
            "risk_level": risk_level,
            "confidence_score": confidence,
            "recommendations": recommendations,
            "prediction_date": (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        }
    except Exception as e:
        return {"error": str(e)}

def detect_anomalies(student_id: str, threshold_std: float = 2.0) -> Dict[str, Any]:
    """
    Detect anomalous behavior patterns in student data
    
    Args:
        student_id: Student identifier
        threshold_std: Standard deviation threshold for anomaly detection
    
    Returns:
        List of detected anomalies
    """
    try:
        activities = get_student_activity_logs(student_id, days=30)
        
        if not activities:
            return {"error": "Insufficient data for anomaly detection"}
        
        anomalies = []
        
        # Calculate statistics
        marks_list = [a['marks_achieved_percent'] for a in activities if a['marks_achieved_percent'] > 0]
        distraction_list = [a['distraction_score'] for a in activities]
        time_list = [a['time_spent_mins'] for a in activities]
        
        if len(marks_list) < 5:
            return {"error": "Insufficient data points"}
        
        # Calculate means and standard deviations
        marks_mean = sum(marks_list) / len(marks_list)
        marks_std = (sum((x - marks_mean) ** 2 for x in marks_list) / len(marks_list)) ** 0.5
        
        distraction_mean = sum(distraction_list) / len(distraction_list)
        distraction_std = (sum((x - distraction_mean) ** 2 for x in distraction_list) / len(distraction_list)) ** 0.5
        
        time_mean = sum(time_list) / len(time_list)
        time_std = (sum((x - time_mean) ** 2 for x in time_list) / len(time_list)) ** 0.5
        
        # Detect anomalies
        for activity in activities:
            activity_anomalies = []
            
            # Check marks anomaly
            if activity['marks_achieved_percent'] > 0:
                marks_z = abs(activity['marks_achieved_percent'] - marks_mean) / marks_std if marks_std > 0 else 0
                if marks_z > threshold_std:
                    activity_anomalies.append({
                        "type": "marks",
                        "value": activity['marks_achieved_percent'],
                        "expected": marks_mean,
                        "z_score": marks_z,
                        "description": f"Unusual marks: {activity['marks_achieved_percent']:.1f}% vs expected {marks_mean:.1f}%"
                    })
            
            # Check distraction anomaly
            distraction_z = abs(activity['distraction_score'] - distraction_mean) / distraction_std if distraction_std > 0 else 0
            if distraction_z > threshold_std:
                activity_anomalies.append({
                    "type": "distraction",
                    "value": activity['distraction_score'],
                    "expected": distraction_mean,
                    "z_score": distraction_z,
                    "description": f"Unusual distraction: {activity['distraction_score']:.1f} vs expected {distraction_mean:.1f}"
                })
            
            # Check time anomaly
            time_z = abs(activity['time_spent_mins'] - time_mean) / time_std if time_std > 0 else 0
            if time_z > threshold_std:
                activity_anomalies.append({
                    "type": "study_time",
                    "value": activity['time_spent_mins'],
                    "expected": time_mean,
                    "z_score": time_z,
                    "description": f"Unusual study time: {activity['time_spent_mins']} mins vs expected {time_mean:.1f} mins"
                })
            
            if activity_anomalies:
                anomalies.append({
                    "date": activity['date'],
                    "anomalies": activity_anomalies
                })
        
        # Summary statistics
        summary = {
            "total_activities_analyzed": len(activities),
            "total_anomalies_detected": len(anomalies),
            "anomaly_rate": len(anomalies) / len(activities) if activities else 0
        }
        
        return {
            "success": True,
            "student_id": student_id,
            "anomalies": anomalies,
            "summary": summary,
            "threshold_used": threshold_std
        }
    except Exception as e:
        return {"error": str(e)}

# ============================================
# TOOL 11: Data Quality Tools
# ============================================

def validate_student_data(student_id: str) -> Dict[str, Any]:
    """
    Validate student data quality and identify issues
    
    Args:
        student_id: Student identifier
    
    Returns:
        Data validation report with issues found
    """
    try:
        activities = get_student_activity_logs(student_id, days=90)
        
        if not activities:
            return {"error": "No data found for student"}
        
        issues = []
        warnings = []
        
        # Check for missing or invalid values
        for activity in activities:
            # Check for zero marks when time was spent
            if activity['time_spent_mins'] > 0 and activity['marks_achieved_percent'] == 0:
                issues.append({
                    "date": activity['date'],
                    "issue": "Zero marks with positive study time",
                    "severity": "high"
                })
            
            # Check for unrealistic distraction scores
            if not (0 <= activity['distraction_score'] <= 10):
                issues.append({
                    "date": activity['date'],
                    "issue": f"Invalid distraction score: {activity['distraction_score']}",
                    "severity": "high"
                })
            
            # Check for unrealistic marks
            if not (0 <= activity['marks_achieved_percent'] <= 100):
                issues.append({
                    "date": activity['date'],
                    "issue": f"Invalid marks: {activity['marks_achieved_percent']}",
                    "severity": "high"
                })
            
            # Check for very short study times
            if activity['time_spent_mins'] < 5:
                warnings.append({
                    "date": activity['date'],
                    "warning": f"Very short study time: {activity['time_spent_mins']} mins",
                    "severity": "low"
                })
            
            # Check for extremely long study times
            if activity['time_spent_mins'] > 300:
                warnings.append({
                    "date": activity['date'],
                    "warning": f"Extremely long study time: {activity['time_spent_mins']} mins",
                    "severity": "medium"
                })
        
        # Check for data gaps
        if len(activities) < 10:
            warnings.append({
                "warning": f"Low data volume: only {len(activities)} activities in 90 days",
                "severity": "medium"
            })
        
        # Calculate data quality score
        total_records = len(activities)
        issue_count = len(issues)
        warning_count = len(warnings)
        
        quality_score = max(0, 100 - (issue_count * 10) - (warning_count * 2))
        
        return {
            "success": True,
            "student_id": student_id,
            "total_records": total_records,
            "issues": issues,
            "warnings": warnings,
            "quality_score": quality_score,
            "data_quality": "Excellent" if quality_score >= 90 else "Good" if quality_score >= 70 else "Fair" if quality_score >= 50 else "Poor"
        }
    except Exception as e:
        return {"error": str(e)}

def clean_student_data(student_id: str) -> Dict[str, Any]:
    """
    Clean student data by fixing common issues
    
    Args:
        student_id: Student identifier
    
    Returns:
        Cleaning report with actions taken
    """
    try:
        validation = validate_student_data(student_id)
        
        if "error" in validation:
            return {"error": validation["error"]}
        
        actions_taken = []
        
        # Note: This is a read-only implementation that reports what would be cleaned
        # In production, you would actually update the database
        
        for issue in validation['issues']:
            if "Invalid distraction score" in issue['issue']:
                actions_taken.append(f"Would fix distraction score on {issue['date']}")
            elif "Invalid marks" in issue['issue']:
                actions_taken.append(f"Would fix marks on {issue['date']}")
            elif "Zero marks with positive study time" in issue['issue']:
                actions_taken.append(f"Would investigate zero marks on {issue['date']}")
        
        for warning in validation['warnings']:
            if "Very short study time" in warning['warning']:
                actions_taken.append(f"Would flag short study time on {warning['date']}")
        
        return {
            "success": True,
            "student_id": student_id,
            "issues_found": len(validation['issues']),
            "warnings_found": len(validation['warnings']),
            "actions_that_would_be_taken": actions_taken,
            "note": "This is a read-only analysis. Implement database updates for actual cleaning."
        }
    except Exception as e:
        return {"error": str(e)}

# ============================================
# TOOL 12: Calendar Integration Tools
# ============================================

def generate_calendar_event(student_id: str, event_type: str = "parent_meeting") -> Dict[str, Any]:
    """
    Generate calendar event data for scheduling
    
    Args:
        student_id: Student identifier
        event_type: Type of event (parent_meeting, staff_review, intervention_checkin)
    
    Returns:
        Calendar event data compatible with Google Calendar, Outlook, etc.
    """
    try:
        analysis = analyze_student_behavior(student_id)
        student_info = get_student_info(student_id)
        
        if "error" in analysis:
            return {"error": "Student not found"}
        
        student_name = student_info.get("name", "Student")
        
        if event_type == "parent_meeting":
            # Schedule parent-teacher meeting
            event = {
                "title": f"Parent-Teacher Meeting: {student_name}",
                "description": f"Discuss {student_name}'s progress and behavioral patterns. Current status: {analysis.get('behavioral_tag', 'Unknown')}, Avg Marks: {analysis.get('avg_marks', 0):.1f}%",
                "duration_minutes": 30,
                "location": "School - Room 101",
                "attendees": [
                    f"parent_of_{student_id}@example.com",
                    "teacher@school.edu"
                ],
                "suggested_times": [
                    {"date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"), "time": "10:00"},
                    {"date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"), "time": "14:00"},
                    {"date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"), "time": "09:00"}
                ],
                "urgency": "high" if analysis.get('behavioral_tag') == "High Flight Risk" else "medium"
            }
        
        elif event_type == "staff_review":
            # Schedule staff review meeting
            event = {
                "title": f"Staff Review: {student_name}",
                "description": f"Review intervention progress and next steps. Current distraction: {analysis.get('avg_distraction', 0):.1f}/10",
                "duration_minutes": 20,
                "location": "School - Staff Room",
                "attendees": [
                    "teacher@school.edu",
                    "counselor@school.edu"
                ],
                "suggested_times": [
                    {"date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"), "time": "08:30"},
                    {"date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"), "time": "15:00"}
                ],
                "urgency": "medium"
            }
        
        elif event_type == "intervention_checkin":
            # Schedule intervention check-in
            event = {
                "title": f"Intervention Check-in: {student_name}",
                "description": f"Monitor intervention effectiveness and adjust as needed. Focus: {analysis.get('behavioral_tag', 'Unknown')}",
                "duration_minutes": 15,
                "location": "School - Office",
                "attendees": [
                    "teacher@school.edu"
                ],
                "suggested_times": [
                    {"date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"), "time": "11:00"},
                    {"date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"), "time": "13:00"}
                ],
                "urgency": "low",
                "recurrence": "weekly"
            }
        
        else:
            return {"error": "Invalid event type"}
        
        return {
            "success": True,
            "student_id": student_id,
            "event_type": event_type,
            "calendar_event": event,
            "format": "ical_compatible"
        }
    except Exception as e:
        return {"error": str(e)}

def generate_recurring_schedule(student_id: str, frequency: str = "weekly") -> Dict[str, Any]:
    """
    Generate recurring schedule for student monitoring
    
    Args:
        student_id: Student identifier
        frequency: Recurrence frequency (weekly, biweekly, monthly)
    
    Returns:
        Recurring schedule data
    """
    try:
        analysis = analyze_student_behavior(student_id)
        student_info = get_student_info(student_id)
        
        if "error" in analysis:
            return {"error": "Student not found"}
        
        student_name = student_info.get("name", "Student")
        
        # Determine check-in frequency based on risk level
        if analysis.get('behavioral_tag') == 'High Flight Risk':
            recommended_frequency = 'weekly'
            checkin_duration = 15
        elif analysis.get('behavioral_tag') == 'Concept Comprehension Issue':
            recommended_frequency = 'biweekly'
            checkin_duration = 10
        else:
            recommended_frequency = 'monthly'
            checkin_duration = 10
        
        schedule = {
            "title": f"Student Check-in: {student_name}",
            "description": f"Regular monitoring check-in for {student_name}. Current status: {analysis.get('behavioral_tag', 'Unknown')}",
            "duration_minutes": checkin_duration,
            "frequency": recommended_frequency,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "attendees": ["teacher@school.edu"],
            "checkpoints": []
        }
        
        # Generate next 4 check-ins
        for i in range(1, 5):
            if recommended_frequency == 'weekly':
                checkin_date = datetime.now() + timedelta(weeks=i)
            elif recommended_frequency == 'biweekly':
                checkin_date = datetime.now() + timedelta(weeks=i*2)
            else:  # monthly
                checkin_date = datetime.now() + timedelta(days=i*30)
            
            schedule['checkpoints'].append({
                "number": i,
                "date": checkin_date.strftime("%Y-%m-%d"),
                "focus": f"Check-in #{i} - Monitor progress"
            })
        
        return {
            "success": True,
            "student_id": student_id,
            "schedule": schedule,
            "recommended_frequency": recommended_frequency
        }
    except Exception as e:
        return {"error": str(e)}

# ============================================
# TOOL 13: Export and Visualization Tools
# ============================================

def export_student_data_to_csv(student_id: str) -> Dict[str, Any]:
    """
    Export student activity data to CSV format
    
    Args:
        student_id: Student identifier
    
    Returns:
        CSV data string
    """
    try:
        activities = get_student_activity_logs(student_id, days=365)
        
        if not activities:
            return {"error": "No data found for student"}
        
        # Create CSV header
        csv_header = "ID,Student ID,Student Name,Date,Time Spent (mins),Distraction Score,Marks Achieved (%)"
        
        # Create CSV rows
        csv_rows = []
        for activity in activities:
            row = f"{activity['id']},{activity['student_id']},{activity['student_name']},{activity['date']},{activity['time_spent_mins']},{activity['distraction_score']},{activity['marks_achieved_percent']}"
            csv_rows.append(row)
        
        csv_data = csv_header + "\n" + "\n".join(csv_rows)
        
        return {
            "success": True,
            "student_id": student_id,
            "csv_data": csv_data,
            "row_count": len(csv_rows)
        }
    except Exception as e:
        return {"error": str(e)}

def export_class_data_to_csv() -> Dict[str, Any]:
    """
    Export all class data to CSV format
    
    Returns:
        CSV data string
    """
    try:
        conn = sqlite3.connect('behavior.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, student_id, student_name, date, time_spent_mins, 
                   distraction_score, marks_achieved_percent
            FROM student_activity
            ORDER BY student_id, date DESC
        """)
        
        activities = cursor.fetchall()
        conn.close()
        
        if not activities:
            return {"error": "No data found"}
        
        # Create CSV header
        csv_header = "ID,Student ID,Student Name,Date,Time Spent (mins),Distraction Score,Marks Achieved (%)"
        
        # Create CSV rows
        csv_rows = []
        for activity in activities:
            row = f"{activity[0]},{activity[1]},{activity[2]},{activity[3]},{activity[4]},{activity[5]},{activity[6]}"
            csv_rows.append(row)
        
        csv_data = csv_header + "\n" + "\n".join(csv_rows)
        
        return {
            "success": True,
            "csv_data": csv_data,
            "row_count": len(csv_rows)
        }
    except Exception as e:
        return {"error": str(e)}

def generate_student_chart_data(student_id: str, chart_type: str = "performance") -> Dict[str, Any]:
    """
    Generate data for student performance charts
    
    Args:
        student_id: Student identifier
        chart_type: Type of chart (performance, distraction, time)
    
    Returns:
        Chart data in JSON format
    """
    try:
        activities = get_student_activity_logs(student_id, days=30)
        
        if not activities:
            return {"error": "No data found for student"}
        
        # Sort by date ascending for chart
        activities_sorted = sorted(activities, key=lambda x: x['date'])
        
        if chart_type == "performance":
            labels = [a['date'] for a in activities_sorted]
            data = [a['marks_achieved_percent'] for a in activities_sorted]
            chart_title = "Performance Over Time"
            y_axis_label = "Marks Achieved (%)"
        elif chart_type == "distraction":
            labels = [a['date'] for a in activities_sorted]
            data = [a['distraction_score'] for a in activities_sorted]
            chart_title = "Distraction Score Over Time"
            y_axis_label = "Distraction Score (0-10)"
        elif chart_type == "time":
            labels = [a['date'] for a in activities_sorted]
            data = [a['time_spent_mins'] for a in activities_sorted]
            chart_title = "Study Time Over Time"
            y_axis_label = "Time Spent (minutes)"
        else:
            return {"error": "Invalid chart type"}
        
        return {
            "success": True,
            "student_id": student_id,
            "chart_type": chart_type,
            "chart_title": chart_title,
            "labels": labels,
            "data": data,
            "y_axis_label": y_axis_label
        }
    except Exception as e:
        return {"error": str(e)}

def generate_class_chart_data(chart_type: str = "comparison") -> Dict[str, Any]:
    """
    Generate data for class-wide charts
    
    Args:
        chart_type: Type of chart (comparison, distribution, trends)
    
    Returns:
        Chart data in JSON format
    """
    try:
        students = get_all_students()
        
        if not students:
            return {"error": "No students found"}
        
        if chart_type == "comparison":
            labels = [s['name'] for s in students]
            marks_data = []
            distraction_data = []
            
            for student in students:
                analysis = analyze_student(student['id'])
                if analysis:
                    marks_data.append(analysis['avg_marks'])
                    distraction_data.append(analysis['avg_distraction'])
            
            return {
                "success": True,
                "chart_type": "comparison",
                "chart_title": "Student Performance Comparison",
                "labels": labels,
                "marks_data": marks_data,
                "distraction_data": distraction_data
            }
        elif chart_type == "distribution":
            overview = get_class_overview()
            distribution = overview.get('behavioral_tag_distribution', {})
            
            labels = list(distribution.keys())
            data = list(distribution.values())
            
            return {
                "success": True,
                "chart_type": "distribution",
                "chart_title": "Behavioral Tag Distribution",
                "labels": labels,
                "data": data
            }
        else:
            return {"error": "Invalid chart type"}
    except Exception as e:
        return {"error": str(e)}

def generate_report_summary_text(student_id: str) -> Dict[str, Any]:
    """
    Generate comprehensive text summary for report
    
    Args:
        student_id: Student identifier
    
    Returns:
        Text summary
    """
    try:
        analysis = analyze_student_behavior(student_id)
        
        if "error" in analysis:
            return analysis
        
        # Generate LLM report for each agent
        behavior_report = generate_llm_agent_report("behavior", analysis)
        learning_path = create_learning_path(student_id)
        learning_report = generate_llm_agent_report("learning_path", learning_path)
        intervention = suggest_intervention(student_id)
        intervention_report = generate_llm_agent_report("intervention", intervention)
        
        # Combine into comprehensive summary
        summary = f"""
STUDENT BEHAVIOR ANALYSIS REPORT
================================
Student ID: {analysis.get('student_id', 'Unknown')}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

BEHAVIORAL ANALYSIS
------------------
{behavior_report or "Analysis not available"}

LEARNING PATH
-------------
{learning_report or "Learning path not available"}

INTERVENTION PLAN
-----------------
{intervention_report or "Intervention plan not available"}

KEY METRICS
-----------
Total Study Time: {analysis.get('total_study_time', 0)} minutes
Average Distraction: {analysis.get('avg_distraction', 0)}/10
Average Marks: {analysis.get('avg_marks', 0)}%
Behavioral Tag: {analysis.get('behavioral_tag', 'Unknown')}
Marks Trend: {analysis.get('marks_trend', 0)}%
"""
        
        return {
            "success": True,
            "student_id": student_id,
            "summary_text": summary,
            "analysis": analysis,
            "learning_path": learning_path,
            "intervention": intervention
        }
    except Exception as e:
        return {"error": str(e)}

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
    ],
    "export_tools": [
        {
            "name": "export_student_data_to_csv",
            "description": "Export student activity data to CSV format",
            "parameters": {
                "student_id": {"type": "string", "required": True}
            }
        },
        {
            "name": "export_class_data_to_csv",
            "description": "Export all class data to CSV format",
            "parameters": {}
        }
    ],
    "visualization_tools": [
        {
            "name": "generate_student_chart_data",
            "description": "Generate data for student performance charts",
            "parameters": {
                "student_id": {"type": "string", "required": True},
                "chart_type": {"type": "string", "required": False, "default": "performance"}
            }
        },
        {
            "name": "generate_class_chart_data",
            "description": "Generate data for class-wide charts",
            "parameters": {
                "chart_type": {"type": "string", "required": False, "default": "comparison"}
            }
        }
    ],
    "report_tools": [
        {
            "name": "generate_report_summary_text",
            "description": "Generate comprehensive text summary for report",
            "parameters": {
                "student_id": {"type": "string", "required": True}
            }
        }
    ],
    "communication_tools": [
        {
            "name": "generate_parent_email",
            "description": "Generate email content for parent communication",
            "parameters": {
                "student_id": {"type": "string", "required": True},
                "email_type": {"type": "string", "required": False, "default": "report"}
            }
        },
        {
            "name": "generate_staff_notification",
            "description": "Generate notification content for staff/teachers",
            "parameters": {
                "student_id": {"type": "string", "required": True},
                "notification_type": {"type": "string", "required": False, "default": "intervention"}
            }
        }
    ],
    "task_management_tools": [
        {
            "name": "create_intervention_task",
            "description": "Create a task for intervention implementation",
            "parameters": {
                "student_id": {"type": "string", "required": True},
                "assigned_to": {"type": "string", "required": True},
                "due_date": {"type": "string", "required": False}
            }
        },
        {
            "name": "create_monitoring_task",
            "description": "Create a task for ongoing student monitoring",
            "parameters": {
                "student_id": {"type": "string", "required": True},
                "assigned_to": {"type": "string", "required": True},
                "monitoring_period_days": {"type": "integer", "required": False, "default": 30}
            }
        },
        {
            "name": "update_task_status",
            "description": "Update task status and add notes",
            "parameters": {
                "task_id": {"type": "string", "required": True},
                "status": {"type": "string", "required": True},
                "notes": {"type": "string", "required": False}
            }
        },
        {
            "name": "get_assigned_tasks",
            "description": "Get all tasks assigned to a specific person",
            "parameters": {
                "assigned_to": {"type": "string", "required": True}
            }
        },
        {
            "name": "get_student_tasks",
            "description": "Get all tasks for a specific student",
            "parameters": {
                "student_id": {"type": "string", "required": True}
            }
        },
        {
            "name": "get_overdue_tasks",
            "description": "Get all overdue tasks",
            "parameters": {}
        }
    ],
    "document_generation_tools": [
        {
            "name": "generate_pdf_report_content",
            "description": "Generate structured content for PDF report",
            "parameters": {
                "student_id": {"type": "string", "required": True}
            }
        },
        {
            "name": "generate_meeting_agenda",
            "description": "Generate agenda for parent-teacher or staff meeting",
            "parameters": {
                "student_id": {"type": "string", "required": True},
                "meeting_type": {"type": "string", "required": False, "default": "parent_teacher"}
            }
        }
    ],
    "advanced_analytics_tools": [
        {
            "name": "predict_student_performance",
            "description": "Predict future student performance based on historical trends",
            "parameters": {
                "student_id": {"type": "string", "required": True},
                "days_ahead": {"type": "integer", "required": False, "default": 30}
            }
        },
        {
            "name": "detect_anomalies",
            "description": "Detect anomalous behavior patterns in student data",
            "parameters": {
                "student_id": {"type": "string", "required": True},
                "threshold_std": {"type": "float", "required": False, "default": 2.0}
            }
        }
    ],
    "data_quality_tools": [
        {
            "name": "validate_student_data",
            "description": "Validate student data quality and identify issues",
            "parameters": {
                "student_id": {"type": "string", "required": True}
            }
        },
        {
            "name": "clean_student_data",
            "description": "Clean student data by fixing common issues",
            "parameters": {
                "student_id": {"type": "string", "required": True}
            }
        }
    ],
    "calendar_tools": [
        {
            "name": "generate_calendar_event",
            "description": "Generate calendar event data for scheduling",
            "parameters": {
                "student_id": {"type": "string", "required": True},
                "event_type": {"type": "string", "required": False, "default": "parent_meeting"}
            }
        },
        {
            "name": "generate_recurring_schedule",
            "description": "Generate recurring schedule for student monitoring",
            "parameters": {
                "student_id": {"type": "string", "required": True},
                "frequency": {"type": "string", "required": False, "default": "weekly"}
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
