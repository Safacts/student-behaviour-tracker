"""
Test script to verify agent can access enhanced parent report
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def get_auth_token():
    """Get authentication token"""
    response = requests.get(f"{BASE_URL}/api/auth/token?user_id=test_parent_report")
    if response.status_code == 200:
        data = response.json()
        return data.get("token")
    return None

def test_parent_report_endpoint(token, student_id):
    """Test the /api/parent/report endpoint directly"""
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/parent/report/{student_id}", headers=headers)
        return response.status_code, response.json()
    except Exception as e:
        return 500, {"error": str(e)}

def test_agent_parent_email(token, student_id):
    """Test if agent can call generate_parent_email via chat"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    payload = {
        "query": f"Send a parent report for student {student_id}",
        "use_llm": True,
        "role": "parent"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/chat", headers=headers, json=payload)
        return response.status_code, response.json()
    except Exception as e:
        return 500, {"error": str(e)}

def main():
    print("Testing Parent Report Agent Access")
    print("=" * 50)
    
    # Get auth token
    print("\n1. Getting authentication token...")
    token = get_auth_token()
    if not token:
        print("❌ Failed to get auth token")
        return
    print("✅ Auth token obtained")
    
    student_id = "S001"
    
    # Test 1: Direct endpoint
    print(f"\n2. Testing /api/parent/report/{student_id} endpoint:")
    print("-" * 50)
    status, result = test_parent_report_endpoint(token, student_id)
    
    if status == 200:
        print(f"✅ Status: {status}")
        print(f"   Student: {result.get('student_name', 'N/A')}")
        print(f"   Status: {result.get('status', {}).get('label', 'N/A')}")
        print(f"   Subjects: {len(result.get('subject_performance', []))}")
        print(f"   Strengths: {result.get('strengths', [])}")
        print(f"   Concerns: {result.get('concerns', [])}")
    else:
        print(f"❌ Status: {status}")
        print(f"   Error: {result.get('error', 'Unknown error')}")
    
    # Test 2: Agent via chat
    print(f"\n3. Testing agent access via chat (parent role):")
    print("-" * 50)
    status, result = test_agent_parent_email(token, student_id)
    
    if status == 200:
        if result.get("success"):
            print(f"✅ Agent successfully processed request")
            print(f"   Tool used: {result.get('tool_used', 'N/A')}")
            response = result.get('natural_language_response', '')
            print(f"   Response: {response[:200]}...")
            
            # Check if it used the parent email tool
            if result.get('tool_used') == 'generate_parent_email':
                print("   ✓ Agent used generate_parent_email tool")
            else:
                print(f"   ⚠ Agent used different tool: {result.get('tool_used')}")
        else:
            print(f"❌ Agent failed: {result.get('message', 'Unknown error')}")
    else:
        print(f"❌ Status: {status}")
        print(f"   Error: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 50)
    print("Testing complete!")

if __name__ == "__main__":
    main()
