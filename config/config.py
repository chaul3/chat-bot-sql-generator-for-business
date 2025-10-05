# Configuration file for the chatbot
import os
class Config:
    # Database settings
    DATABASE_PATH = "data/mock_database/sample.db"
    
    # CSV settings
    CSV_UPLOAD_PATH = "data/csv_files/"
    MAX_CSV_SIZE_MB = 100
    
    # Model settings
    MODEL_PATH = "models/"
    BASE_MODEL_NAME = "microsoft/DialoGPT-medium"
    FINE_TUNED_MODEL_PATH = "models/fine_tuned_chatbot"
    
    # OpenAI settings (if using OpenAI API)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = "gpt-3.5-turbo"
    
    # Training settings
    TRAINING_EPOCHS = 3
    LEARNING_RATE = 5e-5
    BATCH_SIZE = 2
    MAX_LENGTH = 512
    
    # Streamlit settings
    PAGE_TITLE = "Intelligent Database & CSV Chatbot"
    PAGE_ICON = "🤖"
    
    # File paths
    TRAINING_DATA_PATH = "data/training_data/"
    LOGS_PATH = "logs/"
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        directories = [
            cls.CSV_UPLOAD_PATH,
            cls.MODEL_PATH,
            cls.TRAINING_DATA_PATH,
            cls.LOGS_PATH,
            os.path.dirname(cls.DATABASE_PATH)
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
