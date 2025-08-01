"""
Script to fine-tune the chatbot model using prepared training data
"""
import sys
import os
import json

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.fine_tuning.model_manager import ModelManager
from src.database.db_manager import DatabaseManager
from config.config import Config

def fine_tune_chatbot():
    """Fine-tune the chatbot model with training data"""
    print("🤖 Starting chatbot fine-tuning process...")
    
    # Initialize model manager
    model_manager = ModelManager(Config.MODEL_PATH)
    
    # Load training data
    training_file = os.path.join(Config.TRAINING_DATA_PATH, "comprehensive_training_data.json")
    if not os.path.exists(training_file):
        print(f"❌ Training data file not found: {training_file}")
        print("Please run initialize_project.py first")
        return
    
    with open(training_file, 'r') as f:
        training_data = json.load(f)
    
    print(f"📊 Loaded {len(training_data)} training examples")
    
    # Get additional SQL questions from database
    try:
        db_manager = DatabaseManager()
        db_manager.initialize_sample_db()
        sql_questions = db_manager.get_training_questions()
        
        # Add SQL questions to training data
        for sql_qa in sql_questions:
            training_data.append({
                "question": sql_qa["question"],
                "answer": f"Here's the SQL query: {sql_qa['sql_query']}"
            })
        
        print(f"📊 Added {len(sql_questions)} SQL questions from database")
    except Exception as e:
        print(f"⚠️ Warning: Could not load SQL questions from database: {e}")
    
    # Load base model
    print("📥 Loading base model...")
    if not model_manager.load_base_model(Config.BASE_MODEL_NAME):
        print("❌ Failed to load base model")
        return
    
    # Start fine-tuning
    print("🔧 Starting fine-tuning...")
    success = model_manager.fine_tune_model(
        training_data=training_data,
        output_dir=Config.FINE_TUNED_MODEL_PATH,
        num_epochs=Config.TRAINING_EPOCHS,
        learning_rate=Config.LEARNING_RATE
    )
    
    if success:
        print("✅ Fine-tuning completed successfully!")
        print(f"📁 Model saved to: {Config.FINE_TUNED_MODEL_PATH}")
        
        # Test the fine-tuned model
        print("🧪 Testing fine-tuned model...")
        test_questions = [
            "What tables are in the database?",
            "Show me the total sales amount",
            "Generate a SQL query to find customers"
        ]
        
        for question in test_questions:
            response = model_manager.get_finetuned_response(question)
            print(f"Q: {question}")
            print(f"A: {response}\n")
    else:
        print("❌ Fine-tuning failed!")

if __name__ == "__main__":
    fine_tune_chatbot()
