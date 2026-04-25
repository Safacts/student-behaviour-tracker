"""
Workflow Automation Engine - n8n-like workflow execution system
"""
import sqlite3
import json
import uuid
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class NodeStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Node:
    id: str
    type: str
    config: Dict[str, Any]
    status: NodeStatus = NodeStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@dataclass
class Edge:
    source: str
    target: str
    condition: Optional[str] = None

@dataclass
class Workflow:
    id: str
    name: str
    description: str
    nodes: List[Node]
    edges: List[Edge]
    status: WorkflowStatus = WorkflowStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class WorkflowEngine:
    """Execute workflows with node-based orchestration"""
    
    def __init__(self, db_path: str = "behavior.db"):
        self.db_path = db_path
        self._init_workflow_tables()
    
    def _init_workflow_tables(self):
        """Initialize workflow tables in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workflows (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                nodes JSON NOT NULL,
                edges JSON NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workflow_executions (
                id TEXT PRIMARY KEY,
                workflow_id TEXT NOT NULL,
                status TEXT NOT NULL,
                result JSON,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (workflow_id) REFERENCES workflows(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_workflow(self, workflow: Workflow) -> str:
        """Save workflow to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        nodes_data = [
            {
                "id": node.id,
                "type": node.type,
                "config": node.config,
                "status": node.status.value
            }
            for node in workflow.nodes
        ]
        
        edges_data = [
            {"source": edge.source, "target": edge.target, "condition": edge.condition}
            for edge in workflow.edges
        ]
        
        cursor.execute("""
            INSERT OR REPLACE INTO workflows (id, name, description, nodes, edges, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            workflow.id,
            workflow.name,
            workflow.description,
            json.dumps(nodes_data),
            json.dumps(edges_data),
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
        
        return workflow.id
    
    def load_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Load workflow from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM workflows WHERE id = ?", (workflow_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        workflow_id, name, description, nodes_json, edges_json, created_at, updated_at = row
        
        nodes_data = json.loads(nodes_json)
        edges_data = json.loads(edges_json)
        
        nodes = [
            Node(
                id=n["id"],
                type=n["type"],
                config=n["config"],
                status=NodeStatus(n.get("status", "pending"))
            )
            for n in nodes_data
        ]
        
        edges = [
            Edge(
                source=e["source"],
                target=e["target"],
                condition=e.get("condition")
            )
            for e in edges_data
        ]
        
        conn.close()
        
        return Workflow(
            id=workflow_id,
            name=name,
            description=description,
            nodes=nodes,
            edges=edges
        )
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, description, created_at FROM workflows ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        workflows = [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "created_at": row[3]
            }
            for row in rows
        ]
        
        conn.close()
        return workflows
    
    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a workflow"""
        workflow = self.load_workflow(workflow_id)
        
        if not workflow:
            return {"success": False, "error": "Workflow not found"}
        
        execution_id = str(uuid.uuid4())
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.now()
        
        # Save execution record
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO workflow_executions (id, workflow_id, status, started_at)
            VALUES (?, ?, ?, ?)
        """, (execution_id, workflow_id, "running", workflow.started_at))
        conn.commit()
        conn.close()
        
        try:
            # Execute nodes in dependency order
            execution_order = self._get_execution_order(workflow)
            
            for node_id in execution_order:
                node = next(n for n in workflow.nodes if n.id == node_id)
                
                # Check if node should be skipped (conditional edges)
                if self._should_skip_node(node, workflow):
                    node.status = NodeStatus.SKIPPED
                    continue
                
                # Execute node
                node.status = NodeStatus.RUNNING
                result = self._execute_node(node, workflow)
                
                if result["success"]:
                    node.status = NodeStatus.COMPLETED
                    node.result = result["data"]
                else:
                    node.status = NodeStatus.FAILED
                    node.error = result["error"]
                    workflow.status = WorkflowStatus.FAILED
                    break
            
            if workflow.status != WorkflowStatus.FAILED:
                workflow.status = WorkflowStatus.COMPLETED
            
            workflow.completed_at = datetime.now()
            
            # Update execution record
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE workflow_executions 
                SET status = ?, completed_at = ?, result = ?
                WHERE id = ?
            """, (
                workflow.status.value,
                workflow.completed_at,
                json.dumps({
                    "node_results": [
                        {
                            "id": n.id,
                            "type": n.type,
                            "status": n.status.value,
                            "result": n.result,
                            "error": n.error
                        }
                        for n in workflow.nodes
                    ]
                }),
                execution_id
            ))
            conn.commit()
            conn.close()
            
            # Save updated workflow state
            self.save_workflow(workflow)
            
            return {
                "success": True,
                "execution_id": execution_id,
                "workflow_id": workflow_id,
                "status": workflow.status.value,
                "node_results": [
                    {
                        "id": n.id,
                        "type": n.type,
                        "status": n.status.value,
                        "result": n.result,
                        "error": n.error
                    }
                    for n in workflow.nodes
                ]
            }
            
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.completed_at = datetime.now()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE workflow_executions 
                SET status = 'failed', completed_at = ?, result = ?
                WHERE id = ?
            """, (
                workflow.completed_at,
                json.dumps({"error": str(e)}),
                execution_id
            ))
            conn.commit()
            conn.close()
            
            return {
                "success": False,
                "execution_id": execution_id,
                "error": str(e)
            }
    
    def _get_execution_order(self, workflow: Workflow) -> List[str]:
        """Get topological execution order of nodes"""
        # Build dependency graph
        dependencies = {node.id: [] for node in workflow.nodes}
        for edge in workflow.edges:
            dependencies[edge.target].append(edge.source)
        
        # Topological sort
        visited = set()
        order = []
        
        def visit(node_id):
            if node_id in visited:
                return
            for dep in dependencies[node_id]:
                visit(dep)
            visited.add(node_id)
            order.append(node_id)
        
        for node in workflow.nodes:
            visit(node.id)
        
        return order
    
    def _should_skip_node(self, node: Node, workflow: Workflow) -> bool:
        """Check if node should be skipped based on conditional edges"""
        incoming_edges = [e for e in workflow.edges if e.target == node.id]
        
        for edge in incoming_edges:
            if edge.condition:
                source_node = next(n for n in workflow.nodes if n.id == edge.source)
                if not self._evaluate_condition(edge.condition, source_node.result):
                    return True
        
        return False
    
    def _evaluate_condition(self, condition: str, data: Dict[str, Any]) -> bool:
        """Evaluate a condition against node result data"""
        # Simple condition evaluation - can be enhanced
        if condition == "has_data":
            return bool(data and len(data) > 0)
        elif condition == "no_data":
            return not (data and len(data) > 0)
        return True
    
    def _execute_node(self, node: Node, workflow: Workflow) -> Dict[str, Any]:
        """Execute a single node"""
        from workflow_nodes import NodeExecutor
        
        executor = NodeExecutor()
        return executor.execute(node, workflow)

if __name__ == "__main__":
    # Test workflow engine
    engine = WorkflowEngine()
    
    # Create a simple workflow
    workflow = Workflow(
        id=str(uuid.uuid4()),
        name="Test Workflow",
        description="A test workflow",
        nodes=[
            Node(id="node1", type="data_query", config={"query": "SELECT * FROM student_activity LIMIT 10"}),
            Node(id="node2", type="ai_process", config={"prompt": "Summarize the data"})
        ],
        edges=[Edge(source="node1", target="node2")]
    )
    
    engine.save_workflow(workflow)
    print("Workflow saved:", workflow.id)
    
    # List workflows
    workflows = engine.list_workflows()
    print("Workflows:", workflows)
