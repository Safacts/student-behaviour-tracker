"""
Agent Orchestrator for Conversational API
Handles natural language queries and routes to appropriate agent tools
"""

from typing import Dict, List, Any, Optional, Callable
from groq import Groq
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class ToolRegistry:
    """Registry of all available agent tools with descriptions for LLM understanding"""
    
    def __init__(self):
        self.tools = {}
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize all available tools with descriptions"""
        from agents import (
            analyze_student_behavior,
            create_learning_path,
            suggest_intervention,
            identify_at_risk_students,
            get_class_overview,
            generate_parent_email,
            generate_staff_notification,
            create_intervention_task,
            create_monitoring_task,
            update_task_status,
            get_assigned_tasks,
            get_student_tasks,
            get_overdue_tasks,
            predict_student_performance,
            detect_anomalies,
            assign_teacher_to_student,
            get_teacher_responsibilities,
            generate_teacher_report
        )
        
        # Register tools with natural language descriptions
        self.register_tool(
            "analyze_student_behavior",
            analyze_student_behavior,
            "Analyze a student's behavioral patterns, study habits, and engagement. Returns insights about focus, distraction, and learning patterns.",
            {"student_id": "The ID of the student to analyze (e.g., S001)"}
        )
        
        self.register_tool(
            "create_learning_path",
            create_learning_path,
            "Create a personalized learning path for a student based on their current performance and goals.",
            {"student_id": "The ID of the student"}
        )
        
        self.register_tool(
            "suggest_intervention",
            suggest_intervention,
            "Suggest appropriate interventions for a student who may be struggling or at risk.",
            {"student_id": "The ID of the student"}
        )
        
        self.register_tool(
            "identify_at_risk_students",
            identify_at_risk_students,
            "Identify all students who are at risk based on their performance metrics.",
            {"threshold_marks": "Optional: Minimum marks threshold (default: 50.0)"}
        )
        
        self.register_tool(
            "get_class_overview",
            get_class_overview,
            "Get an overview of the entire class including statistics and trends.",
            {}
        )
        
        self.register_tool(
            "generate_parent_email",
            generate_parent_email,
            "Generate an email to a parent about their child's progress or issues.",
            {"student_id": "The ID of the student", "email_type": "Type of email: report, warning, or intervention"}
        )
        
        self.register_tool(
            "generate_staff_notification",
            generate_staff_notification,
            "Generate a notification for staff about a student.",
            {"student_id": "The ID of the student", "notification_type": "Type of notification"}
        )
        
        self.register_tool(
            "create_intervention_task",
            create_intervention_task,
            "Create an intervention task for a student and assign it to a teacher.",
            {"student_id": "The ID of the student", "assigned_to": "The ID of the teacher to assign to", "due_date": "Optional: Due date in YYYY-MM-DD format"}
        )
        
        self.register_tool(
            "create_monitoring_task",
            create_monitoring_task,
            "Create a monitoring task to track a student's progress over time.",
            {"student_id": "The ID of the student", "assigned_to": "The ID of the teacher to assign to", "monitoring_period_days": "Number of days to monitor (default: 30)"}
        )
        
        self.register_tool(
            "update_task_status",
            update_task_status,
            "Update the status of a task (e.g., mark as completed).",
            {"task_id": "The ID of the task", "status": "New status: pending, in_progress, completed, cancelled", "notes": "Optional: Notes about the update"}
        )
        
        self.register_tool(
            "get_assigned_tasks",
            get_assigned_tasks,
            "Get all tasks assigned to a specific teacher or user.",
            {"assigned_to": "The ID of the user"}
        )
        
        self.register_tool(
            "get_student_tasks",
            get_student_tasks,
            "Get all tasks for a specific student.",
            {"student_id": "The ID of the student"}
        )
        
        self.register_tool(
            "get_overdue_tasks",
            get_overdue_tasks,
            "Get all tasks that are overdue.",
            {}
        )
        
        self.register_tool(
            "predict_student_performance",
            predict_student_performance,
            "Predict a student's future performance based on historical data.",
            {"student_id": "The ID of the student", "days_ahead": "Optional: Number of days to predict ahead (default: 30)"}
        )
        
        self.register_tool(
            "detect_anomalies",
            detect_anomalies,
            "Detect anomalies in a student's behavior or performance patterns.",
            {"student_id": "The ID of the student", "threshold_std": "Optional: Standard deviation threshold (default: 2.0)"}
        )
        
        self.register_tool(
            "assign_teacher_to_student",
            assign_teacher_to_student,
            "Assign a teacher to a student for a specific subject.",
            {"student_id": "The ID of the student", "teacher_id": "The ID of the teacher", "subject": "The subject"}
        )
        
        self.register_tool(
            "get_teacher_responsibilities",
            get_teacher_responsibilities,
            "Get all responsibilities assigned to a teacher.",
            {"teacher_id": "The ID of the teacher"}
        )
        
        self.register_tool(
            "generate_teacher_report",
            generate_teacher_report,
            "Generate a comprehensive report for a teacher about their assigned students.",
            {"teacher_id": "The ID of the teacher"}
        )
    
    def register_tool(self, name: str, func: Callable, description: str, parameters: Dict[str, str]):
        """Register a tool with its metadata"""
        self.tools[name] = {
            "function": func,
            "description": description,
            "parameters": parameters
        }
    
    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def get_all_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered tools"""
        return self.tools
    
    def get_tool_descriptions(self) -> str:
        """Get a formatted string of all tool descriptions for LLM"""
        descriptions = []
        for name, tool in self.tools.items():
            param_desc = ", ".join([f"{k}: {v}" for k, v in tool["parameters"].items()])
            descriptions.append(f"- {name}: {tool['description']}. Parameters: {param_desc if param_desc else 'None'}")
        return "\n".join(descriptions)


class IntentParser:
    """Parse natural language queries to determine intent and extract parameters"""
    
    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry
        self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
    
    def parse_query(self, query: str) -> Dict[str, Any]:
        """Parse a natural language query to extract intent and parameters"""
        if not self.client:
            # Fallback to simple pattern matching if no LLM available
            return self._simple_parse(query)
        
        tool_descriptions = self.tool_registry.get_tool_descriptions()
        
        prompt = f"""
You are an intent parser for a student behavior analysis system. Analyze the user's query and determine which tool to call and what parameters to extract.

Available tools:
{tool_descriptions}

User query: "{query}"

Respond in JSON format with this structure:
{{
    "tool": "tool_name or null if no tool matches",
    "parameters": {{"param_name": "value or null if not provided"}},
    "confidence": 0.0 to 1.0,
    "reasoning": "brief explanation of why this tool was chosen"
}}

If no tool matches the query, set tool to null and explain why in reasoning.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            print(f"LLM parsing failed: {e}, falling back to simple parse")
            return self._simple_parse(query)
    
    def _simple_parse(self, query: str) -> Dict[str, Any]:
        """Simple pattern-based parsing as fallback"""
        query_lower = query.lower()
        
        # Extract student ID
        student_id = None
        student_match = re.search(r's(?:tudent)?\s*([sS]\d{3})', query)
        if student_match:
            student_id = student_match.group(1).upper()
        
        # Extract teacher ID
        teacher_id = None
        teacher_match = re.search(r't(?:eacher)?\s*([tT]\d{3})', query)
        if teacher_match:
            teacher_id = teacher_match.group(1).upper()
        
        # Simple intent matching
        if "analyze" in query_lower or "behavior" in query_lower:
            return {
                "tool": "analyze_student_behavior",
                "parameters": {"student_id": student_id},
                "confidence": 0.7,
                "reasoning": "Query mentions analysis or behavior"
            }
        elif "intervention" in query_lower and "create" in query_lower:
            return {
                "tool": "create_intervention_task",
                "parameters": {"student_id": student_id, "assigned_to": teacher_id},
                "confidence": 0.7,
                "reasoning": "Query mentions creating intervention"
            }
        elif "task" in query_lower and "assign" in query_lower:
            return {
                "tool": "create_intervention_task",
                "parameters": {"student_id": student_id, "assigned_to": teacher_id},
                "confidence": 0.6,
                "reasoning": "Query mentions task assignment"
            }
        elif "at risk" in query_lower or "risk" in query_lower:
            return {
                "tool": "identify_at_risk_students",
                "parameters": {},
                "confidence": 0.8,
                "reasoning": "Query mentions at-risk students"
            }
        elif "class" in query_lower or "overview" in query_lower:
            return {
                "tool": "get_class_overview",
                "parameters": {},
                "confidence": 0.7,
                "reasoning": "Query mentions class overview"
            }
        elif "learning path" in query_lower:
            return {
                "tool": "create_learning_path",
                "parameters": {"student_id": student_id},
                "confidence": 0.7,
                "reasoning": "Query mentions learning path"
            }
        elif "predict" in query_lower or "performance" in query_lower:
            return {
                "tool": "predict_student_performance",
                "parameters": {"student_id": student_id},
                "confidence": 0.7,
                "reasoning": "Query mentions prediction or performance"
            }
        else:
            return {
                "tool": None,
                "parameters": {},
                "confidence": 0.0,
                "reasoning": "No matching tool found for this query"
            }


class ConversationalRouter:
    """Route conversational queries to appropriate tools and generate responses"""
    
    def __init__(self, tool_registry: ToolRegistry, intent_parser: IntentParser):
        self.tool_registry = tool_registry
        self.intent_parser = intent_parser
        self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a natural language query and return a response"""
        # Parse the query
        parsed = self.intent_parser.parse_query(query)
        
        if not parsed["tool"]:
            return {
                "success": False,
                "message": f"I couldn't understand what you want to do. {parsed['reasoning']}",
                "suggestion": "Try asking about analyzing a student, creating tasks, or getting class overview."
            }
        
        # Get the tool
        tool = self.tool_registry.get_tool(parsed["tool"])
        if not tool:
            return {
                "success": False,
                "message": f"Tool '{parsed['tool']}' not found in registry."
            }
        
        # Extract parameters, filtering out None values
        parameters = {k: v for k, v in parsed["parameters"].items() if v is not None}
        
        # Call the tool
        try:
            result = tool["function"](**parameters)
            
            # Generate natural language response
            response = self._generate_response(query, parsed, result)
            
            return {
                "success": True,
                "tool_used": parsed["tool"],
                "tool_description": tool["description"],
                "result": result,
                "natural_language_response": response,
                "confidence": parsed["confidence"]
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error executing tool: {str(e)}",
                "tool_used": parsed["tool"]
            }
    
    def _generate_response(self, query: str, parsed: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Generate a natural language response based on the result"""
        if not self.client:
            # Fallback to simple response
            return self._simple_response(parsed, result)
        
        prompt = f"""
You are a helpful assistant for a student behavior analysis system. The user asked: "{query}"

We used the tool: {parsed['tool']}
Tool description: {self.tool_registry.get_tool(parsed['tool'])['description']}

The tool returned this result:
{json.dumps(result, indent=2, default=str)}

Generate a natural, conversational response to the user. Be helpful and explain what the tool found or did. Keep it concise but informative.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM response generation failed: {e}, falling back to simple response")
            return self._simple_response(parsed, result)
    
    def _simple_response(self, parsed: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Simple response generation as fallback"""
        tool_name = parsed["tool"]
        
        if tool_name == "analyze_student_behavior":
            if "error" in result:
                return f"Sorry, I couldn't analyze the student: {result['error']}"
            return f"Analysis complete. The student has a behavioral tag of '{result.get('behavioral_tag', 'unknown')}' with average marks of {result.get('avg_marks', 0)}% and average distraction score of {result.get('avg_distraction', 0)}/10."
        
        elif tool_name == "identify_at_risk_students":
            if "error" in result:
                return f"Sorry, I couldn't identify at-risk students: {result['error']}"
            count = len(result.get("at_risk_students", []))
            return f"Found {count} at-risk students: {', '.join([s['student_id'] for s in result.get('at_risk_students', [])])}"
        
        elif tool_name == "get_class_overview":
            if "error" in result:
                return f"Sorry, I couldn't get class overview: {result['error']}"
            return f"Class overview: {result.get('total_students', 0)} students, average marks {result.get('class_avg_marks', 0)}%, average distraction {result.get('class_avg_distraction', 0)}/10."
        
        elif tool_name == "create_intervention_task":
            if "error" in result:
                return f"Sorry, I couldn't create the intervention task: {result['error']}"
            return f"Successfully created intervention task {result.get('task_id', 'unknown')} for student {result.get('student_id', 'unknown')}."
        
        else:
            if "error" in result:
                return f"Operation completed with an error: {result['error']}"
            return f"Operation completed successfully. Tool: {tool_name}"


# Global instances
tool_registry = ToolRegistry()
intent_parser = IntentParser(tool_registry)
conversational_router = ConversationalRouter(tool_registry, intent_parser)
