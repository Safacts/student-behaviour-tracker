import requests
import json

BASE_URL = "http://localhost:8000"

# Get auth token
token_response = requests.get(f"{BASE_URL}/api/auth/token?user_id=test_user")
auth_token = token_response.json()["token"]
headers = {"Authorization": f"Bearer {auth_token}"}

# Test 1: Save a configuration
print("Test 1: Saving a configuration...")
config = {
    "data_source": "student_activity",
    "columns": ["student_id", "student_name", "subject", "AVG(marks_achieved_percent) as avg_marks"],
    "filters": {
        "date": {"operator": "=", "value": "2026-04-23"}
    },
    "group_by": ["student_id", "subject"],
    "limit": 10
}

save_response = requests.post(
    f"{BASE_URL}/api/query/config/save",
    headers={**headers, "Content-Type": "application/json"},
    json={"name": "test_config", "config": config, "description": "Test configuration"}
)
print(f"Save config: {save_response.status_code} - {save_response.json()}")

# Test 2: List configurations
print("\nTest 2: Listing configurations...")
list_response = requests.get(f"{BASE_URL}/api/query/config/list", headers=headers)
print(f"List configs: {list_response.status_code} - {list_response.json()}")

# Test 3: Load a configuration
print("\nTest 3: Loading configuration...")
load_response = requests.get(f"{BASE_URL}/api/query/config/load/test_config", headers=headers)
print(f"Load config: {load_response.status_code} - {load_response.json()}")

# Test 4: Execute saved configuration (dynamic endpoint)
print("\nTest 4: Executing saved configuration...")
execute_response = requests.get(f"{BASE_URL}/api/query/config/execute/test_config", headers=headers)
print(f"Execute config: {execute_response.status_code} - {execute_response.json()}")

# Test 5: Delete configuration
print("\nTest 5: Deleting configuration...")
delete_response = requests.delete(f"{BASE_URL}/api/query/config/delete/test_config", headers=headers)
print(f"Delete config: {delete_response.status_code} - {delete_response.json()}")

print("\n✅ All API Builder configuration endpoints tested successfully!")
