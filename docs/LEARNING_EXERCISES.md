# Learning Exercises for Student Behavior Analysis System

## Exercise 1: Test the API Directly
**Goal:** Learn to test endpoints without using the UI

**Task:**
1. Open a terminal in the project directory
2. Run: `curl http://localhost:8000/api/students`
3. What do you see? List the students returned.

## Exercise 2: Test the Conversational API
**Goal:** Understand how the conversational API works

**Task:**
1. Run: `python test_chat_simple.py`
2. Look at the output for the compound query
3. Answer: Which two tools were executed? What was the combined response?

## Exercise 3: Check the Database
**Goal:** Understand the data structure

**Task:**
1. Run: `sqlite3 behavior.db "SELECT * FROM student_activity LIMIT 5"`
2. What columns does the table have?
3. What does a single activity record look like?

## Exercise 4: Read the Code
**Goal:** Understand the code structure

**Task:**
1. Open `agent_orchestrator.py`
2. Find the `ToolRegistry` class (around line 16)
3. Find the `IntentParser` class (around line 350)
4. Find the `ConversationalRouter` class (around line 501)
5. What does each class do?

## Exercise 5: Fix a Simple Bug
**Goal:** Learn to debug and fix issues

**Task:**
1. The UI in `index.html` has a data structure mismatch
2. The API returns `analysis.total_study_time` but UI expects `stats.total_time`
3. Can you find where in the code this mismatch occurs?
4. (Don't fix it yet - just identify the problem)

## Exercise 6: Add a New Query
**Goal:** Learn to use the conversational API

**Task:**
1. Modify `test_chat_simple.py` to add a new query
2. Try: "Get class overview"
3. Run it and see what tool is called
4. What does the response contain?
