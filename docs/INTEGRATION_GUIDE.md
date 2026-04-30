# Student Behavior Analytics - Step-by-Step Integration Guide

## 🎯 Overview
This guide shows you how to integrate the Student Behavior Analytics microservice into your existing project using the agentic AI framework.

## 🌐 Available Pages
- **Dashboard**: http://localhost:8000/ (Original basic functionality)
- **Testing**: http://localhost:8000/dashboard (Visual testing interface)
- **Agents**: http://localhost:8000/agents (Agentic AI interface)
- **Monitor**: http://localhost:8000/monitor (System troubleshooting)
- **Integration**: http://localhost:8000/docs (Complete API documentation)

---

## 🚀 Step 1: Quick Start (5 Minutes)

### 1.1 Test the Service
```bash
# Check if service is running
curl http://localhost:8000/api/students
```

**Expected Response:**
```json
[{"id": "S001", "name": "Alex"}, {"id": "S002", "name": "Bella"}, {"id": "S003", "name": "Charlie"}]
```

### 1.2 Verify Agent Capabilities
```bash
# Test all agents
curl http://localhost:8000/api/agents
```

**Expected Response:**
```json
{
  "agents": [
    {
      "name": "Behavior Analysis Agent",
      "endpoint": "/api/agents/behavior/{student_id}",
      "capabilities": ["Behavior pattern analysis", "Risk factor identification"]
    },
    {
      "name": "Learning Path Agent", 
      "endpoint": "/api/agents/learning-path/{student_id}",
      "capabilities": ["Learning path creation", "Milestone generation"]
    },
    {
      "name": "Intervention Agent",
      "endpoint": "/api/agents/intervention/{student_id}", 
      "capabilities": ["Intervention strategies", "Urgency assessment"]
    }
  ]
}
```

---

## 🔧 Step 2: Choose Your Integration Approach

### Option A: Simple API Integration (Recommended)
**Best for:** Quick integration, existing frontend, minimal changes

### Option B: Full Agent Integration
**Best for:** New projects, maximum AI capabilities, comprehensive analysis

### Option C: Hybrid Approach
**Best for:** Gradual migration, testing capabilities

---

## 📋 Option A: Simple API Integration

### 2.1 Basic Student Data
```javascript
// Add to your existing JavaScript
class StudentAnalytics {
    constructor() {
        this.baseURL = 'http://localhost:8000';
    }
    
    async getStudents() {
        const response = await fetch(`${this.baseURL}/api/students`);
        return await response.json();
    }
    
    async getStudentReport(studentId) {
        const response = await fetch(`${this.baseURL}/api/report/${studentId}`);
        return await response.json();
    }
}

// Usage
const analytics = new StudentAnalytics();
const students = await analytics.getStudents();
console.log('Students:', students);
```

### 2.2 Python Integration
```python
# Add to your existing Python project
import requests

class StudentAnalyticsAPI:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
    
    def get_students(self):
        response = requests.get(f'{self.base_url}/api/students')
        return response.json()
    
    def get_student_report(self, student_id):
        response = requests.get(f'{self.base_url}/api/report/{student_id}')
        return response.json()

# Usage
analytics = StudentAnalyticsAPI()
students = analytics.get_students()
print(f"Students: {students}")
```

### 2.3 React Integration
```jsx
// Add to your React component
import React, { useState, useEffect } from 'react';

function StudentDashboard() {
    const [students, setStudents] = useState([]);
    
    useEffect(() => {
        fetch('http://localhost:8000/api/students')
            .then(res => res.json())
            .then(setStudents);
    }, []);

    return (
        <div>
            <h2>Students</h2>
            {students.map(student => (
                <div key={student.id}>
                    {student.name} ({student.id})
                </div>
            ))}
        </div>
    );
}
```

---

## 🤖 Option B: Full Agent Integration

### 3.1 Behavior Analysis Agent
**Purpose:** Identify at-risk students and behavioral patterns

```javascript
// Advanced behavior analysis
async function getBehaviorAnalysis(studentId) {
    const response = await fetch(`http://localhost:8000/api/agents/behavior/${studentId}`);
    const data = await response.json();
    
    console.log('Risk Factors:', data.risk_factors);
    console.log('Confidence Score:', data.confidence_score);
    console.log('Recommendations:', data.recommendations);
    
    // Use in your application
    if (data.confidence_score > 0.8) {
        showHighRiskAlert(data);
    }
    
    return data;
}
```

### 3.2 Learning Path Agent
**Purpose:** Create personalized educational roadmaps

```javascript
// Learning path integration
async function getLearningPath(studentId) {
    const response = await fetch(`http://localhost:8000/api/agents/learning-path/${studentId}`);
    const data = await response.json();
    
    console.log('Learning Level:', data.learning_level);
    console.log('Milestones:', data.milestones);
    console.log('Duration:', data.estimated_duration);
    
    // Display learning path in your UI
    displayLearningPath(data);
    
    return data;
}

function displayLearningPath(pathData) {
    const pathContainer = document.getElementById('learning-path');
    pathContainer.innerHTML = `
        <h3>Learning Path: ${pathData.learning_level}</h3>
        <h4>Estimated Duration: ${pathData.estimated_duration}</h4>
        <ul>
            ${pathData.milestones.map(milestone => `<li>${milestone}</li>`).join('')}
        </ul>
    `;
}
```

### 3.3 Intervention Agent
**Purpose:** Proactive student support strategies

```javascript
// Intervention planning
async function getInterventionPlan(studentId) {
    const response = await fetch(`http://localhost:8000/api/agents/intervention/${studentId}`);
    const data = await response.json();
    
    console.log('Urgency Level:', data.urgency_level);
    console.log('Strategies:', data.intervention_strategies);
    console.log('Timeline:', data.timeline);
    
    // Handle urgent interventions
    if (data.urgency_level === 'Critical') {
        triggerImmediateAlert(data);
    }
    
    return data;
}

function triggerImmediateAlert(interventionData) {
    // Send notification, email, or alert
    alert(`CRITICAL: Immediate intervention required for student!`);
    
    // Log intervention for tracking
    logIntervention(interventionData);
}
```

---

## 🎯 Option C: Comprehensive Analysis

### 4.1 All Agents Combined
**Purpose:** Complete student analysis with all AI insights

```javascript
// Comprehensive analysis using all agents
async function getComprehensiveAnalysis(studentId) {
    const response = await fetch(`http://localhost:8000/api/agents/comprehensive/${studentId}`);
    const data = await response.json();
    
    console.log('Overall Risk Level:', data.summary.overall_risk_level);
    console.log('Success Probability:', data.summary.success_probability);
    console.log('Recommended Actions:', data.summary.recommended_actions);
    
    // Use comprehensive data
    displayComprehensiveResults(data);
    
    return data;
}

function displayComprehensiveResults(analysisData) {
    const resultsContainer = document.getElementById('analysis-results');
    
    resultsContainer.innerHTML = `
        <div class="risk-assessment">
            <h3>Risk Level: ${analysisData.summary.overall_risk_level}</h3>
            <div class="success-probability">
                Success Probability: ${(analysisData.summary.success_probability * 100).toFixed(1)}%
            </div>
        </div>
        
        <div class="recommendations">
            <h4>Recommended Actions:</h4>
            <ul>
                ${analysisData.summary.recommended_actions.map(action => `<li>${action}</li>`).join('')}
            </ul>
        </div>
    `;
}
```

---

## 🛠️ Step 3: Implementation Examples

### 5.1 Dashboard Integration
**Add to existing dashboard:**

```html
<!-- Add to your existing dashboard -->
<div class="student-analytics-widget">
    <h3>Student Behavior Analysis</h3>
    <div id="analytics-content">
        Loading...
    </div>
</div>

<script>
// Load student analytics
async function loadStudentAnalytics() {
    try {
        const students = await fetch('http://localhost:8000/api/students').then(r => r.json());
        const studentSelect = document.getElementById('student-select');
        
        // Populate student dropdown
        students.forEach(student => {
            const option = document.createElement('option');
            option.value = student.id;
            option.textContent = student.name;
            studentSelect.appendChild(option);
        });
        
        // Load analysis on selection
        studentSelect.addEventListener('change', async (e) => {
            const studentId = e.target.value;
            const analysis = await fetch(`http://localhost:8000/api/agents/comprehensive/${studentId}`).then(r => r.json());
            
            // Display results in your dashboard
            updateDashboardWidget(analysis);
        });
        
    } catch (error) {
        console.error('Failed to load analytics:', error);
        document.getElementById('analytics-content').innerHTML = 
            '<p class="error">Failed to load student analytics</p>';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', loadStudentAnalytics);
</script>
```

### 5.2 Alert System Integration
**Real-time notifications for at-risk students:**

```javascript
// Alert system for critical interventions
class InterventionAlertSystem {
    constructor() {
        this.baseURL = 'http://localhost:8000';
        this.checkInterval = 60000; // Check every minute
        this.alertThresholds = {
            critical: 0.9,
            high: 0.7
        };
    }
    
    startMonitoring() {
        setInterval(() => {
            this.checkAllStudents();
        }, this.checkInterval);
    }
    
    async checkAllStudents() {
        try {
            const students = await fetch(`${this.baseURL}/api/students`).then(r => r.json());
            
            for (const student of students) {
                const analysis = await fetch(`${this.baseURL}/api/agents/comprehensive/${student.id}`).then(r => r.json());
                
                if (analysis.summary.success_probability < this.alertThresholds.critical) {
                    this.triggerCriticalAlert(student, analysis);
                } else if (analysis.summary.success_probability < this.alertThresholds.high) {
                    this.triggerHighRiskAlert(student, analysis);
                }
            }
        } catch (error) {
            console.error('Monitoring error:', error);
        }
    }
    
    triggerCriticalAlert(student, analysis) {
        // Send email, SMS, or push notification
        this.sendNotification({
            type: 'CRITICAL',
            student: student.name,
            message: 'Immediate intervention required',
            actions: analysis.summary.recommended_actions
        });
    }
    
    sendNotification(alertData) {
        // Integrate with your existing notification system
        console.log('ALERT:', alertData);
        
        // Example: Send to your notification service
        // yourNotificationService.send(alertData);
        
        // Example: Display in UI
        this.displayAlert(alertData);
    }
    
    displayAlert(alertData) {
        const alertContainer = document.getElementById('alert-container');
        const alertElement = document.createElement('div');
        alertElement.className = `alert alert-${alertData.type.toLowerCase()}`;
        alertElement.innerHTML = `
            <h4>${alertData.type}: ${alertData.student}</h4>
            <p>${alertData.message}</p>
            <ul>
                ${alertData.actions.map(action => `<li>${action}</li>`).join('')}
            </ul>
        `;
        AlertContainer.appendChild(alertElement);
    }
}

// Start monitoring
const alertSystem = new InterventionAlertSystem();
alertSystem.startMonitoring();
```

---

## 📊 Step 4: Data Visualization

### 6.1 Risk Level Visualization
```javascript
// Visualize risk levels across all students
async function visualizeRiskLevels() {
    const response = await fetch('http://localhost:8000/api/students').then(r => r.json());
    
    // Get comprehensive analysis for all students
    const analyses = await Promise.all(
        response.data.map(student => 
            fetch(`http://localhost:8000/api/agents/comprehensive/${student.id}`).then(r => r.json())
        )
    );
    
    // Create risk visualization
    const riskData = analyses.map(analysis => ({
        student: analysis.student_id,
        riskLevel: analysis.summary.overall_risk_level,
        probability: analysis.summary.success_probability
    }));
    
    // Display in your charting library
    displayRiskChart(riskData);
}

function displayRiskChart(data) {
    const ctx = document.getElementById('risk-chart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.student),
            datasets: [{
                label: 'Risk Level',
                data: data.map(d => d.riskLevel === 'Critical' ? 3 : d.riskLevel === 'High' ? 2 : d.riskLevel === 'Medium' ? 1 : 0),
                backgroundColor: 'rgba(255, 99, 132, 0.2)'
            }]
        }
    });
}
```

---

## 🔒 Step 5: Production Deployment

### 7.1 Environment Configuration
**Production settings:**

```bash
# Set environment variables
export ANALYTICS_API_URL="https://your-domain.com/api"
export OPENAI_API_KEY="your-production-api-key"
export NODE_ENV="production"

# Run with production configuration
python main.py
```

### 7.2 Docker Deployment
**Containerize the integration:**

```dockerfile
# Dockerfile for your integrated application
FROM node:18-alpine

WORKDIR /app

# Copy your application
COPY your-frontend/ .
COPY package*.json ./

# Install dependencies
RUN npm install

# Expose port
EXPOSE 3000

# Start your application
CMD ["npm", "start"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  your-frontend:
    build: .
    ports:
      - "3000:3000"
    environment:
      - ANALYTICS_API_URL=http://analytics:8000
    depends_on:
      - analytics
  
  analytics:
    build: ./analytics
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

---

## 🎯 Quick Reference

### API Endpoints Summary
| Endpoint | Purpose | Example |
|----------|---------|---------|
| `/api/students` | Get all students | `curl http://localhost:8000/api/students` |
| `/api/report/{id}` | Basic student report | `curl http://localhost:8000/api/report/S001` |
| `/api/agents/behavior/{id}` | Behavior analysis | `curl http://localhost:8000/api/agents/behavior/S001` |
| `/api/agents/learning-path/{id}` | Learning path | `curl http://localhost:8000/api/agents/learning-path/S001` |
| `/api/agents/intervention/{id}` | Interventions | `curl http://localhost:8000/api/agents/intervention/S001` |
| `/api/agents/comprehensive/{id}` | All agents | `curl http://localhost:8000/api/agents/comprehensive/S001` |

### Response Formats
**Basic Student Report:**
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
  "ai_recommendation": "Detailed recommendation text..."
}
```

**Comprehensive Analysis:**
```json
{
  "student_id": "S001",
  "comprehensive_analysis": {
    "behavior_analysis": { /* behavior agent data */ },
    "learning_path": { /* learning agent data */ },
    "intervention_plan": { /* intervention agent data */ }
  },
  "summary": {
    "overall_risk_level": "High",
    "recommended_actions": ["Action 1", "Action 2", "Action 3"],
    "success_probability": 0.8
  }
}
```

---

## ✅ Integration Checklist

### Pre-Integration
- [ ] Service is running at http://localhost:8000
- [ ] All endpoints tested and working
- [ ] Environment variables configured
- [ ] Network access verified

### Post-Integration
- [ ] Student data loading correctly
- [ ] Agent analyses displaying properly
- [ ] Error handling implemented
- [ ] Performance testing completed
- [ ] User acceptance testing done

---

## 🆘 Support

### Troubleshooting
1. **Service not responding**: Check if Python service is running
2. **API errors**: Verify endpoint URLs and parameters
3. **Missing data**: Ensure student database exists
4. **Performance issues**: Check network latency and response times

### Contact
- **Documentation**: http://localhost:8000/docs
- **Monitoring**: http://localhost:8000/monitor
- **Testing**: http://localhost:8000/agents

---

## 🎉 Success Metrics

Your integration is successful when:
- ✅ Students load and display correctly
- ✅ Agent analyses provide actionable insights
- ✅ Risk assessments trigger appropriate alerts
- ✅ Learning paths guide student development
- ✅ Interventions support at-risk students
- ✅ System monitors health and performance

**You now have a complete agentic AI system for student behavior analytics!**
