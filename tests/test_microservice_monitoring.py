"""
Test script for Microservice Monitoring
Tests /api/health, /api/health/detailed, /api/health/debug endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_basic_health():
    """Test the basic /api/health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        return response.status_code, response.json()
    except Exception as e:
        return 500, {"error": str(e)}

def test_detailed_health():
    """Test the /api/health/detailed endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/health/detailed")
        return response.status_code, response.json()
    except Exception as e:
        return 500, {"error": str(e)}

def test_debug_report():
    """Test the /api/health/debug endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/health/debug")
        return response.status_code, response.json()
    except Exception as e:
        return 500, {"error": str(e)}

def main():
    print("Testing Microservice Monitoring")
    print("=" * 50)
    
    # Test 1: Basic health check
    print("\n1. Testing /api/health (basic health check):")
    print("-" * 50)
    status, result = test_basic_health()
    
    if status == 200:
        print(f"✅ Status: {status}")
        print(f"   Response: {json.dumps(result, indent=2)}")
    else:
        print(f"❌ Status: {status}")
        print(f"   Error: {result.get('error', 'Unknown error')}")
    
    # Test 2: Detailed health check
    print("\n2. Testing /api/health/detailed (comprehensive health check):")
    print("-" * 50)
    status, result = test_detailed_health()
    
    if status == 200:
        print(f"✅ Status: {status}")
        print(f"   Overall Status: {result.get('overall_status', 'N/A')}")
        
        # Check individual component statuses
        components = result.get('components', {})
        print(f"   Components Checked:")
        for component, status_info in components.items():
            comp_status = status_info.get('status', 'unknown')
            print(f"     - {component}: {comp_status}")
            if comp_status != 'healthy':
                print(f"       Issue: {status_info.get('message', 'No message')}")
    else:
        print(f"❌ Status: {status}")
        print(f"   Error: {result.get('error', 'Unknown error')}")
    
    # Test 3: Debug report
    print("\n3. Testing /api/health/debug (debug report):")
    print("-" * 50)
    status, result = test_debug_report()
    
    if status == 200:
        print(f"✅ Status: {status}")
        print(f"   System Status: {result.get('system_status', 'N/A')}")
        
        # Check if recommendations are present
        recommendations = result.get('recommendations', [])
        if recommendations:
            print(f"   Recommendations ({len(recommendations)}):")
            for i, rec in enumerate(recommendations, 1):
                print(f"     {i}. {rec}")
        else:
            print(f"   No recommendations (system is healthy)")
        
        # Check issues found
        issues = result.get('issues', [])
        if issues:
            print(f"   Issues Found ({len(issues)}):")
            for issue in issues:
                print(f"     - {issue}")
        else:
            print(f"   No issues found")
    else:
        print(f"❌ Status: {status}")
        print(f"   Error: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 50)
    print("Testing complete!")

if __name__ == "__main__":
    main()
