#!/usr/bin/env python3
"""
Quick test script to verify the chatbot components are working
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def test_basic_functionality():
    """Test basic functionality without external dependencies"""
    print("🧪 Testing Chatbot Components...")
    
    # Test 1: Question Classifier
    print("\n1. Testing Question Classifier...")
    try:
        from src.utils.question_classifier import QuestionClassifier
        classifier = QuestionClassifier()
        
        test_questions = [
            "What tables are in the database?",
            "Show me the average sales amount",
            "Generate a SQL query for customers"
        ]
        
        for q in test_questions:
            classification = classifier.classify(q)
            print(f"   '{q}' → {classification}")
        
        print("   ✅ Question Classifier working!")
        
    except Exception as e:
        print(f"   ❌ Question Classifier failed: {e}")
    
    # Test 2: Database Manager (basic)
    print("\n2. Testing Database Manager...")
    try:
        from src.database.db_manager import DatabaseManager
        db_manager = DatabaseManager(":memory:")  # Use in-memory DB for testing
        db_manager.initialize_sample_db()
        
        schema = db_manager.get_schema_info()
        print(f"   Created {len(schema)} tables: {list(schema.keys())}")
        print("   ✅ Database Manager working!")
        
    except Exception as e:
        print(f"   ❌ Database Manager failed: {e}")
    
    # Test 3: CSV Analyzer (basic)
    print("\n3. Testing CSV Analyzer...")
    try:
        from src.csv_processor.csv_analyzer import CSVAnalyzer
        import pandas as pd
        import io
        
        # Create sample CSV data
        csv_data = """name,age,salary
Alice,25,50000
Bob,30,60000
Charlie,35,70000"""
        
        analyzer = CSVAnalyzer()
        csv_buffer = io.StringIO(csv_data)
        
        success = analyzer.load_csv(csv_buffer)
        if success:
            summary = analyzer.get_summary()
            print(f"   Loaded CSV with {analyzer.df.shape[0]} rows, {analyzer.df.shape[1]} columns")
            print("   ✅ CSV Analyzer working!")
        else:
            print("   ❌ CSV Analyzer failed to load data")
        
    except Exception as e:
        print(f"   ❌ CSV Analyzer failed: {e}")
    
    # Test 4: Training Data Generation
    print("\n4. Testing Training Data...")
    try:
        from data.training_data.sample_training_data import create_comprehensive_training_data
        training_data = create_comprehensive_training_data()
        print(f"   Generated {len(training_data)} training examples")
        print("   ✅ Training Data Generator working!")
        
    except Exception as e:
        print(f"   ❌ Training Data Generator failed: {e}")
    
    print("\n🎉 Basic functionality test complete!")

def demo_chatbot_capabilities():
    """Demonstrate chatbot capabilities with sample data"""
    print("\n🚀 Demonstrating Chatbot Capabilities...")
    
    try:
        # Initialize components
        from src.database.db_manager import DatabaseManager
        from src.csv_processor.csv_analyzer import CSVAnalyzer
        from data.create_sample_data import create_sample_sales_data
        
        print("\n📊 Sample Database Demo:")
        db_manager = DatabaseManager(":memory:")
        db_manager.initialize_sample_db()
        
        # Show sample queries
        queries = [
            "SELECT COUNT(*) as total_customers FROM customers",
            "SELECT category, COUNT(*) as products FROM products GROUP BY category",
            "SELECT SUM(total_amount) as total_revenue FROM orders"
        ]
        
        for query in queries:
            result = db_manager.execute_query(query)
            print(f"Query: {query}")
            print(f"Result: {result}\n")
        
        print("📈 Sample CSV Demo:")
        sales_df = create_sample_sales_data()
        print("Sample Sales Data:")
        print(sales_df.head())
        
        # Analyze the data
        analyzer = CSVAnalyzer()
        import io
        csv_buffer = io.StringIO()
        sales_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        analyzer.load_csv(csv_buffer)
        
        questions = [
            "What's the total sales amount?",
            "Which product has the highest sales?",
            "What's the distribution by region?"
        ]
        
        for question in questions:
            answer = analyzer.analyze_question(question)
            print(f"Q: {question}")
            print(f"A: {answer}\n")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    test_basic_functionality()
    demo_chatbot_capabilities()
    
    print("\n📝 Next Steps:")
    print("1. Run the web interface: streamlit run main.py")
    print("2. Try the CLI version: python scripts/cli_chatbot.py")
    print("3. Explore the Jupyter notebook: notebooks/demo.ipynb")
    print("4. Add your OpenAI API key to .env for full functionality")
