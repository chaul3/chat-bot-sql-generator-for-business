"""
Test script for the local chatbot engine
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from src.chatbot.local_chatbot_engine import LocalChatbotEngine
from src.database.db_manager import DatabaseManager
from src.csv_processor.csv_analyzer import CSVAnalyzer
from data.create_sample_data import generate_all_sample_csvs

def test_local_chatbot():
    """Test the local chatbot engine"""
    print("🤖 Testing Local Chatbot Engine")
    print("=" * 50)
    
    # Initialize components
    print("1. Initializing components...")
    chatbot = LocalChatbotEngine()
    db_manager = DatabaseManager()
    csv_analyzer = CSVAnalyzer()
    
    # Setup database
    print("2. Setting up database...")
    db_manager.initialize_sample_db()
    
    # Generate and load CSV data
    print("3. Generating CSV data...")
    csv_files = generate_all_sample_csvs()
    sales_file = csv_files.get('sales')
    if sales_file and os.path.exists(sales_file):
        csv_analyzer.load_csv(sales_file)
        print(f"   Loaded CSV: {sales_file}")
    
    # Prepare context
    context = {
        'db_manager': db_manager,
        'csv_analyzer': csv_analyzer
    }
    
    # Test questions
    test_questions = [
        "What tables are in the database?",
        "Show me the database schema",
        "Generate SQL to get all customers",
        "What's the total sales amount?",
        "How many products do we have?",
        "Show me customer demographics",
        "Create a query for top selling products"
    ]
    
    print("\n4. Testing chatbot responses:")
    print("-" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔸 Question {i}: {question}")
        try:
            response = chatbot.process_question(question, context)
            print(f"💬 Response: {response[:200]}{'...' if len(response) > 200 else ''}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Local chatbot test completed!")

if __name__ == "__main__":
    test_local_chatbot()
