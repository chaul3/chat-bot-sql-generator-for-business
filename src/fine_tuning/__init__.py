"""
Model manager for fine-tuning and managing different models
"""
import os
import json
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
from typing import List, Dict, Any, Optional

class ModelManager:
    def __init__(self, model_path: str = "models/"):
        """
        Initialize model manager
        
        Args:
            model_path: Path to store/load models
        """
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self.fine_tuned_model = None
        self.fine_tuned_tokenizer = None
        
        # Ensure model directory exists
        os.makedirs(model_path, exist_ok=True)
    
    def load_base_model(self, model_name: str = "microsoft/DialoGPT-medium"):
        """Load base model for fine-tuning"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Add padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            print(f"Loaded base model: {model_name}")
            return True
            
        except Exception as e:
            print(f"Error loading base model: {e}")
            return False
    
    def prepare_training_data(self, questions_and_answers: List[Dict[str, str]]) -> Dataset:
        """
        Prepare training data for fine-tuning
        
        Args:
            questions_and_answers: List of dicts with 'question' and 'answer' keys
            
        Returns:
            Hugging Face Dataset object
        """
        # Prepare conversation format
        conversations = []
        for qa in questions_and_answers:
            conversation = f"User: {qa['question']}\nAssistant: {qa['answer']}"
            conversations.append({"text": conversation})
        
        return Dataset.from_list(conversations)
    
    def tokenize_data(self, dataset: Dataset) -> Dataset:
        """Tokenize the dataset for training"""
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"], 
                truncation=True, 
                padding=True, 
                max_length=512
            )
        
        return dataset.map(tokenize_function, batched=True)
    
    def fine_tune_model(self, 
                       training_data: List[Dict[str, str]], 
                       output_dir: str = None,
                       num_epochs: int = 3,
                       learning_rate: float = 5e-5) -> bool:
        """
        Fine-tune the model on training data
        
        Args:
            training_data: List of question-answer pairs
            output_dir: Directory to save the fine-tuned model
            num_epochs: Number of training epochs
            learning_rate: Learning rate for training
            
        Returns:
            True if fine-tuning successful, False otherwise
        """
        try:
            if not self.model or not self.tokenizer:
                print("Base model not loaded. Loading default model...")
                self.load_base_model()
            
            if not output_dir:
                output_dir = os.path.join(self.model_path, "fine_tuned_chatbot")
            
            # Prepare training dataset
            dataset = self.prepare_training_data(training_data)
            tokenized_dataset = self.tokenize_data(dataset)
            
            # Split into train/validation
            train_size = int(0.8 * len(tokenized_dataset))
            train_dataset = tokenized_dataset.select(range(train_size))
            val_dataset = tokenized_dataset.select(range(train_size, len(tokenized_dataset)))
            
            # Training arguments
            training_args = TrainingArguments(
                output_dir=output_dir,
                overwrite_output_dir=True,
                num_train_epochs=num_epochs,
                per_device_train_batch_size=2,
                per_device_eval_batch_size=2,
                warmup_steps=100,
                logging_steps=10,
                save_steps=500,
                evaluation_strategy="steps",
                eval_steps=500,
                learning_rate=learning_rate,
                weight_decay=0.01,
                logging_dir=f"{output_dir}/logs",
                save_total_limit=2,
                prediction_loss_only=True,
            )
            
            # Data collator
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer,
                mlm=False,
            )
            
            # Trainer
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=val_dataset,
                data_collator=data_collator,
            )
            
            # Train
            print("Starting fine-tuning...")
            trainer.train()
            
            # Save the fine-tuned model
            trainer.save_model()
            self.tokenizer.save_pretrained(output_dir)
            
            print(f"Fine-tuning completed. Model saved to: {output_dir}")
            
            # Load the fine-tuned model
            self.load_fine_tuned_model(output_dir)
            
            return True
            
        except Exception as e:
            print(f"Error during fine-tuning: {e}")
            return False
    
    def load_fine_tuned_model(self, model_path: str) -> bool:
        """Load a fine-tuned model"""
        try:
            self.fine_tuned_tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.fine_tuned_model = AutoModelForCausalLM.from_pretrained(model_path)
            
            print(f"Loaded fine-tuned model from: {model_path}")
            return True
            
        except Exception as e:
            print(f"Error loading fine-tuned model: {e}")
            return False
    
    def get_finetuned_response(self, question: str, context: str = "") -> str:
        """
        Generate response using fine-tuned model
        
        Args:
            question: User's question
            context: Additional context
            
        Returns:
            Generated response
        """
        if not self.fine_tuned_model or not self.fine_tuned_tokenizer:
            return "Fine-tuned model not available. Please train or load a model first."
        
        try:
            # Prepare input
            if context:
                input_text = f"Context: {context}\nUser: {question}\nAssistant:"
            else:
                input_text = f"User: {question}\nAssistant:"
            
            # Tokenize input
            inputs = self.fine_tuned_tokenizer.encode(input_text, return_tensors="pt")
            
            # Generate response
            with torch.no_grad():
                outputs = self.fine_tuned_model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 150,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.fine_tuned_tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.fine_tuned_tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the assistant's response
            if "Assistant:" in response:
                response = response.split("Assistant:")[-1].strip()
            
            return response
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def create_training_data_from_csv_and_sql(self, 
                                            csv_questions: List[str], 
                                            sql_questions: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Create training data from CSV questions and SQL question-answer pairs
        
        Args:
            csv_questions: List of CSV-related questions
            sql_questions: List of SQL question-answer pairs
            
        Returns:
            Combined training data
        """
        training_data = []
        
        # Add SQL questions (already have answers)
        for sql_qa in sql_questions:
            training_data.append({
                "question": sql_qa["question"],
                "answer": f"Here's the SQL query: {sql_qa['sql_query']}"
            })
        
        # Add CSV questions with generic answers
        csv_answer_templates = {
            "average": "I'll calculate the average for you using the CSV data.",
            "sum": "Let me compute the total from the CSV data.",
            "count": "I'll count the occurrences in the CSV data.",
            "distribution": "I'll analyze the distribution in the CSV data.",
            "correlation": "I'll examine the correlations in the CSV data."
        }
        
        for csv_question in csv_questions:
            # Determine answer based on question type
            answer = "I'll analyze the CSV data to answer your question."
            question_lower = csv_question.lower()
            
            for keyword, template in csv_answer_templates.items():
                if keyword in question_lower:
                    answer = template
                    break
            
            training_data.append({
                "question": csv_question,
                "answer": answer
            })
        
        return training_data
    
    def save_training_data(self, training_data: List[Dict[str, str]], filename: str = "training_data.json"):
        """Save training data to file"""
        try:
            filepath = os.path.join(self.model_path, filename)
            with open(filepath, 'w') as f:
                json.dump(training_data, f, indent=2)
            print(f"Training data saved to: {filepath}")
            return True
        except Exception as e:
            print(f"Error saving training data: {e}")
            return False
    
    def load_training_data(self, filename: str = "training_data.json") -> List[Dict[str, str]]:
        """Load training data from file"""
        try:
            filepath = os.path.join(self.model_path, filename)
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading training data: {e}")
            return []
