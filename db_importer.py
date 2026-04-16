import sqlite3
import os
import re
import json
from datetime import datetime

DB_PATH = "students_analysis.db"
SQL_DIR = r"C:\internship\student_behavior_analysis\db_resources\Dump20260412\Dump20260412"

def parse_time(time_str):
    if not time_str or not isinstance(time_str, str): return None
    try:
        clean = time_str.replace(" ", "").lower().strip()
        return datetime.strptime(clean, "%I:%M%p")
    except: return None

def calculate_duration(s, e):
    t1, t2 = parse_time(s), parse_time(e)
    if t1 and t2:
        diff = (t2 - t1).total_seconds()
        d = int((diff + 86400 if diff < 0 else diff) / 60)
        return d
    return 0

def normalize_session(conn, student_id, raw_json):
    if not raw_json: return
    try:
        data = json.loads(raw_json)
        if not isinstance(data, list): data = [data]
    except: return
    cursor = conn.cursor()
    for day_entry in data:
        log_date = day_entry.get('dat', 'Unknown')
        for cat in ['sci', 'soc', 'smt', 'gam', 'pq', 'hm', 'm']:
            if cat in day_entry and isinstance(day_entry[cat], dict):
                obj = day_entry[cat]
                sess = obj.get('sessions', [])
                if not sess and obj.get('st') and obj.get('et'): sess = [obj]
                for s in sess:
                    cursor.execute("""
                        INSERT INTO student_session_analytics 
                        (student_id, log_date, subject_category, lesson_name, quiz_score, time_spent_minutes)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (student_id, log_date, cat, s.get('ln', 'Unknown'), str(s.get('qm', '')), calculate_duration(s.get('st'), s.get('et'))))

def extract_records(content):
    # Find the big VALUES (...) string
    match = re.search(r"VALUES\s*(.*);", content, re.S | re.I)
    if not match: return []
    vals_text = match.group(1).strip()
    
    records = []
    current_rec = []
    in_quote = False
    in_rec = False
    escaped = False
    
    for i, char in enumerate(vals_text):
        if escaped:
            current_rec.append(char)
            escaped = False
            continue
        if char == "\\":
            escaped = True
            current_rec.append(char)
            continue
        if char == "'":
            in_quote = not in_quote
            current_rec.append(char)
            continue
        if char == "(" and not in_quote:
            in_rec = True
            current_rec = []
            continue
        if char == ")" and not in_quote:
            in_rec = False
            records.append("".join(current_rec))
            continue
        if in_rec:
            current_rec.append(char)
            
    return records

def parse_record_vals(rec_text):
    vals = []
    curr = []
    iq = False
    esc = False
    for i, char in enumerate(rec_text):
        if esc:
            curr.append(char)
            esc = False
            continue
        if char == "\\":
            esc = True
            curr.append(char)
            continue
        if char == "'":
            iq = not iq
            curr.append(char)
            continue
        if char == "," and not iq:
            vals.append("".join(curr).strip())
            curr = []
        else:
            curr.append(char)
    vals.append("".join(curr).strip())
    
    cleaned = []
    for v in vals:
        if v.upper() == 'NULL': cleaned.append(None)
        elif v.startswith("'"): cleaned.append(v[1:-1].replace("''", "'").replace("\\'", "'").replace('\\"', '"').replace('\\\\', '\\'))
        else:
            try: cleaned.append(int(v))
            except: cleaned.append(v)
    return cleaned

def run_import():
    if os.path.exists(DB_PATH): os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE student_session_analytics (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, log_date TEXT, subject_category TEXT, lesson_name TEXT, quiz_score TEXT, time_spent_minutes INTEGER)")
    cursor.execute("CREATE TABLE rubix_students_data (id INTEGER PRIMARY KEY, student_id INTEGER, parent_id INTEGER, lesson_mode_data TEXT, general_mode_data TEXT, created_at TEXT, updated_at TEXT)")
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, name TEXT, role TEXT, class TEXT, school TEXT, rewards_points INTEGER)")

    files = sorted([f for f in os.listdir(SQL_DIR) if f.endswith('.sql')])
    for filename in files:
        print(f"Processing {filename}...")
        path = os.path.join(SQL_DIR, filename)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            recs = extract_records(content)
            
            if "students_data" in filename:
                for r in recs:
                    v = parse_record_vals(r)
                    if len(v) >= 7:
                        cursor.execute("INSERT OR IGNORE INTO rubix_students_data (id, student_id, parent_id, lesson_mode_data, general_mode_data, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)", v[:7])
                print(f"  Inserted {len(recs)} student logs.")
            elif "users.sql" in filename:
                for r in recs:
                    v = parse_record_vals(r)
                    if len(v) >= 18:
                        cursor.execute("INSERT OR IGNORE INTO users (id, username, name, role, class, school, rewards_points) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                       (v[0], v[1], v[3], v[6], v[8], v[9], v[17]))
            else:
                # Basic Generic Import
                table_name = filename.replace("rubix_", "").replace(".sql", "")
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (data TEXT)")
                for r in recs:
                    cursor.execute(f"INSERT INTO {table_name} (data) VALUES (?)", (r,))

    print("Running normalization...")
    cursor.execute("SELECT student_id, lesson_mode_data FROM rubix_students_data")
    count = 0
    for r in cursor.fetchall():
        normalize_session(conn, r[0], r[1])
    
    conn.commit()
    final_count = cursor.execute("SELECT count(*) FROM student_session_analytics").fetchone()[0]
    conn.close()
    print(f"Done! Created {final_count} normalized sessions.")

if __name__ == "__main__":
    run_import()
