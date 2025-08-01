"""
Core chatbot engine that handles question processing and routing
"""
import openai
import os
from typing import Dict, List, Optional
from ..database.db_manager import DatabaseManager
from ..csv_processor.csv_analyzer import CSVAnalyzer
from ..utils.question_classifier import QuestionClassifier
from ..fine_tuning.model_manager import ModelManager

class ChatbotEngine:
    def __init__(self):
        """Initialize the chatbot engine with all necessary components"""
        self.db_manager = DatabaseManager()
        self.csv_analyzer = CSVAnalyzer()
        self.question_classifier = QuestionClassifier()
        self.model_manager = ModelManager()
        
        # Set OpenAI API key from environment
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
    def process_question(self, question: str, model_type: str = "GPT-3.5-turbo") -> str:
        """
        Process a user question and return an appropriate response
        
        Args:
            question: User's question
            model_type: Type of model to use for processing
            
        Returns:
            String response to the user's question
        """
        try:
            # Classify the question type
            question_type = self.question_classifier.classify(question)
            
            if question_type == "database":
                return self._handle_database_question(question, model_type)
            elif question_type == "csv":
                return self._handle_csv_question(question, model_type)
            elif question_type == "schema":
                return self._handle_schema_question(question, model_type)
            else:
                return self._handle_general_question(question, model_type)
                
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def _handle_database_question(self, question: str, model_type: str) -> str:
        """Handle questions related to database queries"""
        try:
            # Get database schema context
            schema_info = self.db_manager.get_schema_info()
            
            # Generate SQL query if needed
            if "sql" in question.lower() or "query" in question.lower():
                sql_query = self._generate_sql_query(question, schema_info, model_type)
                result = self.db_manager.execute_query(sql_query)
                return f"SQL Query: ```sql\n{sql_query}\n```\n\nResult:\n{result}"
            else:
                # Use LLM to answer based on schema
                context = f"Database Schema: {schema_info}"
                return self._get_llm_response(question, context, model_type)
                
        except Exception as e:
            return f"Error processing database question: {str(e)}"
    
    def _handle_csv_question(self, question: str, model_type: str) -> str:
        """Handle questions related to CSV data analysis"""
        try:
            if not self.csv_analyzer.has_data():
                return "No CSV data loaded. Please upload a CSV file first."
            
            # Analyze CSV data based on question
            analysis_result = self.csv_analyzer.analyze_question(question)
            
            # Generate visualization if applicable
            if "chart" in question.lower() or "plot" in question.lower():
                chart_data = self.csv_analyzer.generate_chart(question)
                return f"{analysis_result}\n\nChart data: {chart_data}"
            
            return analysis_result
            
        except Exception as e:
            return f"Error processing CSV question: {str(e)}"
    
    def _handle_schema_question(self, question: str, model_type: str) -> str:
        """Handle questions about database schema"""
        try:
            schema_info = self.db_manager.get_detailed_schema()
            context = f"Detailed Database Schema: {schema_info}"
            return self._get_llm_response(question, context, model_type)
            
        except Exception as e:
            return f"Error processing schema question: {str(e)}"
    
    def _handle_general_question(self, question: str, model_type: str) -> str:
        """Handle general questions"""
        return self._get_llm_response(question, "", model_type)
    
    def _generate_sql_query(self, question: str, schema_info: Dict, model_type: str) -> str:
        """Generate SQL query based on natural language question"""
        prompt = f"""
        Given the following database schema:
        {schema_info}
        
        Generate a SQL query to answer this question: {question}
        
        Return only the SQL query without any explanation.
        """
        
        response = self._get_llm_response(prompt, "", model_type)
        # Extract SQL from response if it contains markdown
        if "```sql" in response:
            sql = response.split("```sql")[1].split("```")[0].strip()
            return sql
        return response.strip()
    
    def _get_llm_response(self, question: str, context: str, model_type: str) -> str:
        """Get response from language model"""
        try:
            if model_type == "Local Fine-tuned":
                return self.model_manager.get_finetuned_response(question, context)
            
            # Use OpenAI API
            messages = [
                {"role": "system", "content": f"You are a helpful assistant for database and CSV data analysis. Context: {context}"},
                {"role": "user", "content": question}
            ]
            
            model_name = "gpt-3.5-turbo" if model_type == "GPT-3.5-turbo" else "gpt-4"
            
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error getting LLM response: {str(e)}"
    
    def generate_sample_questions(self) -> List[str]:
        """Generate sample questions based on available data"""
        questions = [
            "What tables are available in the database?",
            "Show me the schema for the users table",
            "What's the total sales amount in the CSV?",
            "Generate a SQL query to find the top 10 customers",
            "What are the column names in the CSV file?",
            "Show me statistics about the data"
        ]
        
        # Add dynamic questions based on actual data
        if self.db_manager.has_connection():
            tables = self.db_manager.get_table_names()
            for table in tables[:3]:  # Limit to first 3 tables
                questions.append(f"What's in the {table} table?")
        
        if self.csv_analyzer.has_data():
            columns = self.csv_analyzer.get_column_names()
            for col in columns[:3]:  # Limit to first 3 columns
                questions.append(f"What's the distribution of {col}?")
        
        return questions
