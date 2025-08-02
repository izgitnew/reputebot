#!/usr/bin/env python3
"""
Show the exact response the bot would generate for a mention.
"""

from analyze import SentimentAnalyzer
from vibe import VibeAnalyzer
from responder import ResponseGenerator

def show_mention_response():
    """Show what response the bot would generate for the user's mention."""
    
    # The text from your mention (based on what the bot detected)
    mention_text = "@reputebot.bsky.social"
    author_handle = "testmybot.bsky.social"  # From the logs
    
    print(f"📝 Analyzing mention: '{mention_text}'")
    print(f"👤 Author: @{author_handle}")
    print("-" * 60)
    
    # Initialize analyzers
    sentiment_analyzer = SentimentAnalyzer()
    vibe_analyzer = VibeAnalyzer()
    response_generator = ResponseGenerator()
    
    # Analyze the text
    sentiment_result = sentiment_analyzer.analyze_sentiment(mention_text)
    vibe_result = vibe_analyzer.analyze_vibe(mention_text)
    
    print("🔍 Analysis Results:")
    print(f"   Sentiment: {sentiment_result['overall_sentiment']}")
    print(f"   Vibe Score: {vibe_result['overall_vibe']:.3f}")
    print(f"   Hashtags: {vibe_result['hashtags']}")
    print(f"   Mentions: {vibe_result['mentions']}")
    print()
    
    # Generate reputation response
    response = response_generator.generate_response(sentiment_result, vibe_result, mention_text, author_handle)
    
    print("🤖 REPUTATION ANALYSIS RESPONSE:")
    print("=" * 60)
    if response:
        print(response)
    else:
        print("No response generated (post doesn't meet criteria)")
    print("=" * 60)

if __name__ == "__main__":
    show_mention_response() 