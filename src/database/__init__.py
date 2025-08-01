"""
Database manager for handling database connections, schema reading, and query execution
"""
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, inspect, text
from typing import Dict, List, Any, Optional
import os

class DatabaseManager:
    def __init__(self, db_path: str = None):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path or os.path.join("data", "mock_database", "sample.db")
        self.engine = None
        self.connection = None
        
    def initialize_sample_db(self):
        """Initialize a sample database with mock data"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            # Create database connection
            self.engine = create_engine(f"sqlite:///{self.db_path}")
            
            # Create sample tables with data
            self._create_sample_tables()
            
            print(f"Sample database initialized at: {self.db_path}")
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise
    
    def _create_sample_tables(self):
        """Create sample tables with mock data"""
        
        # Customers table
        customers_data = [
            (1, "John Doe", "john@email.com", 28, "New York", "2023-01-15"),
            (2, "Jane Smith", "jane@email.com", 34, "Los Angeles", "2023-02-20"),
            (3, "Bob Johnson", "bob@email.com", 45, "Chicago", "2023-03-10"),
            (4, "Alice Brown", "alice@email.com", 29, "Houston", "2023-04-05"),
            (5, "Charlie Wilson", "charlie@email.com", 38, "Phoenix", "2023-05-12")
        ]
        
        customers_df = pd.DataFrame(customers_data, columns=[
            'customer_id', 'name', 'email', 'age', 'city', 'registration_date'
        ])
        customers_df.to_sql('customers', self.engine, if_exists='replace', index=False)
        
        # Products table
        products_data = [
            (1, "Laptop", "Electronics", 999.99, 50),
            (2, "Smartphone", "Electronics", 699.99, 100),
            (3, "Desk Chair", "Furniture", 199.99, 25),
            (4, "Monitor", "Electronics", 299.99, 30),
            (5, "Keyboard", "Electronics", 79.99, 75)
        ]
        
        products_df = pd.DataFrame(products_data, columns=[
            'product_id', 'name', 'category', 'price', 'stock_quantity'
        ])
        products_df.to_sql('products', self.engine, if_exists='replace', index=False)
        
        # Orders table
        orders_data = [
            (1, 1, 1, 2, 1999.98, "2023-06-01"),
            (2, 2, 2, 1, 699.99, "2023-06-02"),
            (3, 3, 3, 1, 199.99, "2023-06-03"),
            (4, 1, 4, 1, 299.99, "2023-06-04"),
            (5, 4, 5, 2, 159.98, "2023-06-05"),
            (6, 2, 1, 1, 999.99, "2023-06-06"),
            (7, 5, 2, 1, 699.99, "2023-06-07")
        ]
        
        orders_df = pd.DataFrame(orders_data, columns=[
            'order_id', 'customer_id', 'product_id', 'quantity', 'total_amount', 'order_date'
        ])
        orders_df.to_sql('orders', self.engine, if_exists='replace', index=False)
        
        # SQL Questions table for fine-tuning
        sql_questions_data = [
            (1, "How many customers do we have?", "SELECT COUNT(*) FROM customers;"),
            (2, "What's the average age of customers?", "SELECT AVG(age) FROM customers;"),
            (3, "List all products in Electronics category", "SELECT * FROM products WHERE category = 'Electronics';"),
            (4, "Total revenue from orders", "SELECT SUM(total_amount) FROM orders;"),
            (5, "Top 3 customers by order value", "SELECT c.name, SUM(o.total_amount) as total FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id ORDER BY total DESC LIMIT 3;")
        ]
        
        sql_questions_df = pd.DataFrame(sql_questions_data, columns=[
            'question_id', 'question', 'sql_query'
        ])
        sql_questions_df.to_sql('sql_questions', self.engine, if_exists='replace', index=False)
    
    def connect(self):
        """Establish database connection"""
        if not self.engine:
            self.engine = create_engine(f"sqlite:///{self.db_path}")
        self.connection = self.engine.connect()
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def has_connection(self) -> bool:
        """Check if database connection exists"""
        return self.engine is not None
    
    def get_schema_info(self) -> Dict[str, Any]:
        """Get basic schema information"""
        if not self.engine:
            return {"error": "No database connection"}
        
        try:
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            
            schema_info = {}
            for table in tables:
                columns = inspector.get_columns(table)
                schema_info[table] = {
                    "columns": [{"name": col["name"], "type": str(col["type"])} for col in columns],
                    "row_count": self._get_table_row_count(table)
                }
            
            return schema_info
            
        except Exception as e:
            return {"error": f"Error getting schema: {e}"}
    
    def get_detailed_schema(self) -> Dict[str, Any]:
        """Get detailed schema information including foreign keys and indexes"""
        if not self.engine:
            return {"error": "No database connection"}
        
        try:
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            
            detailed_schema = {}
            for table in tables:
                columns = inspector.get_columns(table)
                foreign_keys = inspector.get_foreign_keys(table)
                indexes = inspector.get_indexes(table)
                
                detailed_schema[table] = {
                    "columns": columns,
                    "foreign_keys": foreign_keys,
                    "indexes": indexes,
                    "row_count": self._get_table_row_count(table),
                    "sample_data": self._get_sample_data(table, limit=3)
                }
            
            return detailed_schema
            
        except Exception as e:
            return {"error": f"Error getting detailed schema: {e}"}
    
    def get_table_names(self) -> List[str]:
        """Get list of table names"""
        if not self.engine:
            return []
        
        try:
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except Exception as e:
            print(f"Error getting table names: {e}")
            return []
    
    def _get_table_row_count(self, table_name: str) -> int:
        """Get row count for a table"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                return result.scalar()
        except Exception as e:
            print(f"Error getting row count for {table_name}: {e}")
            return 0
    
    def _get_sample_data(self, table_name: str, limit: int = 3) -> List[Dict]:
        """Get sample data from a table"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT {limit}"))
                columns = result.keys()
                rows = result.fetchall()
                return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Error getting sample data for {table_name}: {e}")
            return []
    
    def execute_query(self, query: str) -> str:
        """Execute a SQL query and return results"""
        if not self.engine:
            return "No database connection"
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                
                if result.returns_rows:
                    rows = result.fetchall()
                    columns = result.keys()
                    
                    if not rows:
                        return "Query executed successfully, but returned no results."
                    
                    # Format results as a table
                    formatted_result = []
                    formatted_result.append(" | ".join(columns))
                    formatted_result.append("-" * len(" | ".join(columns)))
                    
                    for row in rows:
                        formatted_result.append(" | ".join(str(value) for value in row))
                    
                    return "\n".join(formatted_result)
                else:
                    return "Query executed successfully."
                    
        except Exception as e:
            return f"Error executing query: {e}"
    
    def get_training_questions(self) -> List[Dict[str, str]]:
        """Get SQL questions for fine-tuning"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT question, sql_query FROM sql_questions"))
                rows = result.fetchall()
                return [{"question": row[0], "sql_query": row[1]} for row in rows]
        except Exception as e:
            print(f"Error getting training questions: {e}")
            return []
