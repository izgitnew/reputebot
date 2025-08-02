#!/usr/bin/env python3
"""
Debug script to see which keywords are matching for content classification.
"""

from responder import ResponseGenerator
import re

def debug_keyword_matching():
    """Debug which keywords are matching for different content types."""
    print("🔍 Debugging Keyword Matching...")
    
    response_gen = ResponseGenerator()
    
    test_cases = [
        {
            "content": "Bitcoin just hit a new all-time high! The crypto market is showing incredible momentum with Ethereum and other altcoins following suit.",
            "description": "Finance content (Crypto)"
        },
        {
            "content": "New research shows promising results in cancer treatment. The clinical trial data indicates a 60% improvement in patient outcomes.",
            "description": "Health/Science content"
        },
        {
            "content": "Climate change is accelerating faster than predicted. We need immediate action on renewable energy and carbon reduction.",
            "description": "Environment content"
        },
        {
            "content": "The new RPG game just launched and it's incredible! The graphics are stunning and the multiplayer features are revolutionary.",
            "description": "Gaming content"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n--- {test_case['description']} ---")
        print(f"Content: {test_case['content']}")
        
        content_lower = test_case['content'].lower()
        content_words = set(content_lower.split())
        
        print(f"Content words: {content_words}")
        
        # Check each category
        for category, keywords in response_gen.content_keywords.items():
            matches = []
            for keyword in keywords:
                if keyword in content_words or keyword in content_lower:
                    matches.append(keyword)
            
            if matches:
                print(f"  {category}: {matches}")
        
        # Show what would be detected
        archetype = response_gen._get_archetype(test_case['content'])
        feed_category = response_gen._get_feed_category(test_case['content'])
        print(f"  Detected: {archetype} -> {feed_category}")

if __name__ == "__main__":
    debug_keyword_matching() 