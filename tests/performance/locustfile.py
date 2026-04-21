"""
Locust performance testing file for Student Behavior Analytics API
"""
from locust import HttpUser, task, between
import json
import random

class StudentBehaviorUser(HttpUser):
    """Simulated user for load testing the Student Behavior Analytics API"""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Called when a simulated user starts"""
        # Test health endpoint first
        self.client.get("/health/live")
        
        # Get list of students
        response = self.client.get("/api/v1/students/list")
        if response.status_code == 200:
            data = response.json()
            self.students = data.get("data", {}).get("students", [])
        else:
            self.students = []
    
    @task(3)
    def get_student_summary(self):
        """Get student summary - high frequency task"""
        if self.students:
            student_id = random.choice(self.students).get("student_id", "test001")
            self.client.get(f"/api/v1/analytics/students/{student_id}/summary")
    
    @task(2)
    def get_student_activity(self):
        """Get student activity - medium frequency task"""
        if self.students:
            student_id = random.choice(self.students).get("student_id", "test001")
            self.client.get(f"/api/v1/analytics/students/{student_id}/activity")
    
    @task(2)
    def get_student_trends(self):
        """Get student trends - medium frequency task"""
        if self.students:
            student_id = random.choice(self.students).get("student_id", "test001")
            self.client.get(f"/api/v1/analytics/students/{student_id}/trends")
    
    @task(1)
    def run_behavior_analysis(self):
        """Run behavior analysis agent - lower frequency task"""
        if self.students:
            student_id = random.choice(self.students).get("student_id", "test001")
            self.client.post(
                "/api/v1/agents/analyze",
                json={
                    "agent_type": "behavior_analysis",
                    "student_id": student_id,
                    "parameters": {}
                }
            )
    
    @task(1)
    def run_learning_path(self):
        """Run learning path agent - lower frequency task"""
        if self.students:
            student_id = random.choice(self.students).get("student_id", "test001")
            self.client.post(
                "/api/v1/agents/learning-path",
                json={
                    "student_id": student_id,
                    "subject_focus": random.choice(["math", "science", "english"]),
                    "difficulty_level": random.choice(["beginner", "intermediate", "advanced"])
                }
            )
    
    @task(1)
    def create_student_activity(self):
        """Create student activity - lower frequency task"""
        student_id = f"test_user_{random.randint(1000, 9999)}"
        self.client.post(
            "/api/v1/students/activity",
            json={
                "student_id": student_id,
                "student_name": f"Test Student {random.randint(1000, 9999)}",
                "log_date": "2024-01-15",
                "subject_category": random.choice(["math", "science", "english", "history"]),
                "lesson_name": f"Test Lesson {random.randint(1, 100)}",
                "quiz_score": f"{random.randint(60, 95)}%",
                "time_spent_minutes": random.randint(20, 90),
                "distraction_score": round(random.uniform(1.0, 5.0), 1),
                "marks_achieved_percent": random.randint(60, 95)
            }
        )
    
    @task(1)
    def get_available_agents(self):
        """Get available agents - informational task"""
        self.client.get("/api/v1/agents/available")
    
    @task(1)
    def get_class_summary(self):
        """Get class summary - informational task"""
        class_names = ["Grade10", "Grade11", "Grade12", "ClassA", "ClassB"]
        class_name = random.choice(class_names)
        self.client.get(f"/api/v1/analytics/class/{class_name}/summary")

class AdminUser(HttpUser):
    """Simulated admin user for testing admin endpoints"""
    
    wait_time = between(2, 5)
    weight = 1  # Lower weight compared to regular users
    
    def on_start(self):
        """Called when admin user starts"""
        self.client.get("/health/")
    
    @task(2)
    def health_check(self):
        """Perform health checks"""
        self.client.get("/health/live")
        self.client.get("/health/ready")
        self.client.get("/health/")
    
    @task(1)
    def get_metrics(self):
        """Get application metrics"""
        self.client.get("/metrics")
    
    @task(1)
    def batch_analysis(self):
        """Run batch analysis"""
        self.client.post(
            "/api/v1/analytics/batch-analysis",
            json={
                "student_ids": ["test001", "test002", "test003"],
                "analysis_type": "comprehensive",
                "days": 30
            }
        )
    
    @task(1)
    def agent_pipeline(self):
        """Run agent pipeline"""
        if hasattr(self, 'students') and self.students:
            student_id = random.choice(self.students).get("student_id", "test001")
            self.client.post(
                "/api/v1/agents/pipeline",
                json={
                    "student_id": student_id,
                    "agent_types": ["behavior_analysis", "learning_path", "intervention"]
                }
            )

class LegacyUser(HttpUser):
    """Simulated user for testing legacy endpoints"""
    
    wait_time = between(1, 4)
    weight = 0.5  # Lower weight for legacy endpoints
    
    @task(3)
    def get_legacy_students(self):
        """Get students using legacy endpoint"""
        self.client.get("/api/students")
    
    @task(2)
    def get_legacy_activity(self):
        """Get activity logs using legacy endpoint"""
        self.client.get("/api/activity-logs")
    
    @task(1)
    def get_legacy_report(self):
        """Get report using legacy endpoint"""
        student_ids = ["S001", "S002", "S003", "test001"]
        student_id = random.choice(student_ids)
        self.client.get(f"/api/report/{student_id}")
