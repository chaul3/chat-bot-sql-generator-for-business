import streamlit as st
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Import with fallback for missing dependencies
try:
    from src.chatbot.chatbot_engine import ChatbotEngine
    from src.database.db_manager import DatabaseManager
    from src.csv_processor.csv_analyzer import CSVAnalyzer
except ImportError as e:
    st.error(f"Missing dependencies. Please run: pip install -r requirements.txt\nError: {e}")
    st.stop()

def main():
    st.set_page_config(
        page_title="Intelligent Database & CSV Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Intelligent Database & CSV Chatbot")
    st.markdown("Ask questions about your database schema or analyze CSV data!")
    
    # Initialize components
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotEngine()
        st.session_state.db_manager = DatabaseManager()
        st.session_state.csv_analyzer = CSVAnalyzer()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Database section
        st.subheader("Database")
        if st.button("Load Sample Database"):
            st.session_state.db_manager.initialize_sample_db()
            st.success("Sample database loaded!")
        
        # CSV section
        st.subheader("CSV Files")
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        if uploaded_file:
            st.session_state.csv_analyzer.load_csv(uploaded_file)
            st.success("CSV file loaded!")
        
        # Model section
        st.subheader("Model")
        model_type = st.selectbox(
            "Select Model",
            ["GPT-3.5-turbo", "Local Fine-tuned", "Llama-2"]
        )
    
    # Main chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Chat Interface")
        
        # Chat history
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about your database or CSV data..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.process_question(
                        prompt, 
                        model_type=model_type
                    )
                st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    with col2:
        st.subheader("Quick Actions") 
        
        if st.button("Show Database Schema"):
            schema = st.session_state.db_manager.get_schema_info()
            st.json(schema)
        
        if st.button("CSV Summary"):
            if hasattr(st.session_state.csv_analyzer, 'df'):
                summary = st.session_state.csv_analyzer.get_summary()
                st.json(summary)
        
        if st.button("Generate Sample Questions"):
            questions = st.session_state.chatbot.generate_sample_questions()
            for q in questions:
                st.write(f"• {q}")

if __name__ == "__main__":
    main()
