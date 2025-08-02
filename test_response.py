#!/usr/bin/env python3
"""
Test script to see what response the bot would generate.
"""

from analyze import SentimentAnalyzer
from vibe import VibeAnalyzer
from responder import ResponseGenerator

def test_response(text):
    """Test what response the bot would generate for given text."""
    print(f"📝 Testing text: '{text}'")
    print("-" * 50)
    
    # Initialize analyzers
    sentiment_analyzer = SentimentAnalyzer()
    vibe_analyzer = VibeAnalyzer()
    response_generator = ResponseGenerator()
    
    # Analyze the text
    sentiment_result = sentiment_analyzer.analyze_sentiment(text)
    vibe_result = vibe_analyzer.analyze_vibe(text)
    
    # Show analysis results
    print(f"🎭 Sentiment: {sentiment_result['overall_sentiment']}")
    print(f"📊 VADER Scores: {sentiment_result['vader_scores']}")
    print(f"🌟 Vibe Score: {vibe_result['overall_vibe']:.3f}")
    print(f"🏷️ Hashtags: {vibe_result['hashtags']}")
    print(f"👥 Mentions: {vibe_result['mentions']}")
    
    # Generate response
    response = response_generator.generate_response(sentiment_result, vibe_result)
    
    print("-" * 50)
    if response:
        print(f"🤖 Bot Response: '{response}'")
    else:
        print("🤖 Bot Response: No response generated (post doesn't meet criteria)")
    
    return response

if __name__ == "__main__":
    # Test with different types of posts
    test_texts = [
        "I'm having such a great day! Everything is going amazing! 😊",
        "This is absolutely terrible. I hate everything right now.",
        "Just had lunch. It was okay.",
        "@reputebot.bsky.social can you analyze this post?",
        "I love coding and building things! #tech #programming",
        "Feeling really down today. Nothing seems to be working out.",
        "Just finished reading a book. It was interesting.",
        "OMG this is the best thing ever! 🔥🔥🔥"
    ]
    
    for text in test_texts:
        test_response(text)
        print("\n" + "="*60 + "\n") 