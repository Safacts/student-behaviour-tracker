import requests
import json

# Test weekly report
print("=== Test Weekly Report ===")
response = requests.get("http://localhost:8000/api/report/weekly?start_date=2026-04-16&end_date=2026-04-23")
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))
print()

# Test weekly report with student filter
print("=== Test Weekly Report (Student S001) ===")
response = requests.get("http://localhost:8000/api/report/weekly?start_date=2026-04-16&end_date=2026-04-23&student_id=S001")
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))
print()

# Test daily report
print("=== Test Daily Report ===")
response = requests.get("http://localhost:8000/api/report/daily?date=2026-04-23")
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))
print()

# Test daily report with student filter
print("=== Test Daily Report (Student S001) ===")
response = requests.get("http://localhost:8000/api/report/daily?date=2026-04-23&student_id=S001")
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))
