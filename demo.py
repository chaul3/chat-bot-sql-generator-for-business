#!/usr/bin/env python3
"""
Simple demo script showing the chatbot capabilities
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def main():
    print("🤖 Intelligent Database & CSV Chatbot Demo")
    print("=" * 50)
    
    # Test Question Classification
    print("\n1. 🧠 Question Classification Demo")
    print("-" * 30)
    
    try:
        from src.utils.question_classifier import QuestionClassifier
        classifier = QuestionClassifier()
        
        test_questions = [
            "What tables are in the database?",
            "Show me the SQL schema",
            "What's the average sales in the CSV?",
            "Calculate correlation between variables",
            "Hello, what can you do?"
        ]
        
        for question in test_questions:
            classification = classifier.classify(question)
            print(f"'{question}' → {classification}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Test Database Management
    print("\n2. 🗄️ Database Management Demo")
    print("-" * 30)
    
    try:
        from src.database.db_manager import DatabaseManager
        
        # Use in-memory database for demo
        db_manager = DatabaseManager(":memory:")
        db_manager.initialize_sample_db()
        
        print("✅ Sample database created with tables:")
        schema = db_manager.get_schema_info()
        for table_name, info in schema.items():
            print(f"  - {table_name}: {info['row_count']} rows")
        
        # Execute a sample query
        print("\n📊 Sample Query Results:")
        result = db_manager.execute_query("SELECT COUNT(*) as customer_count FROM customers")
        print(f"Total customers: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Test CSV Analysis
    print("\n3. 📈 CSV Analysis Demo")
    print("-" * 30)
    
    try:
        from src.csv_processor.csv_analyzer import CSVAnalyzer
        from data.create_sample_data import create_sample_sales_data
        import io
        
        # Create sample data
        sales_df = create_sample_sales_data()
        print(f"✅ Created sample sales data: {sales_df.shape[0]} rows, {sales_df.shape[1]} columns")
        
        # Load into analyzer
        analyzer = CSVAnalyzer()
        csv_buffer = io.StringIO()
        sales_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        success = analyzer.load_csv(csv_buffer)
        if success:
            print("✅ CSV data loaded successfully")
            
            # Ask sample questions
            questions = [
                "What's the total sales amount?",
                "What's the average quantity sold?",
                "How many different products are there?"
            ]
            
            for question in questions:
                answer = analyzer.analyze_question(question)
                print(f"Q: {question}")
                print(f"A: {answer}\n")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Show training data
    print("\n4. 🤖 Training Data Demo")
    print("-" * 30)
    
    try:
        from data.training_data.sample_training_data import create_comprehensive_training_data
        
        training_data = create_comprehensive_training_data()
        print(f"✅ Generated {len(training_data)} training examples")
        
        print("\nSample training examples:")
        for i, example in enumerate(training_data[:3]):
            print(f"{i+1}. Q: {example['question']}")
            print(f"   A: {example['answer']}\n")
    
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n🎉 Demo Complete!")
    print("\n📝 To use the full chatbot:")
    print("1. Install all dependencies: pip install -r requirements.txt")
    print("2. Add OpenAI API key to .env file")
    print("3. Run web interface: streamlit run main.py")
    print("4. Or use CLI: python scripts/cli_chatbot.py")

if __name__ == "__main__":
    main()
