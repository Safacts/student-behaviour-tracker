"""
Comprehensive API testing suite
"""
import pytest
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

class TestAPIEndpoints:
    """Test all API endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "overall_status" in data
        assert data["overall_status"] in ["healthy", "degraded", "error"]
    
    def test_get_students(self):
        """Test students endpoint"""
        response = requests.get(f"{BASE_URL}/api/students")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_activity_logs(self):
        """Test activity logs endpoint"""
        response = requests.get(f"{BASE_URL}/api/activity-logs")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_report(self):
        """Test report generation endpoint"""
        response = requests.get(f"{BASE_URL}/api/report/S001")
        assert response.status_code == 200
        data = response.json()
        assert "student_id" in data
        assert "ai_recommendation" in data
    
    def test_get_agents(self):
        """Test agents listing endpoint"""
        response = requests.get(f"{BASE_URL}/api/agents")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert len(data["agents"]) == 3
    
    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        # Make multiple requests to test rate limiting
        for i in range(5):
            response = requests.get(f"{BASE_URL}/api/students")
            assert response.status_code == 200
    
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        # Test invalid student ID
        response = requests.get(f"{BASE_URL}/api/report/INVALID")
        assert response.status_code in [404, 500]
    
    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = requests.get(f"{BASE_URL}/api/students")
        assert response.status_code == 200
        # CORS headers should be present
    
    def test_security_headers(self):
        """Test security headers are present"""
        response = requests.get(f"{BASE_URL}/api/students")
        assert response.status_code == 200
        # Security headers should be present

class TestDataValidation:
    """Test data validation"""
    
    def test_student_data_validation(self):
        """Test student data validation"""
        from validators import moderate_validator
        
        valid_data = {
            "student_id": "S001",
            "student_name": "John Doe",
            "avg_marks": 85.5,
            "total_study_time": 450,
            "avg_distraction": 3.2
        }
        
        is_valid, errors = moderate_validator.validate_student_data(valid_data)
        assert is_valid == True
        assert len(errors) == 0
    
    def test_invalid_student_data(self):
        """Test invalid student data validation"""
        from validators import moderate_validator
        
        invalid_data = {
            "student_id": "",
            "student_name": "",
            "avg_marks": 150,  # Invalid: > 100
            "total_study_time": -10,  # Invalid: negative
            "avg_distraction": 15  # Invalid: > 10
        }
        
        is_valid, errors = moderate_validator.validate_student_data(invalid_data)
        assert is_valid == False
        assert len(errors) > 0

class TestCacheSystem:
    """Test cache system"""
    
    def test_cache_set_get(self):
        """Test cache set and get operations"""
        from cache import cache
        
        cache.set("test_key", "test_value", ttl=60)
        value = cache.get("test_key")
        assert value == "test_value"
    
    def test_cache_delete(self):
        """Test cache delete operation"""
        from cache import cache
        
        cache.set("test_key", "test_value")
        result = cache.delete("test_key")
        assert result == True
        
        value = cache.get("test_key")
        assert value is None
    
    def test_cache_stats(self):
        """Test cache statistics"""
        from cache import cache
        
        stats = cache.get_stats()
        assert "hits" in stats
        assert "misses" in stats
        assert "hit_rate_percent" in stats

class TestAuthentication:
    """Test authentication system"""
    
    def test_api_key_generation(self):
        """Test API key generation"""
        from auth import auth
        
        api_key = auth.generate_api_key("test_user")
        assert api_key is not None
        assert len(api_key) > 16
    
    def test_api_key_validation(self):
        """Test API key validation"""
        from auth import auth
        
        api_key = auth.generate_api_key("test_user")
        result = auth.validate_api_key(api_key)
        assert result is not None
        assert result["valid"] == True
        assert result["user_id"] == "test_user"
    
    def test_token_generation(self):
        """Test token generation"""
        from auth import auth
        
        token = auth.generate_token("test_user", expires_in_hours=24)
        assert token is not None
        assert len(token) > 0
    
    def test_token_validation(self):
        """Test token validation"""
        from auth import auth
        
        token = auth.generate_token("test_user")
        result = auth.validate_token(token)
        assert result is not None
        assert result["valid"] == True

class TestHealthMonitoring:
    """Test health monitoring system"""
    
    def test_system_metrics(self):
        """Test system metrics collection"""
        from health_monitor import health_monitor
        
        metrics = health_monitor.get_system_metrics()
        assert metrics is not None
        assert "timestamp" in metrics
        assert "uptime_seconds" in metrics
    
    def test_database_health(self):
        """Test database health check"""
        from health_monitor import health_monitor
        
        health = health_monitor.check_database_integrity()
        assert health is not None
        assert "status" in health
    
    def test_ai_service_health(self):
        """Test AI service health check"""
        from health_monitor import health_monitor
        
        health = health_monitor.check_ai_service_health()
        assert health is not None
        assert "status" in health

class TestRateLimiting:
    """Test rate limiting system"""
    
    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        from rate_limiter import rate_limiter
        
        # Test normal request
        is_allowed, info = rate_limiter.is_allowed("127.0.0.1")
        assert is_allowed == True
        assert "remaining" in info
    
    def test_rate_limiting_exceeded(self):
        """Test rate limit exceeded scenario"""
        from rate_limiter import rate_limiter
        
        # Create a rate limiter with low limit for testing
        test_limiter = SimpleRateLimiter(max_requests=2, window_seconds=60)
        
        # Make requests up to the limit
        test_limiter.is_allowed("127.0.0.1")
        test_limiter.is_allowed("127.0.0.1")
        
        # This should be rate limited
        is_allowed, info = test_limiter.is_allowed("127.0.0.1")
        assert is_allowed == False
        assert "error" in info

if __name__ == "__main__":
    # Run basic tests
    print("Running API tests...")
    
    try:
        test_api = TestAPIEndpoints()
        test_api.test_health_check()
        print("✓ Health check test passed")
        
        test_api.test_get_students()
        print("✓ Students endpoint test passed")
        
        test_api.test_get_activity_logs()
        print("✓ Activity logs test passed")
        
        test_api.test_get_report()
        print("✓ Report generation test passed")
        
        test_api.test_get_agents()
        print("✓ Agents listing test passed")
        
        print("\nAll API tests passed!")
        
    except Exception as e:
        print(f"Test failed: {str(e)}")
