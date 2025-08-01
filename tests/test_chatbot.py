"""
Unit tests for the chatbot components
"""
import unittest
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

class TestQuestionClassifier(unittest.TestCase):
    """Test the question classifier"""
    
    def setUp(self):
        from src.utils.question_classifier import QuestionClassifier
        self.classifier = QuestionClassifier()
    
    def test_database_questions(self):
        """Test database question classification"""
        questions = [
            "Show me all tables in the database",
            "Generate a SQL query to find customers",
            "What's the schema of the users table?"
        ]
        
        for question in questions:
            result = self.classifier.classify(question)
            self.assertIn(result, ["database", "schema"])
    
    def test_csv_questions(self):
        """Test CSV question classification"""
        questions = [
            "What's the average sales amount?",
            "Show me the distribution of ages",
            "Calculate the correlation between variables"
        ]
        
        for question in questions:
            result = self.classifier.classify(question)
            self.assertEqual(result, "csv")

class TestDatabaseManager(unittest.TestCase):
    """Test the database manager"""
    
    def setUp(self):
        from src.database.db_manager import DatabaseManager
        self.db_manager = DatabaseManager(":memory:")  # Use in-memory database for testing
    
    def test_database_initialization(self):
        """Test database initialization"""
        try:
            self.db_manager.initialize_sample_db()
            self.assertTrue(self.db_manager.has_connection())
        except Exception as e:
            self.fail(f"Database initialization failed: {e}")
    
    def test_schema_info(self):
        """Test schema information retrieval"""
        self.db_manager.initialize_sample_db()
        schema_info = self.db_manager.get_schema_info()
        
        self.assertIsInstance(schema_info, dict)
        self.assertIn("customers", schema_info)
        self.assertIn("products", schema_info)

class TestCSVAnalyzer(unittest.TestCase):
    """Test the CSV analyzer"""
    
    def setUp(self):
        from src.csv_processor.csv_analyzer import CSVAnalyzer
        import pandas as pd
        
        self.analyzer = CSVAnalyzer()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'salary': [50000, 60000, 70000]
        })
    
    def test_data_loading(self):
        """Test CSV data loading"""
        # Create a temporary CSV
        import io
        csv_buffer = io.StringIO()
        self.sample_data.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        result = self.analyzer.load_csv(csv_buffer)
        self.assertTrue(result)
        self.assertTrue(self.analyzer.has_data())
    
    def test_question_analysis(self):
        """Test question analysis"""
        # Load sample data first
        import io
        csv_buffer = io.StringIO()
        self.sample_data.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        self.analyzer.load_csv(csv_buffer)
        
        # Test different question types
        questions = [
            "What's the average age?",
            "What's the total salary?",
            "How many records are there?"
        ]
        
        for question in questions:
            response = self.analyzer.analyze_question(question)
            self.assertIsInstance(response, str)
            self.assertNotIn("Error", response)

if __name__ == "__main__":
    # Create a simple test suite
    suite = unittest.TestSuite()
    
    # Add tests that don't require external dependencies
    suite.addTest(TestQuestionClassifier('test_database_questions'))
    suite.addTest(TestQuestionClassifier('test_csv_questions'))
    
    # Try to add other tests if dependencies are available
    try:
        suite.addTest(TestDatabaseManager('test_database_initialization'))
        suite.addTest(TestDatabaseManager('test_schema_info'))
        suite.addTest(TestCSVAnalyzer('test_data_loading'))
        suite.addTest(TestCSVAnalyzer('test_question_analysis'))
    except ImportError:
        print("⚠️ Some tests skipped due to missing dependencies")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
