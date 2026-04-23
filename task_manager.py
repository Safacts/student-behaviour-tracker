"""
Database-backed Task Management System
Production-ready task tracking with persistent storage
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Any
import uuid


class TaskManager:
    """Database-backed task management"""
    
    def __init__(self, db_path: str = 'behavior.db'):
        self.db_path = db_path
    
    def create_intervention_task(self, student_id: str, priority: str = "medium", due_date: str = None, assigned_to: str = None, assigned_by: str = "system") -> Dict[str, Any]:
        try:
            task_id = str(uuid.uuid4())
            if not due_date:
                due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            sql = "INSERT INTO tasks (task_id, task_type, student_id, assigned_to, assigned_by, status, priority, due_date, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, (task_id, "intervention", student_id, assigned_to, assigned_by, "pending", priority, due_date, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "task_id": task_id,
                "task_type": "intervention",
                "student_id": student_id,
                "assigned_to": assigned_to,
                "assigned_by": assigned_by,
                "status": "pending",
                "priority": priority,
                "due_date": due_date,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "message": f"Intervention task created for student {student_id}"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def create_monitoring_task(self, student_id: str, assigned_to: str, monitoring_period_days: int = 30, assigned_by: str = "system") -> Dict[str, Any]:
        try:
            task_id = str(uuid.uuid4())
            due_date = (datetime.now() + timedelta(days=monitoring_period_days)).strftime("%Y-%m-%d")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            sql = "INSERT INTO tasks (task_id, task_type, student_id, assigned_to, assigned_by, status, priority, due_date, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, (task_id, "monitoring", student_id, assigned_to, assigned_by, "pending", "medium", due_date, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "task_id": task_id,
                "task_type": "monitoring",
                "student_id": student_id,
                "assigned_to": assigned_to,
                "assigned_by": assigned_by,
                "status": "pending",
                "priority": "medium",
                "due_date": due_date,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "monitoring_period_days": monitoring_period_days,
                "message": f"Monitoring task created for student {student_id} for {monitoring_period_days} days"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def update_task_status(self, task_id: str, status: str, notes: str = None, completed_by: str = None) -> Dict[str, Any]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT task_id FROM tasks WHERE task_id = ?", (task_id,))
            if not cursor.fetchone():
                conn.close()
                return {"error": "Task not found"}
            
            if status == "completed":
                sql = "UPDATE tasks SET status = ?, completed_at = ?, completed_by = ?, notes = ? WHERE task_id = ?"
                cursor.execute(sql, (status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), completed_by, notes, task_id))
            else:
                sql = "UPDATE tasks SET status = ?, notes = ? WHERE task_id = ?"
                cursor.execute(sql, (status, notes, task_id))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "task_id": task_id,
                "status": status,
                "completed_by": completed_by,
                "message": f"Task {task_id} status updated to {status}"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_assigned_tasks(self, assigned_to: str) -> Dict[str, Any]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            sql = "SELECT task_id, task_type, student_id, assigned_to, assigned_by, status, priority, due_date, created_at, completed_at, completed_by, notes FROM tasks WHERE assigned_to = ? ORDER BY created_at DESC"
            cursor.execute(sql, (assigned_to,))
            results = cursor.fetchall()
            conn.close()
            
            tasks = []
            for row in results:
                tasks.append({
                    "task_id": row[0],
                    "task_type": row[1],
                    "student_id": row[2],
                    "assigned_to": row[3],
                    "assigned_by": row[4],
                    "status": row[5],
                    "priority": row[6],
                    "due_date": row[7],
                    "created_at": row[8],
                    "completed_at": row[9],
                    "completed_by": row[10],
                    "notes": row[11]
                })
            
            return {
                "success": True,
                "assigned_to": assigned_to,
                "task_count": len(tasks),
                "tasks": tasks
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_student_tasks(self, student_id: str) -> Dict[str, Any]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            sql = "SELECT task_id, task_type, student_id, assigned_to, assigned_by, status, priority, due_date, created_at, completed_at, completed_by, notes FROM tasks WHERE student_id = ? ORDER BY created_at DESC"
            cursor.execute(sql, (student_id,))
            results = cursor.fetchall()
            conn.close()
            
            tasks = []
            for row in results:
                tasks.append({
                    "task_id": row[0],
                    "task_type": row[1],
                    "student_id": row[2],
                    "assigned_to": row[3],
                    "assigned_by": row[4],
                    "status": row[5],
                    "priority": row[6],
                    "due_date": row[7],
                    "created_at": row[8],
                    "completed_at": row[9],
                    "completed_by": row[10],
                    "notes": row[11]
                })
            
            return {
                "success": True,
                "student_id": student_id,
                "task_count": len(tasks),
                "tasks": tasks
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_overdue_tasks(self) -> Dict[str, Any]:
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            sql = "SELECT task_id, task_type, student_id, assigned_to, assigned_by, status, priority, due_date, created_at, completed_at, completed_by, notes FROM tasks WHERE status NOT IN ('completed', 'cancelled') AND due_date < ? ORDER BY due_date ASC"
            cursor.execute(sql, (today,))
            results = cursor.fetchall()
            conn.close()
            
            tasks = []
            for row in results:
                tasks.append({
                    "task_id": row[0],
                    "task_type": row[1],
                    "student_id": row[2],
                    "assigned_to": row[3],
                    "assigned_by": row[4],
                    "status": row[5],
                    "priority": row[6],
                    "due_date": row[7],
                    "created_at": row[8],
                    "completed_at": row[9],
                    "completed_by": row[10],
                    "notes": row[11]
                })
            
            return {
                "success": True,
                "total_overdue": len(tasks),
                "tasks": tasks
            }
        except Exception as e:
            return {"error": str(e)}


class TeacherAssignmentManager:
    """Database-backed teacher assignment management"""
    
    def __init__(self, db_path: str = 'behavior.db'):
        self.db_path = db_path
    
    def assign_teacher_to_student(self, student_id: str, teacher_id: str, subject: str, assigned_by: str = "system") -> Dict[str, Any]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM teacher_assignments WHERE student_id = ? AND teacher_id = ? AND subject = ? AND is_active = 1", (student_id, teacher_id, subject))
            existing = cursor.fetchone()
            
            if existing:
                conn.close()
                return {"error": "Assignment already exists"}
            
            sql = "INSERT INTO teacher_assignments (student_id, teacher_id, subject, assigned_at, assigned_by, is_active) VALUES (?, ?, ?, ?, ?, 1)"
            cursor.execute(sql, (student_id, teacher_id, subject, datetime.now().strftime("%Y-%m-%d"), assigned_by))
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "student_id": student_id,
                "teacher_id": teacher_id,
                "subject": subject,
                "assignment_date": datetime.now().strftime("%Y-%m-%d"),
                "assigned_by": assigned_by,
                "message": f"Teacher {teacher_id} assigned to student {student_id} for {subject}"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_teacher_responsibilities(self, teacher_id: str) -> Dict[str, Any]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            sql = "SELECT student_id, subject, assigned_at, assigned_by FROM teacher_assignments WHERE teacher_id = ? AND is_active = 1 ORDER BY assigned_at DESC"
            cursor.execute(sql, (teacher_id,))
            results = cursor.fetchall()
            conn.close()
            
            if not results:
                return {
                    "success": True,
                    "teacher_id": teacher_id,
                    "total_responsibilities": 0,
                    "student_summary": [],
                    "assignments": []
                }
            
            responsibilities = []
            for row in results:
                student_id, subject, assigned_at, assigned_by = row
                responsibilities.append({
                    "student_id": student_id,
                    "subject": subject,
                    "assigned_date": assigned_at,
                    "assigned_by": assigned_by
                })
            
            student_summary = {}
            for resp in responsibilities:
                student_id = resp['student_id']
                if student_id not in student_summary:
                    student_summary[student_id] = {
                        "student_id": student_id,
                        "subjects": [],
                        "assigned_date": resp['assigned_date']
                    }
                student_summary[student_id]['subjects'].append(resp['subject'])
            
            return {
                "success": True,
                "teacher_id": teacher_id,
                "total_responsibilities": len(responsibilities),
                "student_summary": list(student_summary.values()),
                "assignments": responsibilities
            }
        except Exception as e:
            return {"error": str(e)}


task_manager = TaskManager()
teacher_assignment_manager = TeacherAssignmentManager()
