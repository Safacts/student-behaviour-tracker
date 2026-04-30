# Complete User Guide - Student Behavior Analytics

## 🎯 **Current System Status**

### **What's Working Now:**
- ✅ **Student Data Management** - View and manage student information
- ✅ **Activity Tracking** - Monitor student study patterns and behavior
- ✅ **AI-Powered Reports** - Generate empathetic recommendations using FREE AI
- ✅ **Web Dashboard** - Visual interface for monitoring students
- ✅ **Real-time Analysis** - Behavioral pattern identification
- ✅ **Database Storage** - SQLite database with student activity data

### **What's Currently Disabled:**
- ❌ **Agentic AI Endpoints** - Agent-specific endpoints temporarily removed
- ❌ **Production-Grade Features** - Advanced monitoring, rate limiting, caching (standalone modules available)
- ❌ **WebSocket Updates** - Real-time notifications (standalone module available)
- ❌ **Advanced Authentication** - API key authentication (standalone module available)

---

## 🚀 **Quick Start Guide**

### **1. Start the Service**
```bash
cd C:\internship\student_behavior_analysis
python main.py
```
Service will run on: http://localhost:8000

### **2. Access the Dashboard**
Open your browser: http://localhost:8000/dashboard

### **3. Test the API**
```bash
# Get all students
curl http://localhost:8000/api/students

# Get activity logs
curl http://localhost:8000/api/activity-logs

# Generate student report
curl http://localhost:8000/api/report/S001
```

---

## 📊 **Core Features & Usage**

### **1. Student Management**

#### **View All Students**
**Endpoint:** `GET /api/students`

**Response:**
```json
[
  {"id": "S001", "name": "Alex"},
  {"id": "S002", "name": "Bella"},
  {"id": "S003", "name": "Charlie"}
]
```

**Usage:**
- Navigate to the dashboard
- View student list in the sidebar
- Click on any student to see details

#### **Student Data in Database**
Your database contains:
- **Student ID**: Unique identifier (e.g., S001, S002)
- **Student Name**: Full name
- **Activity Logs**: Daily study sessions with time spent, distraction scores, marks
- **Behavioral Tags**: Auto-generated analysis (High Flight Risk, On Track, etc.)

---

### **2. Activity Monitoring**

#### **View All Activity Logs**
**Endpoint:** `GET /api/activity-logs`

**Response:**
```json
[
  {
    "id": 1,
    "student_id": "S001",
    "student_name": "Alex",
    "date": "2026-04-21",
    "time_spent_mins": 120,
    "distraction_score": 6.5,
    "marks_achieved_percent": 35.0
  }
]
```

**Metrics Explained:**
- **Time Spent**: Minutes spent studying
- **Distraction Score**: 0-10 scale (higher = more distracted)
- **Marks Achieved**: Percentage score (0-100)

---

### **3. AI-Powered Reports**

#### **Generate Student Report**
**Endpoint:** `GET /api/report/{student_id}`

**Response:**
```json
{
  "student_id": "S001",
  "student_name": "Alex",
  "stats": {
    "total_time": 1718,
    "avg_distraction": 6.93,
    "avg_marks": 35.73
  },
  "analysis": {
    "tag": "High Flight Risk"
  },
  "ai_recommendation": "Based on Alex's recent activity report, I would recommend that you and Alex work together to identify and minimize distractions..."
}
```

**How It Works:**
1. **Data Analysis**: System analyzes student's activity patterns
2. **Behavioral Tagging**: Assigns risk level (High Flight Risk, On Track, etc.)
3. **AI Generation**: Uses Groq FREE AI to generate empathetic recommendations
4. **Personalization**: Recommendations are tailored to each student's specific data

**Behavioral Tags:**
- **High Flight Risk**: Low marks (<50%) and/or high distraction (>6)
- **Concept Comprehension Issue**: Low marks (<70%) but low distraction (<3)
- **On Track**: Good marks (>70%) and reasonable distraction

---

### **4. Web Interfaces**

#### **Main Dashboard** (http://localhost:8000/dashboard)
- View all students at a glance
- See behavioral tags and risk levels
- Access detailed reports
- Monitor activity patterns

#### **System Monitor** (http://localhost:8000/monitor)
- System health status
- API response times
- Database information
- Service uptime

#### **Agents Interface** (http://localhost:8000/agents)
- View available AI agents (currently informational only)
- Agent capabilities overview
- Future agentic AI features

#### **Documentation** (http://localhost:8000/docs)
- API documentation
- Feature explanations
- Usage guides

---

## 🤖 **AI System Details**

### **Current AI Implementation**
Your system uses a **Hybrid AI System** that tries multiple AI services:

**Priority Order:**
1. **OpenAI GPT-3.5** - If you have API quota
2. **Google Gemini** - If you have API access
3. **Groq FREE** ✅ - Currently active (completely free)
4. **Hardcoded Fallback** - Rule-based if all AI fails

### **Groq FREE AI (Currently Active)**
- **Model**: Llama 3.1 8B Instant
- **Cost**: Completely free
- **Speed**: Very fast inference
- **Quality**: High-quality empathetic responses
- **Status**: ✅ Working and generating real AI recommendations

### **AI Recommendation Examples**

**For High Flight Risk Student:**
"Based on Alex's recent activity report, I would recommend that you and Alex work together to identify and minimize distractions, setting aside dedicated blocks of time for focused learning. With a current average distraction score of 6.93/10 and a high flight risk status, it's essential to establish a consistent routine and reward system to help Alex stay on track."

**For On Track Student:**
"Test is making good progress with 75.0% average marks. I recommend setting specific academic goals for the next term and exploring subjects of interest to deepen engagement and maintain the positive momentum."

---

## 🎓 **Practical Usage Scenarios**

### **Scenario 1: Monitor At-Risk Students**
1. Go to http://localhost:8000/dashboard
2. Look for students with "High Flight Risk" tag
3. Click on student to view detailed report
4. Read AI-powered recommendations
5. Take action based on suggestions

### **Scenario 2: Track Student Progress**
1. Access activity logs: http://localhost:8000/api/activity-logs
2. Filter by specific student ID
3. Analyze trends in study time and marks
4. Generate weekly reports
5. Compare progress over time

### **Scenario 3: Generate Parent Reports**
1. Select student from dashboard
2. Click "Generate Report"
3. Review AI recommendations
4. Share report with parents
5. Discuss action plan

### **Scenario 4: Identify Intervention Needs**
1. Review all student reports
2. Identify students with concerning patterns
3. Use AI recommendations to plan interventions
4. Monitor intervention effectiveness
5. Adjust strategies as needed

---

## 🔧 **Advanced Usage**

### **Adding New Student Data**
You can add student activity data to the database:

```python
import sqlite3

conn = sqlite3.connect('behavior.db')
cursor = conn.cursor()

# Add new activity record
cursor.execute("""
    INSERT INTO student_activity 
    (student_id, student_name, date, time_spent_mins, distraction_score, marks_achieved_percent)
    VALUES (?, ?, ?, ?, ?, ?)
""", ('S004', 'Diana', '2026-04-21', 150, 4.5, 85.0))

conn.commit()
conn.close()
```

### **Custom Analysis**
Use the analyzer module for custom analysis:

```python
from analyzer import analyze_student

# Analyze a student
analysis = analyze_student('S001')
print(f"Behavioral Tag: {analysis['behavioral_tag']}")
print(f"Average Marks: {analysis['avg_marks']}")
print(f"Average Distraction: {analysis['avg_distraction']}")
```

### **Direct AI Recommendations**
Generate AI recommendations directly:

```python
from llm_service import generate_parent_report

student_data = {
    'student_name': 'Alex',
    'total_study_time': 450,
    'avg_distraction': 6.5,
    'avg_marks': 45.0
}

recommendation = generate_parent_report(student_data, 'High Flight Risk')
print(recommendation)
```

---

## 📈 **Understanding Your Data**

### **Database Schema**
```sql
student_activity table:
- id (integer, primary key)
- student_id (text) - Student identifier
- student_name (text) - Student full name
- date (text) - Activity date
- time_spent_mins (integer) - Study time in minutes
- distraction_score (real) - Distraction level 0-10
- marks_achieved_percent (real) - Marks percentage 0-100
```

### **Analysis Logic**
The system calculates:
- **Total Study Time**: Sum of all study sessions
- **Average Distraction**: Mean of all distraction scores
- **Average Marks**: Mean of all marks achieved
- **Behavioral Tag**: Based on thresholds:
  - High Flight Risk: marks < 50% OR distraction > 6
  - Concept Comprehension Issue: marks < 70% AND distraction < 3
  - On Track: marks > 70%

---

## 🚨 **About Agentic AI**

### **Current Status**
The **Agentic AI features are currently disabled** in the main application. The agent endpoints (`/api/agents/behavior/{student_id}`, `/api/agents/learning-path/{student_id}`, `/api/agents/intervention/{student_id}`) were temporarily removed to fix service startup issues.

### **What Was Planned**
- **Behavior Analysis Agent**: Deep pattern analysis and risk identification
- **Learning Path Agent**: Personalized learning path creation
- **Intervention Agent**: Targeted intervention recommendations

### **What You Have Now**
- **Basic Analysis**: Rule-based behavioral tagging
- **AI Recommendations**: Free AI-powered empathetic reports
- **Data Management**: Complete activity tracking and reporting

### **Future Agentic AI**
To enable agentic AI, the agent endpoints would need to be re-integrated into main.py. The standalone agent logic exists but is not currently connected to the API.

---

## 🎯 **Getting the Most Out of Your System**

### **Best Practices**
1. **Regular Updates**: Add student activity data regularly
2. **Monitor Trends**: Track changes in behavior patterns over time
3. **Act on Recommendations**: Implement AI suggestions
4. **Review Reports**: Check weekly for at-risk students
5. **Database Backups**: Regularly backup behavior.db

### **Daily Workflow**
1. Start the service: `python main.py`
2. Open dashboard: http://localhost:8000/dashboard
3. Review student status
4. Generate reports for at-risk students
5. Share recommendations with stakeholders

### **Weekly Workflow**
1. Analyze activity trends
2. Generate comprehensive reports
3. Review behavioral tag changes
4. Plan interventions for high-risk students
5. Update database with new activity data

---

## 🛠️ **Troubleshooting**

### **Service Won't Start**
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process using port 8000
taskkill /f /pid <PID>

# Restart the service
python main.py
```

### **AI Not Working**
- Check if Groq API key is configured in .env
- Verify internet connection
- Check API key is valid
- System will fall back to hardcoded recommendations if AI fails

### **Database Issues**
- Verify behavior.db exists in the project directory
- Check database permissions
- Backup database before modifications
- Use SQLite tools for direct database access

---

## 📚 **Additional Resources**

### **Key Files**
- **main.py**: Main FastAPI application
- **analyzer.py**: Student behavior analysis logic
- **llm_service.py**: AI recommendation generation (Groq FREE)
- **behavior.db**: SQLite database
- **dashboard.html**: Web dashboard interface
- **OWNERSHIP_GUIDE.md**: Complete system ownership documentation
- **PROJECT_KNOWLEDGE.md**: Technical documentation

### **API Documentation**
- Interactive API docs: http://localhost:8000/docs
- API endpoints: See "Core Features & Usage" section

### **Production-Grade Modules** (Available but not integrated)
- **logger.py**: Structured logging
- **health_monitor.py**: Health monitoring
- **rate_limiter.py**: API rate limiting
- **auth.py**: Authentication system
- **cache.py**: Caching system
- **websocket_manager.py**: Real-time updates
- **validators.py**: Data validation

---

## 🎓 **Summary**

**Your Student Behavior Analytics System currently provides:**
- ✅ Complete student data management
- ✅ Activity tracking and monitoring
- ✅ FREE AI-powered recommendations (Groq)
- ✅ Behavioral analysis and risk identification
- ✅ Web dashboard for easy access
- ✅ Comprehensive reporting system

**What's NOT currently active:**
- ❌ Agentic AI endpoints (temporarily disabled)
- ❌ Production-grade middleware (standalone modules available)
- ❌ Real-time WebSocket updates (standalone module available)

**You can use this system right now to:**
- Monitor student behavior patterns
- Identify at-risk students
- Generate AI-powered recommendations
- Track progress over time
- Make data-driven educational decisions

**The system is fully functional for student behavior analysis with FREE AI recommendations.**
