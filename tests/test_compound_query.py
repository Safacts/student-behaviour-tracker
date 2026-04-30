"""
Simple test script to debug compound query detection
"""

import requests
import json

# Get a token
token_response = requests.get("http://localhost:8000/api/auth/token?user_id=test_user")
token = token_response.json()["token"]

# Test compound query
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

payload = {
    "query": "Analyze student S001 and create a learning path"
}

response = requests.post("http://localhost:8000/api/chat", json=payload, headers=headers)
print("Response status:", response.status_code)
print("Response body:")
print(json.dumps(response.json(), indent=2))
