import subprocess
import sys
import os
import webbrowser
import time

def run_command(command):
    print(f"Running: {command}")
    return subprocess.run(command, shell=True)

def main():
    print("=== Student Behavior Analysis Dashboard Launcher ===")
    
    # 1. Install dependencies
    print("\n[1/3] Installing dependencies...")
    run_command("pip install fastapi uvicorn google-generativeai python-dotenv")

    # 2. Check for database
    print("\n[2/3] Verifying database...")
    if not os.path.exists("students_analysis.db"):
        print("Database not found. Running db_importer.py...")
        run_command("python db_importer.py")
    else:
        print("Database found.")

    # 3. Start API Server
    print("\n[3/3] Launching API Server and Dashboard...")
    print("The dashboard will be available at http://localhost:8000/static/index.html")
    
    # Opening browser slightly before starting server so it loads when ready
    try:
        # Use a small delay for server to boot
        time.sleep(2)
        webbrowser.open("http://localhost:8000/static/index.html")
    except:
        pass

    # Start FastAPI with Uvicorn
    # Loading static files via FastAPI Mount
    print("Starting Uvicorn...")
    run_command("python -m uvicorn api_service:app --reload --port 8000")

if __name__ == "__main__":
    # We need to add the static file mounting to api_service.py if it's not there
    # I'll update api_service.py to serve static files
    main()
