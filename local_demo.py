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

try:
    from src.chatbot.rag_enhancer import SimpleRAGEnhancer
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False

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
    
    if 'rag_enhancer' not in st.session_state:
        if RAG_AVAILABLE:
            st.session_state.rag_enhancer = SimpleRAGEnhancer()
        else:
            st.session_state.rag_enhancer = None
    
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    if 'csv_analyzer' not in st.session_state:
        st.session_state.csv_analyzer = CSVAnalyzer()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'sample_data_loaded' not in st.session_state:
        st.session_state.sample_data_loaded = False
    
    # RAG control settings
    if 'force_rag_mode' not in st.session_state:
        st.session_state.force_rag_mode = None  # None = Auto, True = Force RAG, False = Force Traditional
    if 'rag_enabled' not in st.session_state:
        st.session_state.rag_enabled = True  # Global RAG toggle

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
            
            # Index data for RAG if available
            if st.session_state.rag_enhancer:
                df = pd.read_csv(sales_file)
                st.session_state.rag_enhancer.index_csv_data(df)
        
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
        
        # RAG status
        if RAG_AVAILABLE and st.session_state.rag_enhancer:
            rag_status = st.session_state.rag_enhancer.get_rag_status()
            if rag_status["rag_mode"] == "Advanced":
                st.success("🧠 Advanced RAG Ready")
            else:
                st.info("🧠 Simple RAG Mode")
            
            # Show RAG stats in expander
            with st.expander("📊 RAG Status", expanded=False):
                st.json(rag_status)
        else:
            st.warning("⚠️ RAG not available")
            st.info("Install: `pip install sentence-transformers chromadb`")
        
        st.divider()
        
        # RAG Controls Section
        st.subheader("🧠 RAG Controls")
        
        # Global RAG toggle
        st.session_state.rag_enabled = st.toggle(
            "Enable RAG Enhancement", 
            value=st.session_state.rag_enabled,
            help="Turn RAG enhancement on/off globally",
            disabled=not (RAG_AVAILABLE and st.session_state.rag_enhancer)
        )
        
        if st.session_state.rag_enabled and RAG_AVAILABLE and st.session_state.rag_enhancer:
            # RAG mode selector
            mode_options = {
                "🤖 Auto (Smart Detection)": None,
                "🧠 Force RAG": True,
                "📊 Force Traditional": False
            }
            
            selected_mode = st.selectbox(
                "RAG Mode",
                options=list(mode_options.keys()),
                index=0 if st.session_state.force_rag_mode is None else (1 if st.session_state.force_rag_mode else 2),
                help="Control when to use RAG vs traditional approach"
            )
            
            st.session_state.force_rag_mode = mode_options[selected_mode]
            
            # Show current mode status
            if st.session_state.force_rag_mode is None:
                st.info("🤖 Auto mode: AI decides based on question type")
            elif st.session_state.force_rag_mode:
                st.success("🧠 RAG mode: All questions use RAG enhancement")
            else:
                st.warning("📊 Traditional mode: RAG disabled for testing")
            
            # Quick test buttons
            st.subheader("⚡ Quick RAG Tests")
            
            test_questions = [
                "What's the total sales amount?",
                "Analyze patterns in the sales data",
                "Show correlations in my data"
            ]
            
            for i, test_q in enumerate(test_questions):
                if st.button(f"🧪 Test: {test_q[:25]}...", key=f"test_{i}", use_container_width=True):
                    # Add the test question to chat
                    st.session_state.messages.append({"role": "user", "content": test_q})
                    
                    # Process and add response
                    response = process_user_question(test_q)
                    assistant_message = {"role": "assistant", "content": response["text"]}
                    
                    # Only add data if it exists and is not None
                    if "data" in response and response["data"] is not None:
                        assistant_message["data"] = response["data"]
                    
                    st.session_state.messages.append(assistant_message)
                    st.rerun()
        
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
                
                # Index for RAG if available
                if st.session_state.rag_enhancer:
                    df = pd.read_csv(uploaded_file)
                    st.session_state.rag_enhancer.index_csv_data(df)
                
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
    st.title("🤖 Local Database & CSV Chatbot with RAG")
    st.markdown("**Completely local operation with Retrieval-Augmented Generation - No API keys required!**")
    
    # Show capabilities
    with st.expander("🎯 What can I help you with?", expanded=False):
        col1, col2, col3 = st.columns(3)
        
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
        
        with col3:
            st.markdown("""
            **RAG-Enhanced Analysis:**
            - Analyze patterns in my data
            - Explain trends and insights
            - Compare different segments
            - Tell me about correlations
            """)
    
    # Show RAG status banner
    if RAG_AVAILABLE and st.session_state.rag_enhancer:
        rag_status = st.session_state.rag_enhancer.get_rag_status()
        
        # Current mode display
        if not st.session_state.rag_enabled:
            mode_display = "🚫 RAG Disabled"
            color = "red"
        elif st.session_state.force_rag_mode is None:
            mode_display = "🤖 Auto Mode"
            color = "blue"
        elif st.session_state.force_rag_mode:
            mode_display = "🧠 Force RAG"
            color = "green"
        else:
            mode_display = "📊 Force Traditional"
            color = "orange"
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"🧠 RAG: {rag_status['rag_mode']} | Indexed: {rag_status['indexed_data']['csv_chunks']} chunks | Mode: {mode_display}")
        with col2:
            if st.button("🔄 Reset Chat"):
                st.session_state.messages = []
                st.rerun()
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show data if available
                if "data" in message and message["data"] is not None:
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
                    if "data" in response and response["data"] is not None:
                        if response["data"]["type"] == "dataframe":
                            st.dataframe(response["data"]["content"])
                        elif response["data"]["type"] == "chart":
                            st.plotly_chart(response["data"]["content"], use_container_width=True)
            
            # Add assistant response to history
            assistant_message = {
                "role": "assistant", 
                "content": response["text"]
            }
            
            # Only add data if it exists and is not None
            if "data" in response and response["data"] is not None:
                assistant_message["data"] = response["data"]
            
            st.session_state.messages.append(assistant_message)

def process_user_question(question: str) -> dict:
    """Process user question and return response with optional data"""
    try:
        # Prepare context for the chatbot
        context = {
            'db_manager': st.session_state.db_manager if st.session_state.db_manager.has_connection() else None,
            'csv_analyzer': st.session_state.csv_analyzer if st.session_state.csv_analyzer.has_data() else None
        }
        
        # Determine if we should use RAG based on user controls
        use_rag = False
        approach_reason = ""
        
        if st.session_state.rag_enabled and st.session_state.rag_enhancer:
            if st.session_state.force_rag_mode is None:
                # Auto mode - let RAG enhancer decide
                use_rag = st.session_state.rag_enhancer.should_use_rag(question)
                approach_reason = "Auto-detected" if use_rag else "Auto-detected (Traditional)"
            elif st.session_state.force_rag_mode is True:
                # Force RAG mode
                use_rag = True
                approach_reason = "Force RAG"
            elif st.session_state.force_rag_mode is False:
                # Force Traditional mode
                use_rag = False
                approach_reason = "Force Traditional"
        else:
            use_rag = False
            approach_reason = "RAG Disabled"
        
        if use_rag:
            # Use RAG-enhanced response
            def llm_function(enhanced_query, full_context):
                if st.session_state.chatbot and LOCAL_MODEL_AVAILABLE:
                    return st.session_state.chatbot.process_question(enhanced_query, context)
                else:
                    return process_question_rule_based(enhanced_query, context)
            
            response_text = st.session_state.rag_enhancer.generate_rag_response(question, llm_function)
            # Add approach indicator
            response_text += f"\n\n🧠 *RAG Enhanced ({approach_reason})*"
        else:
            # Use traditional approach
            if st.session_state.chatbot and LOCAL_MODEL_AVAILABLE:
                response_text = st.session_state.chatbot.process_question(question, context)
            else:
                response_text = process_question_rule_based(question, context)
            # Add approach indicator
            response_text += f"\n\n📊 *Traditional Approach ({approach_reason})*"
        
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
