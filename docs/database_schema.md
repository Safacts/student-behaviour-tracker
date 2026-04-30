# Student Behavior Analysis Database Schema

This document outlines the structure of the `students_analysis.db` SQLite database. This schema is designed to support high-performance behavioral analytics and easy navigation of student records.

## Core Analytics Table

### `student_session_analytics`
This is the primary table for behavior analysis. It contains normalized records extracted from the complex JSON blobs in the source data.

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key (Auto-increment) |
| `student_id` | INTEGER | Unique identifier for the student |
| `log_date` | TEXT | Date of the activity (YYYY-MM-DD) |
| `subject_category` | TEXT | Category (e.g., sci, soc, smt, gam, pq, m) |
| `lesson_name` | TEXT | Name of the lesson or activity |
| `quiz_score` | TEXT | Raw score or percentage (if applicable) |
| `time_spent_minutes`| INTEGER | Calculated duration of the session in minutes |

---

## Primary Data Tables

### `rubix_students_data`
Source records for student activity.
- `id`: Unique record ID
- `student_id`: Student identifier
- `parent_id`: Associated parent identifier
- `lesson_mode_data`: (JSON) Detailed academic activity logs
- `general_mode_data`: (JSON) Games, rewards, and general activity logs
- `created_at` / `updated_at`: Timestamps

### `users`
Student and parent profile information.
- `id`: User ID
- `username`: Login handle
- `name`: Full name
- `role`: User role (student/parent/admin)
- `class`: Academic grade
- `school`: Associated institution
- `rewards_points`: Gamification balance

---

## Secondary & Infrastructure Tables
*Note: These tables contain raw record strings (from MySQL dumps) for exploration.*

- `community_chat`: Raw chat records
- `customer_message`: Support and communication logs
- `employee_details`: Staff information
- `feedback`: User-submitted feedback
- `game_progress`: Detailed gamification logs
- `overall_performance`: Academic performance snapshots
- `question_papers`: Meta-data for assessments
- ... (Additional infrastructure tables included in the SQL schema)

---

## Raw SQL Schema definitions

```sql
CREATE TABLE student_session_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    student_id INTEGER, 
    log_date TEXT, 
    subject_category TEXT, 
    lesson_name TEXT, 
    quiz_score TEXT, 
    time_spent_minutes INTEGER
);

CREATE TABLE rubix_students_data (
    id INTEGER PRIMARY KEY, 
    student_id INTEGER, 
    parent_id INTEGER, 
    lesson_mode_data TEXT, 
    general_mode_data TEXT, 
    created_at TEXT, 
    updated_at TEXT
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY, 
    username TEXT, 
    name TEXT, 
    role TEXT, 
    class TEXT, 
    school TEXT, 
    rewards_points INTEGER
);

-- Generic Data Tables (Raw Records)
CREATE TABLE community_chat (data TEXT);
CREATE TABLE customer_message (data TEXT);
CREATE TABLE employee_details (data TEXT);
CREATE TABLE feedback (data TEXT);
CREATE TABLE game_progress (data TEXT);
CREATE TABLE no_of_queries (data TEXT);
CREATE TABLE notification_messages (data TEXT);
CREATE TABLE overall_performance (data TEXT);
CREATE TABLE parent_student_messages (data TEXT);
CREATE TABLE question_papers (data TEXT);
CREATE TABLE reward_bookreading (data TEXT);
CREATE TABLE student_daily_logs (data TEXT);
CREATE TABLE study_plan (data TEXT);
CREATE TABLE super_admin (data TEXT);
```
