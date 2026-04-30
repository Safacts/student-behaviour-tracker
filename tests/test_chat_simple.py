import requests
import json

# Get token
token_response = requests.get("http://localhost:8000/api/auth/token?user_id=test_user")
token_data = token_response.json()
token = token_data["token"]

print(f"Token: {token}")
print()

# Test single query
print("=== Test 1: Single Query ===")
response = requests.post(
    "http://localhost:8000/api/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={"query": "Analyze student S001"}
)
print(json.dumps(response.json(), indent=2))
print()

# Test compound query
print("=== Test 2: Compound Query ===")
response = requests.post(
    "http://localhost:8000/api/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={"query": "Analyze student S001 and create a learning path"}
)
print(json.dumps(response.json(), indent=2))
