#!/usr/bin/env python3
"""
Quick RAG Demo Script
Shows the difference between RAG and traditional approaches
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def main():
    print("🧠 RAG Enhancement Quick Demo")
    print("=" * 40)
    
    try:
        from src.chatbot.rag_enhancer import SimpleRAGEnhancer
        from data.create_sample_data import create_sample_sales_data
        import pandas as pd
        
        # Initialize RAG
        print("Initializing RAG enhancer...")
        rag = SimpleRAGEnhancer()
        status = rag.get_rag_status()
        print(f"✅ RAG Mode: {status['rag_mode']}")
        
        # Create and index sample data
        print("\nCreating sample sales data...")
        sales_df = create_sample_sales_data()
        rag.index_csv_data(sales_df)
        print(f"✅ Indexed {len(sales_df)} rows")
        
        # Demo questions
        demo_questions = [
            "What's the total sales?",  # Traditional
            "Analyze sales patterns and trends",  # RAG
            "Show correlations in the data",  # RAG
            "COUNT(*) FROM sales"  # Traditional
        ]
        
        print("\n🤔 Testing Question Classification:")
        print("-" * 35)
        
        for question in demo_questions:
            should_rag = rag.should_use_rag(question)
            approach = "🧠 RAG" if should_rag else "📊 Traditional"
            print(f"{approach}: {question}")
        
        print("\n📊 RAG Retrieval Example:")
        print("-" * 35)
        
        query = "sales performance analysis"
        docs = rag.retrieve_relevant_data(query, top_k=2)
        print(f"Query: '{query}'")
        print(f"Retrieved {len(docs)} relevant chunks")
        
        if docs:
            for i, doc in enumerate(docs[:1]):
                print(f"\nChunk {i+1}:")
                content_preview = doc['content'][:150] + "..."
                print(f"Content: {content_preview}")
                print(f"Score: {doc.get('score', 'N/A')}")
        
        print("\n✅ RAG Demo Complete!")
        print("\n🚀 Try the full interface:")
        print("   streamlit run local_demo.py")
        
    except ImportError as e:
        print(f"❌ RAG dependencies missing: {e}")
        print("Install with: pip install sentence-transformers chromadb")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
