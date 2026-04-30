"""
Test script for AI Query Building UI Integration
Tests the aiBuildQuery function and /api/query/ai-build endpoint
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def get_auth_token():
    """Get authentication token"""
    response = requests.get(f"{BASE_URL}/api/auth/token?user_id=test_ai_query")
    if response.status_code == 200:
        data = response.json()
        return data.get("token")
    return None

def test_ai_build_endpoint(token, query):
    """Test the /api/query/ai-build endpoint"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    payload = {"query": query}
    
    try:
        response = requests.post(f"{BASE_URL}/api/query/ai-build", headers=headers, json=payload)
        return response.status_code, response.json()
    except Exception as e:
        return 500, {"error": str(e)}

def main():
    print("Testing AI Query Building UI Integration")
    print("=" * 50)
    
    # Get auth token
    print("\n1. Getting authentication token...")
    token = get_auth_token()
    if not token:
        print("❌ Failed to get auth token")
        return
    print("✅ Auth token obtained")
    
    # Test cases
    test_queries = [
        "Show me average marks by subject for students with distraction score above 5",
        "Get all students with marks less than 50",
        "Analyze student behavior for students with high distraction",
        "Show class overview with average marks",
        "Invalid query that should fail"
    ]
    
    print("\n2. Testing AI Build endpoint with various queries:")
    print("-" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        status, result = test_ai_build_endpoint(token, query)
        
        if status == 200:
            print(f"✅ Status: {status}")
            if result.get("success"):
                config = result.get("config", {})
                print(f"   Data Source: {config.get('data_source', 'N/A')}")
                print(f"   Columns: {config.get('columns', [])}")
                print(f"   Filters: {config.get('filters', {})}")
                print(f"   Group By: {config.get('group_by', [])}")
            else:
                print(f"   ❌ API returned success=False: {result.get('message', 'Unknown error')}")
        else:
            print(f"❌ Status: {status}")
            print(f"   Error: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 50)
    print("Testing complete!")

if __name__ == "__main__":
    main()
