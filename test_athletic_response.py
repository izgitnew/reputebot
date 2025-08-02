#!/usr/bin/env python3
"""
Test script to generate a response for The Athletic with new changes.
"""

import asyncio
from dotenv import load_dotenv
from bluesky import BlueskyClient
from responder import ResponseGenerator
from analyze import SentimentAnalyzer
from vibe import VibeAnalyzer

# Load environment variables
load_dotenv()

async def test_athletic_response():
    """Test generating a response for The Athletic."""
    print("🔍 Testing Response Generation for The Athletic...")
    
    bluesky_client = BlueskyClient()
    sentiment_analyzer = SentimentAnalyzer()
    vibe_analyzer = VibeAnalyzer()
    response_generator = ResponseGenerator()
    
    try:
        # Login
        await bluesky_client.login()
        print("✅ Login successful")
        
        # Fetch posts from The Athletic
        print("\n📊 Fetching posts from The Athletic...")
        target_posts = await bluesky_client.get_author_posts("theathletic.com", days_back=30)
        
        if not target_posts:
            print("❌ No posts found")
            return
        
        print(f"📊 Found {len(target_posts)} posts from @theathletic.com")
        
        # Extract text for analysis
        all_post_texts = []
        for post in target_posts:
            if hasattr(post, 'post') and hasattr(post.post, 'record') and hasattr(post.post.record, 'text'):
                all_post_texts.append(post.post.record.text)
        
        if not all_post_texts:
            print("❌ No text found in posts")
            return
        
        # Combine all posts for analysis
        combined_text = " ".join(all_post_texts[:50])  # Use first 50 posts to avoid too much text
        print(f"📝 Combined text length: {len(combined_text)} characters")
        
        # Get timestamps for posts/day calculation
        print("\n📊 Fetching timestamps for posts/day calculation...")
        target_timestamps = await bluesky_client.get_author_post_timestamps("theathletic.com", days_back=30)
        print(f"📊 Found {len(target_timestamps)} timestamps")
        
        # Analyze sentiment and vibe
        print("\n🔍 Analyzing sentiment and vibe...")
        sentiment_result = sentiment_analyzer.analyze_sentiment(combined_text)
        vibe_result = vibe_analyzer.analyze_vibe(combined_text)
        
        print(f"📊 Sentiment score: {sentiment_result['vader_scores']['compound']}")
        print(f"📊 Vibe score: {vibe_result['overall_vibe']}")
        
        # Generate response
        print("\n🎯 Generating response...")
        response = response_generator.generate_response(
            sentiment_result, 
            vibe_result, 
            combined_text, 
            "theathletic.com", 
            target_timestamps
        )
        
        if response:
            print(f"\n✅ Generated Response:")
            print("=" * 50)
            print(response)
            print("=" * 50)
        else:
            print("❌ No response generated")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_athletic_response()) 