import openai
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_fallback_report(student_data, behavioral_tag):
    """
    Generate a meaningful recommendation without external APIs based on behavioral analysis.
    Focus on specific, data-driven insights rather than generic advice.
    """
    student_name = student_data['student_name']
    total_time = student_data['total_study_time']
    avg_distraction = student_data['avg_distraction']
    avg_marks = student_data['avg_marks']
    
    # Additional detailed data if available
    subject_performance = student_data.get('subject_performance', {})
    weak_subjects = student_data.get('weak_subjects', [])
    strong_subjects = student_data.get('strong_subjects', [])
    distraction_patterns = student_data.get('distraction_patterns', {})
    
    # Build specific insights
    insights = []
    
    # Subject-specific insights
    if subject_performance:
        worst_subject = min(subject_performance.items(), key=lambda x: x[1]) if subject_performance else None
        best_subject = max(subject_performance.items(), key=lambda x: x[1]) if subject_performance else None
        if worst_subject and best_subject:
            marks_diff = best_subject[1] - worst_subject[1]
            if marks_diff > 30:
                insights.append(f"Performance varies significantly: {best_subject[0]} at {best_subject[1]}% vs {worst_subject[0]} at {worst_subject[1]}% - consider different study approaches for each subject")
    
    # Distraction pattern insights
    if avg_distraction > 7 and total_time > 300:
        insights.append(f"Despite spending {total_time} minutes studying, high distraction ({avg_distraction}/10) is reducing effectiveness - focus on quality over quantity with 25-minute focused sessions")
    elif avg_distraction < 4 and avg_marks < 50:
        insights.append(f"Focus is excellent ({avg_distraction}/10) but marks are low ({avg_marks}%) - the issue is likely conceptual understanding rather than attention - consider reviewing fundamentals")
    
    # Time vs marks correlation
    if total_time > 400 and avg_marks < 50:
        insights.append(f"Spending {total_time} minutes but achieving only {avg_marks}% - suggests inefficient study methods - try active recall and spaced repetition instead of passive reading")
    elif total_time < 200 and avg_marks > 70:
        insights.append(f"Achieving {avg_marks}% with only {total_time} minutes - excellent study efficiency - maintain this approach and gradually increase time for challenging topics")
    
    # Rule-based recommendations based on data with specific insights
    if behavioral_tag == "High Flight Risk":
        if avg_marks < 40:
            if insights:
                return f"{student_name} is at high flight risk with {avg_marks}% average. {insights[0]} Prioritize identifying the specific gap - is it foundational concepts or application skills?"
            else:
                return f"{student_name} is at high flight risk with {avg_marks}% average. Data shows low performance across subjects - schedule a diagnostic assessment to pinpoint whether the issue is conceptual understanding, test anxiety, or knowledge gaps in specific topics"
        elif avg_distraction > 7:
            if insights:
                return f"{student_name}'s distraction levels ({avg_distraction}/10) are significantly impacting the {total_time} minutes spent studying. {insights[0]} Try studying during morning hours when focus is typically better."
            else:
                return f"{student_name} spends {total_time} minutes studying but distraction ({avg_distraction}/10) is cutting effectiveness by ~60%. Track when distractions occur most - if it's during specific subjects, break those into smaller, more manageable chunks"
        else:
            return f"{student_name} shows {avg_marks}% average with mixed performance indicators. The data suggests inconsistent application of knowledge - practice more problem-solving questions rather than reviewing notes, as this builds application skills"
    
    elif behavioral_tag == "Concept Comprehension Issue":
        if insights:
            return f"{student_name} invests {total_time} minutes with good focus ({avg_distraction}/10) but achieves only {avg_marks}% - {insights[0]} This pattern suggests understanding exists in some areas but not others - identify which specific topics are causing confusion"
        else:
            return f"{student_name} puts in {total_time} minutes with {avg_distraction}/10 distraction but gets {avg_marks}% - this disconnect between effort and results suggests the study method isn't working. Try the Feynman technique: explain concepts aloud to check if understanding is real or illusory"
    
    elif behavioral_tag == "On Track":
        if avg_marks > 80:
            if insights:
                return f"{student_name} excels at {avg_marks}% with efficient study habits. {insights[0]} Challenge yourself with advanced problems to prevent plateauing"
            else:
                return f"{student_name} achieves {avg_marks}% with {total_time} minutes study time - excellent efficiency. To maintain this trajectory, introduce increasingly complex problems rather than more practice of the same level"
        else:
            return f"{student_name} maintains {avg_marks}% average with consistent {total_time} minutes study time. To break through to the next level, identify which specific question types cause the most mistakes and target those specifically"
    
    else:
        return f"{student_name} shows {avg_marks}% with {total_time} minutes study time and {avg_distraction}/10 distraction. Track which subjects have the highest distraction-marks correlation - improving focus in those specific areas could yield the biggest gains"

def generate_gemini_report(student_data, behavioral_tag):
    """
    Generate recommendation using Google Gemini API.
    """
    try:
        if GOOGLE_API_KEY and GOOGLE_API_KEY != "your_google_api_key_here":
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')

            prompt = f"""
            You are an empathetic educational advisor. Write a 3-sentence recommendation for a parent based on their child's weekly activity data:

            Student: {student_data['student_name']}
            Total Time Spent: {student_data['total_study_time']} mins
            Average Distraction Score: {student_data['avg_distraction']}/10
            Average Marks: {student_data['avg_marks']}%
            Behavioral Status: {behavioral_tag}

            CRITICAL: Provide specific, data-driven insights that parents might not notice.
            - Show correlations between metrics (e.g., "High distraction during Physics correlates with 40% lower marks")
            - Highlight specific patterns (e.g., "Focus is excellent in morning sessions but poor in evening")
            - Compare performance across subjects/topics
            - Identify non-obvious insights from the data
            - Avoid generic advice like "study more" or "focus better" - be specific about what the data reveals

            The report should be supportive, concise, and focused on specific, actionable insights from the data.
            """

            response = model.generate_content(prompt)
            return response.text.strip()
        else:
            return None
    except Exception as e:
        return None

def generate_parent_report(student_data, behavioral_tag):
    """
    Hybrid AI system: Try OpenAI first, then Gemini, then fallback to rule-based recommendations.
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

            CRITICAL: Provide specific, data-driven insights that parents might not notice.
            - Show correlations between metrics (e.g., "High distraction during Physics correlates with 40% lower marks")
            - Highlight specific patterns (e.g., "Focus is excellent in morning sessions but poor in evening")
            - Compare performance across subjects/topics
            - Identify non-obvious insights from the data
            - Avoid generic advice like "study more" or "focus better" - be specific about what the data reveals

            The report should be supportive, concise, and focused on specific, actionable insights from the data.
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an empathetic educational advisor who provides specific, data-driven insights rather than generic advice."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # OpenAI failed, try Gemini
            pass
    
    # Try Gemini as second option
    gemini_result = generate_gemini_report(student_data, behavioral_tag)
    if gemini_result:
        return gemini_result
    
    # Both APIs failed or unavailable, use rule-based fallback
    return generate_fallback_report(student_data, behavioral_tag)

def generate_query_from_natural_language(natural_query: str) -> dict:
    """
    Use Groq AI to generate a query configuration from natural language.
    
    Args:
        natural_query: User's natural language request (e.g., "Show me average marks by subject")
    
    Returns:
        Query configuration dict with data_source, columns, filters, group_by, limit
    """
    try:
        from groq import Groq
        
        if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
            return {"error": "Groq API key not configured"}
        
        client = Groq(api_key=GROQ_API_KEY)
        
        prompt = f"""
        You are a SQL query builder assistant. Convert the following natural language request into a JSON configuration for a query builder.

        Available tables and columns:
        - student_activity: id, student_id, student_name, activity_type, subject, topic, chapter, time_spent_mins, marks_achieved_percent, distraction_score, date
        - tasks: id, task_id, student_id, assigned_to, assigned_by, status, priority, due_date, created_at, completed_at, completed_by, notes
        - teacher_assignments: id, student_id, teacher_id, subject, assigned_at, assigned_by, is_active

        Allowed aggregation functions: SUM, AVG, COUNT, MIN, MAX
        Allowed operators: =, !=, >, <, >=, <=, LIKE, IN

        User request: "{natural_query}"

        Return ONLY a valid JSON object with this exact structure:
        {{
            "data_source": "table_name",
            "columns": ["column1", "column2", "AVG(column) as alias"],
            "filters": {{"column": {{"operator": "operator", "value": "value"}}}},
            "group_by": ["column1", "column2"],
            "limit": 100
        }}

        Rules:
        - If user wants averages/sums/counts, include aggregation functions in columns
        - If user wants to filter, add to filters object with operator and value
        - If user wants to group by subject/student/etc, add to group_by array
        - Default limit to 100 if not specified
        - Return ONLY the JSON, no explanation
        """
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a SQL query builder assistant. Return only valid JSON, no explanations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Parse the JSON response
        try:
            # Remove any markdown code blocks if present
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()
            
            query_config = json.loads(result_text)
            
            # Validate required fields
            if "data_source" not in query_config:
                query_config["data_source"] = "student_activity"  # default
            if "columns" not in query_config:
                query_config["columns"] = ["*"]
            if "filters" not in query_config:
                query_config["filters"] = {}
            if "group_by" not in query_config:
                query_config["group_by"] = []
            if "limit" not in query_config:
                query_config["limit"] = 100
            
            return {"success": True, "config": query_config}
            
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse AI response as JSON: {str(e)}"}
            
    except ImportError:
        return {"error": "Groq library not installed. Run: pip install groq"}
    except Exception as e:
        return {"error": f"Failed to generate query from natural language: {str(e)}"}

if __name__ == "__main__":
    # Test with dummy data
    test_data = {
        "student_name": "Alex",
        "total_study_time": 450,
        "avg_distraction": 8.2,
        "avg_marks": 45.0
    }
    print(generate_parent_report(test_data, "High Flight Risk"))
