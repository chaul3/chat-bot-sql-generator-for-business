"""
RAG Enhancement for the chatbot
Retrieval-Augmented Generation for better context-aware responses
"""
import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import sqlite3
import json

# Try to import RAG dependencies with fallbacks
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

class SimpleRAGEnhancer:
    """
    Simplified RAG implementation that works with or without advanced dependencies
    """
    
    def __init__(self, use_advanced_rag: bool = True):
        """Initialize RAG enhancer"""
        self.use_advanced_rag = use_advanced_rag and SENTENCE_TRANSFORMERS_AVAILABLE and CHROMADB_AVAILABLE
        self.embedding_model = None
        self.chroma_client = None
        self.csv_collection = None
        self.db_collection = None
        
        # Simple fallback storage
        self.simple_csv_chunks = []
        self.simple_db_info = []
        self.conversation_history = []
        
        if self.use_advanced_rag:
            self._setup_advanced_rag()
        
        print(f"RAG Mode: {'Advanced' if self.use_advanced_rag else 'Simple'}")
    
    def _setup_advanced_rag(self):
        """Setup advanced RAG with embeddings and vector database"""
        try:
            # Initialize embedding model
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Initialize ChromaDB
            self.chroma_client = chromadb.Client(Settings(
                persist_directory="./chroma_db",
                anonymized_telemetry=False
            ))
            
            # Create collections
            self.csv_collection = self.chroma_client.get_or_create_collection(
                name="csv_data_rag",
                metadata={"description": "CSV data for RAG retrieval"}
            )
            
            self.db_collection = self.chroma_client.get_or_create_collection(
                name="database_rag",
                metadata={"description": "Database schema for RAG retrieval"}
            )
            
        except Exception as e:
            print(f"Advanced RAG setup failed, falling back to simple mode: {e}")
            self.use_advanced_rag = False
    
    def index_csv_data(self, df: pd.DataFrame, chunk_size: int = 20):
        """Index CSV data for retrieval"""
        try:
            if self.use_advanced_rag:
                self._index_csv_advanced(df, chunk_size)
            else:
                self._index_csv_simple(df, chunk_size)
            
            print(f"Indexed CSV data: {len(df)} rows")
            
        except Exception as e:
            print(f"Error indexing CSV data: {e}")
    
    def _index_csv_simple(self, df: pd.DataFrame, chunk_size: int):
        """Index CSV using simple approach"""
        self.simple_csv_chunks = []
        
        for i in range(0, len(df), chunk_size):
            chunk_df = df.iloc[i:i+chunk_size]
            chunk_text = self._dataframe_to_text(chunk_df)
            
            chunk_info = {
                "text": chunk_text,
                "chunk_id": i // chunk_size,
                "start_row": i,
                "end_row": min(i + chunk_size, len(df)),
                "num_rows": len(chunk_df),
                "columns": list(chunk_df.columns)
            }
            self.simple_csv_chunks.append(chunk_info)
    
    def _dataframe_to_text(self, df: pd.DataFrame) -> str:
        """Convert DataFrame chunk to text representation"""
        text_parts = []
        
        # Add column information
        text_parts.append(f"Columns: {', '.join(df.columns)}")
        
        # Add summary statistics for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            text_parts.append("Numeric statistics:")
            for col in numeric_cols[:3]:  # Limit to first 3 numeric columns
                try:
                    stats = df[col].describe()
                    text_parts.append(f"  {col}: mean={stats['mean']:.2f}, min={stats['min']:.2f}, max={stats['max']:.2f}")
                except:
                    text_parts.append(f"  {col}: numeric column")
        
        # Add categorical summaries
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            text_parts.append("Categorical data:")
            for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
                try:
                    unique_vals = df[col].unique()[:3]  # Top 3 unique values
                    text_parts.append(f"  {col}: {', '.join(map(str, unique_vals))}")
                except:
                    text_parts.append(f"  {col}: categorical column")
        
        # Add sample rows
        try:
            text_parts.append("Sample data:")
            sample_rows = df.head(2).to_string(index=False, max_cols=5)
            text_parts.append(sample_rows)
        except:
            text_parts.append("Sample data: [Unable to display]")
        
        return "\n".join(text_parts)
    
    def retrieve_relevant_data(self, query: str, data_type: str = "csv", top_k: int = 3) -> List[Dict]:
        """Retrieve relevant data chunks based on query"""
        try:
            if data_type == "csv" and self.simple_csv_chunks:
                return self._retrieve_simple_csv(query, top_k)
            return []
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return []
    
    def _retrieve_simple_csv(self, query: str, top_k: int) -> List[Dict]:
        """Retrieve using simple keyword matching for CSV"""
        query_lower = query.lower()
        relevant_docs = []
        
        for chunk in self.simple_csv_chunks:
            # Score based on keyword overlap
            score = 0
            chunk_text_lower = chunk['text'].lower()
            
            # Count keyword matches
            for word in query_lower.split():
                if len(word) > 2 and word in chunk_text_lower:
                    score += 1
            
            if score > 0:
                relevant_docs.append({
                    'content': chunk['text'],
                    'metadata': {k: v for k, v in chunk.items() if k != 'text'},
                    'score': score,
                    'id': f"csv_chunk_{chunk['chunk_id']}"
                })
        
        # Sort by score and take top_k
        relevant_docs.sort(key=lambda x: x['score'], reverse=True)
        return relevant_docs[:top_k]
    
    def generate_rag_response(self, query: str, llm_function, context_limit: int = 2000) -> str:
        """Generate response using RAG approach"""
        try:
            # Retrieve relevant data
            csv_docs = self.retrieve_relevant_data(query, "csv", top_k=2)
            
            # Build context
            context_parts = []
            sources = []
            
            # Add CSV context
            if csv_docs:
                context_parts.append("=== Relevant CSV Data ===")
                for doc in csv_docs:
                    context_parts.append(f"Data: {doc['content'][:400]}...")
                sources.append("CSV data")
            
            # Combine context
            full_context = "\n".join(context_parts)
            
            # Truncate if too long
            if len(full_context) > context_limit:
                full_context = full_context[:context_limit] + "..."
            
            # Create enhanced prompt
            if full_context:
                enhanced_query = f"""Based on the following relevant context, please answer the user's question comprehensively:

Context:
{full_context}

User Question: {query}

Please provide a detailed answer based on the context above. Reference specific data points when relevant.
"""
            else:
                enhanced_query = query
            
            # Use existing LLM function
            response = llm_function(enhanced_query, full_context)
            
            # Add source citation if we found relevant context
            if sources:
                response += f"\n\n📊 *Based on: {', '.join(sources)}* (Simple RAG)"
            
            # Store conversation for future context
            self.conversation_history.append({
                "query": query,
                "response": response,
                "sources": sources
            })
            
            return response
            
        except Exception as e:
            print(f"Error in RAG response generation: {e}")
            # Fallback to original query
            return llm_function(query, "")
    
    def should_use_rag(self, query: str) -> bool:
        """Determine if RAG should be used for this query"""
        # Keywords that suggest RAG would be beneficial
        rag_keywords = [
            "analyze", "pattern", "trend", "correlation", "insight", "relationship",
            "compare", "similarity", "difference", "context", "explain", "why",
            "how", "tell me about", "understand", "explore", "investigate"
        ]
        
        query_lower = query.lower()
        
        # Count keyword matches
        rag_score = sum(1 for keyword in rag_keywords if keyword in query_lower)
        
        # If analytical keywords present, use RAG
        if rag_score > 0:
            return True
        
        # For longer queries, prefer RAG
        return len(query.split()) > 6
    
    def get_rag_status(self) -> Dict[str, Any]:
        """Get current RAG status and statistics"""
        status = {
            "rag_mode": "Advanced" if self.use_advanced_rag else "Simple",
            "dependencies_available": {
                "sentence_transformers": SENTENCE_TRANSFORMERS_AVAILABLE,
                "chromadb": CHROMADB_AVAILABLE
            },
            "indexed_data": {
                "csv_chunks": len(self.simple_csv_chunks),
                "conversation_history": len(self.conversation_history)
            }
        }
        
        return status
