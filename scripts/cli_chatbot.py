"""
Simple command-line interface for testing the chatbot
"""
import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.chatbot.chatbot_engine import ChatbotEngine
from src.database.db_manager import DatabaseManager
from src.csv_processor.csv_analyzer import CSVAnalyzer

def main():
    """Run the command-line chatbot interface"""
    print("🤖 Welcome to the Intelligent Database & CSV Chatbot!")
    print("Type 'quit' to exit, 'help' for commands")
    
    # Initialize components
    try:
        chatbot = ChatbotEngine()
        db_manager = DatabaseManager()
        csv_analyzer = CSVAnalyzer()
        
        # Initialize database
        db_manager.initialize_sample_db()
        print("✅ Database initialized")
        
        # Load sample CSV
        csv_path = "data/csv_files/sales_data.csv"
        if os.path.exists(csv_path):
            csv_analyzer.load_csv(csv_path)
            print("✅ Sample CSV loaded")
        
    except Exception as e:
        print(f"❌ Error initializing components: {e}")
        return
    
    print("\n💡 Try asking:")
    print("- 'What tables are in the database?'")
    print("- 'Show me the total sales amount'")
    print("- 'Generate a SQL query to find top customers'")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print("""
Available commands:
- help: Show this help message
- quit: Exit the chatbot
- Any question about the database or CSV data
                """)
                continue
            
            if not user_input:
                continue
            
            # Process the question
            print("🤖 Bot: ", end="")
            response = chatbot.process_question(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
