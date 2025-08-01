"""
Local chatbot engine using open-source models
No API keys required - completely local operation
"""
import os
import json
import re
from typing import List, Dict, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

class LocalChatbotEngine:
    def __init__(self, model_name: str = "microsoft/DialoGPT-small"):
        """
        Initialize local chatbot with open-source model
        
        Args:
            model_name: HuggingFace model name for local inference
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.generator = None
        self.conversation_history = []
        
        # SQL keywords and patterns for query generation
        self.sql_patterns = {
            'select_all': r'\b(show|list|get|display|view)\s+(all\s+)?(\w+)s?\b',
            'count': r'\b(how many|count|number of)\s+(\w+)s?\b',
            'average': r'\b(average|avg|mean)\s+(\w+)\b',
            'sum': r'\b(total|sum)\s+(\w+)\b',
            'max': r'\b(highest|maximum|max|largest)\s+(\w+)\b',
            'min': r'\b(lowest|minimum|min|smallest)\s+(\w+)\b',
            'filter': r'\b(where|with|having)\s+(\w+)\s*(=|>|<|like)\s*(\w+)\b'
        }
        
        # Load model
        self._load_model()
    
    def _load_model(self):
        """Load the local model for inference"""
        try:
            print(f"Loading local model: {self.model_name}")
            
            # Use smaller model for better performance on local machines
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Add special tokens if needed
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Create text generation pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=512,
                do_sample=True,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            print("✅ Local model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("Falling back to rule-based responses...")
            self.generator = None
    
    def process_question(self, question: str, context: Dict = None) -> str:
        """
        Process user question and generate response
        
        Args:
            question: User's question
            context: Optional context (database info, CSV data, etc.)
            
        Returns:
            Generated response
        """
        question_lower = question.lower().strip()
        
        # Classify question type
        question_type = self._classify_question(question_lower)
        
        if question_type == "sql":
            return self._handle_sql_question(question, context)
        elif question_type == "csv":
            return self._handle_csv_question(question, context)
        elif question_type == "schema":
            return self._handle_schema_question(question, context)
        else:
            return self._handle_general_question(question, context)
    
    def _classify_question(self, question: str) -> str:
        """Classify the type of question"""
        sql_keywords = ['sql', 'query', 'database', 'table', 'select', 'insert', 'update', 'delete', 'join']
        csv_keywords = ['csv', 'data', 'average', 'sum', 'total', 'count', 'correlation', 'distribution']
        schema_keywords = ['schema', 'structure', 'tables', 'columns', 'fields']
        
        if any(keyword in question for keyword in sql_keywords):
            return "sql"
        elif any(keyword in question for keyword in csv_keywords):
            return "csv"
        elif any(keyword in question for keyword in schema_keywords):
            return "schema"
        else:
            return "general"
    
    def _handle_sql_question(self, question: str, context: Dict = None) -> str:
        """Handle SQL-related questions"""
        # Generate SQL query based on patterns
        sql_query = self._generate_sql_query(question, context)
        
        if sql_query:
            response = f"Here's the SQL query to answer your question:\n\n```sql\n{sql_query}\n```"
            
            # If we have database context, try to execute
            if context and 'db_manager' in context:
                try:
                    result = context['db_manager'].execute_query(sql_query)
                    response += f"\n\nResult:\n{result}"
                except Exception as e:
                    response += f"\n\nNote: {str(e)}"
            
            return response
        else:
            return self._generate_llm_response(question, "SQL database query generation")
    
    def _handle_csv_question(self, question: str, context: Dict = None) -> str:
        """Handle CSV analysis questions"""
        if context and 'csv_analyzer' in context:
            try:
                return context['csv_analyzer'].analyze_question(question)
            except Exception as e:
                return f"Error analyzing CSV data: {str(e)}"
        else:
            return self._generate_llm_response(question, "CSV data analysis")
    
    def _handle_schema_question(self, question: str, context: Dict = None) -> str:
        """Handle database schema questions"""
        if context and 'db_manager' in context:
            try:
                schema_info = context['db_manager'].get_schema_info()
                
                if "tables" in question.lower():
                    tables = list(schema_info.keys())
                    return f"Available tables in the database:\n" + "\n".join(f"• {table}" for table in tables)
                
                # Look for specific table mentioned
                for table_name in schema_info.keys():
                    if table_name.lower() in question.lower():
                        table_info = schema_info[table_name]
                        columns = [col['name'] for col in table_info['columns']]
                        return f"Schema for '{table_name}' table:\n" + "\n".join(f"• {col}" for col in columns)
                
                return json.dumps(schema_info, indent=2)
            except Exception as e:
                return f"Error getting schema information: {str(e)}"
        else:
            return "No database connection available to show schema information."
    
    def _handle_general_question(self, question: str, context: Dict = None) -> str:
        """Handle general questions"""
        # Predefined responses for common questions
        responses = {
            "hello": "Hello! I'm your local database and CSV analysis assistant. How can I help you today?",
            "help": "I can help you with:\n• Database queries and schema exploration\n• CSV data analysis and insights\n• Generating SQL queries from natural language\n• Statistical analysis and data visualization",
            "what can you do": "I can analyze databases, process CSV files, generate SQL queries, and provide data insights - all running locally on your machine!",
            "how to use": "Simply ask me questions about your data! For example:\n• 'What tables are in the database?'\n• 'Show me the total sales'\n• 'Generate a query to find top customers'"
        }
        
        question_clean = question.lower().strip('?!.,')
        
        for key, response in responses.items():
            if key in question_clean:
                return response
        
        return self._generate_llm_response(question, "general assistance")
    
    def _generate_sql_query(self, question: str, context: Dict = None) -> Optional[str]:
        """Generate SQL query based on question patterns"""
        question_lower = question.lower()
        
        # Get table names from context if available
        tables = []
        if context and 'db_manager' in context:
            try:
                schema = context['db_manager'].get_schema_info()
                tables = list(schema.keys())
            except:
                tables = ['customers', 'products', 'orders']  # fallback
        else:
            tables = ['customers', 'products', 'orders']
        
        # Pattern matching for SQL generation
        for pattern_name, pattern in self.sql_patterns.items():
            match = re.search(pattern, question_lower)
            if match:
                if pattern_name == 'select_all':
                    table = self._find_table_name(match.group(3), tables)
                    if table:
                        return f"SELECT * FROM {table};"
                
                elif pattern_name == 'count':
                    table = self._find_table_name(match.group(2), tables)
                    if table:
                        return f"SELECT COUNT(*) as count FROM {table};"
                
                elif pattern_name == 'average':
                    column = match.group(2)
                    table = self._guess_table_for_column(column, tables)
                    return f"SELECT AVG({column}) as average_{column} FROM {table};"
                
                elif pattern_name == 'sum':
                    column = match.group(2)
                    table = self._guess_table_for_column(column, tables)
                    return f"SELECT SUM({column}) as total_{column} FROM {table};"
        
        # Fallback: simple queries based on keywords
        if 'customer' in question_lower:
            return "SELECT * FROM customers LIMIT 10;"
        elif 'product' in question_lower:
            return "SELECT * FROM products LIMIT 10;"
        elif 'order' in question_lower:
            return "SELECT * FROM orders LIMIT 10;"
        elif 'revenue' in question_lower or 'sales' in question_lower:
            return "SELECT SUM(total_amount) as total_revenue FROM orders;"
        
        return None
    
    def _find_table_name(self, word: str, tables: List[str]) -> Optional[str]:
        """Find best matching table name"""
        if not word:
            return None
            
        word = word.lower()
        
        # Direct match
        if word in tables:
            return word
        
        # Partial match (e.g., "customer" matches "customers")
        for table in tables:
            if word in table or table in word:
                return table
        
        return tables[0] if tables else None
    
    def _guess_table_for_column(self, column: str, tables: List[str]) -> str:
        """Guess which table a column belongs to"""
        column_mappings = {
            'age': 'customers',
            'price': 'products',
            'amount': 'orders',
            'total': 'orders',
            'quantity': 'orders',
            'sales': 'orders'
        }
        
        for key, table in column_mappings.items():
            if key in column.lower() and table in tables:
                return table
        
        return tables[0] if tables else 'customers'
    
    def _generate_llm_response(self, question: str, context_type: str) -> str:
        """Generate response using local LLM or fallback to rule-based"""
        if self.generator:
            try:
                prompt = f"User: {question}\nAssistant:"
                
                # Generate response
                response = self.generator(
                    prompt,
                    max_length=len(prompt.split()) + 50,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True
                )[0]['generated_text']
                
                # Extract only the assistant's response
                if "Assistant:" in response:
                    response = response.split("Assistant:")[-1].strip()
                else:
                    response = response[len(prompt):].strip()
                
                return response if response else self._fallback_response(context_type)
                
            except Exception as e:
                print(f"LLM generation error: {e}")
                return self._fallback_response(context_type)
        else:
            return self._fallback_response(context_type)
    
    def _fallback_response(self, context_type: str) -> str:
        """Fallback responses when LLM is not available"""
        fallbacks = {
            "SQL database query generation": "I can help you generate SQL queries. Please describe what data you want to retrieve from the database.",
            "CSV data analysis": "I can analyze your CSV data. Please specify what kind of analysis you need (averages, totals, distributions, etc.).",
            "general assistance": "I'm here to help with database queries and CSV analysis. What would you like to know about your data?"
        }
        
        return fallbacks.get(context_type, "I'm here to help with your data analysis needs. Could you please rephrase your question?")
    
    def get_capabilities(self) -> Dict[str, str]:
        """Return chatbot capabilities"""
        return {
            "Database Analysis": "Query databases, explore schemas, generate SQL",
            "CSV Processing": "Analyze CSV files, calculate statistics, find insights",
            "Local Operation": "Runs completely offline, no API keys required",
            "Natural Language": "Ask questions in plain English",
            "Multiple Formats": "Supports various data analysis tasks"
        }
