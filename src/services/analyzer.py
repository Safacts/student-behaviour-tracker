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

    if not stats or stats[0] is None:
        conn.close()
        return None

    total_time, avg_distraction, avg_marks = stats

    # Get subject-wise performance
    cursor.execute('''
        SELECT 
            subject,
            AVG(marks_achieved_percent) as avg_marks,
            AVG(distraction_score) as avg_distraction,
            SUM(time_spent_mins) as total_time
        FROM student_activity
        WHERE student_id = ?
        GROUP BY subject
    ''', (student_id,))
    
    subject_stats = cursor.fetchall()
    conn.close()

    # Build subject performance data
    subject_performance = {}
    weak_subjects = []
    strong_subjects = []
    
    for subject, marks, distraction, time_spent in subject_stats:
        subject_performance[subject] = round(marks, 1)
        if marks < 50:
            weak_subjects.append(subject)
        elif marks > 75:
            strong_subjects.append(subject)

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
        "behavioral_tag": behavioral_tag,
        "subject_performance": subject_performance,
        "weak_subjects": weak_subjects,
        "strong_subjects": strong_subjects
    }

if __name__ == "__main__":
    # Test
    print(analyze_student("S001"))
    print(analyze_student("S002"))
    print(analyze_student("S003"))
