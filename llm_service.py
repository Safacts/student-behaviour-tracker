import google.generativeai as genai
try:
    from nidhi_sdk.kavach import load_secrets
    load_secrets("student-behaviour-tracker")
except ImportError:
    pass
import os


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def generate_parent_report(student_data, behavioral_tag):
    """
    Constructs a prompt and calls Gemini to generate a 3-sentence empathetic report.
    """
    if GOOGLE_API_KEY == "[INSERT_API_KEY_HERE]":
        return "AI Report currently unavailable. Please provide a valid Gemini API Key in llm_service.py."

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest')

    prompt = f"""
    You are an empathetic educational advisor. Write a 3-sentence recommendation for a parent based on their child's weekly activity data:
    
    Student: {student_data['student_name']}
    Total Time Spent: {student_data['total_study_time']} mins
    Average Distraction Score: {student_data['avg_distraction']}/10
    Average Marks: {student_data['avg_marks']}%
    Behavioral Status: {behavioral_tag}
    
    The report should be supportive, concise, and focused on improvement or celebration.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating report: {str(e)}"

if __name__ == "__main__":
    # Test with dummy data
    test_data = {
        "student_name": "Alex",
        "total_study_time": 450,
        "avg_distraction": 8.2,
        "avg_marks": 45.0
    }
    print(generate_parent_report(test_data, "High Flight Risk"))
