import sqlite3

conn = sqlite3.connect('behavior.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", tables)

# Check student_activity table structure
if ('student_activity',) in tables:
    cursor.execute("PRAGMA table_info(student_activity)")
    columns = cursor.fetchall()
    print("student_activity columns:", columns)

# Check if there's data
cursor.execute("SELECT COUNT(*) FROM student_activity")
count = cursor.fetchone()[0]
print("student_activity row count:", count)

conn.close()
