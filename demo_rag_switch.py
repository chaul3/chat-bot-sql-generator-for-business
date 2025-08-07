#!/usr/bin/env python3
"""
RAG Switch Demo
Demonstrates the difference between RAG and Traditional approaches
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def demo_rag_switch():
    print("🧪 RAG Switch Demonstration")
    print("=" * 40)
    
    try:
        from src.chatbot.rag_enhancer import SimpleRAGEnhancer
        from data.create_sample_data import create_sample_sales_data
        
        # Initialize RAG
        rag = SimpleRAGEnhancer()
        
        # Create and index sample data
        print("📊 Setting up sample data...")
        sales_df = create_sample_sales_data()
        rag.index_csv_data(sales_df)
        print(f"✅ Indexed {len(sales_df)} rows of sales data")
        
        # Demo questions
        test_questions = [
            "What's the total sales amount?",
            "Analyze patterns in the sales data",
            "Show me correlations in the dataset"
        ]
        
        print("\n🔬 Testing RAG Switch Functionality:")
        print("=" * 50)
        
        for question in test_questions:
            print(f"\n❓ Question: '{question}'")
            print("-" * 60)
            
            # Test Auto mode
            auto_decision = rag.should_use_rag(question)
            print(f"🤖 Auto Mode Decision: {'RAG' if auto_decision else 'Traditional'}")
            
            # Show what each mode would do
            print(f"🧠 Force RAG Mode: Would use RAG enhancement")
            print(f"📊 Force Traditional Mode: Would use traditional approach")
            
            # Explain why
            if auto_decision:
                print("💡 Reason: Question contains analytical keywords")
            else:
                print("💡 Reason: Simple query, traditional approach sufficient")
        
        print("\n" + "=" * 50)
        print("🎯 Key Differences:")
        print("📊 Traditional: Direct data queries, exact answers")
        print("🧠 RAG: Context-aware, analytical insights, pattern recognition")
        print("\n🚀 Try the web interface for interactive testing:")
        print("   streamlit run local_demo.py")
        print("\n📖 See RAG_TESTING_GUIDE.md for detailed instructions")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure all dependencies are installed")

if __name__ == "__main__":
    demo_rag_switch()
