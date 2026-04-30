from llm_service import generate_parent_report

# Test with data that should trigger specific insights
test_data = {
    "student_name": "Alex",
    "total_study_time": 450,
    "avg_distraction": 2.5,
    "avg_marks": 40.0,
    "behavioral_tag": "Concept Comprehension Issue",
    "subject_performance": {
        "Mathematics": 85.0,
        "Physics": 30.0,
        "Chemistry": 45.0,
        "Biology": 40.0
    },
    "weak_subjects": ["Physics", "Chemistry", "Biology"],
    "strong_subjects": ["Mathematics"]
}

print("Testing recommendation with subject performance data:")
print("=" * 60)
result = generate_parent_report(test_data, "Concept Comprehension Issue")
print(result)
print("=" * 60)
