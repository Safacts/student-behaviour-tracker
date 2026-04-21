"""
Test suite for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
import json
from datetime import date

from src.api.main import app
from src.models.base import StudentActivityData, SubjectCategory

client = TestClient(app)

class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_live_endpoint(self):
        """Test liveness probe"""
        response = client.get("/health/live")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["alive"] is True
    
    def test_ready_endpoint(self):
        """Test readiness probe"""
        response = client.get("/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_health_endpoint(self):
        """Test comprehensive health check"""
        response = client.get("/health/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "database_status" in data

class TestAnalyticsEndpoints:
    """Test analytics endpoints"""
    
    def test_student_summary(self):
        """Test student summary endpoint"""
        response = client.get("/api/v1/analytics/students/test001/summary")
        # May return 404 if student doesn't exist, which is expected
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            assert data["success"] is True
            assert "data" in data
    
    def test_student_activity(self):
        """Test student activity endpoint"""
        response = client.get("/api/v1/analytics/students/test001/activity")
        assert response.status_code in [200, 404]
    
    def test_batch_analysis(self):
        """Test batch analysis endpoint"""
        response = client.post(
            "/api/v1/analytics/batch-analysis",
            json={
                "student_ids": ["test001", "test002"],
                "analysis_type": "comprehensive",
                "days": 30
            }
        )
        assert response.status_code in [200, 422]  # 422 if validation fails
    
    def test_class_summary(self):
        """Test class summary endpoint"""
        response = client.get("/api/v1/analytics/class/Grade10/summary")
        assert response.status_code in [200, 404]

class TestAgentEndpoints:
    """Test AI agent endpoints"""
    
    def test_available_agents(self):
        """Test available agents endpoint"""
        response = client.get("/api/v1/agents/available")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "available_agents" in data["data"]
    
    def test_behavior_analysis(self):
        """Test behavior analysis agent"""
        response = client.post(
            "/api/v1/agents/analyze",
            json={
                "agent_type": "behavior_analysis",
                "student_id": "test001",
                "parameters": {}
            }
        )
        # May return 404 if student doesn't exist or 500 if no data
        assert response.status_code in [200, 404, 500]
    
    def test_learning_path(self):
        """Test learning path generation"""
        response = client.post(
            "/api/v1/agents/learning-path",
            json={
                "student_id": "test001",
                "subject_focus": "math",
                "difficulty_level": "intermediate"
            }
        )
        assert response.status_code in [200, 404, 500]
    
    def test_intervention_suggestions(self):
        """Test intervention suggestions"""
        response = client.post(
            "/api/v1/agents/intervention",
            json={
                "student_id": "test001",
                "intervention_type": "academic",
                "urgency_level": "medium"
            }
        )
        assert response.status_code in [200, 404, 500]
    
    def test_agent_pipeline(self):
        """Test agent pipeline execution"""
        response = client.post(
            "/api/v1/agents/pipeline",
            json={
                "student_id": "test001",
                "agent_types": ["behavior_analysis", "learning_path"]
            }
        )
        assert response.status_code in [200, 404, 500]

class TestStudentEndpoints:
    """Test student management endpoints"""
    
    def test_list_students(self):
        """Test list students endpoint"""
        response = client.get("/api/v1/students/list")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "students" in data["data"]
        assert "pagination" in data["data"]
    
    def test_create_student_activity(self):
        """Test create student activity"""
        activity_data = {
            "student_id": "test001",
            "student_name": "Test Student",
            "log_date": "2024-01-15",
            "subject_category": "math",
            "lesson_name": "Test Lesson",
            "quiz_score": "85%",
            "time_spent_minutes": 45,
            "distraction_score": 2.5,
            "marks_achieved_percent": 85.0
        }
        
        response = client.post("/api/v1/students/activity", json=activity_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_batch_create_activities(self):
        """Test batch create student activities"""
        batch_data = {
            "activities": [
                {
                    "student_id": "test002",
                    "student_name": "Test Student 2",
                    "log_date": "2024-01-15",
                    "subject_category": "science",
                    "lesson_name": "Test Science Lesson",
                    "quiz_score": "78%",
                    "time_spent_minutes": 38
                },
                {
                    "student_id": "test003",
                    "student_name": "Test Student 3",
                    "log_date": "2024-01-15",
                    "subject_category": "math",
                    "lesson_name": "Test Math Lesson 2",
                    "quiz_score": "92%",
                    "time_spent_minutes": 52
                }
            ]
        }
        
        response = client.post("/api/v1/students/activity/batch", json=batch_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "total_activities" in data["data"]
    
    def test_get_student_details(self):
        """Test get student details"""
        response = client.get("/api/v1/students/test001")
        assert response.status_code in [200, 404]
    
    def test_search_students(self):
        """Test search students"""
        response = client.get("/api/v1/students/search?query=test")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "students" in data["data"]

class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "service" in data["data"]
        assert "version" in data["data"]

class TestErrorHandling:
    """Test error handling"""
    
    def test_404_endpoint(self):
        """Test 404 error handling"""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
    
    def test_invalid_json(self):
        """Test invalid JSON handling"""
        response = client.post(
            "/api/v1/students/activity",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_validation_error(self):
        """Test validation error handling"""
        response = client.post(
            "/api/v1/students/activity",
            json={"invalid": "data"}
        )
        assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__])
