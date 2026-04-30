"""
Test script for /api/chat endpoint
Tests various query scenarios to identify gaps in intent parsing and parameter extraction
"""

import requests
import json
from datetime import datetime
import os

# Configuration
API_URL = "http://localhost:8000/api/chat"
AUTH_TOKEN = os.getenv("AUTH_TOKEN")  # Use environment variable

# If no token provided, fetch from the auth endpoint
if not AUTH_TOKEN:
    try:
        response = requests.get("http://localhost:8000/api/auth/token?user_id=test_user")
        if response.status_code == 200:
            AUTH_TOKEN = response.json()["token"]
            print(f"Fetched token from auth endpoint: {AUTH_TOKEN[:50]}...")
        else:
            print(f"Failed to fetch token: {response.status_code}")
    except Exception as e:
        print(f"Error fetching token: {e}")

# Test cases
TEST_CASES = [
    {
        "name": "Simple behavior analysis",
        "query": "Analyze student S001",
        "expected_tool": "analyze_student_behavior",
        "expected_params": {"student_id": "S001"},
        "type": "positive"
    },
    {
        "name": "Class overview",
        "query": "Get class overview",
        "expected_tool": "get_class_overview",
        "expected_params": {},
        "type": "positive"
    },
    {
        "name": "Create intervention with parameters",
        "query": "Create intervention for student S001 assigned to teacher T001",
        "expected_tool": "create_intervention_task",
        "expected_params": {"student_id": "S001", "assigned_to": "T001"},
        "type": "positive"
    },
    {
        "name": "Learning path creation",
        "query": "Create learning path for student S002",
        "expected_tool": "create_learning_path",
        "expected_params": {"student_id": "S002"},
        "type": "positive"
    },
    {
        "name": "Identify at-risk students",
        "query": "Show me at-risk students",
        "expected_tool": "identify_at_risk_students",
        "expected_params": {},
        "type": "positive"
    },
    {
        "name": "Student summary",
        "query": "Get summary for student S001",
        "expected_tool": "get_student_summary",
        "expected_params": {"student_id": "S001"},
        "type": "positive"
    },
    {
        "name": "Compound query (negative test)",
        "query": "Analyze student S001 and create a learning path",
        "expected_tool": None,  # Should fail or only execute one tool
        "expected_params": {},
        "type": "negative"
    },
    {
        "name": "Missing student ID",
        "query": "Analyze student",
        "expected_tool": "analyze_student_behavior",
        "expected_params": {"student_id": None},
        "type": "edge_case"
    },
    {
        "name": "Invalid student ID format",
        "query": "Analyze student XYZ",
        "expected_tool": "analyze_student_behavior",
        "expected_params": {"student_id": None},
        "type": "edge_case"
    },
    {
        "name": "Predict performance",
        "query": "Predict performance for student S001",
        "expected_tool": "predict_student_performance",
        "expected_params": {"student_id": "S001"},
        "type": "positive"
    },
    {
        "name": "Get student info",
        "query": "Get information about student S001",
        "expected_tool": "get_student_info",
        "expected_params": {"student_id": "S001"},
        "type": "positive"
    },
    {
        "name": "Activity logs",
        "query": "Show activity logs for student S001 for the last 7 days",
        "expected_tool": "get_student_activity_logs",
        "expected_params": {"student_id": "S001", "days": 7},
        "type": "positive"
    }
]

def run_test(test_case):
    """Run a single test case"""
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": test_case["query"]
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        
        result = {
            "test_name": test_case["name"],
            "query": test_case["query"],
            "status_code": response.status_code,
            "success": response.status_code == 200,
            "response": response.json() if response.status_code == 200 else response.text,
            "expected_tool": test_case["expected_tool"],
            "expected_params": test_case["expected_params"],
            "type": test_case["type"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Check if tool matches expected
        if response.status_code == 200 and test_case["expected_tool"]:
            actual_tool = result["response"].get("tool_used")
            result["tool_match"] = actual_tool == test_case["expected_tool"]
        else:
            result["tool_match"] = None
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "test_name": test_case["name"],
            "query": test_case["query"],
            "status_code": None,
            "success": False,
            "response": str(e),
            "expected_tool": test_case["expected_tool"],
            "expected_params": test_case["expected_params"],
            "type": test_case["type"],
            "timestamp": datetime.now().isoformat(),
            "tool_match": None
        }

def main():
    """Run all test cases and generate report"""
    print("=" * 80)
    print("CHAT API TEST SUITE")
    print("=" * 80)
    print(f"Testing endpoint: {API_URL}")
    print(f"Started at: {datetime.now().isoformat()}")
    print("=" * 80)
    print()
    
    results = []
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"Running test {i}/{len(TEST_CASES)}: {test_case['name']}")
        print(f"  Query: {test_case['query']}")
        
        result = run_test(test_case)
        results.append(result)
        
        if result["success"]:
            print(f"  ✓ Status: {result['status_code']}")
            if result.get("tool_match") is not None:
                if result["tool_match"]:
                    print(f"  ✓ Tool matched: {result['response'].get('tool_used')}")
                else:
                    print(f"  ✗ Tool mismatch: Expected {result['expected_tool']}, got {result['response'].get('tool_used')}")
            print(f"  Confidence: {result['response'].get('confidence', 'N/A')}")
        else:
            print(f"  ✗ Status: {result['status_code']}")
            print(f"  Error: {result['response']}")
        
        print()
    
    # Generate summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    total = len(results)
    successful = sum(1 for r in results if r["success"])
    failed = total - successful
    
    print(f"Total tests: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success rate: {(successful/total)*100:.1f}%")
    print()
    
    # Breakdown by type
    print("Breakdown by test type:")
    for test_type in ["positive", "negative", "edge_case"]:
        type_tests = [r for r in results if r["type"] == test_type]
        type_success = sum(1 for r in type_tests if r["success"])
        print(f"  {test_type}: {type_success}/{len(type_tests)} passed")
    print()
    
    # Tool matching accuracy
    tool_match_tests = [r for r in results if r.get("tool_match") is not None]
    if tool_match_tests:
        tool_matches = sum(1 for r in tool_match_tests if r["tool_match"])
        print(f"Tool matching accuracy: {tool_matches}/{len(tool_match_tests)} ({(tool_matches/len(tool_match_tests))*100:.1f}%)")
    print()
    
    # Save detailed results to file
    output_file = f"chat_api_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Detailed results saved to: {output_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()
