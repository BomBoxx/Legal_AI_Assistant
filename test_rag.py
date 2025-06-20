#!/usr/bin/env python3
"""
Simple test script to verify RAG system functionality
"""

import main as RAG

def test_rag_system():
    print("Testing RAG system...")
    
    # Test query
    test_question = "ما هي الجرائم التي يعاقب عليها القانون"
    print(f"Test question: {test_question}")
    
    try:
        articles, response = RAG.query_rag(test_question, n_results=3)
        
        print(f"\nResponse received: {len(response)} characters")
        print(f"Number of articles retrieved: {len(articles)}")
        
        print("\nResponse preview:")
        print("-" * 50)
        print(response[:500] + "..." if len(response) > 500 else response)
        print("-" * 50)
        
        print("\nArticles preview:")
        for i, article in enumerate(articles[:2], 1):
            print(f"\nArticle {i}:")
            print("-" * 30)
            print(article[:200] + "..." if len(article) > 200 else article)
            print("-" * 30)
            
        return True
        
    except Exception as e:
        print(f"Error testing RAG system: {e}")
        return False

if __name__ == "__main__":
    success = test_rag_system()
    if success:
        print("\n✅ RAG system test completed successfully!")
    else:
        print("\n❌ RAG system test failed!") 