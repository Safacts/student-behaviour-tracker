from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sqlite3
import json
import os
from typing import List, Optional
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = FastAPI(title="Student Behavior Analysis API")

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("WARNING: GOOGLE_API_KEY not found in environment. AI reports will fallback to mock.")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "students_analysis.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/tables")
def list_tables():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row["name"] for row in cursor.fetchall()]
    conn.close()
    return {"tables": tables}

@app.get("/data/{table_name}")
def get_table_data(table_name: str, limit: int = 100, offset: int = 0):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT ? OFFSET ?", (limit, offset))
        rows = [dict(row) for row in cursor.fetchall()]
        cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
        total = cursor.fetchone()["count"]
        conn.close()
        return {"data": rows, "total": total, "limit": limit, "offset": offset}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/analytics/summary")
def get_summary_stats():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT student_id) FROM rubix_students_data")
    total_students = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM student_session_analytics")
    total_sessions = cursor.fetchone()[0]
    cursor.execute("SELECT AVG(time_spent_minutes) FROM student_session_analytics WHERE time_spent_minutes > 0")
    avg_time = cursor.fetchone()[0]
    cursor.execute("SELECT subject_category, COUNT(*) as count FROM student_session_analytics GROUP BY subject_category ORDER BY count DESC")
    subjects = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"total_students": total_students, "total_sessions": total_sessions, "avg_time_minutes": round(avg_time, 2) if avg_time else 0, "subject_distribution": subjects}

@app.get("/analytics/top_students")
def get_top_students(limit: int = 5):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.name, SUM(s.time_spent_minutes) as total_time
        FROM student_session_analytics s
        JOIN users u ON s.student_id = u.id
        GROUP BY u.id
        ORDER BY total_time DESC
        LIMIT ?
    """, (limit,))
    top_students = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"top_students": top_students}

@app.get("/analytics/student/{student_id}")
def get_student_analysis(student_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (student_id,))
    user = cursor.fetchone()
    user_info = dict(user) if user else {"name": f"Student {student_id}"}
    cursor.execute("SELECT log_date, COUNT(*) as count, SUM(time_spent_minutes) as total_minutes FROM student_session_analytics WHERE student_id = ? AND (log_date LIKE '2026-03-%' OR log_date LIKE '2026-04-%') GROUP BY log_date ORDER BY log_date ASC", (student_id,))
    time_series = [dict(row) for row in cursor.fetchall()]
    cursor.execute("SELECT subject_category, COUNT(*) as count, AVG(time_spent_minutes) as avg_minutes FROM student_session_analytics WHERE student_id = ? GROUP BY subject_category", (student_id,))
    subject_stats = [dict(row) for row in cursor.fetchall()]
    cursor.execute("SELECT * FROM student_session_analytics WHERE student_id = ? ORDER BY log_date DESC, id DESC LIMIT 50", (student_id,))
    recent_sessions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"student": user_info, "time_series": time_series, "subject_stats": subject_stats, "recent_sessions": recent_sessions}

def parse_score(score_str: Optional[str]) -> Optional[float]:
    if not score_str: return None
    try:
        if '/' in score_str:
            parts = score_str.split('/')
            return float(parts[0]) / float(parts[1])
        return float(score_str) / 10.0
    except: return None

def generate_llm_report(metrics: dict):
    """Calls Gemini API to generate a professional parent report."""
    study_time = metrics['study_time']
    game_time = metrics['game_time']
    subjects = ", ".join(metrics['subjects'])
    quiz_score = f"{round(metrics['avg_score'] * 100)}%" if metrics['avg_score'] else "N/A"
    
    prompt = f"""
    Act as an elite educational behavioral analyst. Write a structured intelligence report for a student's parent.
    
    Data for the week:
    - Total Focus Time: {study_time} mins
    - Recreational/Game Time: {game_time} mins
    - Covered Domains: {subjects}
    - Proficiency Rating (Avg Quiz): {quiz_score}

    [INTELLIGENCE_SUMMARY]
    Write a single, high-fidelity paragraph that objectively analyzes the student's performance. 
    1. Detail their current engagement level and behavioral trends (how they were).
    2. Identify specific academic or behavioral gaps (where they are lacking).
    3. Provide clear, empathetic, and actionable advice for the parent to help the student overcome these issues (what parents should do).
    
    Keep the tone professional, insightful, and concise. Avoid generic encouragement; focus on the data provided.
    """

    try:
        # Fallback if no API key
        if not os.getenv("GOOGLE_API_KEY"):
            return "Unable to connect to Gemini: GOOGLE_API_KEY missing."

        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return f"AI Report generation temporary unavailable. Technical details: {str(e)}"

@app.get("/analytics/generate_report/{student_id}")
def generate_student_report(student_id: int):
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Get the last 7 available days for this student
    cursor.execute("""
        SELECT DISTINCT log_date 
        FROM student_session_analytics 
        WHERE student_id = ? 
        ORDER BY log_date DESC LIMIT 7
    """, (student_id,))
    dates = [row["log_date"] for row in cursor.fetchall()]
    
    if not dates:
        conn.close()
        raise HTTPException(status_code=404, detail="No activity data found for this student.")
    
    start_date = dates[-1]
    end_date = dates[0]

    # 2. Aggregations
    cursor.execute("""
        SELECT 
            SUM(time_spent_minutes) as total_time,
            SUM(CASE WHEN subject_category = 'gam' THEN time_spent_minutes ELSE 0 END) as game_time,
            GROUP_CONCAT(DISTINCT subject_category) as subjects
        FROM student_session_analytics
        WHERE student_id = ? AND log_date BETWEEN ? AND ?
    """, (student_id, start_date, end_date))
    agg = cursor.fetchone()
    
    # 3. Quiz Score Avg
    cursor.execute("""
        SELECT quiz_score 
        FROM student_session_analytics 
        WHERE student_id = ? AND log_date BETWEEN ? AND ? AND quiz_score != '' AND quiz_score IS NOT NULL
    """, (student_id, start_date, end_date))
    scores = [parse_score(row["quiz_score"]) for row in cursor.fetchall()]
    valid_scores = [s for s in scores if s is not None]
    avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0

    metrics = {
        "study_time": agg["total_time"] or 0,
        "game_time": agg["game_time"] or 0,
        "subjects": (agg["subjects"] or "").split(","),
        "avg_score": avg_score
    }
    
    report_text = generate_llm_report(metrics)
    conn.close()
    
    return {
        "metrics": metrics,
        "report": report_text,
        "period": {"start": start_date, "end": end_date}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
