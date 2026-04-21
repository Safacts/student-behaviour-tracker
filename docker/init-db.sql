-- Database initialization script for PostgreSQL
-- This script creates the necessary tables and indexes for the student behavior analytics microservice

-- Enable UUID extension if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create student_activity table for storing student learning activities
CREATE TABLE IF NOT EXISTS student_activity (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    student_name VARCHAR(255),
    log_date DATE NOT NULL,
    subject_category VARCHAR(20) NOT NULL,
    lesson_name VARCHAR(255) NOT NULL,
    quiz_score VARCHAR(20),
    time_spent_minutes INTEGER NOT NULL DEFAULT 0,
    distraction_score DECIMAL(3,2),
    marks_achieved_percent DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_student_activity_student_id ON student_activity(student_id);
CREATE INDEX IF NOT EXISTS idx_student_activity_log_date ON student_activity(log_date);
CREATE INDEX IF NOT EXISTS idx_student_activity_subject ON student_activity(subject_category);
CREATE INDEX IF NOT EXISTS idx_student_activity_student_date ON student_activity(student_id, log_date);

-- Create users table for student profiles
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    role VARCHAR(50) DEFAULT 'student',
    class VARCHAR(100),
    school VARCHAR(255),
    rewards_points INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create student_session_analytics table for aggregated analytics
CREATE TABLE IF NOT EXISTS student_session_analytics (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    log_date DATE NOT NULL,
    subject_category VARCHAR(20) NOT NULL,
    lesson_name VARCHAR(255),
    quiz_score VARCHAR(20),
    time_spent_minutes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id)
);

-- Create indexes for analytics table
CREATE INDEX IF NOT EXISTS idx_session_analytics_student_id ON student_session_analytics(student_id);
CREATE INDEX IF NOT EXISTS idx_session_analytics_date ON student_session_analytics(log_date);
CREATE INDEX IF NOT EXISTS idx_session_analytics_subject ON student_session_analytics(subject_category);

-- Create rubix_students_data table for raw data import
CREATE TABLE IF NOT EXISTS rubix_students_data (
    id SERIAL PRIMARY KEY,
    student_id INTEGER,
    parent_id INTEGER,
    lesson_mode_data TEXT,
    general_mode_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_student_activity_updated_at BEFORE UPDATE ON student_activity
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_session_analytics_updated_at BEFORE UPDATE ON student_session_analytics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for testing (optional)
INSERT INTO users (username, name, email, role, class, school) VALUES 
('student001', 'John Doe', 'john.doe@school.edu', 'student', 'Grade 10', 'Springfield High School'),
('student002', 'Jane Smith', 'jane.smith@school.edu', 'student', 'Grade 10', 'Springfield High School'),
('student003', 'Bob Johnson', 'bob.johnson@school.edu', 'student', 'Grade 11', 'Springfield High School')
ON CONFLICT (username) DO NOTHING;

-- Insert sample activity data
INSERT INTO student_activity (student_id, student_name, log_date, subject_category, lesson_name, quiz_score, time_spent_minutes, distraction_score, marks_achieved_percent) VALUES 
('student001', 'John Doe', CURRENT_DATE - INTERVAL '1 day', 'math', 'Algebra Basics', '85%', 45, 2.5, 85.0),
('student001', 'John Doe', CURRENT_DATE - INTERVAL '2 days', 'science', 'Physics Fundamentals', '78%', 38, 3.2, 78.0),
('student002', 'Jane Smith', CURRENT_DATE - INTERVAL '1 day', 'math', 'Geometry Basics', '92%', 52, 1.8, 92.0),
('student002', 'Jane Smith', CURRENT_DATE - INTERVAL '2 days', 'science', 'Chemistry Basics', '88%', 41, 2.1, 88.0),
('student003', 'Bob Johnson', CURRENT_DATE - INTERVAL '1 day', 'math', 'Advanced Algebra', '75%', 35, 4.1, 75.0)
ON CONFLICT DO NOTHING;

-- Create view for student analytics summary
CREATE OR REPLACE VIEW student_summary AS
SELECT 
    sa.student_id,
    sa.student_name,
    COUNT(*) as total_sessions,
    SUM(sa.time_spent_minutes) as total_study_time,
    AVG(sa.time_spent_minutes) as avg_session_time,
    AVG(sa.marks_achieved_percent) as avg_marks,
    AVG(sa.distraction_score) as avg_distraction,
    MIN(sa.log_date) as first_activity,
    MAX(sa.log_date) as last_activity,
    COUNT(DISTINCT sa.log_date) as active_days
FROM student_activity sa
GROUP BY sa.student_id, sa.student_name;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

COMMIT;
