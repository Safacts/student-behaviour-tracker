from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sqlite3
import uvicorn

from analyzer import analyze_student
from llm_service import generate_parent_report

app = FastAPI(title="Student Behavior Analysis PoC")

@app.get("/api/students")
def get_students():
    conn = sqlite3.connect('behavior.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT student_id, student_name FROM student_activity")
    students = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    conn.close()
    return students

@app.get("/api/activity-logs")
def get_activity_logs():
    conn = sqlite3.connect('behavior.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student_activity ORDER BY date DESC, id DESC")
    columns = [column[0] for column in cursor.description]
    logs = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return logs

@app.get("/api/report/{student_id}")
def get_report(student_id: str):
    # 1. Run Analysis
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

    # 2. Call LLM for empathetic report
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

# Serve the index.html
@app.get("/")
def read_root():
    return FileResponse("index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
