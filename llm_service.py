import openai
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_fallback_report(student_data, behavioral_tag):
    """
    Generate a meaningful recommendation without external APIs based on behavioral analysis.
    """
    student_name = student_data['student_name']
    total_time = student_data['total_study_time']
    avg_distraction = student_data['avg_distraction']
    avg_marks = student_data['avg_marks']
    
    # Rule-based recommendations based on data
    if behavioral_tag == "High Flight Risk":
        if avg_marks < 40:
            return f"{student_name} is showing significant academic challenges with an average of {avg_marks}%. I recommend scheduling a meeting with teachers to identify specific knowledge gaps and creating a structured study plan with daily check-ins to rebuild confidence and academic foundation."
        elif avg_distraction > 7:
            return f"{student_name} is spending {total_time} minutes studying but high distraction levels ({avg_distraction}/10) are impacting performance. Consider creating a distraction-free study environment and implementing the Pomodoro technique with regular breaks to improve focus and retention."
        else:
            return f"{student_name} needs immediate academic support with current performance at {avg_marks}%. I recommend pairing with a peer tutor for challenging subjects and establishing a consistent daily study routine to build momentum and improve understanding."
    
    elif behavioral_tag == "Concept Comprehension Issue":
        return f"{student_name} is putting in good effort with {total_time} minutes of study time but may need different learning approaches. I recommend using visual aids, hands-on activities, and breaking down complex concepts into smaller, manageable steps to improve comprehension and retention."
    
    elif behavioral_tag == "On Track":
        if avg_marks > 80:
            return f"{student_name} is performing excellently with {avg_marks}% average marks and consistent study habits. I recommend introducing advanced challenges and enrichment activities to maintain engagement and continue the positive academic trajectory."
        else:
            return f"{student_name} is making good progress with {avg_marks}% average marks. I recommend setting specific academic goals for the next term and exploring subjects of interest to deepen engagement and maintain the positive momentum."
    
    else:
        return f"{student_name} shows potential for growth with current study habits. I recommend establishing clear academic goals, regular progress monitoring, and celebrating small achievements to build confidence and maintain motivation throughout the learning journey."

def generate_parent_report(student_data, behavioral_tag):
    """
    Constructs a prompt and calls OpenAI to generate a 3-sentence empathetic report.
    Falls back to rule-based recommendations if API is unavailable.
    """
    # Try OpenAI first
    if OPENAI_API_KEY and OPENAI_API_KEY != "[INSERT_API_KEY_HERE]":
        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)

            prompt = f"""
            You are an empathetic educational advisor. Write a 3-sentence recommendation for a parent based on their child's weekly activity data:
            
            Student: {student_data['student_name']}
            Total Time Spent: {student_data['total_study_time']} mins
            Average Distraction Score: {student_data['avg_distraction']}/10
            Average Marks: {student_data['avg_marks']}%
            Behavioral Status: {behavioral_tag}
            
            The report should be supportive, concise, and focused on improvement or celebration.
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an empathetic educational advisor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Fall back to rule-based recommendations
            return generate_fallback_report(student_data, behavioral_tag)
    
    # No API key available, use fallback
    return generate_fallback_report(student_data, behavioral_tag)

if __name__ == "__main__":
    # Test with dummy data
    test_data = {
        "student_name": "Alex",
        "total_study_time": 450,
        "avg_distraction": 8.2,
        "avg_marks": 45.0
    }
    print(generate_parent_report(test_data, "High Flight Risk"))
