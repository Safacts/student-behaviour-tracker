# 🎓 **Parent Dashboard User Guide**

## **Overview**

The Student Behavior Analytics Parent Dashboard provides comprehensive insights into your child's academic performance, behavioral patterns, and IIT preparation progress. This guide explains how to use all available features and reports.

---

## **📊 Available Reports**

### **1. Daily Reports**
**Purpose**: Track daily study activities and performance

**How to Access**: 
- API Endpoint: `GET /api/communication/parent-email/{student_id}?email_type=report`
- Generates daily progress report via email

**What's Included**:
- Daily study time
- Marks achieved
- Distraction levels
- Behavioral insights
- Recommendations

**When to Use**:
- Check daily progress
- Monitor study habits
- Identify immediate concerns

---

### **2. Weekly Reports**
**Purpose**: Analyze weekly trends and patterns

**How to Access**:
- API Endpoint: `GET /api/communication/parent-email/{student_id}?email_type=report`
- Set to weekly data (last 7 days)

**What's Included**:
- Weekly average marks
- Study time trends
- Distraction patterns
- Behavioral tag changes
- Week-over-week comparison

**When to Use**:
- Review weekly progress
- Identify patterns
- Plan next week's focus

---

### **3. Exam Reports**
**Purpose**: Comprehensive formal documentation for assessments

**How to Access**:
- API Endpoint: `GET /api/documents/pdf-report/{student_id}`
- Generates structured PDF report content

**What's Included**:
- Executive summary
- Behavioral analysis
- Learning path
- Intervention plan (if needed)
- Performance metrics
- Recommendations

**When to Use**:
- Parent-teacher meetings
- Formal documentation
- Academic reviews
- Progress tracking

---

### **4. IIT Preparation Reports**
**Purpose**: Track IIT JEE preparation progress

**How to Access**:
- API Endpoint: `GET /api/iit-prep/report/{student_id}`

**What's Included**:
- **IIT Readiness Score**: Overall preparation level (0-100)
- **Prep Level**: 
  - Advanced (85%+) - Ready for JEE Advanced
  - Intermediate (70-84%) - On track for JEE Mains
  - Foundation (50-69%) - Need concept building
  - Beginner (<50%) - Start from basics
- **Subject Performance**:
  - Physics marks and analysis
  - Chemistry marks and analysis
  - Mathematics marks and analysis
- **Problem Solving Speed**: Fast/Moderate/Needs Improvement
- **Concept Mastery**:
  - Mechanics (Physics)
  - Organic Chemistry
  - Calculus (Math)
- **Time Management**:
  - Total study hours (90 days)
  - Recommended hours (450)
  - Status: On track/Needs improvement
- **Recommendations**: Subject-specific advice
- **Narrative Report**: AI-generated insights

**When to Use**:
- Track IIT preparation progress
- Identify weak subjects
- Plan study schedule
- Assess readiness for exams

---

## **🎯 How to Use the Dashboard**

### **Accessing Reports**

#### **Via API (for developers)**
```bash
# Get daily report
curl http://localhost:8000/api/communication/parent-email/S001?email_type=report

# Get IIT prep report
curl http://localhost:8000/api/iit-prep/report/S001

# Get PDF report
curl http://localhost:8000/api/documents/pdf-report/S001
```

#### **Via Frontend (for users)**
1. Open `agents.html` in browser
2. Enter student ID
3. Select report type
4. View results

---

### **Understanding the Metrics**

#### **Behavioral Tags**
- **High Flight Risk**: Critical - needs immediate intervention
- **Concept Comprehension Issue**: Needs concept review
- **Potential Risk**: Monitor closely
- **Good Standing**: On track

#### **Distraction Score**
- **0-3**: Excellent focus
- **4-6**: Moderate distractions
- **7-10**: High distractions (needs attention)

#### **Marks Achieved**
- **90-100%**: Excellent
- **75-89%**: Good
- **50-74%**: Average
- **Below 50%**: Needs improvement

#### **IIT Readiness Score**
- **85-100%**: Advanced level
- **70-84%**: Intermediate level
- **50-69%**: Foundation level
- **Below 50%**: Beginner level

---

## **📈 Report Types Explained**

### **Daily Report Example**
```
Daily Progress Report for Student (S001)
========================================
Date: 2026-04-22

Today's Performance:
- Study Time: 45 minutes
- Marks Achieved: 75%
- Distraction Level: 6/10

Behavioral Status: On Track

Recommendations:
- Continue current study pattern
- Maintain focus during study sessions
```

### **Weekly Report Example**
```
Weekly Progress Report for Student (S001)
========================================
Period: 2026-04-15 to 2026-04-22

Weekly Averages:
- Average Study Time: 50 minutes/day
- Average Marks: 72%
- Average Distraction: 5.5/10

Trends:
- Marks: +5% from last week
- Distraction: -0.5 from last week
- Study Time: +10 minutes from last week

Behavioral Status: Good Standing
```

### **IIT Prep Report Example**
```
IIT Preparation Report for Student (S001)
=========================================
Date: 2026-04-22

IIT Readiness Score: 36.55/100
Prep Level: Beginner - Start from basics

Subject Performance:
- Physics: 31.17%
- Chemistry: 40.63%
- Mathematics: 37.86%

Problem Solving Speed: Needs Improvement

Concept Mastery:
- Mechanics: Developing
- Organic Chemistry: Developing
- Calculus: Developing

Time Management:
- Total Study Hours (90 days): 28.6 hours
- Recommended Hours: 450 hours
- Status: Needs improvement

Recommendations:
- Focus on Physics fundamentals - start with Mechanics
- Practice JEE Physics problems daily
- Strengthen Chemistry concepts - Organic and Physical
- Solve previous year JEE Chemistry questions
- Master Calculus and Algebra basics
- Practice JEE Mathematics problem sets
- Reduce distractions during study - critical for IIT prep
- Increase study time - IIT requires 6-8 hours daily
```

---

## **🔧 Features Available**

### **Communication Tools**
- **Email Generation**: Automated parent emails
- **Staff Notifications**: Alert teachers about issues

### **Task Management**
- **Intervention Tasks**: Track intervention implementation
- **Monitoring Tasks**: Schedule regular check-ins
- **Task Status**: Update and track progress

### **Calendar Integration**
- **Meeting Scheduling**: Schedule parent-teacher meetings
- **Recurring Check-ins**: Set up regular monitoring

### **Data Quality**
- **Data Validation**: Ensure data accuracy
- **Data Cleaning**: Fix data issues

### **Advanced Analytics**
- **Performance Prediction**: Forecast future performance
- **Anomaly Detection**: Identify unusual patterns

---

## **📱 Dashboard Features (Coming Soon)**

The parent dashboard will include:
- **Real-time Progress Tracking**: Live updates on student performance
- **Visual Charts**: Performance trends and comparisons
- **Alert System**: Automatic notifications for concerns
- **Report Archive**: Historical report access
- **Comparison Tools**: Compare with class averages
- **Goal Setting**: Set and track academic goals
- **Study Planner**: Schedule study sessions
- **Progress Milestones**: Track achievement milestones

---

## **🎓 Understanding IIT Preparation**

### **What is IIT JEE?**
- Indian Institutes of Technology Joint Entrance Examination
- One of the most competitive exams in India
- Requires dedicated preparation (6-8 hours daily)
- Tests Physics, Chemistry, and Mathematics

### **IIT Preparation Levels**

#### **Beginner (Below 50%)**
- Focus on basic concepts
- Start from NCERT textbooks
- Build foundation in all three subjects
- Recommended study time: 4-6 hours daily

#### **Foundation (50-69%)**
- Strengthen concepts
- Practice basic problems
- Focus on weak areas
- Recommended study time: 6-8 hours daily

#### **Intermediate (70-84%)**
- Advanced problem solving
- Previous year papers
- Mock tests
- Recommended study time: 8-10 hours daily

#### **Advanced (85%+)**
- JEE Advanced preparation
- Complex problem solving
- All-India test series
- Recommended study time: 10+ hours daily

### **Subject-Wise Focus**

#### **Physics**
- Mechanics (Foundation)
- Electricity and Magnetism
- Optics
- Modern Physics

#### **Chemistry**
- Organic Chemistry
- Physical Chemistry
- Inorganic Chemistry

#### **Mathematics**
- Calculus
- Algebra
- Coordinate Geometry
- Trigonometry

---

## **📞 Support**

### **For Technical Issues**
- Contact: support@school.edu
- Response Time: 24-48 hours

### **For Academic Concerns**
- Contact: teacher@school.edu
- Response Time: During school hours

### **For IIT Prep Questions**
- Contact: iit-coordinator@school.edu
- Response Time: During school hours

---

## **🔒 Privacy & Security**

- All student data is encrypted
- Reports are accessible only to authorized parents
- No data is shared with third parties
- Compliance with data protection regulations

---

## **📚 Additional Resources**

### **Study Tips**
- Create a distraction-free study environment
- Follow a consistent study schedule
- Take regular breaks (Pomodoro technique)
- Practice previous year papers
- Focus on weak areas

### **IIT Prep Resources**
- NCERT Textbooks
- Previous Year JEE Papers
- Online Test Series
- Coaching Material
- Video Lectures

### **Parent Resources**
- How to support your child
- Understanding behavioral patterns
- Effective communication with teachers
- Creating study environment at home

---

## **✅ Getting Started Checklist**

1. **Setup Account**: Register your parent account
2. **Link Student**: Add your child's student ID
3. **Review Reports**: Check daily/weekly reports
4. **Set Goals**: Define academic objectives
5. **Schedule Meetings**: Plan parent-teacher meetings
6. **Monitor Progress**: Track IIT preparation
7. **Take Action**: Implement recommendations
8. **Stay Engaged**: Regular review and communication

---

## **🎯 Success Tips**

- **Consistent Monitoring**: Check reports regularly
- **Early Intervention**: Address issues early
- **Open Communication**: Talk with teachers regularly
- **Supportive Environment**: Create good study conditions
- **Goal Setting**: Set realistic academic goals
- **Celebrate Progress**: Acknowledge improvements
- **Stay Positive**: Encourage your child
- **Seek Help**: Don't hesitate to ask for support

---

**Your child's success is our priority. Use these tools effectively to support their academic journey!**
