"""
Advanced data validation system
"""
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import re
from enum import Enum

class ValidationError(Exception):
    """Custom validation error"""
    def __init__(self, message: str, field: str = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(message)

class ValidationLevel(Enum):
    """Validation strictness levels"""
    STRICT = "strict"
    MODERATE = "moderate"
    LENIENT = "lenient"

class DataValidator:
    """Production-ready data validator"""
    
    def __init__(self, level: ValidationLevel = ValidationLevel.MODERATE):
        self.level = level
        self.errors = []
        self.warnings = []
    
    def validate_student_id(self, student_id: str) -> Tuple[bool, Optional[str]]:
        """Validate student ID format"""
        if not student_id:
            return False, "Student ID cannot be empty"
        
        if self.level == ValidationLevel.STRICT:
            if not re.match(r'^[A-Z]\d{3,4}$', student_id):
                return False, "Student ID must match pattern: Letter followed by 3-4 digits (e.g., S001)"
        elif self.level == ValidationLevel.MODERATE:
            if len(student_id) < 3:
                return False, "Student ID must be at least 3 characters"
        
        return True, None
    
    def validate_student_name(self, name: str) -> Tuple[bool, Optional[str]]:
        """Validate student name"""
        if not name:
            return False, "Student name cannot be empty"
        
        if len(name) > 100:
            return False, "Student name cannot exceed 100 characters"
        
        if self.level == ValidationLevel.STRICT:
            if not re.match(r'^[a-zA-Z\s\-\'\.]+$', name):
                return False, "Student name contains invalid characters"
        
        return True, None
    
    def validate_marks(self, marks: float) -> Tuple[bool, Optional[str]]:
        """Validate marks percentage"""
        if not isinstance(marks, (int, float)):
            return False, "Marks must be a number"
        
        if marks < 0 or marks > 100:
            return False, "Marks must be between 0 and 100"
        
        return True, None
    
    def validate_study_time(self, time_minutes: int) -> Tuple[bool, Optional[str]]:
        """Validate study time in minutes"""
        if not isinstance(time_minutes, (int, float)):
            return False, "Study time must be a number"
        
        if time_minutes < 0:
            return False, "Study time cannot be negative"
        
        if time_minutes > 1440:  # 24 hours
            return False, "Study time cannot exceed 24 hours (1440 minutes)"
        
        return True, None
    
    def validate_distraction_score(self, score: float) -> Tuple[bool, Optional[str]]:
        """Validate distraction score"""
        if not isinstance(score, (int, float)):
            return False, "Distraction score must be a number"
        
        if score < 0 or score > 10:
            return False, "Distraction score must be between 0 and 10"
        
        return True, None
    
    def validate_date(self, date_str: str) -> Tuple[bool, Optional[str]]:
        """Validate date format"""
        if not date_str:
            return False, "Date cannot be empty"
        
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True, None
        except ValueError:
            return False, "Date must be in YYYY-MM-DD format"
    
    def validate_api_key(self, api_key: str) -> Tuple[bool, Optional[str]]:
        """Validate API key format"""
        if not api_key:
            return False, "API key cannot be empty"
        
        if len(api_key) < 16:
            return False, "API key must be at least 16 characters"
        
        return True, None
    
    def validate_student_data(self, student_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate complete student data"""
        errors = []
        
        # Validate student_id
        valid, error = self.validate_student_id(student_data.get('student_id'))
        if not valid:
            errors.append(error)
        
        # Validate student_name
        valid, error = self.validate_student_name(student_data.get('student_name'))
        if not valid:
            errors.append(error)
        
        # Validate marks
        if 'avg_marks' in student_data:
            valid, error = self.validate_marks(student_data['avg_marks'])
            if not valid:
                errors.append(error)
        
        # Validate study time
        if 'total_study_time' in student_data:
            valid, error = self.validate_study_time(student_data['total_study_time'])
            if not valid:
                errors.append(error)
        
        # Validate distraction score
        if 'avg_distraction' in student_data:
            valid, error = self.validate_distraction_score(student_data['avg_distraction'])
            if not valid:
                errors.append(error)
        
        return len(errors) == 0, errors
    
    def validate_activity_log(self, activity_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate activity log entry"""
        errors = []
        
        # Validate required fields
        if 'student_id' not in activity_data:
            errors.append("Student ID is required")
        else:
            valid, error = self.validate_student_id(activity_data['student_id'])
            if not valid:
                errors.append(error)
        
        if 'date' not in activity_data:
            errors.append("Date is required")
        else:
            valid, error = self.validate_date(activity_data['date'])
            if not valid:
                errors.append(error)
        
        # Validate optional fields
        if 'time_spent_mins' in activity_data:
            valid, error = self.validate_study_time(activity_data['time_spent_mins'])
            if not valid:
                errors.append(error)
        
        if 'distraction_score' in activity_data:
            valid, error = self.validate_distraction_score(activity_data['distraction_score'])
            if not valid:
                errors.append(error)
        
        if 'marks_achieved_percent' in activity_data:
            valid, error = self.validate_marks(activity_data['marks_achieved_percent'])
            if not valid:
                errors.append(error)
        
        return len(errors) == 0, errors
    
    def sanitize_input(self, input_str: str) -> str:
        """Sanitize user input to prevent injection attacks"""
        if not input_str:
            return ""
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", ';', '&', '|', '$', '`', '\\']
        for char in dangerous_chars:
            input_str = input_str.replace(char, '')
        
        return input_str.strip()
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary"""
        return {
            "level": self.level.value,
            "errors": self.errors,
            "warnings": self.warnings,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "is_valid": len(self.errors) == 0
        }

# Global validator instances
strict_validator = DataValidator(ValidationLevel.STRICT)
moderate_validator = DataValidator(ValidationLevel.MODERATE)
lenient_validator = DataValidator(ValidationLevel.LENIENT)
