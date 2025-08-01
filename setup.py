#!/usr/bin/env python3
"""
Quick setup script for the chatbot project
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command with proper error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Intelligent Chatbot Project...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version} detected")
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("⚠️ Some dependencies failed to install. You may need to install them manually.")
    
    # Run project initialization
    if run_command("python initialize_project.py", "Initializing project"):
        print("\n🎉 Setup complete!")
        print("\n📝 Next steps:")
        print("1. Copy .env.example to .env and add your API keys")
        print("2. Run the web interface: streamlit run main.py")
        print("3. Or use CLI: python scripts/cli_chatbot.py")
        print("4. (Optional) Fine-tune model: python scripts/fine_tune_model.py")
    else:
        print("❌ Project initialization failed!")

if __name__ == "__main__":
    main()
