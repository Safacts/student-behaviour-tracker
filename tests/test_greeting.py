import requests
import json

# Get token
token_response = requests.get("http://localhost:8000/api/auth/token?user_id=test_user")
token_data = token_response.json()
token = token_data["token"]

print(f"Token: {token}")
print()

# Test greeting
print("=== Test: Greeting ===")
response = requests.post(
    "http://localhost:8000/api/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={"query": "hi"}
)
print(json.dumps(response.json(), indent=2))
