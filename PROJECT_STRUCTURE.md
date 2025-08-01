# Intelligent Database & CSV Chatbot - Project Structure

## Overview
This is a comprehensive intelligent chatbot that can:
- Read database schemas and answer SQL-related questions
- Analyze CSV files for business insights
- Generate SQL queries from natural language
- Fine-tune models for improved performance
- Provide interactive web and CLI interfaces

## Directory Structure

```
Chat Bot/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── main.py                           # Streamlit web interface
├── setup.py                          # Quick setup script
├── initialize_project.py             # Project initialization
├── .env.example                      # Environment variables template
│
├── src/                              # Source code
│   ├── __init__.py
│   ├── chatbot/                      # Core chatbot logic
│   │   ├── __init__.py
│   │   └── chatbot_engine.py         # Main chatbot engine
│   ├── database/                     # Database management
│   │   ├── __init__.py
│   │   └── db_manager.py             # Database operations
│   ├── csv_processor/                # CSV data processing
│   │   ├── __init__.py
│   │   └── csv_analyzer.py           # CSV analysis logic
│   ├── fine_tuning/                  # Model fine-tuning
│   │   ├── __init__.py
│   │   └── model_manager.py          # Model training/management
│   └── utils/                        # Utility functions
│       ├── __init__.py
│       └── question_classifier.py    # Question classification
│
├── data/                             # Data files
│   ├── create_sample_data.py         # Sample data generator
│   ├── mock_database/                # SQLite database
│   │   └── sample.db                 # Sample database file
│   ├── csv_files/                    # Sample CSV files
│   │   ├── sales_data.csv
│   │   ├── customer_data.csv
│   │   └── employee_data.csv
│   └── training_data/                # Training data for fine-tuning
│       └── sample_training_data.py   # Training data generator
│
├── models/                           # AI models
│   └── fine_tuned_chatbot/           # Fine-tuned model (created after training)
│
├── config/                           # Configuration
│   └── config.py                     # Application configuration
│
├── scripts/                          # Utility scripts
│   ├── fine_tune_model.py            # Model fine-tuning script
│   └── cli_chatbot.py                # Command-line interface
│
├── tests/                            # Unit tests
│   └── test_chatbot.py               # Test suite
│
├── notebooks/                        # Jupyter notebooks
│   └── demo.ipynb                    # Demonstration notebook
│
└── logs/                             # Log files (created during execution)
```

## Key Components

### 1. Database Integration (`src/database/`)
- **db_manager.py**: Handles SQLite database connections, schema reading, and query execution
- Automatically creates sample database with customers, products, orders, and training data
- Supports schema introspection and sample data generation

### 2. CSV Processing (`src/csv_processor/`)
- **csv_analyzer.py**: Processes CSV files and answers business questions
- Supports statistical analysis, correlations, distributions
- Generates insights and visualizations

### 3. Chatbot Engine (`src/chatbot/`)
- **chatbot_engine.py**: Core logic that routes questions and generates responses
- Integrates with both database and CSV components
- Supports multiple model backends (OpenAI, local fine-tuned)

### 4. Fine-tuning Pipeline (`src/fine_tuning/`)
- **model_manager.py**: Handles model training and fine-tuning
- Uses Hugging Face Transformers for local model training
- Combines SQL and CSV questions for comprehensive training

### 5. Web Interface (`main.py`)
- Streamlit-based web application
- Interactive chat interface
- File upload for CSV data
- Database schema visualization

## Getting Started

1. **Quick Setup**: Run `python setup.py`
2. **Manual Setup**: 
   - Install dependencies: `pip install -r requirements.txt`
   - Initialize project: `python initialize_project.py`
3. **Run Web Interface**: `streamlit run main.py`
4. **Run CLI Version**: `python scripts/cli_chatbot.py`

## Features

- 🗄️ **Database Schema Reading**: Automatically analyzes database structure
- 📊 **CSV Data Analysis**: Processes business data from CSV files
- 🤖 **Question Classification**: Intelligently routes questions to appropriate handlers
- 🎯 **Fine-tuning Support**: Improves performance with custom training data
- 🌐 **Multiple Interfaces**: Web UI and command-line options
- 📈 **Visualization**: Chart generation for data insights
- 🔗 **Mock Data**: Built-in sample datasets for testing
