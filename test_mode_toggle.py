import requests
import json

# Get token
token_response = requests.get("http://localhost:8000/api/auth/token?user_id=test_user")
token_data = token_response.json()
token = token_data["token"]

print(f"Token: {token}")
print()

# Test with LLM mode (default)
print("=== Test 1: LLM Mode ===")
response = requests.post(
    "http://localhost:8000/api/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={"query": "Analyze student S001", "use_llm": True}
)
print(json.dumps(response.json(), indent=2))
print()

# Test with Heuristic mode
print("=== Test 2: Heuristic Mode ===")
response = requests.post(
    "http://localhost:8000/api/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={"query": "Analyze student S001", "use_llm": False}
)
print(json.dumps(response.json(), indent=2))
