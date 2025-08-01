"""
Initialization script for the chatbot project
Run this script to set up the entire project with sample data
"""
import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from config.config import Config
from data.create_sample_data import generate_all_sample_csvs
from data.training_data.sample_training_data import create_comprehensive_training_data
from src.database.db_manager import DatabaseManager
from src.fine_tuning.model_manager import ModelManager
import json

def initialize_project():
    """Initialize the entire chatbot project"""
    print("🚀 Initializing Intelligent Chatbot Project...")
    
    # 1. Create necessary directories
    print("📁 Creating directories...")
    Config.ensure_directories()
    
    # 2. Initialize database with sample data
    print("🗄️ Initializing database...")
    try:
        db_manager = DatabaseManager()
        db_manager.initialize_sample_db()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
    
    # 3. Generate sample CSV files
    print("📊 Creating sample CSV files...")
    try:
        csv_files = generate_all_sample_csvs()
        print("✅ Sample CSV files created!")
        for name, path in csv_files.items():
            print(f"   - {name}: {path}")
    except Exception as e:
        print(f"❌ Error creating CSV files: {e}")
    
    # 4. Create training data
    print("🤖 Preparing training data...")
    try:
        training_data = create_comprehensive_training_data()
        
        # Save training data
        training_file = os.path.join(Config.TRAINING_DATA_PATH, "comprehensive_training_data.json")
        with open(training_file, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        print(f"✅ Training data created with {len(training_data)} examples!")
        print(f"   Saved to: {training_file}")
    except Exception as e:
        print(f"❌ Error creating training data: {e}")
    
    # 5. Display next steps
    print("\n🎉 Project initialization complete!")
    print("\n📝 Next steps:")
    print("1. Copy .env.example to .env and add your API keys")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the chatbot: streamlit run main.py")
    print("4. (Optional) Fine-tune the model: python scripts/fine_tune_model.py")
    
    print("\n💡 Sample questions you can ask:")
    print("- 'What tables are in the database?'")
    print("- 'Show me the total sales amount'")
    print("- 'Generate a SQL query to find top customers'")
    print("- 'What's the average customer age?'")

if __name__ == "__main__":
    initialize_project()
