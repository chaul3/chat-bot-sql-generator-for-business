#!/usr/bin/env python3
"""
Safe startup script for local_demo.py with error handling
"""
import sys
import os
import subprocess
def start_streamlit():
    print("🚀 Starting RAG-enhanced chatbot...")
    print("🔧 Fix applied: NoneType data handling")
    
    try:
        # Change to project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        
        # Start streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", "local_demo.py",
            "--server.port", "8504",
            "--server.headless", "false"
        ]
        
        print(f"Running: {' '.join(cmd)}")
        print("🌐 Opening in browser at: http://localhost:8504")
        print("🧪 Test the RAG switch controls!")
        print("📊 Use Quick Test buttons to verify the fix")
        print("\nPress Ctrl+C to stop\n")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error starting streamlit: {e}")

if __name__ == "__main__":
    start_streamlit()
