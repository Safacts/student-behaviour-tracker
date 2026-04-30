"""
Workflow Node Implementations - Execute individual workflow nodes
"""
import sqlite3
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)

class NodeExecutor:
    """Execute workflow nodes"""
    
    def __init__(self, db_path: str = "behavior.db"):
        self.db_path = db_path
        load_dotenv()
    
    def execute(self, node, workflow) -> Dict[str, Any]:
        """Execute a node based on its type"""
        node_type = node.type
        
        if node_type == "data_query":
            return self._execute_data_query(node)
        elif node_type == "ai_process":
            return self._execute_ai_process(node, workflow)
        elif node_type == "email_send":
            return self._execute_email_send(node, workflow)
        elif node_type == "condition":
            return self._execute_condition(node, workflow)
        else:
            return {"success": False, "error": f"Unknown node type: {node_type}"}
    
    def _execute_data_query(self, node) -> Dict[str, Any]:
        """Execute a database query node"""
        try:
            query = node.config.get("query")
            params = node.config.get("params", {})
            
            if not query:
                return {"success": False, "error": "Query not specified"}
            
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Convert rows to list of dicts
            data = [dict(row) for row in rows]
            
            conn.close()
            
            return {
                "success": True,
                "data": data,
                "count": len(data)
            }
        except Exception as e:
            logger.error(f"Data query failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _execute_ai_process(self, node, workflow) -> Dict[str, Any]:
        """Execute an AI processing node"""
        try:
            from llm_service import generate_query_from_natural_language
            
            prompt = node.config.get("prompt")
            input_data = node.config.get("input_data", None)
            
            if not prompt:
                return {"success": False, "error": "Prompt not specified"}
            
            # Use Groq for AI processing
            result = generate_query_from_natural_language(prompt)
            
            return {
                "success": True,
                "data": result
            }
        except Exception as e:
            logger.error(f"AI process failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _execute_email_send(self, node, workflow) -> Dict[str, Any]:
        """Execute an email sending node"""
        try:
            to_email = node.config.get("to")
            subject = node.config.get("subject")
            body = node.config.get("body")
            
            if not all([to_email, subject, body]):
                return {"success": False, "error": "Email configuration incomplete"}
            
            # SMTP configuration
            smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
            smtp_username = os.getenv("SMTP_USERNAME")
            smtp_password = os.getenv("SMTP_PASSWORD")
            
            if not smtp_username or not smtp_password:
                return {"success": False, "error": "SMTP credentials not configured"}
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.quit()
            
            return {
                "success": True,
                "data": {"sent_to": to_email, "subject": subject}
            }
        except Exception as e:
            logger.error(f"Email send failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _execute_condition(self, node, workflow) -> Dict[str, Any]:
        """Execute a condition node"""
        try:
            condition = node.config.get("condition")
            input_data = node.config.get("input_data", {})
            
            if not condition:
                return {"success": False, "error": "Condition not specified"}
            
            # Simple condition evaluation
            result = self._evaluate_condition(condition, input_data)
            
            return {
                "success": True,
                "data": {"condition": condition, "result": result}
            }
        except Exception as e:
            logger.error(f"Condition evaluation failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _evaluate_condition(self, condition: str, data: Dict[str, Any]) -> bool:
        """Evaluate a condition against data"""
        # Simple condition evaluation - can be enhanced
        if condition == "has_data":
            return bool(data and len(data) > 0)
        elif condition == "no_data":
            return not (data and len(data) > 0)
        elif condition == "data_gt_0":
            if isinstance(data, (int, float)):
                return data > 0
            if isinstance(data, list) and len(data) > 0:
                return True
            return False
        return True

if __name__ == "__main__":
    # Test node executor
    executor = NodeExecutor()
    
    # Test data query node
    from workflow_engine import Node
    node = Node(id="test", type="data_query", config={"query": "SELECT * FROM student_activity LIMIT 5"})
    result = executor.execute(node, None)
    print("Data query result:", result)
