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
            generate_teacher_report,
            get_student_info,
            get_all_students,
            get_student_activity_logs,
            get_student_summary,
            generate_pdf_report_content,
            generate_meeting_agenda,
            generate_calendar_event,
            generate_recurring_schedule,
            analyze_topic_performance,
            analyze_chapter_performance,
            generate_iit_prep_report,
            export_student_data_to_csv,
            export_class_data_to_csv,
            generate_student_chart_data,
            generate_class_chart_data,
            generate_report_summary_text,
            validate_student_data,
            clean_student_data,
            add_student_activity
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
        
        self.register_tool(
            "get_student_info",
            get_student_info,
            "Get basic information about a student.",
            {"student_id": "The ID of the student"}
        )
        
        self.register_tool(
            "get_all_students",
            get_all_students,
            "Get a list of all students in the system.",
            {}
        )
        
        self.register_tool(
            "get_student_activity_logs",
            get_student_activity_logs,
            "Get activity logs for a student over a specified time period.",
            {"student_id": "The ID of the student", "days": "Optional: Number of days of history (default: 7)"}
        )
        
        self.register_tool(
            "get_student_summary",
            get_student_summary,
            "Get a summary of a student's overall performance and behavior.",
            {"student_id": "The ID of the student"}
        )
        
        self.register_tool(
            "generate_pdf_report_content",
            generate_pdf_report_content,
            "Generate content for a PDF report about a student.",
            {"student_id": "The ID of the student"}
        )
        
        self.register_tool(
            "generate_meeting_agenda",
            generate_meeting_agenda,
            "Generate an agenda for a meeting (parent-teacher, staff, etc.).",
            {"student_id": "The ID of the student", "meeting_type": "Type of meeting: parent_teacher, staff, etc."}
        )
        
        self.register_tool(
            "generate_calendar_event",
            generate_calendar_event,
            "Generate a calendar event for a student-related activity.",
            {"student_id": "The ID of the student", "event_type": "Type of event: parent_meeting, etc."}
        )
        
        self.register_tool(
            "generate_recurring_schedule",
            generate_recurring_schedule,
            "Generate a recurring schedule for a student.",
            {"student_id": "The ID of the student", "frequency": "Frequency: weekly, biweekly, monthly"}
        )
        
        self.register_tool(
            "analyze_topic_performance",
            analyze_topic_performance,
            "Analyze a student's performance by topic within subjects.",
            {"student_id": "The ID of the student"}
        )
        
        self.register_tool(
            "analyze_chapter_performance",
            analyze_chapter_performance,
            "Analyze a student's performance by chapter within subjects.",
            {"student_id": "The ID of the student"}
        )
        
        self.register_tool(
            "generate_iit_prep_report",
            generate_iit_prep_report,
            "Generate a specialized report for IIT-JEE preparation.",
            {"student_id": "The ID of the student"}
        )
        
        self.register_tool(
            "export_student_data_to_csv",
            export_student_data_to_csv,
            "Export a student's data to CSV format.",
            {"student_id": "The ID of the student"}
        )
        
        self.register_tool(
            "export_class_data_to_csv",
            export_class_data_to_csv,
            "Export the entire class data to CSV format.",
            {}
        )
        
        self.register_tool(
            "generate_student_chart_data",
            generate_student_chart_data,
            "Generate chart data for visualizing student performance.",
            {"student_id": "The ID of the student", "chart_type": "Type of chart: performance, marks, etc."}
        )
        
        self.register_tool(
            "generate_class_chart_data",
            generate_class_chart_data,
            "Generate chart data for visualizing class comparison.",
            {"chart_type": "Type of chart: comparison, distribution, etc."}
        )
        
        self.register_tool(
            "generate_report_summary_text",
            generate_report_summary_text,
            "Generate a text summary of a student's report.",
            {"student_id": "The ID of the student"}
        )
        
        self.register_tool(
            "validate_student_data",
            validate_student_data,
            "Validate a student's data for quality and completeness.",
            {"student_id": "The ID of the student"}
        )
        
        self.register_tool(
            "clean_student_data",
            clean_student_data,
            "Clean and normalize a student's data.",
            {"student_id": "The ID of the student"}
        )
        
        self.register_tool(
            "add_student_activity",
            add_student_activity,
            "Add a new activity log entry for a student.",
            {"student_id": "The ID of the student", "student_name": "Name of the student", "date": "Date in YYYY-MM-DD format", "activity_type": "Type of activity", "subject": "Subject", "topic": "Topic", "chapter": "Chapter", "time_spent_mins": "Time spent in minutes", "marks_achieved_percent": "Marks percentage", "distraction_score": "Distraction score 0-10"}
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
    
    def parse_query(self, query: str, use_llm: bool = True) -> Dict[str, Any]:
        """Parse a natural language query to extract intent and parameters"""
        # Handle greetings first (before LLM call)
        greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
        if any(greeting in query.lower() for greeting in greetings):
            return {
                "tools": [],
                "is_compound": False,
                "confidence": 1.0,
                "is_greeting": True
            }
        
        if not self.client or not use_llm:
            # Fallback to simple pattern matching if no LLM available or heuristic mode requested
            return self._simple_parse(query)
        
        tool_descriptions = self.tool_registry.get_tool_descriptions()
        
        prompt = f"""
You are an intent parser for a student behavior analysis system. Analyze the user's query and determine which tool(s) to call and what parameters to extract.

Available tools:
{tool_descriptions}

User query: "{query}"

Respond in JSON format with this structure:
{{
    "tools": [
        {{
            "tool": "tool_name",
            "parameters": {{"param_name": "value or null if not provided"}},
            "reasoning": "brief explanation of why this tool was chosen"
        }}
    ],
    "is_compound": true/false,
    "confidence": 0.0 to 1.0
}}

IMPORTANT:
- If the query contains multiple actions (e.g., "analyze student AND create learning path"), return multiple tools in the tools array
- If the query contains a single action, return one tool in the tools array
- Set is_compound to true if multiple tools are needed, false otherwise
- If no tool matches, return an empty tools array
"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            print(f"DEBUG: LLM returned for query '{query}': {json.dumps(result, indent=2)}")
            
            # Backward compatibility: if old format, convert to new format
            if "tool" in result and "tools" not in result:
                result["tools"] = [{
                    "tool": result.get("tool"),
                    "parameters": result.get("parameters", {}),
                    "reasoning": result.get("reasoning", "")
                }]
                result["is_compound"] = False
                del result["tool"]
                del result["parameters"]
                del result["reasoning"]
                print(f"DEBUG: Converted old format to new format: {json.dumps(result, indent=2)}")
            
            return result
        except Exception as e:
            print(f"LLM parsing failed: {e}, falling back to simple parse")
            return self._simple_parse(query)
    
    def _simple_parse(self, query: str) -> Dict[str, Any]:
        """Simple pattern-based parsing as fallback"""
        query_lower = query.lower()
        
        # Handle greetings
        greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
        if any(greeting in query_lower for greeting in greetings):
            return {
                "tools": [],
                "is_compound": False,
                "confidence": 1.0,
                "is_greeting": True
            }
        
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
        
        # Detect compound queries (simple heuristic)
        compound_keywords = [" and ", " then ", " also ", " plus ", " followed by "]
        is_compound = any(keyword in query_lower for keyword in compound_keywords)
        
        # Simple intent matching
        if "analyze" in query_lower or "behavior" in query_lower:
            tools = [{
                "tool": "analyze_student_behavior",
                "parameters": {"student_id": student_id},
                "reasoning": "Query mentions analysis or behavior"
            }]
        elif "intervention" in query_lower and "create" in query_lower:
            tools = [{
                "tool": "create_intervention_task",
                "parameters": {"student_id": student_id, "assigned_to": teacher_id},
                "reasoning": "Query mentions creating intervention"
            }]
        elif "task" in query_lower and "assign" in query_lower:
            tools = [{
                "tool": "create_intervention_task",
                "parameters": {"student_id": student_id, "assigned_to": teacher_id},
                "reasoning": "Query mentions task assignment"
            }]
        elif "at risk" in query_lower or "risk" in query_lower:
            tools = [{
                "tool": "identify_at_risk_students",
                "parameters": {},
                "reasoning": "Query mentions at-risk students"
            }]
        elif "class" in query_lower or "overview" in query_lower:
            tools = [{
                "tool": "get_class_overview",
                "parameters": {},
                "reasoning": "Query mentions class overview"
            }]
        else:
            tools = []
        
        # If compound query detected with "and", try to extract second intent
        if is_compound and " and " in query_lower:
            parts = query_lower.split(" and ")
            if len(parts) == 2:
                second_part = parts[1].strip()
                if "learning path" in second_part or "path" in second_part:
                    tools.append({
                        "tool": "create_learning_path",
                        "parameters": {"student_id": student_id},
                        "reasoning": "Second part mentions learning path"
                    })
                elif "intervention" in second_part:
                    tools.append({
                        "tool": "create_intervention_task",
                        "parameters": {"student_id": student_id, "assigned_to": teacher_id},
                        "reasoning": "Second part mentions intervention"
                    })
        
        return {
            "tools": tools,
            "is_compound": len(tools) > 1,
            "confidence": 0.6 if is_compound else 0.7
        }


class ConversationalRouter:
    """Route conversational queries to appropriate tools and generate responses"""
    
    def __init__(self, tool_registry: ToolRegistry, intent_parser: IntentParser):
        self.tool_registry = tool_registry
        self.intent_parser = intent_parser
        self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
    
    def _get_role_greeting(self, role: str) -> str:
        """Get role-based greeting response"""
        greetings = {
            "developer": "Hello! I'm your AI assistant for the student behavior analytics system. I can help you with technical details, API documentation, debugging, and system analysis.",
            "student": "Hello! I'm here to help you understand your learning patterns and improve your academic performance. I can analyze your study habits and suggest improvements.",
            "faculty": "Hello! I'm your AI assistant for class management. I can help you analyze student performance, identify at-risk students, and suggest teaching strategies.",
            "parent": "Hello! I'm here to help you understand your child's academic journey. I can provide insights into their progress and suggest ways to support their learning.",
            "principal": "Hello! I'm your AI assistant for school-wide analytics. I can help you with performance metrics, trends, and strategic insights for the institution."
        }
        return greetings.get(role, greetings["student"])
    
    def _adapt_response_for_role(self, response: str, role: str, tool_used: str) -> str:
        """Adapt the response based on user role"""
        # Role-specific adaptations
        role_prefixes = {
            "developer": {
                "default": "🔧 Technical details: "
            },
            "student": {
                "default": "📚 Here's what you need to know: "
            },
            "faculty": {
                "default": "👨‍🏫 Teaching insight: "
            },
            "parent": {
                "default": "👨‍👩‍👧 For your child: "
            },
            "principal": {
                "default": "🏫 School-wide view: "
            }
        }
        
        # Add role-specific context
        prefix = role_prefixes.get(role, {}).get("default", "")
        
        # For technical queries, developers get more detail
        if role == "developer" and tool_used in ["behavior", "learning_path", "intervention"]:
            response = response + " [API endpoints: /api/agents/" + tool_used + "/{student_id}]"
        
        # For students, simplify the language
        if role == "student":
            response = response.replace("behavioral patterns", "study habits")
            response = response.replace("intervention strategies", "improvement tips")
            response = response.replace("performance metrics", "your progress")
        
        return prefix + response
    
    def process_query(self, query: str, use_llm: bool = True, role: str = "student") -> Dict[str, Any]:
        """Process a natural language query and return a response"""
        # Parse the query
        parsed = self.intent_parser.parse_query(query, use_llm)
        
        # Check if no tools were found
        if not parsed.get("tools") or len(parsed["tools"]) == 0:
            # Handle greetings with role-based responses
            if parsed.get("is_greeting"):
                greeting_response = self._get_role_greeting(role)
                return {
                    "success": True,
                    "tool_used": "greeting",
                    "natural_language_response": greeting_response,
                    "confidence": 1.0,
                    "is_compound": False
                }
            return {
                "success": False,
                "message": f"I couldn't understand what you want to do.",
                "suggestion": "Try asking about analyzing a student, creating tasks, or getting class overview."
            }
        
        # Handle compound queries (multiple tools)
        if parsed.get("is_compound", False):
            return self._process_compound_query(query, parsed, role)
        
        # Handle single tool queries (backward compatibility)
        tool_info = parsed["tools"][0]
        tool_name = tool_info["tool"]
        tool = self.tool_registry.get_tool(tool_name)
        
        if not tool:
            return {
                "success": False,
                "message": f"Tool '{tool_name}' not found in registry."
            }
        
        # Extract parameters, filtering out None values
        parameters = {k: v for k, v in tool_info["parameters"].items() if v is not None}
        
        # Call the tool
        try:
            result = tool["function"](**parameters)
            
            # Generate natural language response with role context
            response = self._generate_response(query, tool_info, result, role)
            
            return {
                "success": True,
                "tool_used": tool_name,
                "tool_description": tool["description"],
                "result": result,
                "natural_language_response": response,
                "confidence": parsed["confidence"],
                "is_compound": False
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error executing tool: {str(e)}",
                "tool_used": tool_name
            }
    
    def _process_compound_query(self, query: str, parsed: Dict[str, Any], role: str = "student") -> Dict[str, Any]:
        """Process a compound query with multiple tools"""
        tools_info = parsed["tools"]
        results = []
        errors = []
        
        for tool_info in tools_info:
            tool_name = tool_info["tool"]
            tool = self.tool_registry.get_tool(tool_name)
            
            if not tool:
                errors.append(f"Tool '{tool_name}' not found in registry.")
                continue
            
            # Extract parameters, filtering out None values
            parameters = {k: v for k, v in tool_info["parameters"].items() if v is not None}
            
            # Call the tool
            try:
                result = tool["function"](**parameters)
                results.append({
                    "tool": tool_name,
                    "tool_description": tool["description"],
                    "result": result,
                    "success": True
                })
            except Exception as e:
                errors.append(f"Error executing {tool_name}: {str(e)}")
                results.append({
                    "tool": tool_name,
                    "tool_description": tool["description"],
                    "result": None,
                    "success": False,
                    "error": str(e)
                })
        
        # Generate combined response
        combined_response = self._generate_compound_response(query, results, role)
        
        return {
            "success": len([r for r in results if r["success"]]) > 0,
            "is_compound": True,
            "tools_used": [r["tool"] for r in results],
            "results": results,
            "errors": errors,
            "natural_language_response": combined_response,
            "confidence": parsed["confidence"]
        }
    
    def _get_role_greeting(self, role: str) -> str:
        """Generate a role-based greeting message"""
        greetings = {
            "developer": "Hello! I'm your AI assistant for student behavior analytics. I can help you with technical details, API documentation, debugging, and system integration. Ask me about endpoints, data structures, or development workflows.",
            "student": "Hello! I'm your AI assistant for student behavior analytics. I can help you understand your learning patterns, suggest study strategies, and explain your progress in simple terms. Try asking: 'How am I doing in my studies?' or 'What can I do to improve?'",
            "faculty": "Hello! I'm your AI assistant for student behavior analytics. I can help you with class insights, teaching recommendations, and student performance analysis. Try asking: 'Show me class performance' or 'Which students need intervention?'",
            "parent": "Hello! I'm your AI assistant for student behavior analytics. I can help you understand your child's progress, identify concerns, and suggest next steps. Try asking: 'How is my child doing?' or 'What should I focus on?'",
            "principal": "Hello! I'm your AI assistant for student behavior analytics. I can help you with school-wide metrics, trends, and strategic insights. Try asking: 'Show me school-wide performance' or 'What are the key trends?'"
        }
        return greetings.get(role, greetings["student"])
    
    def _get_role_instructions(self, role: str) -> str:
        """Get role-specific instructions for response generation"""
        instructions = {
            "developer": "Provide technical details, API information, debugging suggestions, and system-level insights. Use technical terminology when appropriate.",
            "student": "Provide simple, actionable explanations. Avoid jargon. Focus on what the student can do to improve. Be encouraging and supportive.",
            "faculty": "Provide class-level insights, teaching recommendations, and pedagogical suggestions. Focus on actionable classroom strategies.",
            "parent": "Provide information about child's progress in understandable terms. Focus on concerns and practical next steps for parents. Be reassuring but honest.",
            "principal": "Provide school-wide metrics, trends, and strategic insights. Focus on data-driven decision making and systemic improvements."
        }
        return instructions.get(role, instructions["student"])
    
    def _generate_response(self, query: str, tool_info: Dict[str, Any], result: Dict[str, Any], role: str = "student") -> str:
        """Generate a natural language response based on the result"""
        if not self.client:
            # Fallback to simple response with role context
            return self._simple_response(tool_info, result, role)
        
        tool_name = tool_info["tool"]
        tool = self.tool_registry.get_tool(tool_name)
        
        # Get role-specific instructions
        role_instructions = self._get_role_instructions(role)
        
        prompt = f"""
You are a helpful assistant for a student behavior analysis system. The user asked: "{query}"

User role: {role}
{role_instructions}

We used the tool: {tool_name}
Tool description: {tool['description'] if tool else 'Unknown'}

The tool returned this result:
{json.dumps(result, indent=2, default=str)}

Generate a natural, conversational response to the user. Be helpful and explain what the tool found or did. Keep it concise but informative. Tailor your response to the user's role ({role}).
"""
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM response generation failed: {e}, falling back to simple response")
            return self._simple_response(tool_info, result, role)
    
    def _generate_compound_response(self, query: str, results: List[Dict[str, Any]], role: str = "student") -> str:
        """Generate a combined natural language response for compound queries"""
        if not self.client:
            # Fallback to simple compound response
            return self._simple_compound_response(results)
        
        # Build a summary of all tool results
        results_summary = []
        for result in results:
            if result["success"]:
                results_summary.append(f"- {result['tool']}: {json.dumps(result['result'], indent=2, default=str)}")
            else:
                results_summary.append(f"- {result['tool']}: Failed - {result.get('error', 'Unknown error')}")
        
        # Get role-specific instructions
        role_instructions = self._get_role_instructions(role)
        
        prompt = f"""
You are a helpful assistant for a student behavior analysis system. The user asked: "{query}"

User role: {role}
{role_instructions}

We executed multiple tools and got these results:
{chr(10).join(results_summary)}

Generate a natural, conversational response that combines all these results into a coherent summary. Explain what each tool found or did, and provide an overall synthesis. Keep it concise but informative. Tailor your response to the user's role ({role}).
"""
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM compound response generation failed: {e}, falling back to simple response")
            return self._simple_compound_response(results, role)
    
    def _simple_response(self, tool_info: Dict[str, Any], result: Dict[str, Any], role: str = "student") -> str:
        """Simple response generation as fallback"""
        tool_name = tool_info["tool"]
        
        if tool_name == "analyze_student_behavior":
            if "error" in result:
                return f"Sorry, I couldn't analyze the student: {result['error']}"
            base_response = f"Analysis complete. The student has a behavioral tag of '{result.get('behavioral_tag', 'unknown')}' with average marks of {result.get('avg_marks', 0)}% and average distraction score of {result.get('avg_distraction', 0)}/10."
            return self._adapt_response_for_role(base_response, role, tool_name)
        
        elif tool_name == "identify_at_risk_students":
            if "error" in result:
                return f"Sorry, I couldn't identify at-risk students: {result['error']}"
            count = len(result.get("at_risk_students", []))
            base_response = f"Found {count} at-risk students: {', '.join([s['student_id'] for s in result.get('at_risk_students', [])])}"
            return self._adapt_response_for_role(base_response, role, tool_name)
        
        elif tool_name == "get_class_overview":
            if "error" in result:
                return f"Sorry, I couldn't get class overview: {result['error']}"
            base_response = f"Class overview: {result.get('total_students', 0)} students, average marks {result.get('class_avg_marks', 0)}%, average distraction {result.get('class_avg_distraction', 0)}/10."
            return self._adapt_response_for_role(base_response, role, tool_name)
        
        elif tool_name == "create_intervention_task":
            if "error" in result:
                return f"Sorry, I couldn't create the intervention task: {result['error']}"
            return f"Successfully created intervention task {result.get('task_id', 'unknown')} for student {result.get('student_id', 'unknown')}."
        
        else:
            if "error" in result:
                return f"Operation completed with an error: {result['error']}"
            return f"Operation completed successfully. Tool: {tool_name}"
    
    def _simple_compound_response(self, results: List[Dict[str, Any]], role: str = "student") -> str:
        """Simple compound response generation as fallback"""
        responses = []
        for result in results:
            if result["success"]:
                tool_name = result["tool"]
                result_data = result["result"]
                if tool_name == "analyze_student_behavior":
                    responses.append(f"Analysis: behavioral tag '{result_data.get('behavioral_tag', 'unknown')}', marks {result_data.get('avg_marks', 0)}%")
                elif tool_name == "create_learning_path":
                    responses.append(f"Learning path created at level '{result_data.get('level', 'unknown')}'")
                elif tool_name == "create_intervention_task":
                    responses.append(f"Intervention task {result_data.get('task_id', 'unknown')} created")
                else:
                    responses.append(f"{tool_name}: completed successfully")
            else:
                responses.append(f"{result['tool']}: failed - {result.get('error', 'Unknown error')}")
        
        # Add role-specific context
        role_context = ""
        if role == "student":
            role_context = " Here's what I found for your studies."
        elif role == "parent":
            role_context = " Here's what I found about your child."
        elif role == "faculty":
            role_context = " Here are the class insights."
        elif role == "principal":
            role_context = " Here are the school-wide metrics."
        elif role == "developer":
            role_context = " Here are the technical details."
        
        return "I've completed the following tasks: " + ". ".join(responses) + role_context


# Global instances
tool_registry = ToolRegistry()
intent_parser = IntentParser(tool_registry)
conversational_router = ConversationalRouter(tool_registry, intent_parser)
