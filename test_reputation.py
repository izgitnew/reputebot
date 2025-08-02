#!/usr/bin/env python3
"""
Test script to see the new reputation analysis response format.
"""

from analyze import SentimentAnalyzer
from vibe import VibeAnalyzer
from responder import ResponseGenerator

def test_reputation_response(text, author_handle="testuser.bsky.social"):
    """Test the new reputation analysis response format."""
    print(f"📝 Testing reputation analysis for: '{text}'")
    print(f"👤 Author: @{author_handle}")
    print("-" * 60)
    
    # Initialize analyzers
    sentiment_analyzer = SentimentAnalyzer()
    vibe_analyzer = VibeAnalyzer()
    response_generator = ResponseGenerator()
    
    # Analyze the text
    sentiment_result = sentiment_analyzer.analyze_sentiment(text)
    vibe_result = vibe_analyzer.analyze_vibe(text)
    
    # Generate reputation response
    response = response_generator.generate_response(sentiment_result, vibe_result, text, author_handle)
    
    if response:
        print("🤖 Reputation Analysis Response:")
        print(response)
    else:
        print("🤖 No response generated (post doesn't meet criteria)")
    
    return response

if __name__ == "__main__":
    # Test with different types of posts
    test_cases = [
        {
            "text": "Just built an amazing new API for sentiment analysis! The code is so clean and the documentation is comprehensive. Love sharing knowledge with the community! #tech #programming #api",
            "author": "dev.bsky.social"
        },
        {
            "text": "Reading this fascinating book about philosophy and consciousness. The author's insights are really making me think deeply about the nature of reality. Highly recommend! #books #philosophy #consciousness",
            "author": "thinker.bsky.social"
        },
        {
            "text": "Feeling really frustrated with the current state of tech. Everything feels so corporate and soulless. Wish we could go back to the early days of the web.",
            "author": "critic.bsky.social"
        },
        {
            "text": "@reputebot.bsky.social can you analyze my account? I post about design and creativity mostly.",
            "author": "designer.bsky.social"
        },
        {
            "text": "Had an amazing lunch today! The new restaurant downtown has incredible food. The chef really knows how to balance flavors. #food #lunch #restaurant",
            "author": "foodie.bsky.social"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}")
        print(f"{'='*60}")
        test_reputation_response(test_case["text"], test_case["author"])
        print(f"\n{'='*60}\n") 