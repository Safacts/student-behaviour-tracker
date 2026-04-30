"""
Test suite for V2 API endpoints with authentication and rate limiting
"""
import pytest
import requests
import time

BASE_URL = "http://localhost:8000"

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_generate_token(self):
        """Test token generation"""
        response = requests.get(f"{BASE_URL}/api/auth/token?user_id=T001")
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert data["success"] == True
        return data["token"]
    
    def test_auth_stats(self):
        """Test auth statistics"""
        response = requests.get(f"{BASE_URL}/api/auth/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_api_keys" in data
        assert "active_sessions" in data

class TestV2TaskEndpoints:
    """Test V2 task management endpoints"""
    
    def test_create_intervention_without_auth(self):
        """Test that endpoint requires authentication"""
        response = requests.get(f"{BASE_URL}/api/v2/tasks/create/intervention?student_id=S001&priority=high")
        assert response.status_code == 401
    
    def test_create_intervention_with_auth(self):
        """Test creating intervention task with authentication"""
        # Generate token
        token_response = requests.get(f"{BASE_URL}/api/auth/token?user_id=T001")
        token = token_response.json()["token"]
        
        # Create task
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/api/v2/tasks/create/intervention?student_id=S001&priority=high&assigned_to=T001",
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "task_id" in data
        return data["task_id"]
    
    def test_create_monitoring_with_auth(self):
        """Test creating monitoring task with authentication"""
        token_response = requests.get(f"{BASE_URL}/api/auth/token?user_id=T001")
        token = token_response.json()["token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/api/v2/tasks/create/monitoring?student_id=S001&assigned_to=T001&monitoring_period_days=30",
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
    
    def test_get_assigned_tasks_with_auth(self):
        """Test getting assigned tasks with authentication"""
        token_response = requests.get(f"{BASE_URL}/api/auth/token?user_id=T001")
        token = token_response.json()["token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v2/tasks/assigned/T001", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
    
    def test_get_student_tasks_with_auth(self):
        """Test getting student tasks with authentication"""
        token_response = requests.get(f"{BASE_URL}/api/auth/token?user_id=T001")
        token = token_response.json()["token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v2/tasks/student/S001", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
    
    def test_get_overdue_tasks_with_auth(self):
        """Test getting overdue tasks with authentication"""
        token_response = requests.get(f"{BASE_URL}/api/auth/token?user_id=T001")
        token = token_response.json()["token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v2/tasks/overdue", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data

class TestV2TeacherEndpoints:
    """Test V2 teacher assignment endpoints"""
    
    def test_assign_teacher_with_auth(self):
        """Test assigning teacher with authentication"""
        token_response = requests.get(f"{BASE_URL}/api/auth/token?user_id=T001")
        token = token_response.json()["token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/api/v2/teacher/assign?student_id=S001&teacher_id=T002&subject=Physics",
            headers=headers
        )
        assert response.status_code in [200, 409]  # 409 if already exists
    
    def test_get_teacher_responsibilities_with_auth(self):
        """Test getting teacher responsibilities with authentication"""
        token_response = requests.get(f"{BASE_URL}/api/auth/token?user_id=T001")
        token = token_response.json()["token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v2/teacher/responsibilities/T001", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "assignments" in data

class TestRateLimiting:
    """Test rate limiting"""
    
    def test_rate_limit(self):
        """Test that rate limiting works"""
        token_response = requests.get(f"{BASE_URL}/api/auth/token?user_id=T001")
        token = token_response.json()["token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Make 101 requests to exceed the rate limit (100 per minute)
        for i in range(101):
            response = requests.get(f"{BASE_URL}/api/v2/tasks/overdue", headers=headers)
            if response.status_code == 429:
                break
        
        # Last request should be rate limited
        assert response.status_code == 429

class TestInputValidation:
    """Test input validation"""
    
    def test_invalid_student_id(self):
        """Test that invalid student ID is rejected"""
        token_response = requests.get(f"{BASE_URL}/api/auth/token?user_id=T001")
        token = token_response.json()["token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/api/v2/tasks/create/intervention?student_id=invalid&priority=high",
            headers=headers
        )
        assert response.status_code == 400
    
    def test_invalid_priority(self):
        """Test that invalid priority is rejected"""
        token_response = requests.get(f"{BASE_URL}/api/auth/token?user_id=T001")
        token = token_response.json()["token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/api/v2/tasks/create/intervention?student_id=S001&priority=invalid",
            headers=headers
        )
        assert response.status_code == 400
    
    def test_missing_required_parameter(self):
        """Test that missing required parameter is rejected"""
        token_response = requests.get(f"{BASE_URL}/api/auth/token?user_id=T001")
        token = token_response.json()["token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/api/v2/tasks/create/monitoring?student_id=S001&monitoring_period_days=30",
            headers=headers
        )
        assert response.status_code == 400

if __name__ == "__main__":
    print("Running V2 endpoint tests...")
    pytest.main([__file__, "-v"])
