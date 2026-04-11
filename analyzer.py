import sqlite3

def analyze_student(student_id):
    conn = sqlite3.connect('behavior.db')
    cursor = conn.cursor()

    # Aggregate stats for the last 7 days (or all data for now)
    cursor.execute('''
        SELECT 
            SUM(time_spent_mins) as total_time,
            AVG(distraction_score) as avg_distraction,
            AVG(marks_achieved_percent) as avg_marks
        FROM student_activity
        WHERE student_id = ?
    ''', (student_id,))
    
    stats = cursor.fetchone()
    conn.close()

    if not stats or stats[0] is None:
        return None

    total_time, avg_distraction, avg_marks = stats

    # Heuristic Logic
    behavioral_tag = "On Track"
    
    if avg_distraction > 5:
        behavioral_tag = "High Flight Risk"
    elif avg_marks < 75 and avg_distraction < 3:
        behavioral_tag = "Concept Comprehension Issue"
    elif avg_marks >= 85:
        behavioral_tag = "On Track"

    return {
        "student_id": student_id,
        "total_study_time": total_time,
        "avg_distraction": round(avg_distraction, 2),
        "avg_marks": round(avg_marks, 2),
        "behavioral_tag": behavioral_tag
    }

if __name__ == "__main__":
    # Test
    print(analyze_student("S001"))
    print(analyze_student("S002"))
    print(analyze_student("S003"))
