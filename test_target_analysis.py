#!/usr/bin/env python3
"""
Test script to simulate analyzing a target account when mentioned in a reply.
"""

from analyze import SentimentAnalyzer
from vibe import VibeAnalyzer
from responder import ResponseGenerator

def test_target_account_analysis():
    """Test analyzing a target account's posts."""
    
    # Simulate analyzing a target account's recent posts
    target_handle = "targetuser.bsky.social"
    
    # Sample posts from the target account (what the bot would fetch)
    target_posts = [
        "Just built an amazing new API for sentiment analysis! The code is so clean and the documentation is comprehensive. Love sharing knowledge with the community! #tech #programming #api",
        "Reading this fascinating book about philosophy and consciousness. The author's insights are really making me think deeply about the nature of reality. Highly recommend! #books #philosophy #consciousness",
        "Had an amazing lunch today! The new restaurant downtown has incredible food. The chef really knows how to balance flavors. #food #lunch #restaurant",
        "Feeling really frustrated with the current state of tech. Everything feels so corporate and soulless. Wish we could go back to the early days of the web.",
        "Just finished reading a book. It was interesting."
    ]
    
    print(f"🎯 Analyzing target account: @{target_handle}")
    print(f"📊 Found {len(target_posts)} recent posts")
    print("-" * 60)
    
    # Initialize analyzers
    sentiment_analyzer = SentimentAnalyzer()
    vibe_analyzer = VibeAnalyzer()
    response_generator = ResponseGenerator()
    
    # Combine all posts for analysis
    combined_text = " ".join(target_posts)
    print(f"📝 Combined text length: {len(combined_text)} characters")
    
    # Analyze sentiment and vibe of the target account's content
    sentiment_result = sentiment_analyzer.analyze_sentiment(combined_text)
    vibe_result = vibe_analyzer.analyze_vibe(combined_text)
    
    print("\n🔍 Analysis Results:")
    print(f"   Sentiment: {sentiment_result['overall_sentiment']}")
    print(f"   Vibe Score: {vibe_result['overall_vibe']:.3f}")
    print(f"   Hashtags: {vibe_result['hashtags']}")
    print(f"   Mentions: {vibe_result['mentions']}")
    print()
    
    # Generate reputation response for the target account
    response = response_generator.generate_response(sentiment_result, vibe_result, combined_text, target_handle)
    
    print("🤖 REPUTATION ANALYSIS RESPONSE:")
    print("=" * 60)
    if response:
        print(response)
    else:
        print("No response generated (posts don't meet criteria)")
    print("=" * 60)

if __name__ == "__main__":
    test_target_account_analysis() 