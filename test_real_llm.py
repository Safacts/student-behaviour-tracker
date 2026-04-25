import requests
import json

# Get token
token_response = requests.get("http://localhost:8000/api/auth/token?user_id=test_user")
token_data = token_response.json()
token = token_data["token"]

print(f"Token: {token}")
print()

# Test with a complex query that requires LLM
print("=== Test: Complex Query with LLM ===")
response = requests.post(
    "http://localhost:8000/api/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={"query": "What can you tell me about student S001's performance in mathematics?", "use_llm": True}
)
result = response.json()
print(f"Success: {result.get('success')}")
print(f"Tool used: {result.get('tool_used')}")
print(f"Confidence: {result.get('confidence')}")
print(f"Response: {result.get('natural_language_response', 'N/A')[:200]}...")
print()

print("=== Test: Same Query with Heuristic ===")
response = requests.post(
    "http://localhost:8000/api/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={"query": "What can you tell me about student S001's performance in mathematics?", "use_llm": False}
)
result = response.json()
print(f"Success: {result.get('success')}")
print(f"Tool used: {result.get('tool_used')}")
print(f"Confidence: {result.get('confidence')}")
print(f"Response: {result.get('message', result.get('natural_language_response', 'N/A'))[:200]}...")
