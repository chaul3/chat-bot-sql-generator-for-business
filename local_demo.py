"""
Enhanced local web interface for the chatbot
Completely local operation with improved UI
"""
import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Import with graceful fallbacks
try:
    from src.chatbot.local_chatbot_engine import LocalChatbotEngine
    LOCAL_MODEL_AVAILABLE = True
except ImportError:
    LOCAL_MODEL_AVAILABLE = False

from src.database.db_manager import DatabaseManager
from src.csv_processor.csv_analyzer import CSVAnalyzer
from data.create_sample_data import generate_all_sample_csvs

def initialize_session_state():
    """Initialize session state variables"""
    if 'chatbot' not in st.session_state:
        if LOCAL_MODEL_AVAILABLE:
            st.session_state.chatbot = LocalChatbotEngine()
        else:
            st.session_state.chatbot = None
    
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    
    if 'csv_analyzer' not in st.session_state:
        st.session_state.csv_analyzer = CSVAnalyzer()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'sample_data_loaded' not in st.session_state:
        st.session_state.sample_data_loaded = False

def load_sample_data():
    """Load all sample data"""
    try:
        # Initialize database
        st.session_state.db_manager.initialize_sample_db()
        
        # Generate CSV files
        csv_files = generate_all_sample_csvs()
        
        # Load sales data into CSV analyzer
        sales_file = csv_files.get('sales')
        if sales_file and os.path.exists(sales_file):
            st.session_state.csv_analyzer.load_csv(sales_file)
        
        st.session_state.sample_data_loaded = True
        return True, csv_files
    except Exception as e:
        return False, str(e)

def create_sidebar():
    """Create the sidebar with controls"""
    with st.sidebar:
        st.header("🔧 Local Chatbot Controls")
        
        # Model status
        if LOCAL_MODEL_AVAILABLE and st.session_state.chatbot:
            st.success("✅ Local AI Model Ready")
        else:
            st.warning("⚠️ Using Rule-based Responses")
            st.info("Install transformers for AI model: `pip install transformers torch`")
        
        st.divider()
        
        # Data loading section
        st.subheader("📊 Data Management")
        
        if st.button("🔄 Load Sample Data", use_container_width=True):
            with st.spinner("Loading sample data..."):
                success, result = load_sample_data()
                if success:
                    st.success("Sample data loaded!")
                    st.rerun()
                else:
                    st.error(f"Error: {result}")
        
        # Database status
        if st.session_state.db_manager.has_connection():
            st.success("🗄️ Database Connected")
        else:
            st.info("🗄️ Database: Not Connected")
        
        # CSV status
        if st.session_state.csv_analyzer.has_data():
            shape = st.session_state.csv_analyzer.df.shape
            st.success(f"📈 CSV Loaded: {shape[0]} rows × {shape[1]} cols")
        else:
            st.info("📈 CSV: No data loaded")
        
        st.divider()
        
        # CSV file upload
        st.subheader("📁 Upload Your Data")
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        if uploaded_file:
            try:
                st.session_state.csv_analyzer.load_csv(uploaded_file)
                st.success("CSV uploaded successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error uploading CSV: {e}")
        
        st.divider()
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("📋 Show Database Schema", use_container_width=True):
            if st.session_state.db_manager.has_connection():
                schema = st.session_state.db_manager.get_schema_info()
                st.json(schema)
            else:
                st.warning("Please load sample data first")
        
        if st.button("📊 CSV Summary", use_container_width=True):
            if st.session_state.csv_analyzer.has_data():
                summary = st.session_state.csv_analyzer.get_summary()
                st.json(summary)
            else:
                st.warning("Please upload or load CSV data first")

def create_main_interface():
    """Create the main chat interface"""
    st.title("🤖 Local Database & CSV Chatbot")
    st.markdown("**Completely local operation - No API keys required!**")
    
    # Show capabilities
    with st.expander("🎯 What can I help you with?", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Database Questions:**
            - What tables are in the database?
            - Show me all customers
            - Generate SQL for top products
            - How many orders do we have?
            """)
        
        with col2:
            st.markdown("""
            **CSV Analysis:**
            - What's the total sales amount?
            - Show average customer age
            - Find correlations in data
            - Which product has highest sales?
            """)
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show data if available
                if "data" in message:
                    if message["data"]["type"] == "dataframe":
                        st.dataframe(message["data"]["content"])
                    elif message["data"]["type"] == "chart":
                        st.plotly_chart(message["data"]["content"], use_container_width=True)
        
        # Chat input
        if prompt := st.chat_input("Ask about your database or CSV data..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Processing..."):
                    response = process_user_question(prompt)
                    st.markdown(response["text"])
                    
                    # Display additional data if available
                    if "data" in response:
                        if response["data"]["type"] == "dataframe":
                            st.dataframe(response["data"]["content"])
                        elif response["data"]["type"] == "chart":
                            st.plotly_chart(response["data"]["content"], use_container_width=True)
            
            # Add assistant response to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response["text"],
                **({k: v for k, v in response.items() if k != "text"})
            })

def process_user_question(question: str) -> dict:
    """Process user question and return response with optional data"""
    try:
        # Prepare context for the chatbot
        context = {
            'db_manager': st.session_state.db_manager if st.session_state.db_manager.has_connection() else None,
            'csv_analyzer': st.session_state.csv_analyzer if st.session_state.csv_analyzer.has_data() else None
        }
        
        # Use local chatbot if available, otherwise use rule-based responses
        if st.session_state.chatbot and LOCAL_MODEL_AVAILABLE:
            response_text = st.session_state.chatbot.process_question(question, context)
        else:
            response_text = process_question_rule_based(question, context)
        
        # Try to generate additional data/visualizations
        additional_data = None
        
        # Check if question involves CSV analysis and we have data
        if context['csv_analyzer'] and any(word in question.lower() for word in ['chart', 'plot', 'graph', 'visualize']):
            try:
                chart_data = context['csv_analyzer'].generate_chart(question)
                if 'error' not in chart_data:
                    fig = create_chart_from_data(chart_data)
                    if fig:
                        additional_data = {"type": "chart", "content": fig}
            except Exception as e:
                print(f"Chart generation error: {e}")
        
        # Check if we should show data table
        elif context['csv_analyzer'] and 'show data' in question.lower():
            try:
                df_sample = context['csv_analyzer'].df.head(10)
                additional_data = {"type": "dataframe", "content": df_sample}
            except Exception as e:
                print(f"Data display error: {e}")
        
        result = {"text": response_text}
        if additional_data:
            result["data"] = additional_data
        
        return result
        
    except Exception as e:
        return {"text": f"Sorry, I encountered an error: {str(e)}"}

def process_question_rule_based(question: str, context: dict) -> str:
    """Process questions using rule-based logic when AI model is not available"""
    question_lower = question.lower()
    
    # Database questions
    if any(word in question_lower for word in ['table', 'database', 'schema']):
        if context['db_manager']:
            if 'table' in question_lower:
                schema = context['db_manager'].get_schema_info()
                tables = list(schema.keys())
                return f"Available tables in the database:\n" + "\n".join(f"• {table}" for table in tables)
            else:
                schema = context['db_manager'].get_schema_info()
                return f"Database contains {len(schema)} tables: {', '.join(schema.keys())}"
        else:
            return "No database connection. Please load sample data first."
    
    # SQL generation
    elif any(word in question_lower for word in ['sql', 'query']):
        if 'customer' in question_lower:
            return "Here's a SQL query for customers:\n```sql\nSELECT * FROM customers LIMIT 10;\n```"
        elif 'product' in question_lower:
            return "Here's a SQL query for products:\n```sql\nSELECT * FROM products ORDER BY price DESC;\n```"
        elif 'order' in question_lower:
            return "Here's a SQL query for orders:\n```sql\nSELECT * FROM orders ORDER BY order_date DESC;\n```"
        else:
            return "I can help generate SQL queries. Please specify what data you're looking for (customers, products, orders)."
    
    # CSV questions
    elif context['csv_analyzer']:
        return context['csv_analyzer'].analyze_question(question)
    
    # General questions
    elif any(word in question_lower for word in ['hello', 'hi', 'help']):
        return """Hello! I'm your local database and CSV analysis assistant. 

I can help you with:
• Database queries and schema exploration
• CSV data analysis and insights  
• Generating SQL queries from natural language
• Statistical analysis and data visualization

Try asking: "What tables are in the database?" or "Show me the total sales amount"
"""
    
    else:
        return "I can help with database queries and CSV analysis. Please load some data first and ask about your tables or CSV files."

def create_chart_from_data(chart_data: dict):
    """Create plotly chart from chart data"""
    try:
        if chart_data["type"] == "histogram":
            fig = px.histogram(
                x=chart_data["data"], 
                title=chart_data["title"],
                labels={'x': chart_data["column"], 'y': 'Count'}
            )
            return fig
        
        elif chart_data["type"] == "scatter":
            fig = px.scatter(
                x=chart_data["x"], 
                y=chart_data["y"],
                title=chart_data["title"],
                labels={'x': chart_data["x_column"], 'y': chart_data["y_column"]}
            )
            return fig
        
        elif chart_data["type"] == "bar":
            fig = px.bar(
                x=chart_data["labels"], 
                y=chart_data["values"],
                title=chart_data["title"],
                labels={'x': chart_data["column"], 'y': 'Count'}
            )
            return fig
        
    except Exception as e:
        print(f"Error creating chart: {e}")
    
    return None

def create_stats_dashboard():
    """Create a statistics dashboard"""
    if not st.session_state.sample_data_loaded:
        st.info("Load sample data to see statistics dashboard")
        return
    
    st.header("📊 Data Statistics Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗄️ Database Stats")
        if st.session_state.db_manager.has_connection():
            schema = st.session_state.db_manager.get_schema_info()
            
            for table_name, info in schema.items():
                st.metric(
                    label=f"{table_name.title()} Table",
                    value=f"{info['row_count']} rows"
                )
    
    with col2:
        st.subheader("📈 CSV Stats")
        if st.session_state.csv_analyzer.has_data():
            df = st.session_state.csv_analyzer.df
            
            st.metric("Total Records", len(df))
            st.metric("Columns", len(df.columns))
            
            # Show numerical summary
            numerical_cols = df.select_dtypes(include=['number']).columns
            if len(numerical_cols) > 0:
                col = numerical_cols[0]
                st.metric(f"Avg {col}", f"{df[col].mean():.2f}")

def main():
    """Main application function"""
    st.set_page_config(
        page_title="Local Database & CSV Chatbot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Create layout
    create_sidebar()
    
    # Main content tabs
    tab1, tab2 = st.tabs(["💬 Chat Interface", "📊 Dashboard"])
    
    with tab1:
        create_main_interface()
    
    with tab2:
        create_stats_dashboard()
    
    # Footer
    st.markdown("---")
    st.markdown("🔒 **Completely Local** - No data leaves your machine | 🤖 **Open Source** - No API keys required")

if __name__ == "__main__":
    main()
