import sqlite3
import random
from datetime import datetime, timedelta

def generate_data():
    conn = sqlite3.connect('behavior.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            student_name TEXT,
            activity_type TEXT,
            subject TEXT,
            topic TEXT,
            chapter TEXT,
            time_spent_mins INTEGER,
            marks_achieved_percent REAL,
            distraction_score INTEGER,
            date TEXT
        )
    ''')

    # Clear old data
    cursor.execute('DELETE FROM student_activity')

    students = [
        {"id": "S001", "name": "Alex", "persona": "distracted"},
        {"id": "S002", "name": "Bella", "persona": "hard_worker"},
        {"id": "S003", "name": "Charlie", "persona": "high_achiever"}
    ]

    activities = ["Lesson Concept", "Practice Questions", "Quiz", "Chess Play", "Games", "Community Chat"]
    
    subjects = ["Physics", "Chemistry", "Mathematics", "Biology", "English"]
    
    topics = {
        "Physics": ["Mechanics", "Electricity", "Optics", "Thermodynamics"],
        "Chemistry": ["Organic Chemistry", "Physical Chemistry", "Inorganic Chemistry"],
        "Mathematics": ["Algebra", "Calculus", "Geometry", "Trigonometry"],
        "Biology": ["Cell Biology", "Genetics", "Ecology"],
        "English": ["Grammar", "Literature", "Writing"]
    }
    
    chapters = {
        "Physics": ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4"],
        "Chemistry": ["Chapter 1", "Chapter 2", "Chapter 3"],
        "Mathematics": ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4"],
        "Biology": ["Chapter 1", "Chapter 2", "Chapter 3"],
        "English": ["Chapter 1", "Chapter 2", "Chapter 3"]
    }
    
    start_date = datetime.now() - timedelta(days=7)

    for day in range(8):  # 7 days + today
        current_date = (start_date + timedelta(days=day)).strftime('%Y-%m-%d')
        
        for student in students:
            # Each student does 3-5 activities per day
            num_activities = random.randint(3, 5)
            
            for _ in range(num_activities):
                activity = random.choice(activities)
                subject = random.choice(subjects)
                topic = random.choice(topics[subject])
                chapter = random.choice(chapters[subject])
                
                # Default values
                time_spent = random.randint(20, 60)
                marks = random.randint(40, 95)
                distraction = random.randint(1, 5)

                # Apply Persona Logic
                if student["persona"] == "distracted":
                    if activity in ["Games", "Community Chat"]:
                        time_spent = random.randint(60, 120)
                        distraction = random.randint(8, 10)
                        marks = 0
                    elif activity in ["Lesson Concept", "Quiz"]:
                        distraction = random.randint(7, 10)
                        marks = random.randint(20, 50)
                
                elif student["persona"] == "hard_worker":
                    if activity in ["Lesson Concept", "Practice Questions"]:
                        time_spent = random.randint(80, 150)
                        distraction = 0 # As requested: zero distraction
                        # Low marks on "IIT-JEE" prep (represented by Quiz/Practice)
                        marks = random.randint(30, 55)
                    elif activity in ["Games", "Chess Play"]:
                        # Hard workers don't spend much time here
                        time_spent = random.randint(5, 15)
                        distraction = 0
                
                elif student["persona"] == "high_achiever":
                    distraction = random.randint(1, 2)
                    marks = random.randint(85, 98)
                    if activity == "Chess Play":
                        time_spent = random.randint(60, 120) # 1-2 hours of Chess
                    else:
                        time_spent = random.randint(45, 90)

                cursor.execute('''
                    INSERT INTO student_activity 
                    (student_id, student_name, activity_type, subject, topic, chapter, time_spent_mins, marks_achieved_percent, distraction_score, date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (student["id"], student["name"], activity, subject, topic, chapter, time_spent, marks, distraction, current_date))

    conn.commit()
    conn.close()
    print("Synthetic data generated successfully in behavior.db")

if __name__ == "__main__":
    generate_data()
