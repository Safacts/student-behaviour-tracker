# Complete Ownership Guide - Student Behavior Analytics Microservice

## 🎯 **Quick Start - Run Your Service**

### **Start the Service**
```bash
cd C:\internship\student_behavior_analysis
python main.py
```

### **Stop the Service**
```bash
# Find the process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /f /pid <PID>

# Or kill all Python processes
taskkill /f /im python.exe
```

### **Access Your Service**
- **Main Dashboard**: http://localhost:8000/
- **API Testing**: http://localhost:8000/api/students
- **Agent Interface**: http://localhost:8000/agents
- **Documentation**: http://localhost:8000/docs

---

## 📚 **Understanding Your System Architecture**

### **Core Components**
1. **main.py** - Main FastAPI application (146 lines)
2. **analyzer.py** - Student behavior analysis logic
3. **llm_service.py** - AI-powered report generation
4. **behavior.db** - SQLite database with student data

### **API Endpoints**
- `GET /api/students` - List all students
- `GET /api/activity-logs` - Get all activity logs  
- `GET /api/report/{student_id}` - Generate student report
- `GET /api/agents` - List available AI agents

### **Database Schema**
```
student_activity table:
- id (primary key)
- student_id (student identifier)
- student_name (student name)
- date (activity date)
- time_spent_mins (study time in minutes)
- distraction_score (0-10 scale)
- marks_achieved_percent (0-100 percentage)
```

---

## 🔧 **Daily Operations**

### **Check Service Status**
```bash
# Check if service is running
netstat -ano | findstr :8000

# Test API endpoint
curl http://localhost:8000/api/students
```

### **View Logs**
```bash
# Main application logs
type logs\main_20260421.log

# API request logs
type logs\api_20260421.log
```

### **Restart Service**
```bash
# Kill existing process
taskkill /f /im python.exe

# Start fresh
python main.py
```

---

## 🚀 **Making Changes to Your Code**

### **Modify API Endpoints**
**File**: `main.py`

**Example**: Add new endpoint
```python
@app.get("/api/custom")
def custom_endpoint():
    """Your custom endpoint"""
    return {"message": "Hello World"}
```

**Steps**:
1. Edit `main.py`
2. Save the file
3. Restart the service
4. Test the new endpoint

### **Modify Analysis Logic**
**File**: `analyzer.py`

**Key Function**: `analyze_student(student_id)`

**Steps**:
1. Edit the analysis logic
2. Restart the service
3. Test with `/api/report/{student_id}`

### **Modify AI Recommendations**
**File**: `llm_service.py`

**Key Functions**: 
- `generate_parent_report()` - AI-powered
- `generate_fallback_report()` - Rule-based

**Steps**:
1. Edit the recommendation logic
2. Restart the service
3. Test with `/api/report/{student_id}`

---

## 🗄️ **Database Management**

### **View Database Contents**
```bash
# Using Python
python -c "import sqlite3; conn = sqlite3.connect('behavior.db'); cursor = conn.cursor(); cursor.execute('SELECT * FROM student_activity'); print(cursor.fetchall())"
```

### **Add Student Data**
```python
import sqlite3

conn = sqlite3.connect('behavior.db')
cursor = conn.cursor()
cursor.execute("""
    INSERT INTO student_activity (student_id, student_name, date, time_spent_mins, distraction_score, marks_achieved_percent)
    VALUES ('S004', 'Diana', '2026-04-21', 120, 3.5, 85.0)
""")
conn.commit()
conn.close()
```

### **Backup Database**
```bash
copy behavior.db behavior_backup.db
```

---

## 🐳 **Production Deployment**

### **Docker Deployment**
```bash
# Build Docker image
docker build -t student-behavior-analytics .

# Run container
docker run -p 8000:8000 -v ./behavior.db:/app/behavior.db student-behavior-analytics
```

### **Docker Compose Deployment**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### **Environment Configuration**
**File**: `.env.production`

**Key Variables**:
```
OPENAI_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///behavior.db
LOG_LEVEL=INFO
RATE_LIMIT_MAX_REQUESTS=100
```

---

## 📊 **Monitoring and Maintenance**

### **Health Checks**
```bash
# Basic health check
curl http://localhost:8000/

# Test core endpoints
curl http://localhost:8000/api/students
curl http://localhost:8000/api/report/S001
```

### **Performance Monitoring**
- Check response times in logs
- Monitor database size
- Track API request patterns
- Review error logs regularly

### **Log Analysis**
```bash
# Count API requests
type logs\api_20260421.log | findstr /C:"API Request" | find /c /v ""

# Find errors
type logs\main_20260421.log | findstr /C:"ERROR"
```

---

## 🛠️ **Troubleshooting**

### **Service Won't Start**
**Problem**: Port already in use
```bash
# Check what's using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /f /pid <PID>
```

**Problem**: Import errors
```bash
# Check if dependencies are installed
pip install -r requirements.txt
```

### **API Returns Errors**
**Problem**: Database locked
```bash
# Close all connections and restart
taskkill /f /im python.exe
python main.py
```

**Problem**: Student not found
- Check student ID format (e.g., "S001")
- Verify student exists in database

### **AI Recommendations Not Working**
**Problem**: OpenAI API key missing
- Set `OPENAI_API_KEY` in environment
- Falls back to rule-based recommendations if missing

---

## 🎓 **Advanced Features**

### **Production-Grade Components** (Available as Standalone Modules)

All production-grade features are implemented as standalone modules in the repository. You can integrate them as needed:

#### **1. Structured Logging** (`logger.py`)
```python
from logger import main_logger, api_logger

# Usage
main_logger.info("System started")
api_logger.api_request(method="GET", endpoint="/api/students", status_code=200)
```

#### **2. Rate Limiting** (`rate_limiter.py`)
```python
from rate_limiter import rate_limiter

# Usage
is_allowed, info = rate_limiter.is_allowed(client_ip)
if not is_allowed:
    return {"error": "Rate limit exceeded"}
```

#### **3. Caching** (`cache.py`)
```python
from cache import cache

# Usage
cache.set("key", "value", ttl=60)
value = cache.get("key")
```

#### **4. Authentication** (`auth.py`)
```python
from auth import auth

# Usage
api_key = auth.generate_api_key("user_id")
result = auth.validate_api_key(api_key)
```

#### **5. Data Validation** (`validators.py`)
```python
from validators import moderate_validator

# Usage
is_valid, errors = moderate_validator.validate_student_id("S001")
```

#### **6. Health Monitoring** (`health_monitor.py`)
```python
from health_monitor import health_monitor

# Usage
metrics = health_monitor.get_system_metrics()
health = health_monitor.check_database_integrity()
```

---

## 📈 **Extending Functionality**

### **Add New Analysis Features**
1. Create new function in `analyzer.py`
2. Update `main.py` to expose as API endpoint
3. Test with new endpoint

### **Add New AI Features**
1. Modify `llm_service.py` for new AI capabilities
2. Add new prompts and response handling
3. Test with student data

### **Add Database Tables**
```python
import sqlite3

conn = sqlite3.connect('behavior.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS new_table (
        id INTEGER PRIMARY KEY,
        field1 TEXT,
        field2 INTEGER
    )
""")
conn.commit()
conn.close()
```

---

## 🔐 **Security Best Practices**

### **API Key Management**
- Never commit API keys to git
- Use environment variables
- Rotate keys regularly
- Use different keys for dev/prod

### **Database Security**
- Regular backups
- Access control
- Input validation
- SQL injection prevention

### **Network Security**
- Use HTTPS in production
- Implement rate limiting
- Validate input data
- Use CORS properly

---

## 📝 **Git Operations**

### **Check Status**
```bash
git status
```

### **Commit Changes**
```bash
git add .
git commit -m "Your commit message"
git push
```

### **View History**
```bash
git log --oneline
```

### **Rollback Changes**
```bash
git checkout -- filename
```

---

## 🎯 **Daily Checklist**

- [ ] Check service is running
- [ ] Review error logs
- [ ] Monitor API performance
- [ ] Backup database
- [ ] Test key endpoints
- [ ] Review system resources

---

## 📞 **Support and Resources**

### **Key Files Reference**
- `main.py` - Main application
- `analyzer.py` - Analysis logic
- `llm_service.py` - AI recommendations
- `PROJECT_KNOWLEDGE.md` - Complete system documentation
- `INTEGRATION_GUIDE.md` - Integration instructions

### **Quick Commands**
```bash
# Start service
python main.py

# Stop service
taskkill /f /im python.exe

# Test API
curl http://localhost:8000/api/students

# Check logs
type logs\main_20260421.log

# Git status
git status
```

---

## 🚀 **Next Steps for Full Production**

To make this truly production-ready, consider:

1. **Database Migration**: Move from SQLite to PostgreSQL
2. **Caching Layer**: Implement Redis for distributed caching
3. **Load Balancing**: Use Nginx for production traffic
4. **Monitoring**: Set up Prometheus/Grafana
5. **CI/CD Pipeline**: Implement automated testing and deployment
6. **Security**: Add JWT authentication, HTTPS, rate limiting
7. **Scalability**: Horizontal scaling with Kubernetes
8. **Backup Strategy**: Automated database backups
9. **Alerting**: Set up monitoring alerts
10. **Documentation**: API documentation with Swagger

---

## 🎓 **Learning Resources**

### **FastAPI**
- Official docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

### **SQLite**
- Python docs: https://docs.python.org/3/library/sqlite3.html
- SQL tutorial: https://www.w3schools.com/sql/

### **OpenAI API**
- Documentation: https://platform.openai.com/docs
- Quickstart: https://platform.openai.com/docs/quickstart

### **Docker**
- Get started: https://docs.docker.com/get-started/
- Compose: https://docs.docker.com/compose/

---

## 🏆 **Success Metrics**

Your system is working successfully when:
- ✅ Service starts without errors
- ✅ All API endpoints return correct data
- ✅ AI recommendations are generated
- ✅ Database operations work smoothly
- ✅ Logs are being written
- ✅ System responds within acceptable time limits
- ✅ No error messages in logs
- ✅ Git repository is clean and up to date

---

**You now have complete ownership of this Student Behavior Analytics Microservice!**
