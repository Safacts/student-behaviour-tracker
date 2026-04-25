"""
Test script for weekly and daily report APIs
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_weekly_report():
    """Test weekly report endpoint"""
    print("\n=== Testing Weekly Report ===")
    try:
        response = requests.get(f"{BASE_URL}/api/report/weekly?start_date=2024-01-01&end_date=2024-01-31")
        print(f"Status: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"Report type: {data.get('report_type')}")
            print(f"Date range: {data.get('date_range')}")
            print(f"Number of results: {len(data.get('data', []))}")
            print("✅ Weekly report API working")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_weekly_report_with_student():
    """Test weekly report with student filter"""
    print("\n=== Testing Weekly Report with Student Filter ===")
    try:
        response = requests.get(f"{BASE_URL}/api/report/weekly?start_date=2024-01-01&end_date=2024-01-31&student_id=S001")
        print(f"Status: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"Report type: {data.get('report_type')}")
            print(f"Student filter: {data.get('student_filter')}")
            print(f"Number of results: {len(data.get('data', []))}")
            print("✅ Weekly report with student filter working")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_daily_report():
    """Test daily report endpoint"""
    print("\n=== Testing Daily Report ===")
    try:
        response = requests.get(f"{BASE_URL}/api/report/daily?date=2024-01-15")
        print(f"Status: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"Report type: {data.get('report_type')}")
            print(f"Date: {data.get('date')}")
            print(f"Summary: {data.get('summary')}")
            print(f"Number of activities: {len(data.get('activities', []))}")
            print("✅ Daily report API working")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_daily_report_with_student():
    """Test daily report with student filter"""
    print("\n=== Testing Daily Report with Student Filter ===")
    try:
        response = requests.get(f"{BASE_URL}/api/report/daily?date=2024-01-15&student_id=S001")
        print(f"Status: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"Report type: {data.get('report_type')}")
            print(f"Student filter: {data.get('student_filter')}")
            print(f"Summary: {data.get('summary')}")
            print(f"Number of activities: {len(data.get('activities', []))}")
            print("✅ Daily report with student filter working")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    print("Testing Weekly and Daily Report APIs")
    print("=" * 50)
    
    test_weekly_report()
    test_weekly_report_with_student()
    test_daily_report()
    test_daily_report_with_student()
    
    print("\n" + "=" * 50)
    print("Test complete")
