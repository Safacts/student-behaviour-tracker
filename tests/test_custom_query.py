import requests
import json

# Get token
token_response = requests.get("http://localhost:8000/api/auth/token?user_id=test_user")
token_data = token_response.json()
token = token_data["token"]

print(f"Token: {token}")
print()

# Test 1: Get allowed tables
print("=== Test 1: Get Allowed Tables ===")
response = requests.get(
    "http://localhost:8000/api/query/tables",
    headers={"Authorization": f"Bearer {token}"}
)
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))
print()

# Test 2: Simple custom query
print("=== Test 2: Simple Custom Query ===")
config = {
    "data_source": "student_activity",
    "columns": ["student_id", "student_name", "subject", "time_spent_mins"],
    "filters": {
        "date": {"operator": "=", "value": "2026-04-23"}
    },
    "limit": 5
}
response = requests.post(
    "http://localhost:8000/api/query/custom",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json=config
)
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))
