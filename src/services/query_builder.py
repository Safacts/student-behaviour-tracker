"""
QueryBuilderService - Safe dynamic query construction for API Builder
"""
import sqlite3
from typing import Dict, Any, List, Optional
import logging
import json

logger = logging.getLogger(__name__)

class QueryBuilderService:
    """Service for building and executing safe dynamic queries"""
    
    # Whitelist of allowed tables and columns for security
    ALLOWED_TABLES = {
        'student_activity': {
            'columns': ['id', 'student_id', 'student_name', 'activity_type', 'subject', 
                       'topic', 'chapter', 'time_spent_mins', 'marks_achieved_percent', 
                       'distraction_score', 'date']
        },
        'tasks': {
            'columns': ['id', 'task_id', 'student_id', 'assigned_to', 'assigned_by', 
                       'status', 'priority', 'due_date', 'created_at', 'completed_at', 
                       'completed_by', 'notes']
        },
        'teacher_assignments': {
            'columns': ['id', 'student_id', 'teacher_id', 'subject', 'assigned_at', 
                       'assigned_by', 'is_active']
        }
    }
    
    # Allowed aggregation functions
    ALLOWED_AGGREGATIONS = ['SUM', 'AVG', 'COUNT', 'MIN', 'MAX']
    
    # Allowed comparison operators
    ALLOWED_OPERATORS = ['=', '!=', '>', '<', '>=', '<=', 'LIKE', 'IN']
    
    def __init__(self, db_path: str = 'behavior.db'):
        self.db_path = db_path
        self._init_config_table()
    
    def _init_config_table(self):
        """Initialize the API Builder configuration table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_builder_configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                config_json TEXT NOT NULL,
                created_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_config(self, name: str, config: Dict[str, Any], description: str = None, created_by: str = None) -> Dict[str, Any]:
        """Save a configuration to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            config_json = json.dumps(config)
            
            cursor.execute('''
                INSERT INTO api_builder_configs (name, description, config_json, created_by)
                VALUES (?, ?, ?, ?)
            ''', (name, description, config_json, created_by))
            
            conn.commit()
            config_id = cursor.lastrowid
            conn.close()
            
            logger.info(f"Saved API Builder config: {name} (ID: {config_id})")
            return {"success": True, "config_id": config_id, "name": name}
        except sqlite3.IntegrityError:
            conn.close()
            logger.error(f"Configuration with name '{name}' already exists")
            return {"success": False, "error": f"Configuration with name '{name}' already exists"}
        except Exception as e:
            logger.error(f"Failed to save config: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def load_config(self, name: str) -> Dict[str, Any]:
        """Load a configuration from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, description, config_json, created_by, created_at
                FROM api_builder_configs
                WHERE name = ?
            ''', (name,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return {"success": False, "error": f"Configuration '{name}' not found"}
            
            config_id, name, description, config_json, created_by, created_at = row
            
            return {
                "success": True,
                "config_id": config_id,
                "name": name,
                "description": description,
                "config": json.loads(config_json),
                "created_by": created_by,
                "created_at": created_at
            }
        except Exception as e:
            logger.error(f"Failed to load config: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def list_configs(self, created_by: str = None) -> Dict[str, Any]:
        """List all saved configurations"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if created_by:
                cursor.execute('''
                    SELECT id, name, description, created_by, created_at
                    FROM api_builder_configs
                    WHERE created_by = ?
                    ORDER BY created_at DESC
                ''', (created_by,))
            else:
                cursor.execute('''
                    SELECT id, name, description, created_by, created_at
                    FROM api_builder_configs
                    ORDER BY created_at DESC
                ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            configs = []
            for row in rows:
                config_id, name, description, created_by, created_at = row
                configs.append({
                    "id": config_id,
                    "name": name,
                    "description": description,
                    "created_by": created_by,
                    "created_at": created_at
                })
            
            return {"success": True, "configs": configs}
        except Exception as e:
            logger.error(f"Failed to list configs: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def delete_config(self, name: str) -> Dict[str, Any]:
        """Delete a configuration"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM api_builder_configs
                WHERE name = ?
            ''', (name,))
            
            conn.commit()
            deleted = cursor.rowcount
            conn.close()
            
            if deleted == 0:
                return {"success": False, "error": f"Configuration '{name}' not found"}
            
            logger.info(f"Deleted API Builder config: {name}")
            return {"success": True, "message": f"Configuration '{name}' deleted"}
        except Exception as e:
            logger.error(f"Failed to delete config: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def validate_table(self, table: str) -> bool:
        """Validate table name against whitelist"""
        return table in self.ALLOWED_TABLES
    
    def validate_column(self, table: str, column: str) -> bool:
        """Validate column name against whitelist"""
        if table not in self.ALLOWED_TABLES:
            return False
        
        # Handle aggregation functions with aliases (e.g., "AVG(marks_achieved_percent) as avg_marks")
        if '(' in column and ')' in column:
            # Extract column name from aggregation
            import re
            match = re.search(r'\(([^)]+)\)', column)
            if match:
                inner_column = match.group(1).strip()
                return inner_column in self.ALLOWED_TABLES[table]['columns']
        
        return column in self.ALLOWED_TABLES[table]['columns'] or column == '*'
    
    def build_query(self, config: Dict[str, Any]) -> tuple:
        """
        Build a safe SQL query from configuration
        Returns: (query, params)
        """
        table = config.get('data_source')
        
        # Validate table
        if not self.validate_table(table):
            raise ValueError(f"Invalid or unauthorized table: {table}")
        
        # Validate columns
        columns = config.get('columns', ['*'])
        for col in columns:
            if col != '*' and not self.validate_column(table, col):
                raise ValueError(f"Invalid or unauthorized column: {col} in table {table}")
        
        # Build SELECT clause
        select_clause = ', '.join(columns) if columns else '*'
        
        # Build WHERE clause
        where_clause, where_params = self._build_where_clause(table, config.get('filters', {}))
        
        # Build GROUP BY clause
        group_by_clause = self._build_group_by(config.get('group_by', []), table)
        
        # Build HAVING clause
        having_clause, having_params = self._build_having_clause(config.get('having', {}), table)
        
        # Build ORDER BY clause
        order_by_clause = self._build_order_by(config.get('order_by', []), table)
        
        # Build LIMIT clause
        limit_clause = f"LIMIT {config.get('limit', 100)}" if config.get('limit') else ""
        
        # Combine all clauses
        query = f"SELECT {select_clause} FROM {table}"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        if group_by_clause:
            query += f" GROUP BY {group_by_clause}"
        
        if having_clause:
            query += f" HAVING {having_clause}"
        
        if order_by_clause:
            query += f" ORDER BY {order_by_clause}"
        
        if limit_clause:
            query += f" {limit_clause}"
        
        # Combine all parameters
        all_params = where_params + having_params
        
        return query, all_params
    
    def _build_where_clause(self, table: str, filters: Dict[str, Any]) -> tuple:
        """Build WHERE clause from filters"""
        if not filters:
            return "", []
        
        conditions = []
        params = []
        
        for field, filter_config in filters.items():
            # Validate column
            if not self.validate_column(table, field):
                raise ValueError(f"Invalid column in WHERE: {field}")
            
            operator = filter_config.get('operator', '=')
            value = filter_config.get('value')
            
            if operator not in self.ALLOWED_OPERATORS:
                raise ValueError(f"Invalid operator: {operator}")
            
            if operator == 'IN':
                if not isinstance(value, list):
                    raise ValueError("IN operator requires a list of values")
                placeholders = ', '.join(['?' for _ in value])
                conditions.append(f"{field} IN ({placeholders})")
                params.extend(value)
            else:
                conditions.append(f"{field} {operator} ?")
                params.append(value)
        
        where_clause = ' AND '.join(conditions)
        return where_clause, params
    
    def _build_group_by(self, group_by: List[str], table: str) -> str:
        """Build GROUP BY clause"""
        if not group_by:
            return ""
        
        for col in group_by:
            if not self.validate_column(table, col):
                raise ValueError(f"Invalid column in GROUP BY: {col}")
        
        return ', '.join(group_by)
    
    def _build_having_clause(self, having: Dict[str, Any], table: str) -> tuple:
        """Build HAVING clause"""
        if not having:
            return "", []
        
        conditions = []
        params = []
        
        for agg_config in having:
            func = agg_config.get('function', 'COUNT')
            column = agg_config.get('column', '*')
            operator = agg_config.get('operator', '>')
            value = agg_config.get('value')
            
            if func not in self.ALLOWED_AGGREGATIONS:
                raise ValueError(f"Invalid aggregation function: {func}")
            
            if column != '*' and not self.validate_column(table, column):
                raise ValueError(f"Invalid column in HAVING: {column}")
            
            conditions.append(f"{func}({column}) {operator} ?")
            params.append(value)
        
        having_clause = ' AND '.join(conditions)
        return having_clause, params
    
    def _build_order_by(self, order_by: List[Dict[str, str]], table: str) -> str:
        """Build ORDER BY clause"""
        if not order_by:
            return ""
        
        order_clauses = []
        for order_config in order_by:
            column = order_config.get('column')
            direction = order_config.get('direction', 'ASC')
            
            if not self.validate_column(table, column):
                raise ValueError(f"Invalid column in ORDER BY: {column}")
            
            if direction.upper() not in ['ASC', 'DESC']:
                raise ValueError(f"Invalid sort direction: {direction}")
            
            order_clauses.append(f"{column} {direction}")
        
        return ', '.join(order_clauses)
    
    def execute_query(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute a query built from configuration"""
        try:
            query, params = self.build_query(config)
            logger.info(f"Executing query: {query}")
            logger.info(f"Params: {params}")
            
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(query, params)
            results = [dict(row) for row in cursor.fetchall()]
            
            conn.close()
            
            return results
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise
