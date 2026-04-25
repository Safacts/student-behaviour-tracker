"""
Test script for Role-Based Chat System
Tests all 5 roles (developer, student, faculty, parent, principal)
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def get_auth_token():
    """Get authentication token"""
    response = requests.get(f"{BASE_URL}/api/auth/token?user_id=test_role_chat")
    if response.status_code == 200:
        data = response.json()
        return data.get("token")
    return None

def test_chat_endpoint(token, query, role="student"):
    """Test the /api/chat endpoint with role parameter"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    payload = {
        "query": query,
        "use_llm": True,
        "role": role
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/chat", headers=headers, json=payload)
        return response.status_code, response.json()
    except Exception as e:
        return 500, {"error": str(e)}

def main():
    print("Testing Role-Based Chat System")
    print("=" * 50)
    
    # Get auth token
    print("\n1. Getting authentication token...")
    token = get_auth_token()
    if not token:
        print("❌ Failed to get auth token")
        return
    print("✅ Auth token obtained")
    
    # Roles to test
    roles = ["developer", "student", "faculty", "parent", "principal"]
    
    # Test greeting for each role
    print("\n2. Testing greeting responses for each role:")
    print("-" * 50)
    
    for role in roles:
        print(f"\nRole: {role}")
        status, result = test_chat_endpoint(token, "hello", role)
        
        if status == 200:
            if result.get("success"):
                response = result.get("natural_language_response", "")
                print(f"✅ Greeting: {response[:100]}...")
            else:
                print(f"❌ Error: {result.get('message', 'Unknown error')}")
        else:
            print(f"❌ Status: {status}")
    
    # Test tool-based responses for each role
    print("\n3. Testing tool-based responses for each role:")
    print("-" * 50)
    
    test_query = "Analyze student S001"
    
    for role in roles:
        print(f"\nRole: {role}")
        print(f"Query: {test_query}")
        status, result = test_chat_endpoint(token, test_query, role)
        
        if status == 200:
            if result.get("success"):
                response = result.get("natural_language_response", "")
                print(f"✅ Response: {response[:150]}...")
                
                # Check if response is role-appropriate
                if role == "developer":
                    if "technical" in response.lower() or "api" in response.lower():
                        print("   ✓ Contains technical language (appropriate)")
                elif role == "student":
                    if "study" in response.lower() or "improve" in response.lower():
                        print("   ✓ Contains study advice (appropriate)")
                elif role == "faculty":
                    if "class" in response.lower() or "teaching" in response.lower():
                        print("   ✓ Contains teaching insights (appropriate)")
                elif role == "parent":
                    if "child" in response.lower() or "progress" in response.lower():
                        print("   ✓ Contains parent-focused content (appropriate)")
                elif role == "principal":
                    if "school" in response.lower() or "metrics" in response.lower():
                        print("   ✓ Contains school-wide insights (appropriate)")
            else:
                print(f"❌ Error: {result.get('message', 'Unknown error')}")
        else:
            print(f"❌ Status: {status}")
    
    print("\n" + "=" * 50)
    print("Testing complete!")

if __name__ == "__main__":
    main()
